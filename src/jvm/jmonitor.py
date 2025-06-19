# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

import jni
from .lib import public
from .lib import obj


@public
class JMonitor(obj):
    """Java Monitor"""

    __slots__ = ('_jobj', '_own', '__monitored')

    # self._jobj: jni.jobject

    def __init__(self, jobj: jni.jobject, own: bool = True):
        """Initializer"""
        self._jobj = jni.NULL
        self._own  = own
        self.__monitored = False
        with self.jvm as (jvm, jenv):
            if not jobj:
                from .jconstants import EStatusCode
                from .jvm        import JVMError
                raise JVMError(EStatusCode.UNKNOWN, "Allocating null Object")
            self._jobj = jni.cast(jenv.NewGlobalRef(jobj) if own else jobj, jni.jobject)
            jenv.MonitorEnter(self._jobj)
            self.__monitored = True

    def __del__(self):
        """Finalizer"""
        if not self._own or not self.jvm: return
        try: jvm, jenv = self.jvm
        except Exception: return  # pragma: no cover
        if jvm.jnijvm:
            if self.__monitored:
                jenv.MonitorExit(self._jobj)
            jenv.DeleteGlobalRef(self._jobj)

    handle = property(lambda self: self._jobj)

    def __enter__(self):
        """Enter context"""
        return self

    def __exit__(self, *exc_info):
        """Exit context"""
        del exc_info
        if not self.__monitored: return
        with self.jvm as (jvm, jenv):
            jenv.MonitorExit(self._jobj)
            self.__monitored = False

    def __str__(self):
        """Returns the hash code of this monitor"""
        # TODO
        raise NotImplementedError("JMonitor.__str__ not implemented")
