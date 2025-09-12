# app.py
from __future__ import annotations
import asyncio
import math
import os
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
import panel as pn
import json
import atexit
from pathlib import Path
from runtime_support import (
    setup_client_from_env,
    api_get_ship_nav,
    api_get_system_waypoints,
    status_value,
    is_in_transit,
)
from openapi_client.api.fleet_api import FleetApi
from openapi_client.api.systems_api import SystemsApi
from openapi_client.api.agents_api import AgentsApi
from runtime_support import api_get_my_agent, api_get_my_ships
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Range1d

# Persist routes across reloads
ROUTES_FILE = Path(os.getenv("ST_ROUTES_PATH", Path.home() / ".spacetraders" / "routes.json"))
ROUTES_FILE.parent.mkdir(parents=True, exist_ok=True)

# track last arrived waypoint (optional arrival-legs)
_last_arrived_wp: Optional[str] = None

def _norm_seg(a: float, b: float, c: float, d: float) -> tuple[float, float, float, float]:
    return (round(float(a), 6), round(float(b), 6), round(float(c), 6), round(float(d), 6))

def _save_routes_to_disk() -> None:
    try:
        data = [list(seg) for seg in sorted(_routes_seen)]
        tmp = ROUTES_FILE.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, indent=2))
        tmp.replace(ROUTES_FILE)
    except Exception as e:
        print(f"[WARN] Failed to save routes: {e!r}")

def _load_routes_from_disk() -> set[tuple[float, float, float, float]]:
    try:
        if ROUTES_FILE.exists():
            raw = json.loads(ROUTES_FILE.read_text())
            segs = set()
            for item in raw:
                if isinstance(item, (list, tuple)) and len(item) == 4:
                    segs.add(_norm_seg(*item))
            return segs
    except Exception as e:
        print(f"[WARN] Failed to load routes: {e!r}")
    return set()

def add_persistent_route(a: float, b: float, c: float, d: float) -> None:
    seg = _norm_seg(a, b, c, d)
    if seg not in _routes_seen:
        _routes_seen.add(seg)
        _save_routes_to_disk()

def _apply_map_container_size():
    if fit_width.value:
        # Fill available width; height controlled by Bokeh aspect_ratio
        map_frame.sizing_mode = "stretch_width"
        map_frame.width = None
        map_frame.height = None
    else:
        # Fixed square container
        s = int(map_size.value)
        map_frame.sizing_mode = "fixed"
        map_frame.width = s
        map_frame.height = s

from math import isnan as _isnan
from bokeh.plotting import figure as _bk_figure
from bokeh.models import ColumnDataSource, Range1d

def _blank_figure():
    p = _bk_figure(match_aspect=True, toolbar_location=None)
    # frameless black canvas
    p.background_fill_color = "black"
    p.border_fill_alpha = 0
    p.outline_line_color = None
    for ax in p.axis: ax.visible = False
    p.grid.visible = False
    p.min_border = p.min_border_left = p.min_border_right = 0
    p.min_border_top = p.min_border_bottom = 0
    return p

