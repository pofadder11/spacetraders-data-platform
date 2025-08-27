import json
import sqlite3
from typing import Any, Dict, List, Union

import pandas as pd


def extract_api_data(
    api_response: Union[Dict[str, Any], List[Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    """
    Safely extract the 'data' field from an API response.
    Converts a dict to a single-item list if needed.
    Returns an empty list if the response is invalid.
    """
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


def flatten_json(
    d: Dict[str, Any], parent_key: str = "", sep: str = "_"
) -> Dict[str, Any]:
    """Recursively flatten nested JSON dictionaries."""
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_json(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items


def flatten_dict(
    d: Dict[str, Any], parent_key: str = "", sep: str = "_"
) -> Dict[str, Any]:
    """Recursively flatten nested dicts (does not flatten lists)."""
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items


def write_to_db(
    conn: sqlite3.Connection, table_name: str, records: List[Dict[str, Any]]
):
    if not records:
        print(f"[INFO] No records to write for {table_name}, skipping.")
        return
    try:
        df = pd.DataFrame(records)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"[INFO] {table_name} updated with {len(df)} records.")
    except Exception as e:
        print(f"[ERROR] Failed to write {table_name}: {e}")


def normalize_fleet(conn: sqlite3.Connection, fleet_json: Dict[str, Any]):
    fleet_data = fleet_json.get("data", fleet_json)
    if isinstance(fleet_data, dict):
        fleet_data = [fleet_data]
    elif not isinstance(fleet_data, list):
        print("[WARNING] Unexpected fleet data format, skipping normalization.")
        return

    specs_records = []
    nav_records = []
    modules_records = []
    mounts_records = []
    cargo_inventory_records = []

    for ship in fleet_data:
        ship_symbol = ship.get("symbol")

        # -----------------------
        # fleet_specs
        # -----------------------
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
                    flatten_dict(specs.pop(nested_field), parent_key=nested_field)
                )
        specs["ship_symbol"] = ship_symbol
        specs_records.append(specs)

        # -----------------------
        # fleet_nav
        # -----------------------
        if "nav" in ship:
            nav_data = flatten_dict(ship["nav"])
            # Convert lists to JSON strings
            for k, v in nav_data.items():
                if isinstance(v, list):
                    nav_data[k] = json.dumps(v)
            nav_data["ship_symbol"] = ship_symbol
            nav_records.append(nav_data)

        # -----------------------
        # fleet_modules
        # -----------------------
        for mod in ship.get("modules", []):
            mod_copy = flatten_dict(mod)
            for k, v in mod_copy.items():
                if isinstance(v, list):
                    mod_copy[k] = json.dumps(v)
            mod_copy["ship_symbol"] = ship_symbol
            modules_records.append(mod_copy)

        # -----------------------
        # fleet_mounts
        # -----------------------
        for mount in ship.get("mounts", []):
            mount_copy = flatten_dict(mount)
            for k, v in mount_copy.items():
                if isinstance(v, list):
                    mount_copy[k] = json.dumps(v)
            mount_copy["ship_symbol"] = ship_symbol
            mounts_records.append(mount_copy)

        # -----------------------
        # fleet_cargo_inventory
        # -----------------------
        for cargo in ship.get("cargo", {}).get("inventory", []):
            cargo_copy = flatten_dict(cargo)
            for k, v in cargo_copy.items():
                if isinstance(v, list):
                    cargo_copy[k] = json.dumps(v)
            cargo_copy["ship_symbol"] = ship_symbol
            cargo_inventory_records.append(cargo_copy)

    # -----------------------
    # Write all tables
    # -----------------------
    write_to_db(conn, "fleet_specs", specs_records)
    write_to_db(conn, "fleet_nav", nav_records)
    write_to_db(conn, "fleet_modules", modules_records)
    write_to_db(conn, "fleet_mounts", mounts_records)
    write_to_db(conn, "fleet_cargo_inventory", cargo_inventory_records)


# --- Waypoints ---
def normalize_waypoints(conn: sqlite3.Connection, waypoints_json: List[Dict[str, Any]]):
    """Normalize waypoints JSON into waypoints + traits tables."""
    waypoints_data = waypoints_json.get("data", waypoints_json)
    if isinstance(waypoints_data, dict):
        waypoints_data = [waypoints_data]
    elif not isinstance(waypoints_data, list):
        print("[WARNING] Unexpected fleet data format, skipping normalization.")
        return

    waypoint_records = []
    trait_records = []

    for wp in waypoints_data:
        # Extract core waypoint info
        waypoint_record = {
            "symbol": wp.get("symbol"),
            "system_symbol": wp.get("systemSymbol"),
            "type": wp.get("type"),
        }
        waypoint_records.append(waypoint_record)

        # Handle traits
        for trait in wp.get("traits", []):
            trait_records.append(
                {
                    "waypoint_symbol": wp.get("symbol"),
                    "trait_symbol": trait.get("symbol"),
                }
            )

    write_to_db(conn, "waypoints", waypoint_records)
    write_to_db(conn, "traits", trait_records)


# --- Shipyards ---
def normalize_shipyards(conn: sqlite3.Connection, shipyards_json: List[Dict[str, Any]]):
    """Normalize shipyards JSON into shipyards table."""
    shipyards_data = shipyards_json.get("data", shipyards_json)
    if isinstance(shipyards_data, dict):
        shipyards_data = [shipyards_data]
    elif not isinstance(shipyards_data, list):
        print("[WARNING] Unexpected fleet data format, skipping normalization.")
        return

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

    write_to_db(conn, "shipyards", shipyard_records)


# --- Shipyard Ships ---
def normalize_shipyard_ships(
    conn: sqlite3.Connection, shipyard_ships_json: List[Dict[str, Any]]
):
    """Normalize available ships in a shipyard into shipyard_ships table."""
    shipyard_ships_data = shipyard_ships_json.get("data", shipyard_ships_json)
    if isinstance(shipyard_ships_data, dict):
        shipyard_ships_data = [shipyard_ships_data]
    elif not isinstance(shipyard_ships_data, list):
        print("[WARNING] Unexpected fleet data format, skipping normalization.")
        return

    ship_records = []

    for s in shipyard_ships_data:
        record = {
            "shipyard_symbol": s.get("shipyardSymbol"),
            "ship_type": s.get("type"),
            "cost": s.get("purchasePrice"),
            # Dump everything else as JSON for "other_details"
            "other_details": json.dumps(
                {
                    k: v
                    for k, v in s.items()
                    if k not in ["shipyardSymbol", "type", "purchasePrice"]
                }
            ),
        }
        ship_records.append(record)

    write_to_db(conn, "shipyard_ships", ship_records)
