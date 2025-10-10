# adapters/market_adapter.py
from __future__ import annotations
from typing import Iterable, List, Tuple
from datetime import datetime
from domain.market_rows import (
    MarketExportRow, MarketImportRow, MarketExchangeRow,
    MarketTransactionRow, MarketGoodRow
)

def g(obj, *attrs):
    cur = obj
    for a in attrs:
        cur = getattr(cur, a, None)
        if cur is None:
            return None
    return cur

def adapt_market_exports(market_dto, waypoint_symbol: str) -> List[MarketExportRow]:
    rows: List[MarketExportRow] = []
    for item in getattr(market_dto, "exports", None) or []:
        trade_symbol = getattr(item, "symbol", None)
        if not trade_symbol:
            continue
        rows.append(MarketExportRow(
            id=f"{waypoint_symbol}#{trade_symbol}",
            waypoint_symbol=waypoint_symbol,
            trade_symbol=trade_symbol,
            name=getattr(item, "name", None),
            description=getattr(item, "description", None),
        ))
    return rows

def adapt_market_imports(market_dto, waypoint_symbol: str) -> List[MarketImportRow]:
    rows: List[MarketImportRow] = []
    for item in getattr(market_dto, "imports", None) or []:
        trade_symbol = getattr(item, "symbol", None)
        if not trade_symbol:
            continue
        rows.append(MarketImportRow(
            id=f"{waypoint_symbol}#{trade_symbol}",
            waypoint_symbol=waypoint_symbol,
            trade_symbol=trade_symbol,
            name=getattr(item, "name", None),
            description=getattr(item, "description", None),
        ))
    return rows

def adapt_market_exchange(market_dto, waypoint_symbol: str) -> List[MarketExchangeRow]:
    rows: List[MarketExchangeRow] = []
    for item in getattr(market_dto, "exchange", None) or []:
        trade_symbol = getattr(item, "symbol", None)
        if not trade_symbol:
            continue
        rows.append(MarketExchangeRow(
            id=f"{waypoint_symbol}#{trade_symbol}",
            waypoint_symbol=waypoint_symbol,
            trade_symbol=trade_symbol,
            name=getattr(item, "name", None),
            description=getattr(item, "description", None),
        ))
    return rows

def adapt_market_transactions(market_dto, waypoint_symbol: str) -> List[MarketTransactionRow]:
    rows: List[MarketTransactionRow] = []
    for tx in getattr(market_dto, "transactions", None) or []:
        ship_symbol = getattr(tx, "ship_symbol", None)
        trade_symbol = getattr(tx, "trade_symbol", None)
        ts = getattr(tx, "timestamp", None)
        # fallback if timestamp missing
        ts = ts or datetime.utcnow()
        ts_iso = ts.isoformat() if hasattr(ts, "isoformat") else str(ts)
        tx_type = getattr(tx, "type", None)  # "BUY" | "SELL"
        rows.append(MarketTransactionRow(
            id=f"{waypoint_symbol}#{ship_symbol or 'UNKNOWN'}#{trade_symbol or 'UNKNOWN'}#{ts_iso}",
            waypoint_symbol=waypoint_symbol,
            ship_symbol=ship_symbol,
            trade_symbol=trade_symbol,
            tx_type=tx_type,
            units=getattr(tx, "units", None),
            price_per_unit=getattr(tx, "price_per_unit", None),
            total_price=getattr(tx, "total_price", None),
            timestamp=ts,
        ))
    return rows

def adapt_market_goods(market_dto, waypoint_symbol: str) -> List[MarketGoodRow]:
    rows: List[MarketGoodRow] = []
    for gitem in getattr(market_dto, "trade_goods", None) or getattr(market_dto, "tradegoods", None) or []:
        trade_symbol = getattr(gitem, "symbol", None) or getattr(gitem, "trade_symbol", None)
        if not trade_symbol:
            continue
        rows.append(MarketGoodRow(
            id=f"{waypoint_symbol}#{trade_symbol}",
            waypoint_symbol=waypoint_symbol,
            trade_symbol=trade_symbol,
            type=getattr(gitem, "type", None),
            trade_volume=getattr(gitem, "trade_volume", None),
            supply=getattr(gitem, "supply", None),
            activity=getattr(gitem, "activity", None),
            purchase_price=getattr(gitem, "purchase_price", None),
            sell_price=getattr(gitem, "sell_price", None),
        ))
    return rows

def adapt_market_all(market_dto, waypoint_symbol: str) -> Tuple[
    List[MarketExportRow], List[MarketImportRow], List[MarketExchangeRow],
    List[MarketTransactionRow], List[MarketGoodRow]
]:
    return (
        adapt_market_exports(market_dto, waypoint_symbol),
        adapt_market_imports(market_dto, waypoint_symbol),
        adapt_market_exchange(market_dto, waypoint_symbol),
        adapt_market_transactions(market_dto, waypoint_symbol),
        adapt_market_goods(market_dto, waypoint_symbol),
    )