def build_bokeh_map(df_wp: pd.DataFrame,
                    routes: list[tuple[float,float,float,float]],
                    df_match: pd.DataFrame,
                    df_rest: pd.DataFrame,
                    ship_xy: tuple[Optional[float], Optional[float]],
                    zoom: float = 1.0):
    # ---- handle empty / missing data robustly ----
    if df_wp is None or df_wp.empty or "x" not in df_wp or "y" not in df_wp:
        return _blank_figure()

    # sanitize coords (drop NaNs)
    dfc = df_wp[["x","y"]].dropna()
    if dfc.empty:
        return _blank_figure()

    try:
        x_min, x_max = float(dfc["x"].min()), float(dfc["x"].max())
        y_min, y_max = float(dfc["y"].min()), float(dfc["y"].max())
        if any(_isnan(v) for v in (x_min, x_max, y_min, y_max)):
            raise ValueError
    except Exception:
        # fallback box around (0,0)
        x_min, x_max, y_min, y_max = -10.0, 10.0, -10.0, 10.0

    pad = 5.0
    cx = (x_min + x_max) / 2.0
    cy = (y_min + y_max) / 2.0
    span_x = (x_max - x_min) + 2*pad
    span_y = (y_max - y_min) + 2*pad
    base = max(span_x, span_y, 1.0)
    half = (base / max(float(zoom or 1.0), 1e-6)) / 2.0

    x0, x1 = cx - half, cx + half
    y0, y1 = cy - half, cy + half

    p = _bk_figure(
        x_range=Range1d(x0, x1),
        y_range=Range1d(y0, y1),
        match_aspect=True,
        toolbar_location=None,
    )

    # frameless black styling
    p.background_fill_color = "black"
    p.border_fill_alpha = 0
    p.outline_line_color = None
    for ax in p.axis: ax.visible = False
    p.grid.visible = False
    p.min_border = p.min_border_left = p.min_border_right = 0
    p.min_border_top = p.min_border_bottom = 0

    # --- routes (two-pass glow) ---
    if routes:
        xs0, ys0, xs1, ys1 = zip(*routes)
        rsrc = ColumnDataSource(dict(x0=xs0, y0=ys0, x1=xs1, y1=ys1))
        p.segment("x0","y0","x1","y1", source=rsrc, line_color="#7ddac5", line_width=4, line_alpha=0.35)
        p.segment("x0","y0","x1","y1", source=rsrc, line_color="#c7ffe3", line_width=2, line_alpha=0.9)

    # --- non-selected waypoints: halo + outline ---
    if isinstance(df_rest, pd.DataFrame) and not df_rest.empty:
        src = ColumnDataSource(df_rest)
        p.circle("x","y", source=src, size=12, fill_alpha=0.0, line_color="white", line_alpha=0.18, line_width=7)
        p.circle("x","y", source=src, size=8,  fill_alpha=0.0, line_color="white", line_alpha=0.9,  line_width=2)

    # --- selected traits: neon glow + core ---
    if isinstance(df_match, pd.DataFrame) and not df_match.empty:
        msrc = ColumnDataSource(df_match)
        p.circle("x","y", source=msrc, size=16, fill_alpha=0.12, line_color="color", line_alpha=0.35, line_width=7, color="color")
        p.circle("x","y", source=msrc, size=9,  fill_alpha=0.9,  line_color="#e8ffe8", line_alpha=0.7, line_width=1.0, color="color")

    # --- ship marker ---
    if isinstance(ship_xy, (tuple, list)) and len(ship_xy) == 2:
        cx, cy = ship_xy
        if cx is not None and cy is not None:
            p.triangle(x=[cx], y=[cy], size=14, fill_color="#e0ffe2", line_color=None)

    return p



# load persisted routes at startup & save on exit
_routes_seen = _load_routes_from_disk()
atexit.register(_save_routes_to_disk)

MAP_HEIGHT = 650

# --- Color palette (approx of your oklch black→green ramp) ---
PALETTE = [
    "#232a25", "#1a3a2f", "#225340", "#2a6c52",
    "#318764", "#39a276", "#41bd89"
]

# Add a bright neon palette for trait colors
NEON = [
    "#39FF14",  # neon green
    "#00F5FF",  # electric cyan
    "#FF5AF1",  # neon magenta
    "#FFD166",  # warm neon yellow
    "#9DFF00",  # lime
    "#7DF9FF",  # laser blue
    "#FF6EC7",  # hot pink
    "#F9F871",  # pastel neon yellow
]

# Map waypoint types to colors (feel free to expand/massage)
TYPE_COLOR_MAP = {
    "PLANET": PALETTE[2],
    "MOON": PALETTE[3],
    "ASTEROID": PALETTE[1],
    "ASTEROID_BASE": PALETTE[0],
    "ENGINEERED_ASTEROID": PALETTE[0],
    "GAS_GIANT": PALETTE[4],
    "JUMP_GATE": PALETTE[6],
    "FUEL_STATION": PALETTE[5],
    # default fallback for anything else:
    "_default": "#7bd4a6",
}

# sprite (optional): set ST_SHIP_SPRITE_URL in env to a PNG URL if you want an image instead of a triangle marker
SHIP_SPRITE_URL = os.getenv("ST_SHIP_SPRITE_URL", "").strip() or None

