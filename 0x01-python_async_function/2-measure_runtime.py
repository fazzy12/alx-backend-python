#!/usr/bin/env python3
"""
This project module contains a function that takes in two
integer arguments and measures the total execution time.
Returns a float which is the total execution time over n
(first parameter).
"""

import time
import asyncio

wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    This is a function to measure that takes in two
    integer arguments and measures the total execution time.
        Returns: A float which is the total execution time over n
        (first parameter).
    """
    start = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    total_time = time.perf_counter() - start
    return total_time / n
