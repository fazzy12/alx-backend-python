#!/usr/bin/env python3
"""
This project contains a type-annotated function
that takes a float multiplier as argument and returns
a function that multiplies a float by multiplier.
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    This method  takes a float multiplier as
    argument and returns a function that multiplies a
    float by multiplier.
    Returns:
        A function.
    """
    def multi_func(x: float) -> float:
        """
        Returns  float.
        """
        return x * multiplier
    return multi_func
