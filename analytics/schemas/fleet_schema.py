import os
import sqlite3

import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table, html


# --- Helper function to pull fleet data ---
def load_fleet_data(db_path="spacetraders.db"):
    if not os.path.exists(db_path):
        print(f"[WARN] Database not found at {db_path}")
        return pd.DataFrame([])

    try:
        conn = sqlite3.connect(db_path)
        query = """
        SELECT
            nav.ship_symbol,
            specs.registration_name AS name,
            specs.registration_factionSymbol AS faction_symbol,
            specs.registration_role AS role,
            nav.systemSymbol AS system_symbol,
            nav.waypointSymbol AS waypoint_symbol,
            nav.status,
            nav.cargo_units,
            nav.cargo_capacity,
            nav.flightMode AS flight_mode,
            specs.fuel_current,
            specs.fuel_capacity,
            specs.cooldown_remainingSeconds AS cooldown_remaining_seconds,
            specs.frame_symbol,
            specs.frame_name,
            specs.frame_condition,
            specs.frame_integrity,
            specs.reactor_name,
            specs.reactor_powerOutput,
            specs.engine_name,
            specs.engine_speed,
            specs.crew_current,
            specs.crew_required,
            specs.crew_capacity,
            specs.crew_morale,
            specs.frame_quality
        FROM fleet_nav nav
        LEFT JOIN fleet_specs specs
        ON nav.ship_symbol = specs.ship_symbol
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"[ERROR] Failed to load fleet data: {e}")
        return pd.DataFrame([])


# --- Define the layout for the fleet dashboard ---
fleet_layout = dbc.Container(
    [
        html.H2("Fleet Overview", className="mb-4"),
        dbc.Row(
            [
                dbc.Col(
                    dash_table.DataTable(
                        id="fleet-table",
                        columns=[
                            {"name": "Ship Symbol", "id": "ship_symbol"},
                            {"name": "Name", "id": "name"},
                            {"name": "Faction", "id": "faction_symbol"},
                            {"name": "Role", "id": "role"},
                            {"name": "System", "id": "system_symbol"},
                            {"name": "Waypoint", "id": "waypoint_symbol"},
                            {"name": "Status", "id": "status"},
                            {"name": "Flight Mode", "id": "flight_mode"},
                            {"name": "Fuel", "id": "fuel_current"},
                            {"name": "Fuel Capacity", "id": "fuel_capacity"},
                            {"name": "Cargo", "id": "cargo_units"},
                            {"name": "Cargo Capacity", "id": "cargo_capacity"},
                            {
                                "name": "Cooldown (s)",
                                "id": "cooldown_remaining_seconds",
                            },
                            {"name": "Frame", "id": "frame_name"},
                            {"name": "Condition", "id": "frame_condition"},
                            {"name": "Integrity", "id": "frame_integrity"},
                            {"name": "Reactor", "id": "reactor_name"},
                            {"name": "Power Output", "id": "reactor_power_output"},
                            {"name": "Engine", "id": "engine_name"},
                            {"name": "Speed", "id": "engine_speed"},
                            {"name": "Crew", "id": "crew_current"},
                            {"name": "Crew Required", "id": "crew_required"},
                            {"name": "Crew Capacity", "id": "crew_capacity"},
                            {"name": "Crew Morale", "id": "crew_morale"},
                            {"name": "Quality", "id": "quality"},
                        ],
                        data=load_fleet_data().to_dict("records"),
                        page_size=15,
                        filter_action="native",
                        sort_action="native",
                        style_table={"overflowX": "auto"},
                        style_cell={
                            "textAlign": "center",
                            "padding": "6px",
                            "fontFamily": "Arial",
                            "fontSize": "14px",
                        },
                        style_header={
                            "fontWeight": "bold",
                            "backgroundColor": "#f8f9fa",
                            "border": "1px solid lightgrey",
                        },
                    ),
                    width=12,
                )
            ]
        ),
    ],
    fluid=True,
)
