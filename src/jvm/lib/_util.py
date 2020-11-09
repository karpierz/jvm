# Copyright (c) 2012-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

__all__ = ('issubtype', 'issequence', 'unique', 'pushd')

import sys
import os
from collections.abc import Sequence
from collections import OrderedDict
from contextlib  import contextmanager
from pathlib     import PurePath


def issubtype(x, t) -> bool:
    return isinstance(x, type) and issubclass(x, t)


def issequence(x) -> bool:
    return isinstance(x, Sequence) and not isinstance(x, (bytes, str))


def unique(seq) -> list:
    # Raymond Hettinger
    # https://twitter.com/raymondh/status/944125570534621185
    # return list(dict.fromkeys(seq)) # Py >= 3.7
    return list(OrderedDict.fromkeys(seq))
    # used = set()
    # return [x for x in seq if x not in used and (used.add(x) or True)]


def remove_all(list, value):
    list[:] = (x for x in list if x != value)


@contextmanager
def pushd(path):
    curr_dir = os.getcwd()
    os.chdir(str(path) if isinstance(path, PurePath) else path)
    yield
    os.chdir(curr_dir)


def print_refinfo(obj):

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
