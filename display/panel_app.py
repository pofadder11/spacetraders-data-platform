from __future__ import annotations

import os
from typing import Any, List

import pandas as pd
import panel as pn
import holoviews as hv
from holoviews.streams import RangeXY
hv.extension("bokeh")
import requests

pn.extension("tabulator")


API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")


def fetch_json(path: str) -> Any:
    url = path if path.startswith("http") else f"{API_BASE}{path}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e), "url": url}


def ensure_list(obj: Any) -> list[dict]:
    """Normalize API responses to a list[dict].

    - If obj is already a list, return as-is.
    - If obj is a dict containing 'data' which is a list, return that list.
    - If obj is a dict with error/detail, return empty list.
    - If obj is a dict of scalars (single row), wrap into a one-element list.
    - Else return empty list.
    """
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        if obj.get("error") or obj.get("detail"):
            return []
        data = obj.get("data")
        if isinstance(data, list):
            return data
        return [obj]
    return []


def df_from_offers(data: Any) -> pd.DataFrame:
    rows = ensure_list(data)
    if not rows:
        return pd.DataFrame(columns=["waypoint_symbol", "ship_type", "name", "purchase_price", "observed_at"])  # noqa: E501
    return pd.DataFrame(rows)


def df_from_markets(data: Any) -> pd.DataFrame:
    rows = ensure_list(data)
    if not rows:
        return pd.DataFrame(columns=["waypoint_symbol", "trade_symbol", "sell_price", "purchase_price", "observed_at"])  # noqa: E501
    return pd.DataFrame(rows)


def df_from_actions(data: Any) -> pd.DataFrame:
    rows = ensure_list(data)
    if not rows:
        return pd.DataFrame(columns=["ts", "action"])  # minimal
    return pd.DataFrame(rows)


# Widgets / panes
summary_pane = pn.pane.JSON({}, name="Summary", sizing_mode="stretch_width")
status_alert = pn.pane.Markdown("", sizing_mode="stretch_width")
offers_table = pn.widgets.Tabulator(pd.DataFrame(), pagination="local", page_size=20, height=300)
markets_table = pn.widgets.Tabulator(pd.DataFrame(), pagination="local", page_size=20, height=300)
actions_table = pn.widgets.Tabulator(pd.DataFrame(), pagination="local", page_size=20, height=250)
systems_table = pn.widgets.Tabulator(pd.DataFrame(), pagination="local", page_size=20, height=250)
waypoints_table = pn.widgets.Tabulator(pd.DataFrame(), pagination="local", page_size=20, height=300)
snapshots_table = pn.widgets.Tabulator(pd.DataFrame(), pagination="local", page_size=20, height=300)
yields_table = pn.widgets.Tabulator(pd.DataFrame(), pagination="local", page_size=20, height=250)
map_pane = pn.pane.HoloViews(height=500, sizing_mode="stretch_width")
_range_stream = RangeXY()


