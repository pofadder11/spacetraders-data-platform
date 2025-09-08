from typing import Any

def safe_get(obj: Any, path: str, default=None):
    """
    Safe navigation of nested attributes and dict keys using dotted paths.
    Example: safe_get(dto, "nav.route.destination.symbol")
    """
    cur = obj
    for part in path.split("."):
        if cur is None:
            return default
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            cur = getattr(cur, part, None)
    return cur if cur is not None else default
