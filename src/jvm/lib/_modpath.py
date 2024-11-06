# Copyright (c) 2018 Adam Karpierz
# SPDX-License-Identifier: Zlib

__all__ = ('module_path',)

import sys
import inspect
import pathlib


def module_path(module=None, *, level=1):
    if module is not None:
        mfile = inspect.getfile(module)
    else:
        frame = sys._getframe(level)
        module = inspect.getmodule(frame)
        if module is not None:
            mfile = inspect.getfile(module)
        else:
            mfile = frame.f_globals["__file__"]
    return pathlib.Path(mfile).resolve().parent
