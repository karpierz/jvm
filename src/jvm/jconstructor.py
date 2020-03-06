# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Tuple

from public import public
import jni
from .lib import cached

from .jframe     import JFrame
from .jmember    import JMember
from .jannotated import JAnnotatedElement
from .jclass     import JClass
from .jarguments import JArguments
from .jobject    import JObject


@public
class JConstructor(JMember, JAnnotatedElement):

    """Java Constructor"""

    __slots__ = ()

    @cached
    def _jcid(self, jenv):
        return jenv.FromReflectedMethod(self._jobj)

    @cached
    def getParameterTypes(self) -> Tuple[JClass, ...]:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            arg_types = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                       jvm.Constructor.getParameterTypes),
                                                       jni.jobjectArray)
            jlen = jenv.GetArrayLength(arg_types)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JClass(jenv, jenv.GetObjectArrayElement(arg_types, idx))
                             for idx in range(jlen))

    @cached
    def getExceptionTypes(self) -> Tuple[JClass, ...]:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            arg_types = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                       jvm.Constructor.getExceptionTypes),
                                                       jni.jobjectArray)
            jlen = jenv.GetArrayLength(arg_types)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JClass(jenv, jenv.GetObjectArrayElement(arg_types, idx))
                             for idx in range(jlen))

    @cached
    def isVarArgs(self) -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Constructor.isVarArgs)

    @cached
    def getSignature(self) -> str:

        return "(" + "".join(jcls.getSignature() for jcls in self.getParameterTypes()) + ")V"

    def newInstance(self, jargs: JArguments) -> Optional[JObject]:

        with self.jvm as (jvm, jenv), JFrame(jenv, 2):
            jcls = jenv.CallObjectMethod(self._jobj, jvm.Member.getDeclaringClass)
            jobj = jenv.NewObject(jcls, self._jcid(jenv), jargs.arguments)
            return self.jvm.JObject(jenv, jobj) if jobj else None
