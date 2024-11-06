# Copyright (c) 2012 Adam Karpierz
# SPDX-License-Identifier: Zlib

__all__ = ('cached', 'cached_property')


def cached(method):
    """Decorator to simple cache method's result"""

    from functools import wraps

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = hash(method)
        try:
            return self.__cache__[key]
        except KeyError:
            pass
        except AttributeError:
            self.__cache__ = {}
        self.__cache__[key] = result = method(self, *args, **kwargs)
        return result

    return wrapper


def cached_property(fget=None, fset=None, fdel=None, doc=None):
    """cached_property(fget=None, fset=None, fdel=None, doc=None)

    Property attribute.

      fget
        function to be used for cached getting an attribute value
      fset
        function to be used for setting an attribute value
      fdel
        function to be used for del'ing an attribute
      doc
        docstring
    """
    return property(None if fget is None else cached(fget), fset, fdel, doc)
