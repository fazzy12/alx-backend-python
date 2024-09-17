#!/usr/bin/env python3
from typing import Callable
"""8-make_multiplier.py"""

def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Returns a function that multiplies a float by the given multiplier.

    Args:
        multiplier (float): The value to multiply other float values by.

    Returns:
        Callable[[float], float]: A function that takes a float as input
        and returns the product of the input and the multiplier.
    """
    return lambda x: x * multiplier
