# Copyright (c) 2012-2021 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

__all__ = ('defined',)

import sys

def defined(varname, _getframe=sys._getframe):
    frame = _getframe(1)
    return varname in frame.f_locals or varname in frame.f_globals

del sys
