from __future__ import annotations

import asyncio
from collections import deque
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Deque, Dict, List, Optional


_events: Deque[Dict[str, Any]] = deque(maxlen=500)
_events_lock = asyncio.Lock()
_loops: Dict[str, Dict[str, Any]] = {}
_loops_lock = asyncio.Lock()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


async def log(action: str, **fields: Any) -> None:
    evt = {"ts": _now_iso(), "action": action, **fields}
    async with _events_lock:
        _events.append(evt)


async def get_recent(n: int = 100) -> List[Dict[str, Any]]:
    async with _events_lock:
        return list(_events)[-n:]


async def set_loop_state(name: str, state: str, **fields: Any) -> None:
    async with _loops_lock:
        _loops[name] = {"state": state, "ts": _now_iso(), **fields}


async def get_loops() -> Dict[str, Any]:
    async with _loops_lock:
        return dict(_loops)

