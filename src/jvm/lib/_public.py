# @public -- populate __all__
#
# Copyright (C) 2016-2020 Barry A. Warsaw
#
# This project is licensed under the terms of the Apache 2.0 License.

__all__ = ('public',)

import sys


def public(thing=None, **kwargs):
    mdict = (sys._getframe(1).f_globals
             if thing is None else
             sys.modules[thing.__module__].__dict__)
    dunder_all = mdict.setdefault("__all__", [])
    if not isinstance(dunder_all, list):
        raise ValueError("__all__ must be a list not: {}".format(type(dunder_all)))
    if thing is None:
        for key, value in kwargs.items():
            if key not in dunder_all:
                dunder_all.append(key)
            mdict[key] = value
    else:
        assert not kwargs, ("Keyword arguments are incompatible with use as decorator")
        if thing.__name__ not in dunder_all:
            dunder_all.append(thing.__name__)
    return thing