# ---------- Panel setup ----------
pn.extension("tabulator")

DB_PATH = os.getenv("ST_DB_PATH", "spacetraders.db")
DEFAULT_SHIP = os.getenv("ST_SHIP", "TROOTS-1")

# ---------- Persistent API clients ----------
client = setup_client_from_env()  # keep open for the server lifetime
fleet_api = FleetApi(client)
systems_api = SystemsApi(client)
agents_api = AgentsApi(client)


# ---------- Small DB helpers ----------
def _connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)

def distinct_trade_symbols() -> List[str]:
    sql = "SELECT DISTINCT trade_symbol FROM market_goods_snapshots ORDER BY trade_symbol"
    try:
        with _connect() as conn:
            vals = pd.read_sql_query(sql, conn)["trade_symbol"].dropna().astype(str).tolist()
            return vals
    except Exception:
        return []

def latest_prices_for_trade(trade_symbol: str) -> pd.DataFrame:
    """
    Latest snapshot per (waypoint, trade_symbol), filtered to one trade.
    """
    sql = """
    SELECT g.waypoint_symbol, g.trade_symbol,
           g.purchase_price, g.sell_price, g.supply, g.activity, g.observed_at
    FROM market_goods_snapshots AS g
    JOIN (
        SELECT waypoint_symbol, trade_symbol, MAX(observed_at) AS max_ts
        FROM market_goods_snapshots
        WHERE trade_symbol = :trade
        GROUP BY waypoint_symbol, trade_symbol
    ) t
      ON g.waypoint_symbol = t.waypoint_symbol
     AND g.trade_symbol    = t.trade_symbol
     AND g.observed_at     = t.max_ts
    WHERE g.trade_symbol = :trade
    ORDER BY g.waypoint_symbol
    """
    with _connect() as conn:
        return pd.read_sql_query(sql, conn, params={"trade": trade_symbol})

# ---------- Waypoint / map helpers ----------
def system_from_wp_symbol(wp: str) -> Optional[str]:
    if not isinstance(wp, str):
        return None
    parts = wp.split("-")
    return "-".join(parts[:2]) if len(parts) >= 2 else None

async def load_system_waypoints_df(system_symbol: str) -> pd.DataFrame:
    dtos = await api_get_system_waypoints(systems_api, system_symbol)
    rows = []
    for d in dtos:
        wp = getattr(d, "symbol", None)
        x = getattr(d, "x", None)
        y = getattr(d, "y", None)
        wtype = getattr(d, "type", None)
        traits = getattr(d, "traits", None) or getattr(d, "waypoint_traits", None) or []
        trait_syms = []
        for t in traits:
            sym = getattr(t, "symbol", None) or getattr(t, "trait_symbol", None)
            s = getattr(sym, "value", sym)  # enum -> value or plain str
            if s is not None:
                trait_syms.append(str(s))
        has_market = "MARKETPLACE" in trait_syms
        rows.append({
            "waypoint": wp, "x": x, "y": y,
            "type": str(wtype),
            "marketplace": has_market,
            "traits": trait_syms,            # <-- NEW
        })
    df = pd.DataFrame(rows).dropna(subset=["waypoint", "x", "y"])
    return df

