# Copyright (c) 2012-2022 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

__all__ = ('adict', 'defaultadict')

from collections import defaultdict


class __adict:

    class __AttributeAndKeyError(AttributeError, KeyError):
        __doc__ = AttributeError.__doc__

    def __getattr__(self, name):
        try:
            return self.__getitem__(name)
        except KeyError as exc:
            raise self.__AttributeAndKeyError(*exc.args) from None

    def __setattr__(self, name, value):
        try:
            return self.__setitem__(name, value)
        except KeyError as exc:
            raise self.__AttributeAndKeyError(*exc.args) from None

    def __delattr__(self, name):
        try:
            return self.__delitem__(name)
        except KeyError as exc:
            raise self.__AttributeAndKeyError(*exc.args) from None


class adict(__adict, dict):

    @classmethod
    def fromkeys(cls, seq, value=None):
        self = super().fromkeys(seq, value)
        return cls(self)

    def copy(self):
        return self.__class__(self)


class defaultadict(__adict, defaultdict):

    @classmethod
    def fromkeys(cls, seq, value=None):
        self = super().fromkeys(seq, value)
        return cls(self.default_factory, self)

    def copy(self):
        return self.__class__(self)


del defaultdict
