# Copyright (c) 2012-2022 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

__all__ = ('classproperty',)


class classproperty:

    __slots__ = ('fget', 'fset', 'fdel')

    def __init__(self, fget):
        self.fget = fget
        self.fset = None
        self.fdel = None

    def __get__(self, this, cls):
        return self.fget(cls)