async def ship_nav_info(ship_symbol: str) -> Dict[str, Any]:
    """
    Return dict with ship status, current wp (if docked/orbit), and interpolated (x,y) if in transit.
    """
    nav = await api_get_ship_nav(fleet_api, ship_symbol)
    status = status_value(getattr(nav, "status", None))
    waypoint_symbol = getattr(nav, "waypoint_symbol", None)

    route = getattr(nav, "route", None)
    origin = getattr(route, "origin", None)
    dest = getattr(route, "destination", None)
    dep = getattr(route, "departure_time", None)
    arr = getattr(route, "arrival", None) or getattr(route, "arrival_time", None)

    def _coerce_dt(dt_like):
        if dt_like is None:
            return None
        if isinstance(dt_like, datetime):
            return dt_like if dt_like.tzinfo else dt_like.replace(tzinfo=timezone.utc)
        # strings like "...Z"
        try:
            return datetime.fromisoformat(str(dt_like).replace("Z", "+00:00"))
        except Exception:
            return None

    dep_dt = _coerce_dt(dep)
    arr_dt = _coerce_dt(arr)

    ox, oy = getattr(origin, "x", None), getattr(origin, "y", None)
    dx, dy = getattr(dest, "x", None), getattr(dest, "y", None)

    # Current position
    if is_in_transit(nav) and all(v is not None for v in (ox, oy, dx, dy, dep_dt, arr_dt)):
        now = datetime.now(timezone.utc)
        span = max((arr_dt - dep_dt).total_seconds(), 1.0)
        t = min(max((now - dep_dt).total_seconds() / span, 0.0), 1.0)
        cx = ox + t * (dx - ox)
        cy = oy + t * (dy - oy)
    else:
        # if not in transit, assume we are at current waypoint coords; caller will supply map df
        cx = None
        cy = None

    # Fallback: system symbol
    sys_sym = None
    if waypoint_symbol:
        sys_sym = system_from_wp_symbol(waypoint_symbol)
    elif getattr(origin, "symbol", None):
        sys_sym = system_from_wp_symbol(getattr(origin, "symbol"))
    elif getattr(dest, "symbol", None):
        sys_sym = system_from_wp_symbol(getattr(dest, "symbol"))

    return dict(
        status=status,
        waypoint_symbol=waypoint_symbol,
        origin=(ox, oy, getattr(origin, "symbol", None)),
        destination=(dx, dy, getattr(dest, "symbol", None)),
        position=(cx, cy),  # None if not in transit
        system_symbol=sys_sym,
    )

# ---------- UI widgets ----------
ship_select = pn.widgets.TextInput(name="Ship symbol", value=DEFAULT_SHIP, placeholder="e.g., TROOTS-1")
trade_symbols = distinct_trade_symbols()
trade_select = pn.widgets.Select(name="Trade", value=trade_symbols[0] if trade_symbols else None, options=trade_symbols)
refresh_sec = pn.widgets.IntInput(name="Refresh (s)", value=3, start=1, step=1)
fit_width = pn.widgets.Checkbox(name="Fit width (square)", value=True)
fit_width = pn.widgets.Checkbox(name="Fit width (square)", value=True)
map_size  = pn.widgets.IntSlider(
    name="Map size (px)", start=400, end=1600, step=50, value=900, width=220
)
zoom = pn.widgets.FloatSlider(
    name="Zoom", start=0.5, end=4.0, step=0.1, value=1.0, width=220
)
def _trigger_refresh(_=None):
    asyncio.create_task(_refresh_once())

if hasattr(zoom, "value_throttled"):
    zoom.param.watch(lambda e: _trigger_refresh(), "value_throttled")
else:
    # Older Panel/Bokeh: no throttled channel → just watch normal value
    zoom.param.watch(lambda e: _trigger_refresh(), "value")



