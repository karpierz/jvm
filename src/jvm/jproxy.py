# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Tuple

from public import public
import jni
from .lib import obj

from .jframe  import JFrame
from .jhost   import JHost
from .jobject import JObject


@public
class JProxy(obj):

    __slots__ = ('__interfaces', '_jitf_array')

    def __init__(self, interfaces: Tuple['JClass', ...]):
        self.__interfaces = interfaces
        self._jitf_array  = jni.obj(jni.jobjectArray)
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            itf_arr = jenv.NewObjectArray(len(self.__interfaces), jvm.Class.Class)
            for i, jitf in enumerate(self.__interfaces):
                jenv.SetObjectArrayElement(itf_arr, i, jitf.handle)
            self._jitf_array = jni.cast(jenv.NewGlobalRef(itf_arr), jni.jobjectArray)

    def __del__(self):
        try: jvm, jenv = self.jvm
        except: return  # pragma: no cover
        if jvm.jnijvm:
            jenv.DeleteGlobalRef(self._jitf_array)

    interfaces = property(lambda self: self.__interfaces)

    def newProxy(self, delegate: object) -> Optional[JObject]:

        with self.jvm as (jvm, jenv), JFrame(jenv, 4):
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].j = id(delegate)
            ihandler = jenv.NewObject(jvm.jt_reflect_ProxyHandler.Class,
                                      jvm.jt_reflect_ProxyHandler.Constructor, jargs)
            ihclass = jenv.CallObjectMethod(ihandler, jvm.jt_reflect_ProxyHandler.getClass)
            cloader = jenv.CallObjectMethod(ihclass,  jvm.Class.getClassLoader)
            jargs = jni.new_array(jni.jvalue, 3)
            jargs[0].l = cloader
            jargs[1].l = self._jitf_array
            jargs[2].l = ihandler
            jproxy = jenv.CallStaticObjectMethod(jvm.Proxy.Class,
                                                 jvm.Proxy.newProxyInstance, jargs)
            return self.jvm.JObject(jenv, jproxy) if jproxy else None
