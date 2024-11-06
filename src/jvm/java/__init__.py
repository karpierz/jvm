# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Sequence, Callable
import inspect

import jni


def registerClass(jenv: jni.JNIEnv, class_name: str, class_code,
                  native_methods: Optional[Sequence[Callable]] = None, class_loader=None):

    if inspect.ismodule(class_code) or inspect.isclass(class_code):
        if native_methods is None:
            native_methods = getattr(class_code, "__jnimethods__", ())
        class_code = class_code.__javacode__
    else:
        if native_methods is None: native_methods = ()

    jenv.PushLocalFrame(3)
    try:
        if class_loader is None:
            jcls = jenv.FindClass(b"java/lang/ClassLoader")
            jmid = jenv.GetStaticMethodID(jcls, b"getSystemClassLoader",
                                                b"()Ljava/lang/ClassLoader;")
            class_loader = jenv.CallStaticObjectMethod(jcls, jmid)

        try:
            jcls = jenv.FindClass(class_name.replace(".", "/").encode("utf-8"))
        except Exception:
            size = len(class_code)
            jcls = jenv.DefineClass(class_name.replace(".", "/").encode("utf-8"),
                                    class_loader,
                                    jni.cast(jni.from_buffer(class_code),
                                             jni.POINTER(jni.jbyte)),
                                    size)
        methods = jni.new_array(jni.JNINativeMethod, len(native_methods))
        for idx, method in enumerate(native_methods):
            methods[idx] = method
        jenv.RegisterNatives(jcls, methods, len(methods))
    finally:
        jenv.PopLocalFrame(jni.NULL)


def registerNatives(jenv: jni.JNIEnv, class_name: str, native_methods: Sequence[Callable]):

    if inspect.ismodule(native_methods) or inspect.isclass(native_methods):
        native_methods = getattr(native_methods, "__jnimethods__", ())
    else:
        if native_methods is None: native_methods = ()

    jenv.PushLocalFrame(1)
    try:
        jcls = jenv.FindClass(class_name.replace(".", "/").encode("utf-8"))
        methods = jni.new_array(jni.JNINativeMethod, len(native_methods))
        for idx, method in enumerate(native_methods):
            methods[idx] = method
        jenv.RegisterNatives(jcls, methods, len(methods))
    finally:
        jenv.PopLocalFrame(jni.NULL)


def unregisterNatives(jenv: jni.JNIEnv, class_name: str):

    jenv.PushLocalFrame(1)
    try:
        jcls = jenv.FindClass(class_name.replace(".", "/").encode("utf-8"))
        jenv.UnregisterNatives(jcls)
    finally:
        jenv.PopLocalFrame(jni.NULL)


def throwJavaException(jenv: jni.JNIEnv, jecls, message):

    if isinstance(jecls, str):
        class_name = jecls
        jenv.PushLocalFrame(1)
        try:
            jecls = jenv.FindClass(class_name.replace(".", "/").encode("utf-8"))
            jenv.ThrowNew(jecls, str(message).encode("utf-8"))
        finally:
            jenv.PopLocalFrame(jni.NULL)
    else:
        jenv.ThrowNew(jecls, str(message).encode("utf-8"))
