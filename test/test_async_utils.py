from __future__ import annotations

import asyncio
import math
import types
from functools import partial

import pytest

from services.async_utils import run_to_thread


def add(a, b):
    return a + b


class Acc:
    def __init__(self, base=0):
        self.base = base

    def add(self, x, y=0):
        return self.base + x + y


@pytest.mark.asyncio
async def test_run_to_thread_positional():
    res = await run_to_thread(add, 2, 3)
    assert res == 5


@pytest.mark.asyncio
async def test_run_to_thread_kwargs():
    res = await run_to_thread(pow, 2, exp=5)
    assert res == 32


@pytest.mark.asyncio
async def test_run_to_thread_bound_method():
    acc = Acc(base=10)
    res = await run_to_thread(acc.add, 2, y=3)
    assert res == 15


@pytest.mark.asyncio
async def test_run_to_thread_partial():
    p = partial(add, 10)
    res = await run_to_thread(p, 5)
    assert res == 15


@pytest.mark.asyncio
async def test_run_to_thread_lambda():
    f = lambda x, y: x * y  # noqa: E731
    res = await run_to_thread(f, 4, 7)
    assert res == 28


@pytest.mark.asyncio
async def test_run_to_thread_raises():
    def boom(x):
        raise ValueError(f"bad {x}")

    with pytest.raises(ValueError) as ei:
        await run_to_thread(boom, 42)
    assert "bad 42" in str(ei.value)


@pytest.mark.asyncio
async def test_run_to_thread_callable_check():
    with pytest.raises(TypeError):
        await run_to_thread(123)  # type: ignore[arg-type]

