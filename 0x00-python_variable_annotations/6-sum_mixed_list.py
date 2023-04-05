#!/usr/bin/env python3
"""
This project contains a type-annotated function
that takes a list of integers and floats and returns
their sum as a float.
"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    A method that takes a list of integers
    and floats and returns their sum as a float.
    Returns:
        A sum of integers and floats as a float.
    """
    total: float = 0
    for ele in range(0, len(mxd_lst)):
        total = total + mxd_lst[ele]

    return total
