#!/usr/bin/env python3
"""
coroutinethat takes no arguments. The coroutine 
will execute async_comprehension four times in parallel using
asyncio.gather. This coroutine should measure the
total runtime and return it.
"""
import time
import asyncio


async_comprehension = __import__(
    '1-async_comprehension').async_comprehension

async def measure_runtime() -> float:
    """
    coroutine that takes no
    arguments. The coroutine will execute async_comprehension
    four times in parallel using asyncio.gather.
    Returns:
        The total runtime.
    """
    start = time.perf_counter()
    await asyncio.gather(async_comprehension(), async_comprehension(),
                        async_comprehension(), async_comprehension())
    total_time = time.perf_counter() - start
    return total_time