# --- Custom Trait selector with colored swatches ---
class TraitSelector:
    """Multi-select list of traits with colored swatches matching the map."""
    def __init__(self):
        self._options: list[str] = []
        self._checks: dict[str, tuple[pn.widgets.Checkbox, pn.pane.HTML]] = {}
        self.colors: dict[str, str] = {}   # color per selected trait
        self.panel = pn.Column(sizing_mode="stretch_width")
        self._on_change_cb = None

    def set_on_change(self, cb):
        """Register a callback to run when selection changes."""
        self._on_change_cb = cb
        # rewire watchers on all existing checkboxes
        for cbx, _ in self._iter_cbs():
            cbx.param.watch(self._on_toggle, "value")

    # Public API: selected values (list[str])
    @property
    def value(self) -> list[str]:
        return [t for t, (cbx, _) in self._checks.items() if cbx.value]

    def set_options(self, options: list[str], default: Optional[list[str]] = None):
        """(Re)build the UI with these options; keep existing selections if possible."""
        current = set(self.value)
        self._options = list(options)
        self.panel.objects = []
        self._checks.clear()
        rows = []
        for trait in self._options:
            cbx = pn.widgets.Checkbox(name=trait, value=(trait in current))
            cbx.width_policy = "max"
            cbx.param.watch(self._on_toggle, "value")
            sw = pn.pane.HTML(self._swatch_html("#666666", selected=cbx.value),
                              width=16, height=16, margin=(6, 6, 0, 0))
            rows.append(pn.Row(sw, cbx, sizing_mode="stretch_width"))
            self._checks[trait] = (cbx, sw)

        # Default selection if nothing selected
        if default and not current:
            for t in default:
                if t in self._checks:
                    self._checks[t][0].value = True

        self._reassign_colors()
        self._refresh_swatches()
        self.panel.objects = rows

    # ---- internals ----
    def _iter_cbs(self):
        return [v for v in self._checks.values()]

    def _on_toggle(self, event):
        self._reassign_colors()
        self._refresh_swatches()
        if self._on_change_cb:
            self._on_change_cb()

    def _reassign_colors(self):
        """Assign distinct NEON colors to currently selected traits."""
        sel = sorted(self.value)
        self.colors = {t: NEON[i % len(NEON)] for i, t in enumerate(sel)}

    def _refresh_swatches(self):
        for trait, (cbx, sw) in self._checks.items():
            if cbx.value and trait in self.colors:
                color = self.colors[trait]
                sw.object = self._swatch_html(color, selected=True)
            else:
                sw.object = self._swatch_html("#666666", selected=False)

    @staticmethod
    def _swatch_html(color: str, selected: bool) -> str:
        bg = color if selected else "transparent"
        glow = f"0 0 12px {color}" if selected else "0 0 6px rgba(255,255,255,0.25)"
        return (
            f"<div style='width:12px;height:12px;border-radius:50%;"
            f"background:{bg};border:2px solid {color};box-shadow:{glow};'></div>"
        )

# Instantiate


# ---------- Plot & table panes ----------
map_pane = pn.pane.Bokeh(sizing_mode="stretch_width")
table = pn.widgets.Tabulator(pd.DataFrame(), height=420, sizing_mode="stretch_width", pagination="remote", page_size=20)
agent_info_md = pn.pane.Markdown("", sizing_mode="fixed")
agent_card = pn.Card(
    agent_info_md,
    title="Agent",
    height=30,     # tweak as you like
    sizing_mode="fixed"
)


# ---------- Reactive state ----------
_waypoint_df: Optional[pd.DataFrame] = None  # cached per-system
_cached_system: Optional[str] = None

def _color_for_type(t: str) -> str:
    return TYPE_COLOR_MAP.get(str(t), TYPE_COLOR_MAP["_default"])

def _build_routes_segments() -> hv.Segments | None:
    if not _routes_seen:
        return None
    df = pd.DataFrame([{"x0": a, "y0": b, "x1": c, "y1": d} for (a,b,c,d) in _routes_seen])
    return hv.Segments(df, kdims=["x0","y0","x1","y1"]).opts(line_width=1, line_alpha=0.35, color="#8fd3c0")

def _overlay_map(navinfo: dict[str, Any], df_wp: pd.DataFrame):
    # Which traits are selected?
    selected = set(trait_selector.value)

    # Compute first matching trait
    df = df_wp.copy()
    def _first_match(traits_list):
        if not isinstance(traits_list, (list, tuple)):
            return None
        for t in traits_list:
            if t in selected:
                return t
        return None
    df["match_trait"] = df["traits"].apply(_first_match)

    # Use selector's color mapping (from your custom TraitSelector)
    df["color"] = df["match_trait"].map(getattr(trait_selector, "colors", {}))

    # Persist current route if present
    ox, oy, _ = navinfo["origin"]
    dx, dy, _ = navinfo["destination"]
    if all(v is not None for v in (ox, oy, dx, dy)):
        add_persistent_route(float(ox), float(oy), float(dx), float(dy))

    # Build Bokeh figure
        # Build Bokeh figure (now with zoom)
    df_match = df[df["match_trait"].notna()][["x", "y", "color"]]
    df_rest  = df[df["match_trait"].isna()][["x", "y"]]
    routes = list(_routes_seen)
    ship_xy = navinfo["position"]

    fig = build_bokeh_map(df_wp, routes, df_match, df_rest, ship_xy, zoom=zoom.value)

    # Keep square & user-resizable
    if fit_width.value:
        fig.sizing_mode = "stretch_width"
        fig.aspect_ratio = 1
    else:
        s = int(map_size.value)
        fig.sizing_mode = "fixed"
        fig.width = s
        fig.height = s
        fig.match_aspect = True

    return fig



