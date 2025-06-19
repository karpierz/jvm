# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

import jni
from .lib import public
from .lib import obj


@public
class JContext(obj):

    __slots__ = ('jvm', 'jenv')

    def __init__(self, jenv: jni.JNIEnv | None = None):
        """Initializer"""
        if jenv is None:
            from .jconstants import EStatusCode
            from .jvm        import JVMError
            raise JVMError(EStatusCode.EDETACHED,
                           "Unable to use JVM: thread detached from the VM")
        pjvm = jni.obj(jni.POINTER(jni.JavaVM))
        jenv.GetJavaVM(pjvm)
        from .jvm import _JVM
        jvm = _JVM()
        jvm.jnijvm = jni.JVM(pjvm)
        self.jvm  = jvm   # jvm._JVM
        self.jenv = jenv  # jni.JNIEnv

    def __iter__(self):
        """Iterator"""
        return iter((self.jvm, self.jenv))
