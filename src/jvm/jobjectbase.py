# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional

import jni
from .lib import public
from .lib import obj
from .lib import cached

from .jframe  import JFrame
from .jstring import JString


@public
class JObjectBase(obj):
    """Object Base"""

    __slots__ = ('_jobj', '_own')

    # self._jobj: jni.jobject

    def __init__(self, jenv: jni.JNIEnv, jobj: jni.jobject, own: bool = True):
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
        except Exception: return  # pragma: no cover
        if jvm.jnijvm:
            jenv.DeleteGlobalRef(self._jobj)

    handle = property(lambda self: self._jobj)

    def __hash__(self):
        """Returns a hash code value for the object."""
        return int(self.hashCode())

    def __eq__(self, other):

        if self is other:
            return True

        if not isinstance(other, JObjectBase):
            return NotImplemented

        self_handle  = self._jobj
        other_handle = other.handle

        if self_handle == other_handle:
            return True  # pragma: no cover

        if self.hashCode() != other.hashCode():
            return False

        with self.jvm as (jvm, jenv):
            return jenv.IsSameObject(self_handle, other_handle)

    def __ne__(self, other):
        eq = self.__eq__(other)
        return NotImplemented if eq is NotImplemented else not eq

    def __str__(self):
        """Returns a string representation of the object."""
        return self.toString()

    @cached
    def getClass(self) -> 'JClass':
        """Returns the runtime class of this Object."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.GetObjectClass(self._jobj)
            return self.jvm.JClass(jenv, jcls)

    @cached
    def hashCode(self) -> int:
        """Returns a hash code value for the object."""
        with self.jvm as (jvm, jenv):
            return int(jenv.CallIntMethod(self._jobj, jvm.Object.hashCode))

    @cached
    def toString(self) -> Optional[str]:
        """Returns a string representation of the object."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jstr = jenv.CallObjectMethod(self._jobj, jvm.Object.toString)
            return JString(jenv, jstr, own=False).str if jstr else None

    def equals(self, other) -> bool:
        """Indicates whether some other object is "equal to" this one."""
        if self is other:
            return True

        if not isinstance(other, JObjectBase):
            return False

        self_handle  = self._jobj
        other_handle = other.handle

        if self_handle == other_handle:
            return True  # pragma: no cover

        with self.jvm as (jvm, jenv):
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = other_handle
            return (jenv.IsSameObject(self_handle, other_handle) or
                    jenv.CallBooleanMethod(self_handle, jvm.Object.equals, jargs))
