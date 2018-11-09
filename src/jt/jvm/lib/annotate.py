# Copyright (c) 2012-2018 Adam Karpierz
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib

__all__ = ('annotate',)


def annotate(*args, **kargs):

    """Decorator to set a function's __annotations__ like Py3"""

    def decorate(func):
        if not getattr(func, "__annotations__", None):
            func.__annotations__ = kargs.copy()
            if args:
                func.__annotations__["return"] = args[0]
        return func

    return decorate
