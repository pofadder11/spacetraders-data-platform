import json
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Union

import pandas as pd


class Normalizer:
    """Normalize SpaceTraders API responses into SQLite tables with logs."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    # -----------------------------
    # Utilities
    # -----------------------------
    @staticmethod
    def extract_api_data(
        api_response: Union[Dict[str, Any], List[Dict[str, Any]]],
    ) -> List[Dict[str, Any]]:
        if isinstance(api_response, dict):
            data = api_response.get("data", api_response)
        else:
            data = api_response
        if isinstance(data, dict):
            return [data]
        elif isinstance(data, list):
            return data
        else:
            print("[WARNING] Unexpected API response format, returning empty list.")
            return []

    @staticmethod
    def flatten_dict(
        d: Dict[str, Any], parent_key: str = "", sep: str = "_"
    ) -> Dict[str, Any]:
        """Flatten nested dictionaries (does not flatten lists)."""
        items = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(Normalizer.flatten_dict(v, new_key, sep=sep))
            else:
                items[new_key] = v
        return items

    def _write_to_db(self, table_name: str, records: List[Dict[str, Any]]):
        if not records:
            print(f"[INFO] No records to write for {table_name}, skipping.")
            return
        try:
            df = pd.DataFrame(records)

            # --- Write main table ---
            df.to_sql(table_name, self.conn, if_exists="replace", index=False)
            print(f"[INFO] {table_name} updated with {len(df)} records.")

            # --- Write append-only log table ---
            df_log = df.copy()
            df_log["timestamp"] = datetime.utcnow().isoformat()
            log_table = f"{table_name}_log"
            df_log.to_sql(log_table, self.conn, if_exists="append", index=False)
            print(f"[INFO] {log_table} appended with {len(df_log)} records.")

        except Exception as e:
            print(f"[ERROR] Failed to write {table_name}: {e}")

    # -----------------------------
    # Fleet
    # -----------------------------
    def normalize_fleet(self, fleet_json: Dict[str, Any]):
        fleet_data = self.extract_api_data(fleet_json)

        (
            specs_records,
            nav_records,
            modules_records,
            mounts_records,
            cargo_inventory_records,
        ) = ([], [], [], [], [])

        for ship in fleet_data:
            ship_symbol = ship.get("symbol")

            # fleet_specs
            specs = {
                k: v
                for k, v in ship.items()
                if k not in ["nav", "modules", "mounts", "cargo"]
            }
            for nested_field in [
                "frame",
                "reactor",
                "engine",
                "registration",
                "crew",
                "fuel",
                "cooldown",
            ]:
                if nested_field in specs:
                    specs.update(
                        self.flatten_dict(
                            specs.pop(nested_field), parent_key=nested_field
                        )
                    )
            specs["ship_symbol"] = ship_symbol
            specs_records.append(specs)

            # fleet_nav
            if "nav" in ship:
                nav_data = self.flatten_dict(ship["nav"])
                for k, v in nav_data.items():
                    if isinstance(v, list):
                        nav_data[k] = json.dumps(v)
                nav_data["ship_symbol"] = ship_symbol
                cargo = ship.get("cargo", {})
                nav_data["cargo_capacity"] = cargo.get("capacity", 0)
                nav_data["cargo_units"] = cargo.get("units", 0)
                fuel = ship.get("fuel", {})
                nav_data["fuel_current"] = fuel.get("current", 0)
                nav_data["fuel_capacity"] = fuel.get("capacity", 0)
                cooldown = ship.get("cooldown", {})
                nav_data["cooldown_remaining_seconds"] = cooldown.get(
                    "remainingSeconds", 0
                )
                nav_records.append(nav_data)

            # fleet_modules
            for mod in ship.get("modules", []):
                mod_copy = self.flatten_dict(mod)
                for k, v in mod_copy.items():
                    if isinstance(v, list):
                        mod_copy[k] = json.dumps(v)
                mod_copy["ship_symbol"] = ship_symbol
                modules_records.append(mod_copy)

            # fleet_mounts
            for mount in ship.get("mounts", []):
                mount_copy = self.flatten_dict(mount)
                for k, v in mount_copy.items():
                    if isinstance(v, list):
                        mount_copy[k] = json.dumps(v)
                mount_copy["ship_symbol"] = ship_symbol
                mounts_records.append(mount_copy)

            # fleet_cargo_inventory
            for cargo in ship.get("cargo", {}).get("inventory", []):
                cargo_copy = self.flatten_dict(cargo)
                for k, v in cargo_copy.items():
                    if isinstance(v, list):
                        cargo_copy[k] = json.dumps(v)
                cargo_copy["ship_symbol"] = ship_symbol
                cargo_inventory_records.append(cargo_copy)

        # Write tables
        self._write_to_db("fleet_specs", specs_records)
        self._write_to_db("fleet_nav", nav_records)
        self._write_to_db("fleet_modules", modules_records)
        self._write_to_db("fleet_mounts", mounts_records)
        self._write_to_db("fleet_cargo_inventory", cargo_inventory_records)

    # -----------------------------
    # Waypoints
    # -----------------------------
    def normalize_waypoints(self, waypoints_json: List[Dict[str, Any]]):
        waypoints_data = self.extract_api_data(waypoints_json)
        waypoint_records, trait_records = [], []

        for wp in waypoints_data:
            waypoint_records.append(
                {
                    "symbol": wp.get("symbol"),
                    "system_symbol": wp.get("systemSymbol"),
                    "type": wp.get("type"),
                }
            )
            for trait in wp.get("traits", []):
                trait_records.append(
                    {
                        "waypoint_symbol": wp.get("symbol"),
                        "trait_symbol": trait.get("symbol"),
                    }
                )

        self._write_to_db("waypoints", waypoint_records)
        self._write_to_db("traits", trait_records)

    # -----------------------------
    # Shipyards
    # -----------------------------
    def normalize_shipyards(self, shipyards_json: List[Dict[str, Any]]):
        shipyards_data = self.extract_api_data(shipyards_json)
        shipyard_records = []

        for sy in shipyards_data:
            record = {
                "shipyard_symbol": sy.get("symbol"),
                "waypoint_symbol": sy.get("waypointSymbol"),
                "system_symbol": sy.get("systemSymbol"),
                "is_under_construction": int(sy.get("isUnderConstruction", False)),
                "faction_symbol": (
                    sy.get("faction", {}).get("symbol")
                    if isinstance(sy.get("faction"), dict)
                    else sy.get("faction")
                ),
            }
            shipyard_records.append(record)

        self._write_to_db("shipyards", shipyard_records)

    def normalize_shipyard_ships(self, shipyard_json: dict):
        ships_data = self.extract_api_data(shipyard_json)
        if not ships_data:
            return
        waypoint_symbol = ships_data[0].get("symbol")  # assuming first entry
        records = []
        for ship in ships_data[0].get("ships", []):
            records.append(
                {
                    "waypoint_symbol": waypoint_symbol,
                    "ship_type": ship.get("type"),
                    "purchase_price": ship.get("purchasePrice"),
                    "quality": ship.get("frame", {}).get("quality"),
                    "supply": ship.get("supply"),
                    "reactor_symbol": ship.get("reactor", {}).get("symbol"),
                    "engine_symbol": ship.get("engine", {}).get("symbol"),
                }
            )
        self._write_to_db("shipyard_ships", records)

    # -----------------------------
    # Contracts
    # -----------------------------
    def normalize_contracts(self, contract_json: dict):
        contract_data = self.extract_api_data(contract_json)
        records = []

        for ct in contract_data:
            deliver = ct.get("terms", {}).get("deliver", [{}])[0]
            terms_payment = ct.get("terms", {}).get("payment", {})
            record = {
                "contract_id": ct.get("id"),
                "type": ct.get("type"),
                "deadline": ct.get("terms", {}).get("deadline"),
                "payment_on_accept": terms_payment.get("onAccepted"),
                "payment_on_complete": terms_payment.get("onFulfilled"),
                "accepted": int(ct.get("accepted", False)),
                "fulfilled": int(ct.get("fulfilled", False)),
                "trade_symbol": deliver.get("tradeSymbol"),
                "destination_symbol": deliver.get("destinationSymbol"),
                "units_required": deliver.get("unitsRequired"),
                "units_fulfilled": deliver.get("unitsFulfilled"),
            }
            records.append(record)

        self._write_to_db("contracts", records)

    def normalize_journey(self, navigation_json: dict, ship_symbol: str):
        navigation_data = self.extract_api_data(navigation_json)
        records = []
        for nv in navigation_data:
            record = {
                "ship_symbol": ship_symbol,
                "arrival_time": nv.get("nav", {}).get("route", {}).get("arrival"),
                "dest_x": nv.get("nav", {})
                .get("route", {})
                .get("destination", {})
                .get("x"),
                "dest_y": nv.get("nav", {})
                .get("route", {})
                .get("destination", {})
                .get("y"),
                "ori_x": nv.get("nav", {}).get("route", {}).get("origin", {}).get("x"),
                "ori_y": nv.get("nav", {})
                .get("route", {})
                .get("destination", {})
                .get("y"),
            }
            records.append(record)

        self._write_to_db("journeys", records)
