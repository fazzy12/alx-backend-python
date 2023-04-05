#!/usr/bin/env python3
'''
This contains a function.
'''
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    '''
    Return the arguments if it is a list otherwise None.
    '''
    if lst:
        return lst[0]
    else:
        return None
