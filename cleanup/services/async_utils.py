from __future__ import annotations

import asyncio
from typing import Any, Callable


async def run_to_thread(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Lightweight wrapper around asyncio.to_thread.

    Ensures we pass a callable (not the result of a call). Useful for testing
    consistent argument parsing/forwarding.
    """
    if not callable(func):
        raise TypeError(f"run_to_thread expected a callable, got: {type(func)!r}")
    return await asyncio.to_thread(func, *args, **kwargs)

