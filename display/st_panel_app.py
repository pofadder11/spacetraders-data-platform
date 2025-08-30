import sqlite3

import holoviews as hv
import pandas as pd
import panel as pn

pn.extension("tabulator")  # Interactive tables
hv.extension("bokeh")  # Backend renderer


def load_ships():
    conn = sqlite3.connect("spacetraders.db")
    df = pd.read_sql_query(
        "SELECT ship_symbol AS name, route_origin_x as x, route_origin_y as y, status FROM fleet_nav",
        conn,
    )
    conn.close()
    return df


def load_waypoints():
    conn = sqlite3.connect("spacetraders.db")
    df = pd.read_sql_query("SELECT symbol as name, x, y FROM waypoints", conn)
    conn.close()
    return df


"""
# --------------------------
# Fake SpaceTraders data
# --------------------------
waypoints = pd.DataFrame({
    "name": ["WP-1", "WP-2", "WP-3", "WP-4"],
    "x": [2, 8, 5, 12],
    "y": [3, 1, 7, 9]
})

ships = pd.DataFrame({
    "name": ["SHIP-A", "SHIP-B", "SHIP-C"],
    "x": [2, 5, 8],
    "y": [3, 7, 2],
    "status": ["Docked", "In Transit", "Mining"],
    "credits": [1000, 2000, 1500]
})
"""
ships = load_ships()
waypoints = load_waypoints()

# --------------------------
# Visual Elements
# --------------------------

# Waypoints map
waypoint_map = waypoints.hvplot.scatter(
    x="x",
    y="y",
    color="gray",
    size=150,
    hover_cols=["name"],
    marker="triangle",
    title="🌌 Star Map",
)


# Ships map (dynamic)
def get_ship_map():
    return ships.hvplot.scatter(
        x="x", y="y", by="status", size=200, hover_cols=["name", "status"]
    )


def update_from_db():
    global ships, waypoints
    ships = load_ships()
    waypoints = load_waypoints()

    ship_table.value = ships
    map_pane.object = waypoints.hvplot.scatter(
        x="x", y="y", color="gray", size=150, hover_cols=["name"], marker="triangle"
    ) * ships.hvplot.scatter(
        x="x", y="y", by="status", size=200, hover_cols=["name", "status"]
    )


# Ship table
ship_table = pn.widgets.Tabulator(ships, pagination="remote", page_size=5)

# --------------------------
# Animation logic
# --------------------------

# Periodic callback
callback = pn.state.add_periodic_callback(
    update_from_db, period=5000
)  # refresh every 5s


# --------------------------
# Dashboard Layout
# --------------------------

map_pane = pn.pane.HoloViews(waypoint_map * get_ship_map(), sizing_mode="stretch_both")

dashboard = pn.template.FastListTemplate(
    title="🚀 SpaceTraders Control Center",
    main=[
        "## Fleet Map & Status",
        pn.Row(map_pane, ship_table),
    ],
)

dashboard.servable()
