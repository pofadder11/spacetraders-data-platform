"""File-based session memory utilities for Codex CLI.

This module provides helpers to persist conversational and task context in
``.codex/`` so sessions can be resumed later or shared across tools.

Conventions
-----------
- History is stored per session as JSONL at ``.codex/history/<session_id>.jsonl``
- Durable summary lives at ``.codex/session/summary.md``
- Optional plan snapshot at ``.codex/plan.json``

Environment
-----------
- Set ``CODEX_SESSION_ID`` to control which history file to append to.
  Callers may also pass an explicit ``session_id`` to functions.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, Optional
import json
from datetime import datetime, timezone
import os


ROOT = Path.cwd()
CODEX_DIR = ROOT / ".codex"
HISTORY_DIR = CODEX_DIR / "history"
SESSION_DIR = CODEX_DIR / "session"
SUMMARY_PATH = SESSION_DIR / "summary.md"
PLAN_PATH = CODEX_DIR / "plan.json"


def _ensure_dirs() -> None:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    SESSION_DIR.mkdir(parents=True, exist_ok=True)


def default_session_id() -> str:
    """Return the default session id (ENV or date-based).

    Falls back to a date-based id like ``session-YYYYMMDD``.
    """
    sid = os.environ.get("CODEX_SESSION_ID")
    if sid:
        return sid
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"session-{today}"


def history_path(session_id: Optional[str] = None) -> Path:
    _ensure_dirs()
    sid = session_id or default_session_id()
    return HISTORY_DIR / f"{sid}.jsonl"


def append_history(
    role: str,
    content: str,
    *,
    session_id: Optional[str] = None,
    meta: Optional[Dict[str, Any]] = None,
) -> Path:
    """Append a history record to the session JSONL file.

    Returns the path to the history file for convenience.
    """
    path = history_path(session_id)
    rec = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "role": role,
        "content": content,
        "meta": meta or {},
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return path


def iter_history(session_id: Optional[str] = None, limit: Optional[int] = None) -> Iterator[Dict[str, Any]]:
    """Yield history records for the given session id (most recent last).

    If ``limit`` is provided, only the last N records are yielded.
    """
    path = history_path(session_id)
    if not path.exists():
        return iter(())
    # Efficient tail if limit specified
    lines: Iterable[str]
    with path.open("r", encoding="utf-8") as f:
        if limit is None:
            lines = f.readlines()
        else:
            from collections import deque
            lines = list(deque(f, maxlen=limit))
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def load_summary() -> str:
    _ensure_dirs()
    if SUMMARY_PATH.exists():
        return SUMMARY_PATH.read_text(encoding="utf-8")
    return ""


def save_summary(text: str) -> None:
    _ensure_dirs()
    SUMMARY_PATH.write_text(text, encoding="utf-8")


def load_plan() -> Dict[str, Any]:
    _ensure_dirs()
    if PLAN_PATH.exists():
        try:
            return json.loads(PLAN_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"steps": [], "updated_at": None}


def save_plan(plan: Dict[str, Any]) -> None:
    _ensure_dirs()
    payload = dict(plan)
    payload.setdefault("updated_at", datetime.now(timezone.utc).isoformat())
    PLAN_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


__all__ = [
    "default_session_id",
    "history_path",
    "append_history",
    "iter_history",
    "load_summary",
    "save_summary",
    "load_plan",
    "save_plan",
]

