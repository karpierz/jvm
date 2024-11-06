# Copyright (c) 2012 Adam Karpierz
# SPDX-License-Identifier: Zlib

__all__ = ('defined',)

import sys

def defined(varname, _getframe=sys._getframe):
    frame = _getframe(1)
    return varname in frame.f_locals or varname in frame.f_globals

del sys
