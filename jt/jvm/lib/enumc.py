# Copyright (c) 2012-2018 Adam Karpierz
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib

__all__ = ('enumc',)


def enumc(*enums, **kwenums):

    return type(str("Enum"), (), dict(zip(enums, range(len(enums))), **kwenums))
