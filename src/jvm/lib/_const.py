# Copyright (c) 2012 Adam Karpierz
# SPDX-License-Identifier: Zlib

__all__ = ('const', 'weakconst')

import weakref


class const:

    __slots__ = ('__value', '__doc__')

    def __init__(self, value=None, doc=None):
        self.__value = value
        self.__doc__ = doc

    def __get__(self, this, cls):
        return self.__value

    def __set__(self, this, value):
        raise TypeError("readonly attribute")

    def __delete__(self, this):
        raise TypeError("readonly attribute")


class weakconst:

    __slots__ = ('__value', '__doc__')

    def __init__(self, value=None, doc=None):
        self.__value = weakref.ref(value)
        self.__doc__ = doc

    def __get__(self, this, cls):
        return self.__value()

    def __set__(self, this, value):
        raise TypeError("readonly attribute")

    def __delete__(self, this):
        raise TypeError("readonly attribute")
