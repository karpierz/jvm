# Copyright (c) 2012 Adam Karpierz
# SPDX-License-Identifier: Zlib

__all__ = ('to_int', 'to_float')


def to_int(val) -> int:
    return int(val if hasattr(val, "__int__")
                   or hasattr(val, "__trunc__") else None)


def to_float(val) -> float:
    return float(val if hasattr(val, "__float__") else None)
