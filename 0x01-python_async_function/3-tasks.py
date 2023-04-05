#!/usr/bin/env python3
"""
The project module contains a function that takes in an
integer and returns a asyncio.Task
"""

import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    This module contains a function that takes in an
    integer.
        Returns: A asyncio.Task
    """
    t = asyncio.create_task(wait_random(max_delay))
    return t
