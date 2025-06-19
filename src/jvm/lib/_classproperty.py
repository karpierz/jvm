# Copyright (c) 2012 Adam Karpierz
# SPDX-License-Identifier: Zlib

__all__ = ('classproperty',)


class classproperty:

    __slots__ = ('_fget', 'fset', 'fdel', '__doc__')

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        """Initializer"""
        self._fget = fget
        if fset is not None or fdel is not None:
            raise ValueError("classproperty only implements fget.")
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = self._fget.__doc__
        self.__doc__ = doc

    def __get__(self, this, cls):
        """???"""
        fget = self._fget
        if fget is None:
            raise AttributeError("unreadable attribute")
        if not callable(fget):
            raise TypeError("'{}' object is not callable".format(
                            fget.__class__.__name__))
        return fget(cls)

    @property
    def fget(self):
        return self._fget
