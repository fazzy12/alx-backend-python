#!/usr/bin/env python3
"""9-element_length.py"""

from typing import Iterable, Sequence, List, Tuple

def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Takes an iterable of sequences and returns a list of tuples,
    where each tuple contains a sequence and its corresponding length.

    Args:
        lst (Iterable[Sequence]): An iterable containing sequence elements
        (e.g., strings, lists).

    Returns:
        List[Tuple[Sequence, int]]: A list of tuples where each tuple
        contains a sequence
                                    and the length of that sequence.
    """
    return [(i, len(i)) for i in lst]
