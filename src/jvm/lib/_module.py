# Copyright (c) 2018-2021 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

__all__ = ('module_path',)

import sys
import pathlib


def module_path():
    frame = sys._getframe(1)
    return pathlib.Path(frame.f_globals["__file__"]).resolve().parent
