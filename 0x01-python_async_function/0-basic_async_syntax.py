#!/usr/bin/env python3
"""
contains an asynchronous coroutine that
takes an integer argument with a default value of 10, waits
for a random delay (float) between 0 and 10 and then returns
the value of the delay.
"""

import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """
    asynchronous coroutine that takes a parameter
    (integer), waits for a random delay and returns the value
    of the delay (float).
    Returns:
        Value of random delay (float).
    """
    i = random.uniform(0, max_delay)
    await asyncio.sleep(i)
    return i
