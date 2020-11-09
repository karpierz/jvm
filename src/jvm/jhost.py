# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import ctypes as ct
import traceback

from .lib import public

from .jhostabc import JHostABC

PyEval_SaveThread    = lambda *args, **kwargs: None  # !!! Py_UNBLOCK_THREADS
PyEval_RestoreThread = lambda *args, **kwargs: None  # !!! Py_BLOCK_THREADS
PyGILState_Ensure    = lambda *args, **kwargs: None  # !!!
PyGILState_Release   = lambda *args, **kwargs: None  # !!!
Py_IncRef = ct.pythonapi.Py_IncRef
Py_IncRef.argtypes = [ct.py_object]
Py_IncRef.restype  = None
Py_DecRef = ct.pythonapi.Py_DecRef
Py_DecRef.argtypes = [ct.py_object]
Py_DecRef.restype  = None


@public
class JHost(JHostABC):

    __slots__ = ()

    class ThreadState(JHostABC.ThreadState):

        __slots__ = ('_state',)

        def __init__(self):
            self._state = None

        def __enter__(self):
            self._state = None  # PyEval_SaveThread()

        def __exit__(self, *exc_info):
            del exc_info
            # PyEval_RestoreThread(self._state)

    class CallbackState(JHostABC.CallbackState):

        __slots__ = ('ctx', '_state')

        def __init__(self, ctx=None):
            self.ctx    = ctx
            self._state = None

        def __enter__(self):
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
            del exc_info
            # PyGILState_Release(self._state)

    @classmethod
    def incRef(cls, obj):
        Py_IncRef(obj)

    @classmethod
    def decRef(cls, obj):
        Py_DecRef(obj)