def _wp_coords(df_wp: pd.DataFrame, wp_symbol: Optional[str]) -> Optional[tuple[float,float]]:
    if not wp_symbol or df_wp is None or df_wp.empty:
        return None
    row = df_wp[df_wp["waypoint"] == wp_symbol]
    if row.empty:
        return None
    return float(row.iloc[0]["x"]), float(row.iloc[0]["y"])

async def _refresh_once():
    global _cached_system, _waypoint_df, _last_arrived_wp

    # 1) get ship symbol up front
    ship = (ship_select.value or "").strip()
    if not ship:
        return

    # 2) nav snapshot (derived + interpolated)
    nav = await ship_nav_info(ship)
    sys_sym = nav.get("system_symbol")
    if not sys_sym:
        return

    # 3) ensure waypoints cache for this system
    if _cached_system != sys_sym or _waypoint_df is None or _waypoint_df.empty:
        _waypoint_df = await load_system_waypoints_df(sys_sym)
        _cached_system = sys_sym

        # populate trait selector options
        traits_all: set[str] = set()
        for ts in _waypoint_df["traits"]:
            if isinstance(ts, (list, tuple)):
                traits_all.update(map(str, ts))
        opts = sorted(traits_all)

        # default to MARKETPLACE if present and nothing selected yet
        default_sel = ["MARKETPLACE"] if "MARKETPLACE" in traits_all else None
        trait_selector.set_options(opts, default=default_sel)


    # 4) if stationary, set position to current waypoint coords
    if nav["position"] == (None, None):
        wp = nav.get("waypoint_symbol")
        if wp and _waypoint_df is not None:
            row = _waypoint_df[_waypoint_df["waypoint"] == wp]
            if not row.empty:
                nav["position"] = (float(row.iloc[0]["x"]), float(row.iloc[0]["y"]))

    # 5) persist a leg on ARRIVAL (covers missed in-transit moments)
    try:
        nav_now = await api_get_ship_nav(fleet_api, ship)  # fresh status (enum)
        wp_now = nav.get("waypoint_symbol")
        if not is_in_transit(nav_now) and wp_now:
            if _last_arrived_wp is None:
                _last_arrived_wp = wp_now
            elif _last_arrived_wp != wp_now:
                def _wp_coords(df_wp, wp_sym):
                    r = df_wp[df_wp["waypoint"] == wp_sym]
                    if r.empty: return None
                    return float(r.iloc[0]["x"]), float(r.iloc[0]["y"])
                prev_xy = _wp_coords(_waypoint_df, _last_arrived_wp)
                cur_xy  = _wp_coords(_waypoint_df, wp_now)
                if prev_xy and cur_xy and prev_xy != cur_xy:
                    add_persistent_route(prev_xy[0], prev_xy[1], cur_xy[0], cur_xy[1])
                _last_arrived_wp = wp_now
    except Exception as e:
        print("[WARN] arrival-route persistence failed:", repr(e))

    # 6) update map + table
    if _waypoint_df is not None and not _waypoint_df.empty:
        _apply_map_container_size()
        map_pane.object = _overlay_map(nav, _waypoint_df)

    if trade_select.value:
        df = latest_prices_for_trade(trade_select.value)
        table.value = df

    # --- Agent summary (credits + ship count) ---
    try:
        agent = await api_get_my_agent(agents_api)
        credits = getattr(agent, "credits", None)
        # Some SDKs may use 'credit' or nested models; keep fallbacks:
        credits = credits if isinstance(credits, (int, float)) else getattr(agent, "credit", 0)
        ships = await api_get_my_ships(fleet_api)
        ship_count = len(ships) if isinstance(ships, (list, tuple)) else 0

        # Format nicely with thousands separators
        agent_info_md.object = f"**Credits:** {credits:,.0f}  \n**Ships:** {ship_count}"
    except Exception as e:
        # Don't break the app if this fails
        agent_info_md.object = "**Credits:** —  \n**Ships:** —"

