# Copyright (c) 2018 Adam Karpierz
# SPDX-License-Identifier: Zlib

from __future__ import annotations

__all__ = ('dll_path', 'python_dll_path')

from pathlib import Path


def dll_path(handle) -> Path | None:
    """???"""
    import ctypes as ct
    from ctypes.wintypes import HANDLE, LPWSTR, DWORD
    MAX_PATH = 520
    buf = ct.create_unicode_buffer(MAX_PATH)
    GetModuleFileName = ct.windll.kernel32.GetModuleFileNameW
    GetModuleFileName.argtypes = HANDLE, LPWSTR, DWORD
    GetModuleFileName.restype  = DWORD
    result = GetModuleFileName(handle, buf, len(buf))
    dll_path = buf.value
    return (Path(dll_path) if result != 0
            and dll_path and Path(dll_path).exists() else None)


def python_dll_path() -> Path | None:
    """???"""
    import ctypes as ct
    return dll_path(ct.pythonapi._handle)
