# domain/market_rows.py
from __future__ import annotations
from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field

# 1) exports
class MarketExportRow(BaseModel):
    id: str                                     # f"{waypoint_symbol}#{trade_symbol}"
    waypoint_symbol: str
    trade_symbol: str
    name: Optional[str] = None
    description: Optional[str] = None

# 2) imports
class MarketImportRow(BaseModel):
    id: str
    waypoint_symbol: str
    trade_symbol: str
    name: Optional[str] = None
    description: Optional[str] = None

# 3) exchange
class MarketExchangeRow(BaseModel):
    id: str
    waypoint_symbol: str
    trade_symbol: str
    name: Optional[str] = None
    description: Optional[str] = None

# 4) transactions (market history at the waypoint)
TxType = Literal["BUY", "SELL"]
class MarketTransactionRow(BaseModel):
    id: str                                     # f"{waypoint_symbol}#{ship_symbol or 'UNKNOWN'}#{trade_symbol}#{timestamp_iso}"
    waypoint_symbol: str
    ship_symbol: Optional[str] = None
    trade_symbol: Optional[str] = None
    tx_type: Optional[TxType] = None            # BUY|SELL (as reported)
    units: Optional[int] = None
    price_per_unit: Optional[int] = None
    total_price: Optional[int] = None
    timestamp: Optional[datetime] = None

# 5) tradegoods (current market snapshot for each good)
SupplyLevel = Optional[str]   # e.g., "SCARCE" | "ABUNDANT"
ActivityLevel = Optional[str] # e.g., "WEAK" | "STRONG"
class MarketGoodRow(BaseModel):
    id: str                                     # f"{waypoint_symbol}#{trade_symbol}"
    waypoint_symbol: str
    trade_symbol: str
    type: Optional[str] = None
    trade_volume: Optional[int] = None
    supply: SupplyLevel = None
    activity: ActivityLevel = None
    purchase_price: Optional[int] = None
    sell_price: Optional[int] = None
