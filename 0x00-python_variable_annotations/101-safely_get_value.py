#!/usr/bin/env python3
'''
This contains a function.
'''
from typing import Tuple, Mapping, Any, TypeVar, Union


T = TypeVar('T')


def safely_get_value(
    dct: Mapping, key: Any, default: Union[T, None] = None
) -> Union[Any, T]:
    '''
    This returns the key value of the dct if it exists, otherwise default.
    '''
    if key in dct:
        return dct[key]
    else:
        return default
