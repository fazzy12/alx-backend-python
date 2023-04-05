#!/usr/bin/env python3
"""
The project contains a type-annotated function that
takes a list of floats as argument and returns their sum as
a float.
"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """
    The method takes a list of floats
    as argument and returns their sum as a float.
    Returns:
        A sum of floats as a float.
    """
    return sum(input_list)
