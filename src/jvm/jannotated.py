# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

from typing import Tuple

import jni
from .lib import public
from .lib import obj
from .lib import cached

from .jframe      import JFrame
from .jannotation import JAnnotation


@public
class JAnnotatedElement(obj):
    """Java AnnotatedElement"""

    __slots__ = ()

    @cached
    def getDeclaredAnnotations(self) -> Tuple[JAnnotation, ...]:
        """Returns annotations that are directly present on this element."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                  jvm.AnnotatedElement.getDeclaredAnnotations),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JAnnotation(jenv, jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))

    @cached
    def getAnnotations(self) -> Tuple[JAnnotation, ...]:
        """Returns annotations that are directly present on this element."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                  jvm.AnnotatedElement.getAnnotations),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JAnnotation(jenv, jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))
