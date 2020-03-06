# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional

from public import public
import jni
from .lib import obj
from .lib import cached

from .jframe      import JFrame
from .jstring     import JString
from .jobjectbase import JObjectBase


@public
class JAnnotation(obj):

    """Java Annotation"""

    __slots__ = ('_jobj', '_own')

    # self._jobj: jni.jobject

    def __init__(self, jenv: jni.JNIEnv, jobj: jni.jobject, own: bool=True):
        self._jobj = jni.NULL
        self._own  = own
        if not jobj:
            from .jconstants import EStatusCode
            from .jvm        import JVMException
            raise JVMException(EStatusCode.UNKNOWN, "Allocating null Object")
        self._jobj = jni.cast(jenv.NewGlobalRef(jobj) if own else jobj, jni.jobject)

    def __del__(self):
        if not self._own or not self.jvm: return
        try: jvm, jenv = self.jvm
        except: return  # pragma: no cover
        if jvm.jnijvm:
            jenv.DeleteGlobalRef(self._jobj)

    handle = property(lambda self: self._jobj)

    def __hash__(self):
        return int(self.hashCode())

    def __str__(self):
        return self.toString()

    @cached
    def annotationType(self) -> 'JClass':

        from .jclass import JClass

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.CallObjectMethod(self._jobj, jvm.Annotation.annotationType)
            return self.jvm.JClass(jenv, jcls)

    @cached
    def hashCode(self) -> int:

        with self.jvm as (jvm, jenv):
            return int(jenv.CallIntMethod(self._jobj, jvm.Annotation.hashCode))

    @cached
    def toString(self) -> Optional[str]:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jstr = jenv.CallObjectMethod(self._jobj, jvm.Annotation.toString)
            return JString(jenv, jstr, own=False).str if jstr else None

    def equals(self, other) -> bool:

        if self is other:
            return True

        if not isinstance(other, (JObjectBase, JAnnotation)):
            return False

        self_handle  = self._jobj
        other_handle = other.handle

        if self_handle == other_handle:
            return True  # pragma: no cover

        with self.jvm as (jvm, jenv):
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = other_handle
            return (jenv.IsSameObject(self_handle, other_handle) or
                    jenv.CallBooleanMethod(self_handle, jvm.Annotation.equals, jargs))
