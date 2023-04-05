#!/usr/bin/env python3
"""
This project contains a type-annotated function
that takes parameters and returns a list of values.
"""
from typing import Sequence, Iterable, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    This method takes parameters and returns
    a list of values.
    Returns:
        List of values with the appropriate types.
    """
    return [(i, len(i)) for i in lst]
