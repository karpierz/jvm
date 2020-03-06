# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional

from public import public
import jni
from .lib import obj

# A default number of local references to reserve when using the
# PushLocalFrame JNI method. Most native jvm methods need a few local java
# references that are deleted before the method returns. Rather than trying
# to get an exact number of local references for every frame it is simpler
# to overallocate. The JNI specification mandates that there are at least
# 16 local references avaialble when enetering native code from java so
# using the same value as a default for creating new local frames means
# that native methods will have the same number of local references
# available regardless of whether the frame was created by JNI or by a call
# from PushLocalFrame.

JLOCAL_REFS = 0  # 16


@public
class JFrame(obj):

    __slots__ = ('__jenv', '__size')

    def __init__(self, jenv: jni.JNIEnv, size: int=0):
        self.__jenv = jenv
        self.__size = max(size, JLOCAL_REFS) if size else 0

    def __enter__(self):
        if self.__size: self.__jenv.PushLocalFrame(self.__size)
        return self

    def reset(self, size: Optional[int]=None):
        if self.__size: self.__jenv.PopLocalFrame(jni.NULL)
        if size is not None: self.__size = size
        if self.__size: self.__jenv.PushLocalFrame(self.__size)

    def __exit__(self, *exc_info):
        del exc_info
        if not self.__jenv: return
        if self.__size: self.__jenv.PopLocalFrame(jni.NULL)
