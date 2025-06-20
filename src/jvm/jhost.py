# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

import ctypes as ct
import traceback

from .lib import public
from .lib import platform

from .jhostabc import JHostABC

PyEval_SaveThread    = lambda *args, **kwargs: None  # !!! Py_UNBLOCK_THREADS
PyEval_RestoreThread = lambda *args, **kwargs: None  # !!! Py_BLOCK_THREADS
PyGILState_Ensure    = lambda *args, **kwargs: None  # !!!
PyGILState_Release   = lambda *args, **kwargs: None  # !!!

if platform.is_cpython:
    Py_IncRef = ct.pythonapi.Py_IncRef
    Py_IncRef.argtypes = [ct.py_object]
    Py_IncRef.restype  = None
    Py_DecRef = ct.pythonapi.Py_DecRef
    Py_DecRef.argtypes = [ct.py_object]
    Py_DecRef.restype  = None
else:
    __objects = []
    def Py_IncRef(obj): __objects.insert(0, obj)
    def Py_DecRef(obj): __objects.remove(obj)


@public
class JHost(JHostABC):
    """???"""

    __slots__ = ()

    class ThreadState(JHostABC.ThreadState):
        """???"""

        __slots__ = ('_state',)

        def __init__(self):
            """Initializer"""
            self._state = None

        def __enter__(self):
            """Enter context"""
            self._state = None  # PyEval_SaveThread()

        def __exit__(self, *exc_info):
            """Exit context"""
            del exc_info
            # PyEval_RestoreThread(self._state)

    class CallbackState(JHostABC.CallbackState):
        """???"""

        __slots__ = ('ctx', '_state')

        def __init__(self, ctx=None):
            """Initializer"""
            self.ctx    = ctx
            self._state = None

        def __enter__(self):
            """Enter context"""
            try:
                self._state = None  # PyGILState_Ensure()
                # make sure the thread-local is initialized
                try:
                    jvm, jenv = self.ctx
                    vm = jvm.data.jvm
                    vm.__ensure__
                except (TypeError, AttributeError, KeyError):
                    pass
                else:
                    vm.__ensure__()
            except Exception as exc:
                # TODO: turn py error into exception !!!
                traceback.print_exc()
                raise exc

        def __exit__(self, *exc_info):
            """Exit context"""
            del exc_info
            # PyGILState_Release(self._state)

    @classmethod
    def incRef(cls, obj):
        Py_IncRef(obj)

    @classmethod
    def decRef(cls, obj):
        Py_DecRef(obj)
