#!/usr/bin/env python3

from typing import List, Union

"""function will have type annotations using
the typing module to specify
the expected input type (List[Union[int, float]])
and return type (float)."""

def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """return type is always a float."""
    return float(sum(mxd_lst))
