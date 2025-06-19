# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

from pathlib import Path
import contextlib

from ..lib import public
from ..lib import adict

from . import _windows

RegPath = Path


@public
class JVMFinder(_windows.JVMFinder):
    """Cygwin JVM library finder class"""

    def _get_winreg(self):
        return adict(
            HKEY_LOCAL_MACHINE = "HKEY_LOCAL_MACHINE",
            HKEY_CURRENT_USER  = "HKEY_CURRENT_USER",
        )

    @contextlib.contextmanager
    def _open_key(self, key, sub_key, **kwargs):
        yield key/sub_key

    def _sub_keys(self, key):
        return []

    def _query_value(self, key, value_name):
        with open((RegPath("/proc/registry")/key/value_name).as_posix()) as f:
            return f.read().split('\x00')
