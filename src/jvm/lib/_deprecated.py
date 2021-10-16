# Copyright (c) 2012-2021 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

__all__ = ('deprecated',)


def deprecated(func):
    """This is a decorator which can be used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used."""

    from functools import wraps
    from warnings  import warn

    @wraps(func)
    def wrapper(*args, **kargs):
        warn("Call to deprecated function '{}' ({}:{}).".format(
             func.__name__,
             func.__code__.co_filename,
             func.__code__.co_firstlineno + 1),
             category=DeprecationWarning, stacklevel=2)
        return func(*args, **kargs)

    return wrapper
