# Copyright (c) 2012-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

__all__ = ('cached', 'property_cached')


def cached(method):
    """Decorator to simple cache method's result"""

    from functools import wraps

    @wraps(method)
    def wrapper(self, *args, **kargs):
        key = hash(method)
        try:
            return self.__cache__[key]
        except KeyError:
            pass
        except AttributeError:
            self.__cache__ = {}
        self.__cache__[key] = result = method(self, *args, **kargs)
        return result

    return wrapper


def property_cached(fget=None, fset=None, fdel=None, doc=None):
    """property_cached(fget=None, fset=None, fdel=None, doc=None)

    Property attribute.

      fget
        function to be used for cached getting an attribute value
      fset
        function to be used for setting an attribute value
      fdel
        function to be used for del'ing an attribute
      doc
        docstring"""

    return property(None if fget is None else cached(fget), fset, fdel, doc)
