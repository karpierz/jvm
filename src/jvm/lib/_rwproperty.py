# Read & write properties
#
# Copyright (c) 2006 by Philipp "philiKON" von Weitershausen
#                       philikon@philikon.de
#
# Freely distributable under the terms of the Zope Public License, v2.1.

__all__ = ('get', 'set', 'delete')

import sys


class _property:

    def __new__(cls, func):
        # ugly, but common hack
        oldprop = sys._getframe(1).f_locals.get(func.__name__)
        if oldprop is None:
            return cls.create_property(func)
        elif isinstance(oldprop, property):
            return cls.enhance_property(oldprop, func)
        else:
            raise TypeError("read & write properties cannot be mixed with "
                            "other attributes except regular property objects.")

    @staticmethod
    def create_property(func):
        raise NotImplementedError()

    @staticmethod
    def enhance_property(oldprop, func):
        raise NotImplementedError()


class get(_property):

    @staticmethod
    def create_property(func):
        return property(func)

    @staticmethod
    def enhance_property(oldprop, func):
        return property(func, oldprop.fset, oldprop.fdel)


class set(_property):  # noqa: A001

    @staticmethod
    def create_property(func):
        return property(None, func)

    @staticmethod
    def enhance_property(oldprop, func):
        return property(oldprop.fget, func, oldprop.fdel)


class delete(_property):

    @staticmethod
    def create_property(func):
        return property(None, None, func)

    @staticmethod
    def enhance_property(oldprop, func):
        return property(oldprop.fget, oldprop.fset, func)


if __name__ == "__main__":
    import doctest
    doctest.testfile("rwproperty.txt")
