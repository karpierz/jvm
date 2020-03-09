# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional

from public import public
import jni
from .lib import obj


@public
class JContext(obj):

    __slots__ = ('jvm', 'jenv')

    def __init__(self, jenv: Optional[jni.JNIEnv]=None):
        if jenv is None:
            from .jconstants import EStatusCode
            from .jvm        import JVMException
            raise JVMException(EStatusCode.EDETACHED,
                               "Unable to use JVM: thread detached from the VM")
        pjvm = jni.obj(jni.POINTER(jni.JavaVM))
        jenv.GetJavaVM(pjvm)
        from .jvm import _JVM
        jvm = _JVM()
        jvm.jnijvm = jni.JVM(pjvm)
        self.jvm  = jvm   # jvm._JVM
        self.jenv = jenv  # jni.JNIEnv

    def __iter__(self):
        return iter((self.jvm, self.jenv))
