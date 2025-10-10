# adapters/transaction_adapter.py
from __future__ import annotations
from typing import Optional
from datetime import datetime
from domain.transaction import Transaction, TxAction

def g(obj, *attrs):
    cur = obj
    for a in attrs:
        cur = getattr(cur, a, None)
        if cur is None:
            return None
    return cur

def adapt_refuel_to_transaction(resp_dto, agent_symbol: str) -> Optional[Transaction]:
    """
    SpaceTraders refuel response (FleetApi.refuel_ship) typically includes:
      agent.credits
      fuel.current
      transaction: waypoint_symbol, ship_symbol, trade_symbol, type, units, price_per_unit, total_price, timestamp
    """
    tx = getattr(resp_dto, "transaction", None)
    if not tx:
        return None

    # direction from transaction.type (purchase => DEBIT)
    tx_type = getattr(tx, "type", None)
    direction = "DEBIT" if (tx_type and str(tx_type).upper() == "PURCHASE") else "CREDIT"

    return Transaction(
        timestamp=getattr(tx, "timestamp", None) or datetime.utcnow(),
        tx_action="REFUEL",
        direction=direction,
        agent_symbol=agent_symbol,
        ship_symbol=getattr(tx, "ship_symbol", None),
        waypoint_symbol=getattr(tx, "waypoint_symbol", None),
        trade_symbol=getattr(tx, "trade_symbol", None),
        units=getattr(tx, "units", None),
        price_per_unit=getattr(tx, "price_per_unit", None),
        total_price=getattr(tx, "total_price", None),
        fuel_after=g(resp_dto, "fuel", "current"),
        cargo_units_after=None,
        source="refuel_ship",
    )

def adapt_sell_to_transaction(resp_dto, agent_symbol: str) -> Optional[Transaction]:
    """
    SpaceTraders sell response (FleetApi.sell_cargo) includes:
      agent.credits
      cargo.units (after)
      transaction: waypoint_symbol, ship_symbol, trade_symbol, type, units, price_per_unit, total_price, timestamp
    """
    tx = getattr(resp_dto, "transaction", None)
    if not tx:
        return None

    # direction from transaction.type (sell => CREDIT)
    tx_type = getattr(tx, "type", None)
    direction = "CREDIT" if (tx_type and str(tx_type).upper() == "SELL") else "DEBIT"

    return Transaction(
        timestamp=getattr(tx, "timestamp", None) or datetime.utcnow(),
        tx_action="SELL",
        direction=direction,
        agent_symbol=agent_symbol,
        ship_symbol=getattr(tx, "ship_symbol", None),
        waypoint_symbol=getattr(tx, "waypoint_symbol", None),
        trade_symbol=getattr(tx, "trade_symbol", None),
        units=getattr(tx, "units", None),
        price_per_unit=getattr(tx, "price_per_unit", None),
        total_price=getattr(tx, "total_price", None),
        fuel_after=None,
        cargo_units_after=g(resp_dto, "cargo", "units"),
        source="sell_cargo",
    )

def adapt_buy_to_transaction(resp_dto, agent_symbol: str) -> Transaction:
    tx = getattr(resp_dto, "transaction", None)
    return Transaction(
        timestamp=getattr(tx, "timestamp", None) or datetime.utcnow(),
        tx_action="BUY",
        direction="DEBIT",  # spending credits
        agent_symbol=agent_symbol,
        ship_symbol=getattr(tx, "ship_symbol", None),
        waypoint_symbol=getattr(tx, "waypoint_symbol", None),
        trade_symbol=getattr(tx, "trade_symbol", None),
        units=getattr(tx, "units", None),
        price_per_unit=getattr(tx, "price_per_unit", None),
        total_price=getattr(tx, "total_price", None),
        cargo_units_after=getattr(getattr(resp_dto, "cargo", None), "units", None),
        source="buy_cargo",
    )
