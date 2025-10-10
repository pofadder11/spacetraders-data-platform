# domain/transaction.py
from __future__ import annotations
from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel

Direction = Literal["DEBIT", "CREDIT"]
TxAction = Literal["REFUEL", "SELL", "BUY"]  

class Transaction(BaseModel):
    timestamp: datetime
    tx_action: TxAction
    direction: Direction

    agent_symbol: str
    ship_symbol: str
    waypoint_symbol: Optional[str] = None
    trade_symbol: Optional[str] = None

    units: Optional[int] = None
    price_per_unit: Optional[int] = None
    total_price: Optional[int] = None

    fuel_after: Optional[int] = None
    cargo_units_after: Optional[int] = None

    source: Optional[str] = None
