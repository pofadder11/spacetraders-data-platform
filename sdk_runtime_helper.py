from __future__ import annotations

import asyncio
import inspect
from typing import Any
import sqlite3

conn = sqlite3.connect("spacetraders.db")


# ---------- async bridge + unwrap ---------------------------------------------
async def call_sdk(api_obj: Any, method_name: str, *args, **kwargs) -> Any:
    fn = getattr(api_obj, method_name)
    if inspect.iscoroutinefunction(fn):
        return await fn(*args, **kwargs)
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: fn(*args, **kwargs))

def unwrap_data(resp: Any) -> Any:
    return getattr(resp, "data", resp)
