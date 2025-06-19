# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

import jni

from ..jframe import JFrame
from . import registerClass
from .jnij import jnij


class jt_reflect_ProxyHandler(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        from .org.jt.reflect import ProxyHandler
        registerClass(jenv, "org.jt.reflect.ProxyHandler", ProxyHandler)
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"org/jt/reflect/ProxyHandler")
            self.Class       = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.Constructor = jenv.GetMethodID(jcls, b"<init>",   b"(J)V")
            self.getClass    = jenv.GetMethodID(jcls, b"getClass", b"()Ljava/lang/Class;")

class jt_ref_Reference(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        from .org.jt.ref import Reference
        registerClass(jenv, "org.jt.ref.Reference", Reference)
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"org/jt/ref/Reference")
            self.Class       = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.Constructor = jenv.GetMethodID(jcls, b"<init>", b"(Ljava/lang/Object;JLjava/lang/ref/ReferenceQueue;)V")

class jt_ref_ReferenceQueue(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        from .org.jt.ref import ReferenceQueue, ReferenceQueue_Worker
        registerClass(jenv, "org.jt.ref.ReferenceQueue",        ReferenceQueue)
        registerClass(jenv, "org.jt.ref.ReferenceQueue$Worker", ReferenceQueue_Worker)
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"org/jt/ref/ReferenceQueue")
            self.Class             = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.Constructor       = jenv.GetMethodID(jcls, b"<init>",            b"()V")
            self.start             = jenv.GetMethodID(jcls, b"start",             b"()V")
            self.stop              = jenv.GetMethodID(jcls, b"stop",              b"()V")
            self.registerReference = jenv.GetMethodID(jcls, b"registerReference", b"(Ljava/lang/Object;J)Lorg/jt/ref/Reference;")
