# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Tuple

import jni
from .lib import public
from .lib import cached

from .jconstants  import EStatusCode
from .jframe      import JFrame
from .jstring     import JString
from .jobjectbase import JObjectBase


@public
class JException(JObjectBase):
    """Java Exception"""

    __slots__ = ('__jinfo',)

    # self._jobj:   jni.jthrowable
    # self.__jinfo: jni.jstring

    def __init__(self, thr: jni.Throwable):
        self._jobj   = jni.obj(jni.jthrowable)
        self.__jinfo = jni.obj(jni.jstring)
        _, jenv = self.jvm
        # try:
        jthr  = thr.getCause()
        jinfo = thr.getInfo()
        self._jobj   = jni.cast(jenv.NewGlobalRef(jthr)  if jthr  else 0, jni.jthrowable)
        self.__jinfo = jni.cast(jenv.NewGlobalRef(jinfo) if jinfo else 0, jni.jstring)
        # except jni.Throwable as exc:
        #     JException.__handle_unexpected(exc)
        # except Exception as exc:
        #     self.jvm.handleException(exc)

    def __del__(self):
        try: jvm, jenv = self.jvm
        except Exception: return  # pragma: no cover
        if jvm.jnijvm:
            jenv.DeleteGlobalRef(self._jobj)
            jenv.DeleteGlobalRef(self.__jinfo)

    @classmethod
    def __handle_unexpected(cls, thr: jni.Throwable):
        PyExc = cls.jvm.ExceptionsMap.get(EStatusCode.ERR, RuntimeError)
        raise PyExc("An error occured while handling a Java Exception")

    def asObject(self) -> Optional['JObject']:

        with self.jvm as (jvm, jenv):
            try:
                return self.jvm.JObject(jenv, self._jobj) if self._jobj else None
            except jni.Throwable as exc:
                JException.__handle_unexpected(exc)

    @cached
    def getClass(self) -> Optional['JClass']:
        """Returns the runtime class of this Object."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            try:
                if jvm is None or jenv is None or not self._jobj:
                    return None
                jcls = jenv.GetObjectClass(self._jobj)
                return self.jvm.JClass(jenv, jcls)
            except jni.Throwable as exc:
                JException.__handle_unexpected(exc)

    @cached
    def hashCode(self) -> Optional[int]:
        """Returns a hash code value for the object.
        See Object.hashCode() for a complete description.
        """
        with self.jvm as (jvm, jenv):
            try:
                if jvm is None or jenv is None or not self._jobj:
                    return None
                return int(jenv.CallIntMethod(self._jobj, jvm.Object.hashCode))
            except jni.Throwable as exc:
                JException.__handle_unexpected(exc)

    def toString(self) -> Optional[str]:
        """Returns a string representation of the object."""
        with self.jvm as (jvm, jenv):
            try:
                if jvm is None or jenv is None or not self._jobj:
                    return None
                with JFrame(jenv, 1):
                    jstr = jenv.CallObjectMethod(self._jobj, jvm.Object.toString)
                    return JString(jenv, jstr, own=False).str if jstr else None
            except jni.Throwable as exc:
                JException.__handle_unexpected(exc)

    def getMessage(self) -> Optional[str]:
        """Returns the detail message string of this throwable."""
        with self.jvm as (jvm, jenv):
            try:
                if jvm is None or jenv is None or not self._jobj:
                    return None
                with JFrame(jenv, 1):
                    jstr = jenv.CallObjectMethod(self._jobj, jvm.Throwable.getMessage)
                    return JString(jenv, jstr, own=False).str if jstr else None
            except jni.Throwable as exc:
                JException.__handle_unexpected(exc)

    def getLocalizedMessage(self) -> Optional[str]:
        """Creates a localized description of this throwable."""
        with self.jvm as (jvm, jenv):
            try:
                if jvm is None or jenv is None or not self._jobj:
                    return None
                with JFrame(jenv, 1):
                    jstr = jenv.CallObjectMethod(self._jobj, jvm.Throwable.getLocalizedMessage)
                    return JString(jenv, jstr, own=False).str if jstr else None
            except jni.Throwable as exc:
                JException.__handle_unexpected(exc)

    def getCause(self) -> Optional['JException']:
        """Returns the cause of this throwable or null if the cause is nonexistent
        or unknown.
        """
        with self.jvm as (jvm, jenv):
            try:
                if jvm is None or jenv is None or not self._jobj:
                    return None
                with JFrame(jenv, 1):
                    jthr = jenv.CallObjectMethod(self._jobj, jvm.Throwable.getCause)
                    return self.jvm.JException(jni.Throwable(jthr)) if jthr else None
            except jni.Throwable as exc:
                JException.__handle_unexpected(exc)

    def getStackTrace(self) -> Optional[Tuple['JObject', ...]]:
        """Provides programmatic access to the stack trace information printed by
        printStackTrace().
        """
        with self.jvm as (jvm, jenv):
            try:
                if jvm is None or jenv is None or not self._jobj:
                    return None
                with JFrame(jenv, 1):
                    jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                          jvm.Throwable.getStackTrace),
                                                          jni.jobjectArray)
                    jlen = jenv.GetArrayLength(jarr)
                    with JFrame(jenv, jlen):
                        return tuple(self.jvm.JObject(jenv, jenv.GetObjectArrayElement(jarr, idx))
                                     for idx in range(jlen))
            except jni.Throwable as exc:
                JException.__handle_unexpected(exc)

    def getStackTraceString(self) -> Optional[str]:
        """Returns this throwable and its backtrace information as string printed by
        printStackTrace().
        """
        with self.jvm as (jvm, jenv):
            try:
                if jvm is None or jenv is None or not self._jobj:
                    return None
                with JFrame(jenv, 3):
                    stringWriter = jenv.NewObject(jvm.StringWriter.Class,
                                                  jvm.StringWriter.Constructor)
                    jargs = jni.new_array(jni.jvalue, 1)
                    jargs[0].l = stringWriter
                    printWriter = jenv.NewObject(jvm.PrintWriter.Class,
                                                 jvm.PrintWriter.Constructor, jargs)
                    jargs = jni.new_array(jni.jvalue, 1)
                    jargs[0].l = printWriter
                    jenv.CallVoidMethod(self._jobj,
                                        jvm.Throwable.printStackTrace, jargs)
                    jenv.CallVoidMethod(printWriter, jvm.PrintWriter.flush)

                    jstr = jenv.CallObjectMethod(stringWriter, jvm.Object.toString)
                    return JString(jenv, jstr, own=False).str if jstr else None
            except jni.Throwable as exc:
                JException.__handle_unexpected(exc)

    # Below additions from JNI.

    def throw(self):
        """Causes Java to throw this exception."""
        jvm, jenv = self.jvm
        if self._jobj:
            jenv.Throw(self._jobj)
        else:
            location = JString(jenv, self.__jinfo, own=False).str
            message  = f"Unknown from: {location}" if location else "Unknown"
            jenv.ThrowNew(jvm.java_lang.RuntimeException, message.encode("utf-8"))

    @classmethod
    def printDescribe(cls):
        """Prints an exception and a backtrace of the stack to a system error-reporting
        channel, such as stderr. This is a convenience routine provided for debugging.
        This will only have an effect if the jvm flag 'describe_exceptions' is set.
        """
        with cls.jvm as (jvm, jenv):
            try:
                if jvm.data.get("describe_exceptions", False):
                    jenv.ExceptionDescribe()
            except jni.Throwable as exc:
                JException.__handle_unexpected(exc)
