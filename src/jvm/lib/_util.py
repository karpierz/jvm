# Copyright (c) 2012 Adam Karpierz
# SPDX-License-Identifier: Zlib

__all__ = ('issubtype', 'issequence', 'isiterable', 'remove_all', 'pushd',
           'print_refinfo')

from typing import Any, Sequence, Iterable, Tuple, List, Dict
from collections import abc
import contextlib


def issubtype(x: Any, t: Any) -> bool:
    return isinstance(x, type) and issubclass(x, t)


def issequence(x: Any) -> bool:
    return (isinstance(x, (Sequence, abc.Sequence)) and
            not isinstance(x, (bytes, str)))


def isiterable(x: Any) -> bool:
    return (isinstance(x, (Iterable, abc.Iterable)) and
            not isinstance(x, (bytes, str, String)))


def remove_all(list: List, value: Any) -> None:
    list[:] = (item for item in list if item != value)


@contextlib.contextmanager
def pushd(path):
    import os
    curr_dir = os.getcwd()
    os.chdir(str(path) if isinstance(path, os.PathLike) else path)
    try:
        yield
    finally:
        os.chdir(curr_dir)


def print_refinfo(obj: Any):
    import sys

    def typename(obj):
        try:
            return obj.__class__.__name__
        except AttributeError:
            pass
        try:
            return type(obj).__name__
        except AttributeError:
            pass
        return "???"

    print("Object info report",                       file=sys.stderr)
    print("    obj type: ", typename(obj),            file=sys.stderr)
    print("    obj id:   ", id(obj),                  file=sys.stderr)
    print("    ref count:", sys.getrefcount(obj) - 2, file=sys.stderr)


del contextlib
