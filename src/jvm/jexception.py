# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Tuple

from public import public
import jni
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
        #     JException.__raise_unexpected()
        # except Exception as exc:
        #     self.jvm.handleException(exc)

    def __del__(self):
        try: jvm, jenv = self.jvm
        except: return  # pragma: no cover
        if jvm.jnijvm:
            jenv.DeleteGlobalRef(self._jobj)
            jenv.DeleteGlobalRef(self.__jinfo)

    @classmethod
    def __raise_unexpected(cls):
        PyExc = cls.jvm.ExceptionsMap.get(EStatusCode.ERR, RuntimeError)
        raise PyExc("An error occured while handling a Java Exception")

    def asObject(self) -> Optional['JObject']:

        with self.jvm as (jvm, jenv):
            try:
                return self.jvm.JObject(jenv, self._jobj) if self._jobj else None
            except jni.Throwable as exc:
                JException.__raise_unexpected()

    @cached
    def getClass(self) -> Optional['JClass']:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            try:
                if jvm is None or jenv is None or not self._jobj:
                    return None
                jcls = jenv.GetObjectClass(self._jobj)
                return self.jvm.JClass(jenv, jcls)
            except jni.Throwable as exc:
                JException.__raise_unexpected()

    @cached
    def hashCode(self) -> Optional[int]:

        with self.jvm as (jvm, jenv):
            try:
                if jvm is None or jenv is None or not self._jobj:
                    return None
                return int(jenv.CallIntMethod(self._jobj, jvm.Object.hashCode))
            except jni.Throwable as exc:
                JException.__raise_unexpected()

    def toString(self) -> Optional[str]:

        with self.jvm as (jvm, jenv):
            try:
                if jvm is None or jenv is None or not self._jobj:
                    return None
                with JFrame(jenv, 1):
                    jstr = jenv.CallObjectMethod(self._jobj, jvm.Object.toString)
                    return JString(jenv, jstr, own=False).str if jstr else None
            except jni.Throwable as exc:
                JException.__raise_unexpected()

    def getMessage(self) -> Optional[str]:

        with self.jvm as (jvm, jenv):
            try:
                if jvm is None or jenv is None or not self._jobj:
                    return None
                with JFrame(jenv, 1):
                    jstr = jenv.CallObjectMethod(self._jobj, jvm.Throwable.getMessage)
                    return JString(jenv, jstr, own=False).str if jstr else None
            except jni.Throwable as exc:
                JException.__raise_unexpected()

    def getLocalizedMessage(self) -> Optional[str]:

        with self.jvm as (jvm, jenv):
            try:
                if jvm is None or jenv is None or not self._jobj:
                    return None
                with JFrame(jenv, 1):
                    jstr = jenv.CallObjectMethod(self._jobj, jvm.Throwable.getLocalizedMessage)
                    return JString(jenv, jstr, own=False).str if jstr else None
            except jni.Throwable as exc:
                JException.__raise_unexpected()

    def getCause(self) -> Optional['JException']:

        with self.jvm as (jvm, jenv):
            try:
                if jvm is None or jenv is None or not self._jobj:
                    return None
                with JFrame(jenv, 1):
                    jthr = jenv.CallObjectMethod(self._jobj, jvm.Throwable.getCause)
                    return self.jvm.JException(jni.Throwable(jthr)) if jthr else None
            except jni.Throwable as exc:
                JException.__raise_unexpected()

    def getStackTrace(self) -> Optional[Tuple['JObject', ...]]:

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
                JException.__raise_unexpected()

    def getStackTraceString(self) -> Optional[str]:

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
                JException.__raise_unexpected()

    def throw(self):

        jvm, jenv = self.jvm
        if self._jobj:
            jenv.Throw(self._jobj)
        else:
            location = JString(jenv, self.__jinfo, own=False).str
            message  = "Unknown from: {}".format(location) if location else "Unknown"
            jenv.ThrowNew(jvm.java_lang.RuntimeException, message.encode("utf-8"))

    @classmethod
    def printDescribe(cls):

        with cls.jvm as (jvm, jenv):
            try:
                if jvm.data.get("describe_exceptions", False):
                    jenv.ExceptionDescribe()
            except jni.Throwable as exc:
                JException.__raise_unexpected()