# Periodic refresher
_cb: Optional[pn.io.PeriodicCallback] = None

def start_periodic():
    global _cb
    if _cb is not None:
        _cb.stop()
        _cb = None
    _cb = pn.state.add_periodic_callback(lambda: asyncio.create_task(_refresh_once()), period=refresh_sec.value * 1000, start=True)

def on_controls_change(event=None):
    # restart periodic callback to apply new refresh period
    start_periodic()

refresh_sec.param.watch(on_controls_change, "value")
ship_select.param.watch(on_controls_change, "value")
trade_select.param.watch(lambda e: asyncio.create_task(_refresh_once()), "value")
trait_selector = TraitSelector()
trait_selector.set_on_change(lambda: asyncio.create_task(_refresh_once()))
# Refresh when the user adjusts size/zoom
map_size.param.watch(lambda e: asyncio.create_task(_refresh_once()), "value")
zoom.param.watch(lambda e: asyncio.create_task(_refresh_once()), "value_throttled")
fit_width.param.watch(lambda e: asyncio.create_task(_refresh_once()), "value")

    # ---------- Layout ----------
# ---------- BIG Movement Map (full width) ----------
# give the map more height; width will stretch with layout

# ---------- Controls + Latest Prices BELOW the map (side-by-side) ----------
# Button fix (from earlier): ensure you created restart_btn and wired on_click
restart_btn = pn.widgets.Button(name="Restart Refresh", button_type="primary")
restart_btn.on_click(lambda _e: start_periodic())

controls = pn.Card(
    pn.Column(
        ship_select,
        trade_select,
        refresh_sec,
        fit_width,          
        restart_btn,
        sizing_mode="stretch_width",
    ),
    title="Controls",
    collapsed=False,
    sizing_mode="stretch_width",
)

traits_card = pn.Card(
    pn.Column(
        pn.pane.Markdown("### Traits"),
        trait_selector.panel,   # <-- use the custom panel
        sizing_mode="stretch_width",
    ),
    title="",
    width=300,
    sizing_mode="fixed",
)



prices_card = pn.Card(
    table, title="Latest Prices (per market)", collapsed=False, sizing_mode="stretch_both"
)

# A container with rounded corners & glow for the map
map_frame = pn.Column(
    map_pane,
    sizing_mode="stretch_width",
    margin=0,
    styles={
        "background": "black",
        "border": "2px solid #41bd89",
        "borderRadius": "14px",
        "boxShadow": "0 0 28px rgba(65,189,137,0.7), inset 0 0 14px rgba(65,189,137,0.25)",
        "overflow": "hidden",  # clip the canvas to curved corners
        "padding": "6px",
    },
)

# Top: big map; Bottom: controls + prices side-by-side
# Top row = map (fills left) + traits (fixed right)
# Give the trait card a fixed flex basis (stays 300px when beside map; wraps below if no space)
traits_card.width = 300
traits_card.sizing_mode = "fixed"
traits_card.styles = {"flex": "0 0 300px"}

# Let the map grow and shrink; prefers at least ~480px, but can wrap above/below the trait card
map_frame.styles.update({"flex": "1 1 480px"})

top_wrap = pn.FlexBox(
    map_frame, traits_card,
    sizing_mode="stretch_width",
    styles={"flex-wrap": "wrap", "gap": "12px"}
)


bottom_row = pn.Row(controls, prices_card, sizing_mode="stretch_both")

header_controls = pn.Row(
    map_size, zoom,  # sliders in header
    sizing_mode="fixed"
)

header_row = pn.Row(
    pn.pane.Markdown("# SpaceTraders • Markets & Movement", sizing_mode="stretch_width"),
    pn.Spacer(sizing_mode="stretch_width"),
    header_controls,
    pn.Spacer(width=10),
    agent_card,
    sizing_mode="stretch_width",
)


page = pn.Column(
    header_row,
    top_wrap,
    bottom_row,
    sizing_mode="stretch_width",
    margin=(10, 15),
)


# ---------- Bootstrap + serve ----------
async def _on_load():
    await _refresh_once()
    start_periodic()

pn.state.onload(_on_load)
page.servable(title="SpaceTraders • Markets & Movement")


