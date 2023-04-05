#!/usr/bin/env python3
"""
Contains a asynchronous coroutine
that takes no arguments. The coroutine will collect
10 random numbers using an async comprehensing over
async_generator, then return the 10 random numbers.
"""

from typing import List

async_generator = __import__(
    '0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """
    Asynchronous coroutine that takes no
    arguments. The coroutine will collect 10 random
    numbers using an async comprehensing over
    async_generator.
    Returns:
        A list of 10 random numbers.
    """
    result = [i async for i in async_generator()]
    return result
