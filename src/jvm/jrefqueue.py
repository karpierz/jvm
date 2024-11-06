# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import jni
from .lib import public

from .jframe      import JFrame
from .jhost       import JHost
from .jobjectbase import JObjectBase


@public
class JReferenceQueue(JObjectBase):

    __slots__ = ()

    def __init__(self):
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jobj = jenv.NewObject(jvm.jt_ref_ReferenceQueue.Class,
                                  jvm.jt_ref_ReferenceQueue.Constructor)
            super().__init__(jenv, jobj)

    def start(self):

        with self.jvm as (jvm, jenv):
            jenv.CallVoidMethod(self._jobj, jvm.jt_ref_ReferenceQueue.start)

    def stop(self):

        with self.jvm as (jvm, jenv):
            jenv.CallVoidMethod(self._jobj, jvm.jt_ref_ReferenceQueue.stop)

    def registerReference(self, source: 'JObject', target: object):

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jargs = jni.new_array(jni.jvalue, 2)
            jargs[0].l = source.handle
            jargs[1].j = id(target)
            jenv.CallObjectMethod(self._jobj,
                                  jvm.jt_ref_ReferenceQueue.registerReference,
                                  jargs)
