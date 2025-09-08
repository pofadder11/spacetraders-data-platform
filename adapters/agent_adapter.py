# adapters/agent_adapter.py
from __future__ import annotations
from domain.agent_state import AgentState

def g(obj, *attrs):
    cur = obj
    for a in attrs:
        cur = getattr(cur, a, None)
        if cur is None:
            return None
    return cur

def adapt_agent_from_refuel(resp_dto, fallback_agent_symbol: str) -> AgentState:
    """
    Many action responses include a minimal agent payload with updated credits.
    """
    agent = getattr(resp_dto, "agent", None)
    symbol = getattr(agent, "symbol", None) or fallback_agent_symbol
    return AgentState(
        agent_symbol=symbol,
        credits=getattr(agent, "credits", 0),
        headquarters=getattr(agent, "headquarters", None),
        starting_faction=getattr(agent, "starting_faction", None),
        ship_count=getattr(agent, "ship_count", None),
    )

# You can re-use the same for sell_cargo (identical shape)
adapt_agent_from_sell = adapt_agent_from_refuel