def refresh():
    # Summary header
    summary = fetch_json("/summary")
    summary_pane.object = summary

    # Shipyard offers
    offers = fetch_json("/shipyards/current")
    offers_df = df_from_offers(offers)
    # Age column
    if "observed_at" in offers_df.columns:
        try:
            dt = pd.to_datetime(offers_df["observed_at"], utc=True, errors="coerce")
            age = (pd.Timestamp.utcnow() - dt).dt.total_seconds()
            offers_df["age_s"] = age.fillna(0).astype(int)
        except Exception:
            pass
    offers_table.value = offers_df

    # Markets (optionally filter by top N rows)
    markets = fetch_json("/markets/current")
    markets_df = df_from_markets(markets)
    if "observed_at" in markets_df.columns:
        try:
            dt = pd.to_datetime(markets_df["observed_at"], utc=True, errors="coerce")
            markets_df["age_s"] = (pd.Timestamp.utcnow() - dt).dt.total_seconds().fillna(0).astype(int)
        except Exception:
            pass
    markets_table.value = markets_df

    # Recent actions
    actions = fetch_json("/actions?n=200")
    actions_df = df_from_actions(actions)
    if "ts" in actions_df.columns:
        try:
            dt = pd.to_datetime(actions_df["ts"], utc=True, errors="coerce")
            actions_df["age_s"] = (pd.Timestamp.utcnow() - dt).dt.total_seconds().fillna(0).astype(int)
        except Exception:
            pass
    actions_table.value = actions_df

    # Status line
    err_msgs = []
    for label, payload in ("offers", offers), ("markets", markets), ("actions", actions):
        if isinstance(payload, dict) and payload.get("error"):
            err_msgs.append(f"{label}: {payload.get('error')} ({payload.get('url')})")
    status_alert.object = ("\n".join(err_msgs)) if err_msgs else ""

    # Systems & Waypoints & Snapshots & Yields
    systems = fetch_json("/systems")
    systems_table.value = pd.DataFrame(ensure_list(systems))
    wps = fetch_json("/waypoints")
    waypoints_table.value = pd.DataFrame(ensure_list(wps))
    snaps = fetch_json("/markets/snapshots")
    snaps_df = pd.DataFrame(ensure_list(snaps))
    if "observed_at" in snaps_df.columns:
        try:
            dt = pd.to_datetime(snaps_df["observed_at"], utc=True, errors="coerce")
            snaps_df["age_s"] = (pd.Timestamp.utcnow() - dt).dt.total_seconds().fillna(0).astype(int)
        except Exception:
            pass
    snapshots_table.value = snaps_df
    ylds = fetch_json("/yields")
    ylds_df = pd.DataFrame(ensure_list(ylds))
    if "observed_at" in ylds_df.columns:
        try:
            dt = pd.to_datetime(ylds_df["observed_at"], utc=True, errors="coerce")
            ylds_df["age_s"] = (pd.Timestamp.utcnow() - dt).dt.total_seconds().fillna(0).astype(int)
        except Exception:
            pass
    yields_table.value = ylds_df

    # Map view (waypoints + ships)
    wp_df = pd.DataFrame(ensure_list(wps))
    sp = fetch_json("/viz/ships_positions")
    sp_df = pd.DataFrame(ensure_list(sp))
    layers = []
    if not wp_df.empty:
        pts = hv.Points(wp_df, kdims=["x", "y"], vdims=["symbol", "type"]).opts(
            size=6,
            color="#39FF14",  # neon green
            alpha=0.9,
            tools=["hover"],
            hover_tooltips=[("Waypoint", "@symbol"), ("Type", "@type")],
        )
        layers.append(pts)
    if not sp_df.empty:
        # Overlay by role with distinct markers/colors using Points (2D kdims)
        role_markers = {
            "REFINERY": "square",
            "COMMAND": "diamond",
            "HAULER": "triangle",
            "EXPLORER": "circle",
            "SURVEYOR": "inverted_triangle",
            "EXCAVATOR": "circle_x",
        }
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
        color_map = {role: colors[i % len(colors)] for i, role in enumerate(role_markers.keys())}
        for role, group in sp_df.groupby(sp_df["role"].fillna("UNKNOWN")):
            pts = hv.Points(group, kdims=["x", "y"], vdims=["ship_symbol", "role", "status"]).opts(
                marker=role_markers.get(role, "circle"),
                size=10,
                color="#FF5F1F",  # neon orange
                line_color="black",
                tools=["hover"],
                hover_tooltips=[("Ship", "@ship_symbol"), ("Role", "@role"), ("Status", "@status")],
            )
            layers.append(pts)
    if layers:
        overlay = hv.Overlay(layers)
        # Preserve zoom by applying last known ranges
        opts_kwargs = dict(width=900, height=500, xlabel="x", ylabel="y", bgcolor="black")
        if _range_stream.x_range is not None and _range_stream.y_range is not None:
            x0, x1 = _range_stream.x_range
            y0, y1 = _range_stream.y_range
            if x0 is not None and x1 is not None and y0 is not None and y1 is not None:
                opts_kwargs["xlim"] = (x0, x1)
                opts_kwargs["ylim"] = (y0, y1)
        overlay = overlay.opts(**opts_kwargs)
        map_pane.object = overlay
        # Attach range stream to track future zooms
        try:
            _range_stream.source = overlay
        except Exception:
            pass


refresh_btn = pn.widgets.Button(name="Refresh Now", button_type="primary")
refresh_btn.on_click(lambda *_: refresh())

callback = pn.state.add_periodic_callback(refresh, period=5000)  # 5s


layout = pn.template.FastListTemplate(
    title="SpaceTraders Control Center",
    sidebar=[
        pn.pane.Markdown("### API Base"),
        pn.widgets.StaticText(value=API_BASE),
        refresh_btn,
    ],
    main=[
        pn.pane.Markdown("## Summary"),
        summary_pane,
        status_alert,
        pn.pane.Markdown("## Map"),
        map_pane,
        pn.pane.Markdown("## Shipyard Offers (Current)"),
        offers_table,
        pn.pane.Markdown("## Markets (Current)"),
        markets_table,
        pn.pane.Markdown("## Market Snapshots"),
        snapshots_table,
        pn.pane.Markdown("## Systems"),
        systems_table,
        pn.pane.Markdown("## Waypoints"),
        waypoints_table,
        pn.pane.Markdown("## Recent Actions"),
        actions_table,
        pn.pane.Markdown("## Extraction Yields"),
        yields_table,
    ],
)


def main():
    refresh()
    return layout


# Make the template servable when loaded via `panel serve`
refresh()
layout.servable()

if __name__ == "__main__":
    # Run as plain script (rare); still make it servable
    pn.serve(layout, show=True)
