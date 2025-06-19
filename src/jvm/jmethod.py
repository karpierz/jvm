# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

from typing import Tuple

import jni
from .lib import public
from .lib import cached

from .jframe     import JFrame
from .jmember    import JMember
from .jannotated import JAnnotatedElement
from .jstring    import JString


@public
class JMethod(JMember, JAnnotatedElement):
    """Java Method"""

    __slots__ = ()

    @cached
    def _jmid(self, jenv: jni.JNIEnv) -> jni.jmethodID:
        return jenv.FromReflectedMethod(self._jobj)

    @cached
    def getReturnType(self) -> JClass:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.CallObjectMethod(self._jobj, jvm.Method.getReturnType)
            return self.jvm.JClass(jenv, jcls)

    @cached
    def getParameterTypes(self) -> Tuple[JClass, ...]:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            arg_types = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                       jvm.Method.getParameterTypes),
                                                       jni.jobjectArray)
            jlen = jenv.GetArrayLength(arg_types)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JClass(jenv, jenv.GetObjectArrayElement(arg_types, idx))
                             for idx in range(jlen))

    @cached
    def getExceptionTypes(self) -> Tuple[JClass, ...]:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            arg_types = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                       jvm.Method.getExceptionTypes),
                                                       jni.jobjectArray)
            jlen = jenv.GetArrayLength(arg_types)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JClass(jenv, jenv.GetObjectArrayElement(arg_types, idx))
                             for idx in range(jlen))

    @cached
    def isVarArgs(self) -> bool:
        """Returns True if this method was declared to take a variable number \
        of arguments; returns False otherwise."""
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Method.isVarArgs)

    @cached
    def getSignature(self) -> str:
        """Returns the method signature."""
        return ("(" + "".join(jcls.getSignature() for jcls in self.getParameterTypes()) + ")"
                + self.getReturnType().getSignature())

    def callStaticVoid(self, jcls: JClass, jargs: JArguments) -> None:
        """???."""
        with self.jvm as (jvm, jenv):
            jenv.CallStaticVoidMethod(jcls.handle, self._jmid(jenv), jargs.arguments)
            return None

    def callStaticBoolean(self, jcls: JClass, jargs: JArguments) -> bool:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallStaticBooleanMethod(jcls.handle, self._jmid(jenv), jargs.arguments)

    def callStaticChar(self, jcls: JClass, jargs: JArguments) -> str:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallStaticCharMethod(jcls.handle, self._jmid(jenv), jargs.arguments)

    def callStaticByte(self, jcls: JClass, jargs: JArguments) -> int:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallStaticByteMethod(jcls.handle, self._jmid(jenv), jargs.arguments)

    def callStaticShort(self, jcls: JClass, jargs: JArguments) -> int:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallStaticShortMethod(jcls.handle, self._jmid(jenv), jargs.arguments)

    def callStaticInt(self, jcls: JClass, jargs: JArguments) -> int:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallStaticIntMethod(jcls.handle, self._jmid(jenv), jargs.arguments)

    def callStaticLong(self, jcls: JClass, jargs: JArguments) -> int:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallStaticLongMethod(jcls.handle, self._jmid(jenv), jargs.arguments)

    def callStaticFloat(self, jcls: JClass, jargs: JArguments) -> float:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallStaticFloatMethod(jcls.handle, self._jmid(jenv), jargs.arguments)

    def callStaticDouble(self, jcls: JClass, jargs: JArguments) -> float:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallStaticDoubleMethod(jcls.handle, self._jmid(jenv), jargs.arguments)

    def callStaticString(self, jcls: JClass, jargs: JArguments) -> str | None:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jstr = jenv.CallStaticObjectMethod(jcls.handle, self._jmid(jenv), jargs.arguments)
            return JString(jenv, jstr, own=False).str if jstr else None

    def callStaticObject(self, jcls: JClass, jargs: JArguments) -> JObject | None:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jobj = jenv.CallStaticObjectMethod(jcls.handle, self._jmid(jenv), jargs.arguments)
            return self.jvm.JObject(jenv, jobj) if jobj else None

    def callInstanceVoid(self, this: JObject, jargs: JArguments) -> None:
        """???."""
        with self.jvm as (jvm, jenv):
            jenv.CallVoidMethod(this.handle, self._jmid(jenv), jargs.arguments)
            return None

    def callInstanceBoolean(self, this: JObject, jargs: JArguments) -> bool:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(this.handle, self._jmid(jenv), jargs.arguments)

    def callInstanceChar(self, this: JObject, jargs: JArguments) -> str:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallCharMethod(this.handle, self._jmid(jenv), jargs.arguments)

    def callInstanceByte(self, this: JObject, jargs: JArguments) -> int:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallByteMethod(this.handle, self._jmid(jenv), jargs.arguments)

    def callInstanceShort(self, this: JObject, jargs: JArguments) -> int:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallShortMethod(this.handle, self._jmid(jenv), jargs.arguments)

    def callInstanceInt(self, this: JObject, jargs: JArguments) -> int:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallIntMethod(this.handle, self._jmid(jenv), jargs.arguments)

    def callInstanceLong(self, this: JObject, jargs: JArguments) -> int:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallLongMethod(this.handle, self._jmid(jenv), jargs.arguments)

    def callInstanceFloat(self, this: JObject, jargs: JArguments) -> float:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallFloatMethod(this.handle, self._jmid(jenv), jargs.arguments)

    def callInstanceDouble(self, this: JObject, jargs: JArguments) -> float:
        """???."""
        with self.jvm as (jvm, jenv):
            return jenv.CallDoubleMethod(this.handle, self._jmid(jenv), jargs.arguments)

    def callInstanceString(self, this: JObject, jargs: JArguments) -> str | None:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jstr = jenv.CallObjectMethod(this.handle, self._jmid(jenv), jargs.arguments)
            return JString(jenv, jstr, own=False).str if jstr else None

    def callInstanceObject(self, this: JObject, jargs: JArguments) -> JObject | None:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jobj = jenv.CallObjectMethod(this.handle, self._jmid(jenv), jargs.arguments)
            return self.jvm.JObject(jenv, jobj) if jobj else None


from .jclass     import JClass      # noqa: E402
from .jarguments import JArguments  # noqa: E402
from .jobject    import JObject     # noqa: E402
