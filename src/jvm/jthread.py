# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Tuple

from public import public
import jni

from .jframe       import JFrame
from .jstring      import JString
from .jobjectbase  import JObjectBase
from .jclassloader import JClassLoader


@public
class JThread(JObjectBase):

    """Java Thread"""

    __slots__ = ()

    @classmethod
    def currentThread(cls) -> 'JThread':

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jthread = jenv.CallStaticObjectMethod(jvm.Thread.Class, jvm.Thread.currentThread)
            return cls.jvm.JThread(jenv, jthread)

    def getId(self) -> int:

        with self.jvm as (jvm, jenv):
            return jenv.CallLongMethod(self._jobj, jvm.Thread.getId)

    def getName(self) -> str:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jname = jenv.CallObjectMethod(self._jobj, jvm.Thread.getName)
            return JString(jenv, jname, own=False).str

    def getContextClassLoader(self) -> Optional[JClassLoader]:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcld = jenv.CallObjectMethod(self._jobj, jvm.Thread.getContextClassLoader)
            return self.jvm.JClassLoader(jenv, jcld) if jcld else None

    def setContextClassLoader(self, jcloader: Optional[JClassLoader]):

        with self.jvm as (jvm, jenv):
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = jcloader.handle if jcloader is not None else jni.NULL
            jenv.CallVoidMethod(self._jobj, jvm.Thread.setContextClassLoader, jargs)

    def isDaemon(self) -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Thread.isDaemon)

    def isAlive(self) -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Thread.isAlive)

    def isInterrupted(self) -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Thread.isInterrupted)

    def start(self):

        with self.jvm as (jvm, jenv):
            jenv.CallVoidMethod(self._jobj, jvm.Thread.start)

    def join(self):

        with self.jvm as (jvm, jenv):
            jenv.CallVoidMethod(self._jobj, jvm.Thread.join)

    def interrupt(self):

        with self.jvm as (jvm, jenv):
            jenv.CallVoidMethod(self._jobj, jvm.Thread.interrupt)

    def getStackTrace(self) -> Tuple['JObject', ...]:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                  jvm.Thread.getStackTrace),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JObject(jenv, jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))
