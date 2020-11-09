# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import jni
from .lib import public
from .lib import obj


@public
class JString(obj):

    __slots__ = ('__jstr', '__size', '__jchars')

    def __init__(self, jenv: jni.JNIEnv=None,
                 jstr: jni.jobject=jni.obj(jni.POINTER(jni.jchar)), own: bool = True):
        self.__jstr = jni.cast(jstr, jni.jstring)
        self.__size = 0
        self.__jchars = jni.obj(jni.POINTER(jni.jchar))
        if jenv is not None and jstr:
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

    str = property(lambda self: jni.to_unicode(self.__jchars, size=self.__size))

    def __len__(self):
        return len(self.str)
