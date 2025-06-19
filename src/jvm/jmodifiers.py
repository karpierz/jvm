# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

import jni
from .lib import public
from .lib import obj


@public
class JModifiers(obj):

    __slots__ = ('isPublic', 'isProtected', 'isPrivate', 'isFinal', 'isStatic', 'isAbstract',
                 'modif')

    def __init__(self, jvm, jenv: jni.JNIEnv, modif: int):
        """Initializer"""
        Modif = jvm.Modifier
        jcls = Modif.Class
        jmod = jni.new_array(jni.jvalue, 1)
        jmod[0].i = modif
        self.isPublic    = jenv.CallStaticBooleanMethod(jcls, Modif.isPublic,    jmod)
        self.isProtected = jenv.CallStaticBooleanMethod(jcls, Modif.isProtected, jmod)
        self.isPrivate   = jenv.CallStaticBooleanMethod(jcls, Modif.isPrivate,   jmod)
        self.isFinal     = jenv.CallStaticBooleanMethod(jcls, Modif.isFinal,     jmod)
        self.isStatic    = jenv.CallStaticBooleanMethod(jcls, Modif.isStatic,    jmod)
        self.isAbstract  = jenv.CallStaticBooleanMethod(jcls, Modif.isAbstract,  jmod)
        self.modif       = modif
