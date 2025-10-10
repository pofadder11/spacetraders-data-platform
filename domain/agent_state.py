# domain/agent_state.py
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel

class AgentState(BaseModel):
    agent_symbol: str
    credits: int

    # Optional extra columns you requested (persist if present)
    headquarters: Optional[str] = None
    starting_faction: Optional[str] = None
    ship_count: Optional[int] = None
