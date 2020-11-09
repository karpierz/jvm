# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional

import jni
from .lib import public
from .lib import obj

from .jconstants import EJavaType
from .jframe     import JFrame
from .jclass     import JClass
from .jobject    import JObject
from .jarray     import JArray
from ._util      import str2jchars


@public
class JArguments(obj):
    """ArgumentList"""

    __slots__ = ('__jvalues', '__jtypes', '_own')

    def __init__(self, size: int, own: bool = True):
        self._own = own
        self.__jvalues = (jni.new_array(jni.jvalue, size)
                          if size > 0 else
                          jni.obj(jni.POINTER(jni.jvalue)))
        self.__jtypes  = [EJavaType.VOID] * max(size, 0)

    def __del__(self):
        if not self._own or not self.jvm: return
        try: jvm, jenv = self.jvm
        except Exception: return  # pragma: no cover
        if jvm.jnijvm and self.__jvalues:
            for i, arg in enumerate(self.__jvalues):
                if self.__jtypes[i] >= EJavaType.OBJECT:
                    jenv.DeleteGlobalRef(arg.l)

    arguments = property(lambda self: self.__jvalues)
    argtypes  = property(lambda self: self.__jtypes)

    def setBoolean(self, pos: int, val: bool):

        try:
            self.__jvalues[pos].z = val
            self.__jtypes[pos]    = EJavaType.BOOLEAN
        except Exception as exc:
            self.jvm.handleException(exc)

    def setChar(self, pos: int, val: str):

        try:
            self.__jvalues[pos].c = val
            self.__jtypes[pos]    = EJavaType.CHAR
        except Exception as exc:
            self.jvm.handleException(exc)

    def setByte(self, pos: int, val: int):

        try:
            self.__jvalues[pos].b = val
            self.__jtypes[pos]    = EJavaType.BYTE
        except Exception as exc:
            self.jvm.handleException(exc)

    def setShort(self, pos: int, val: int):

        try:
            self.__jvalues[pos].s = val
            self.__jtypes[pos]    = EJavaType.SHORT
        except Exception as exc:
            self.jvm.handleException(exc)

    def setInt(self, pos: int, val: int):

        try:
            self.__jvalues[pos].i = val
            self.__jtypes[pos]    = EJavaType.INT
        except Exception as exc:
            self.jvm.handleException(exc)

    def setLong(self, pos: int, val: int):

        try:
            self.__jvalues[pos].j = val
            self.__jtypes[pos]    = EJavaType.LONG
        except Exception as exc:
            self.jvm.handleException(exc)

    def setFloat(self, pos: int, val: float):

        try:
            self.__jvalues[pos].f = val
            self.__jtypes[pos]    = EJavaType.FLOAT
        except Exception as exc:
            self.jvm.handleException(exc)

    def setDouble(self, pos: int, val: float):

        try:
            self.__jvalues[pos].d = val
            self.__jtypes[pos]    = EJavaType.DOUBLE
        except Exception as exc:
            self.jvm.handleException(exc)

    def setString(self, pos: int, val: Optional[str]):

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            if val is None:
                self.__jvalues[pos].l = jni.NULL
            else:
                if not isinstance(val, str):
                    raise TypeError("str expected instead of {}".format(type(val)))
                jchars, size, jbuf = str2jchars(val)
                jstr = jenv.NewString(jchars, size)
                self.__jvalues[pos].l = jenv.NewGlobalRef(jstr)
            self.__jtypes[pos] = EJavaType.STRING

    def setClass(self, pos: int, val: Optional[JClass]):

        with self.jvm as (jvm, jenv):
            if val is None:
                self.__jvalues[pos].l = jni.NULL
            else:
                if not isinstance(val, self.jvm.JClass):
                    raise TypeError("JClass expected instead of {}".format(type(val)))
                self.__jvalues[pos].l = jenv.NewGlobalRef(val.handle)
            self.__jtypes[pos]    = EJavaType.CLASS

    def setObject(self, pos: int, val: Optional[JObject]):

        with self.jvm as (jvm, jenv):
            if val is None:
                self.__jvalues[pos].l = jni.NULL
            else:
                if not isinstance(val, self.jvm.JObject):
                    raise TypeError("JObject expected instead of {}".format(type(val)))
                self.__jvalues[pos].l = jenv.NewGlobalRef(val.handle)
            self.__jtypes[pos]    = EJavaType.OBJECT

    def setArray(self, pos: int, val: Optional[JArray]):

        with self.jvm as (jvm, jenv):
            if val is None:
                self.__jvalues[pos].l = jni.NULL
            else:
                if not isinstance(val, self.jvm.JArray):
                    raise TypeError("JArray expected instead of {}".format(type(val)))
                self.__jvalues[pos].l = jenv.NewGlobalRef(val.handle)
            self.__jtypes[pos]    = EJavaType.ARRAY
