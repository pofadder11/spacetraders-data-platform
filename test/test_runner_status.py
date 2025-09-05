from __future__ import annotations

import asyncio
import pytest

from services import runner_status as rs


@pytest.mark.asyncio
async def test_runner_status_log_and_get():
    await rs.log("test.action", foo=1)
    recent = await rs.get_recent(1)
    assert recent and recent[-1]["action"] == "test.action"
    assert recent[-1]["foo"] == 1


@pytest.mark.asyncio
async def test_runner_status_loops_state():
    await rs.set_loop_state("loop1", "running", note="ok")
    loops = await rs.get_loops()
    assert "loop1" in loops
    assert loops["loop1"]["state"] == "running"
    assert loops["loop1"]["note"] == "ok"

