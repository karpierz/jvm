# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

import jni
from .lib import public
from .lib import obj


@public
class JString(obj):

    __slots__ = ('__jstr', '__size', '__jchars')

    def __init__(self, jenv: jni.JNIEnv | None = None,
                 jstr: jni.jobject = jni.obj(jni.POINTER(jni.jchar)), own: bool = True):
        """Initializer"""
        self.__jstr = jni.cast(jstr, jni.jstring)
        self.__size = 0
        self.__jchars = jni.obj(jni.POINTER(jni.jchar))
        if jenv is None or not jstr: return
        length = jenv.GetStringLength(self.__jstr)
        jchars = jenv.GetStringChars(self.__jstr)
        try:
            self.__jchars = jni.new_array(jni.jchar, length + 1)
            jni.memmove(self.__jchars, jchars, length * jni.sizeof(jni.jchar))
            self.__jchars[length] = "\0"
        finally:
            jenv.ReleaseStringChars(self.__jstr, jchars)
        self.__size = length

    length = property(lambda self: self.__size)
    value  = property(lambda self: self.__jchars)

    str = property(lambda self: jni.to_unicode(self.__jchars, size=self.__size))  # noqa: A003

    def __len__(self):
        """Length of"""
        return len(self.str)
