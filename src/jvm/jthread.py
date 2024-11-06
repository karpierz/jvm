# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Tuple

import jni
from .lib import public

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
        """Returns a reference to the currently executing thread object."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jthread = jenv.CallStaticObjectMethod(jvm.Thread.Class,
                                                  jvm.Thread.currentThread)
            return cls.jvm.JThread(jenv, jthread)

    def getId(self) -> int:
        """Returns the identifier of this thread."""
        with self.jvm as (jvm, jenv):
            return jenv.CallLongMethod(self._jobj, jvm.Thread.getId)

    def getName(self) -> str:
        """Returns this thread's name."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jname = jenv.CallObjectMethod(self._jobj, jvm.Thread.getName)
            return JString(jenv, jname, own=False).str

    def getContextClassLoader(self) -> Optional[JClassLoader]:
        """Returns the context ClassLoader for this thread."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcld = jenv.CallObjectMethod(self._jobj, jvm.Thread.getContextClassLoader)
            return self.jvm.JClassLoader(jenv, jcld) if jcld else None

    def setContextClassLoader(self, jcloader: Optional[JClassLoader]):
        """Sets the context ClassLoader for this thread."""
        with self.jvm as (jvm, jenv):
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = jcloader.handle if jcloader is not None else jni.NULL
            jenv.CallVoidMethod(self._jobj, jvm.Thread.setContextClassLoader, jargs)

    def isDaemon(self) -> bool:
        """Tests if this thread is a daemon thread."""
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Thread.isDaemon)

    def isAlive(self) -> bool:
        """Tests if this thread is alive."""
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Thread.isAlive)

    def isInterrupted(self) -> bool:
        """Tests whether the current thread has been interrupted."""
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Thread.isInterrupted)

    def start(self):
        """Causes this thread to begin execution; the Java Virtual Machine calls
        the run method of this thread.
        """
        with self.jvm as (jvm, jenv):
            jenv.CallVoidMethod(self._jobj, jvm.Thread.start)

    def join(self):
        """Waits for this thread to die."""
        with self.jvm as (jvm, jenv):
            jenv.CallVoidMethod(self._jobj, jvm.Thread.join)

    def interrupt(self):
        """Interrupts this thread."""
        with self.jvm as (jvm, jenv):
            jenv.CallVoidMethod(self._jobj, jvm.Thread.interrupt)

    def getStackTrace(self) -> Tuple['JObject', ...]:
        """Returns an array of stack trace elements representing the stack dump
        of this thread.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                  jvm.Thread.getStackTrace),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JObject(jenv,
                                              jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))
