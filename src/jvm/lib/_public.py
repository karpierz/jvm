# @public -- populate __all__
#
# Copyright (C) 2016-2021 Barry A. Warsaw
#
# This project is licensed under the terms of the Apache 2.0 License.

__all__ = ('public', 'private')

import sys


def public(thing=None, **kwargs):
    """Add a name or names to __all__"""
    mdict = (sys._getframe(1).f_globals  # The function call syntax.
             if thing is None else
             sys.modules[thing.__module__].__dict__)  # The decorator syntax.
    dunder_all = mdict.setdefault("__all__", [])
    if not isinstance(dunder_all, list):
        raise ValueError(f"__all__ must be a list not: {type(dunder_all)}")
    if thing is None:
        # The function call form.
        for key, value in kwargs.items():
            if key not in dunder_all:
                dunder_all.append(key)
            mdict[key] = value
    else:
        # The decorator form.
        assert not kwargs, ("Keyword arguments are incompatible with use "
                            "as decorator")
        if thing.__name__ not in dunder_all:
            dunder_all.append(thing.__name__)
    return thing


def private(thing):
    """Remove names from __all__"""
    mdict = sys.modules[thing.__module__].__dict__
    dunder_all = mdict.setdefault("__all__", [])
    if not isinstance(dunder_all, list):
        raise ValueError(f"__all__ must be a list not: {type(dunder_all)}")
    if thing.__name__ in dunder_all:
        dunder_all.remove(thing.__name__)
    return thing
