# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

from typing import Tuple

import jni
from .lib import public
from .lib import obj

from .jframe  import JFrame


@public
class JProxy(obj):

    __slots__ = ('__interfaces', '_jitf_array')

    def __init__(self, interfaces: Tuple[JClass, ...]):
        """Initializer"""
        self.__interfaces = interfaces
        self._jitf_array  = jni.obj(jni.jobjectArray)
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            itf_arr = jenv.NewObjectArray(len(self.__interfaces), jvm.Class.Class)
            for i, jitf in enumerate(self.__interfaces):
                jenv.SetObjectArrayElement(itf_arr, i, jitf.handle)
            self._jitf_array = jni.cast(jenv.NewGlobalRef(itf_arr), jni.jobjectArray)

    def __del__(self):
        """Finalizer"""
        try: jvm, jenv = self.jvm
        except Exception: return  # pragma: no cover
        if jvm.jnijvm:
            jenv.DeleteGlobalRef(self._jitf_array)

    interfaces = property(lambda self: self.__interfaces)

    def newProxy(self, delegate: object) -> JObject | None:

        with self.jvm as (jvm, jenv), JFrame(jenv, 4):
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].j = id(delegate)
            ihandler = jenv.NewObject(jvm.jt_reflect_ProxyHandler.Class,
                                      jvm.jt_reflect_ProxyHandler.Constructor, jargs)
            ihclass = jenv.CallObjectMethod(ihandler, jvm.jt_reflect_ProxyHandler.getClass)
            cloader = jenv.CallObjectMethod(ihclass,  jvm.Class.getClassLoader)
            jargs = jni.new_array(jni.jvalue, 3)
            jargs[0].l = cloader  # noqa: E741
            jargs[1].l = self._jitf_array  # noqa: E741
            jargs[2].l = ihandler  # noqa: E741
            jproxy = jenv.CallStaticObjectMethod(jvm.Proxy.Class,
                                                 jvm.Proxy.newProxyInstance, jargs)
            return self.jvm.JObject(jenv, jproxy) if jproxy else None


from .jclass  import JClass   # noqa: E402
from .jobject import JObject  # noqa: E402
