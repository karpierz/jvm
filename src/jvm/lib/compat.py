# Copyright (c) 2012-2021 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

__all__ = ('byte', 'long', 'obj')

from builtins import int as long

byte = lambda val: val  # ord in Py2


class obj:

    __slots__ = ('__cache__',)

    def __init__(self, *args, **kwargs):
        pass


def meta_dict(cls):
    mdict = cls.__dict__.copy()
    mdict.pop("__dict__", None)
    mdict.pop("__weakref__", None)
    if hasattr(cls, "__qualname__"):
        mdict["__qualname__"] = cls.__qualname__
    slots = mdict.get("__slots__")
    if slots is not None:
        if isinstance(slots, str):
            slots = [slots]
        for slots_var in slots:
            mdict.pop(slots_var)
    return mdict
