# Copyright (c) 2012 Adam Karpierz
# SPDX-License-Identifier: Zlib

__all__ = ('unique', 'iter_unique')

from typing import Any, Optional, Callable, List
from collections.abc import Iterable, Iterator
from itertools import filterfalse


def unique(iterable: Iterable) -> List:
    """List unique elements, preserving order."""
    return list(dict.fromkeys(iterable))


def iter_unique(iterable: Iterable,
                key: Optional[Callable[[Any], Any]] = None) -> Iterator:
    # Borroweed from: https://docs.python.org/3/library/itertools.html
    """List unique elements, preserving order.
    Remember all elements ever seen."""
    # iter_unique('AAAABBBCCDAABBB') --> A B C D
    # iter_unique('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element
