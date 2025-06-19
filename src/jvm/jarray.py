# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

from typing import Sequence, NamedTuple
import sys
import math

import jni
from .lib import public
from .lib import cached
from .lib import memoryview as memview

from .jframe      import JFrame
from .jstring     import JString
from .jobjectbase import JObjectBase
from ._util       import str2jchars

def bitsof(x):  return (int(math.log(x, 2)) + 1)
def bytesof(x): return (int(math.log(x, 2)) + 8) // 8

def is_memview(x): return isinstance(x, (memview, memoryview))


class JArrayBuffer(NamedTuple):
    buf: object
    itemsize: int
    format: bytes  # noqa: A003
    is_copy: bool


@public
class JArray(JObjectBase):
    """Java Array"""

    __slots__ = ()

    _jbyte_equiv_byte    = (jni.sizeof(jni.jbyte) == 1)
    _jchar_equiv_unicode = (jni.sizeof(jni.jchar) == bytesof(sys.maxunicode))

    @staticmethod
    def size(start, stop, step=1):
        return max(0, (stop + step - (1 if step >= 0 else -1) - start) // step)

    @classmethod
    def newBooleanArray(cls, size: int) -> JArray:
        """???."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jenv.NewBooleanArray(size)
            return cls.jvm.JArray(jenv, jarr)

    @classmethod
    def newCharArray(cls, size: int) -> JArray:
        """???."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jenv.NewCharArray(size)
            return cls.jvm.JArray(jenv, jarr)

    @classmethod
    def newByteArray(cls, size: int) -> JArray:
        """???."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jenv.NewByteArray(size)
            return cls.jvm.JArray(jenv, jarr)

    @classmethod
    def newShortArray(cls, size: int) -> JArray:
        """???."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jenv.NewShortArray(size)
            return cls.jvm.JArray(jenv, jarr)

    @classmethod
    def newIntArray(cls, size: int) -> JArray:
        """???."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jenv.NewIntArray(size)
            return cls.jvm.JArray(jenv, jarr)

    @classmethod
    def newLongArray(cls, size: int) -> JArray:
        """???."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jenv.NewLongArray(size)
            return cls.jvm.JArray(jenv, jarr)

    @classmethod
    def newFloatArray(cls, size: int) -> JArray:
        """???."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jenv.NewFloatArray(size)
            return cls.jvm.JArray(jenv, jarr)

    @classmethod
    def newDoubleArray(cls, size: int) -> JArray:
        """???."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jenv.NewDoubleArray(size)
            return cls.jvm.JArray(jenv, jarr)

    @classmethod
    def newStringArray(cls, size: int) -> JArray:
        """???."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jenv.NewObjectArray(size, jvm.String.Class)
            return cls.jvm.JArray(jenv, jarr)

    @classmethod
    def newObjectArray(cls, size: int, componentClass: JClass) -> JArray:
        """???."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jenv.NewObjectArray(size, jni.cast(componentClass.handle, jni.jclass))
            return cls.jvm.JArray(jenv, jarr)

    def __init__(self, jenv: jni.JNIEnv, jarr: jni.jarray, own: bool = True):
        """Initializer"""
        super().__init__(jenv, jni.cast(jarr, jni.jarray), own=own)

    def __hash__(self):
        """Hash value"""
        return super().__hash__()

    def __eq__(self, other):
        """???"""
        if self is other:
            return True

        if not isinstance(other, self.jvm.JArray):
            return NotImplemented

        if len(self) != len(other):
            return False

        return NotImplemented

    def __len__(self):
        """Length of"""
        return self.getLength()

    def asObject(self, own: bool = True) -> JObject:
        """???."""
        with self.jvm as (jvm, jenv):
            return self.jvm.JObject(jenv, self._jobj, own=own)

    @cached
    def getLength(self) -> int:
        """???."""
        with self.jvm as (jvm, jenv):
            return int(jenv.GetArrayLength(self._jobj))

    def getBoolean(self, idx: int) -> bool:
        """???."""
        with self.jvm as (jvm, jenv):
            elem = jni.new(jni.jboolean)
            jenv.GetBooleanArrayRegion(self._jobj, idx, 1, elem)
            return bool(elem[0])

    def getChar(self, idx: int) -> str:
        """???."""
        with self.jvm as (jvm, jenv):
            elem = jni.new_array(jni.jchar, 1)
            jenv.GetCharArrayRegion(self._jobj, idx, 1, elem)
            return elem[0]

    def getByte(self, idx: int) -> int:
        """???."""
        with self.jvm as (jvm, jenv):
            elem = jni.new(jni.jbyte)
            jenv.GetByteArrayRegion(self._jobj, idx, 1, elem)
            return elem[0]

    def getShort(self, idx: int) -> int:
        """???."""
        with self.jvm as (jvm, jenv):
            elem = jni.new(jni.jshort)
            jenv.GetShortArrayRegion(self._jobj, idx, 1, elem)
            return elem[0]

    def getInt(self, idx: int) -> int:
        """???."""
        with self.jvm as (jvm, jenv):
            elem = jni.new(jni.jint)
            jenv.GetIntArrayRegion(self._jobj, idx, 1, elem)
            return elem[0]

    def getLong(self, idx: int) -> int:
        """???."""
        with self.jvm as (jvm, jenv):
            elem = jni.new(jni.jlong)
            jenv.GetLongArrayRegion(self._jobj, idx, 1, elem)
            return elem[0]

    def getFloat(self, idx: int) -> float:
        """???."""
        with self.jvm as (jvm, jenv):
            elem = jni.new(jni.jfloat)
            jenv.GetFloatArrayRegion(self._jobj, idx, 1, elem)
            return elem[0]

    def getDouble(self, idx: int) -> float:
        """???."""
        with self.jvm as (jvm, jenv):
            elem = jni.new(jni.jdouble)
            jenv.GetDoubleArrayRegion(self._jobj, idx, 1, elem)
            return elem[0]

    def getString(self, idx: int) -> str | None:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jstr = jenv.GetObjectArrayElement(self._jobj, idx)
            return JString(jenv, jstr, own=False).str if jstr else None

    def getObject(self, idx: int) -> JObject | None:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jobj = jenv.GetObjectArrayElement(self._jobj, idx)
            return self.jvm.JObject(jenv, jobj) if jobj else None

    def setBoolean(self, idx: int, val: bool):
        """???."""
        with self.jvm as (jvm, jenv):
            elems = jni.new_array(jni.jboolean, 1)
            elems[0] = val
            jenv.SetBooleanArrayRegion(self._jobj, idx, 1, elems)

    def setChar(self, idx: int, val: str):
        """???."""
        with self.jvm as (jvm, jenv):
            elems = jni.new_array(jni.jchar, 1)
            elems[0] = val
            jenv.SetCharArrayRegion(self._jobj, idx, 1, elems)

    def setByte(self, idx: int, val: int):
        """???."""
        with self.jvm as (jvm, jenv):
            elems = jni.new_array(jni.jbyte, 1)
            elems[0] = val
            jenv.SetByteArrayRegion(self._jobj, idx, 1, elems)

    def setShort(self, idx: int, val: int):
        """???."""
        with self.jvm as (jvm, jenv):
            elems = jni.new_array(jni.jshort, 1)
            elems[0] = val
            jenv.SetShortArrayRegion(self._jobj, idx, 1, elems)

    def setInt(self, idx: int, val: int):
        """???."""
        with self.jvm as (jvm, jenv):
            elems = jni.new_array(jni.jint, 1)
            elems[0] = val
            jenv.SetIntArrayRegion(self._jobj, idx, 1, elems)

    def setLong(self, idx: int, val: int):
        """???."""
        with self.jvm as (jvm, jenv):
            elems = jni.new_array(jni.jlong, 1)
            elems[0] = val
            jenv.SetLongArrayRegion(self._jobj, idx, 1, elems)

    def setFloat(self, idx: int, val: float):
        """???."""
        with self.jvm as (jvm, jenv):
            elems = jni.new_array(jni.jfloat, 1)
            elems[0] = val
            jenv.SetFloatArrayRegion(self._jobj, idx, 1, elems)

    def setDouble(self, idx: int, val: float):
        """???."""
        with self.jvm as (jvm, jenv):
            elems = jni.new_array(jni.jdouble, 1)
            elems[0] = val
            jenv.SetDoubleArrayRegion(self._jobj, idx, 1, elems)

    def setString(self, idx: int, val: str | None):
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            if val is None:
                jstr = None
            else:
                jchars, size, jbuf = str2jchars(val)
                jstr = jenv.NewString(jchars, size)
            jenv.SetObjectArrayElement(self._jobj, idx, jstr)

    def setObject(self, idx: int, val: JObject | None):
        """???."""
        with self.jvm as (jvm, jenv):
            jenv.SetObjectArrayElement(self._jobj, idx, val.handle if val is not None else None)

    def getBooleanSlice(self, start: int, stop: int, step: int) -> JArray:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            jarr_ret = jenv.NewBooleanArray(size)
            jels_ret = jenv.GetBooleanArrayElements(jarr_ret)
            try:
                if step == 1:
                    jenv.GetBooleanArrayRegion(jarr, start, size, jels_ret)
                else:
                    jels = jenv.GetBooleanArrayElements(jarr)
                    try:
                        for ix, idx in enumerate(range(start, stop, step)):
                            jels_ret[ix] = jels[idx]
                    finally:
                        jenv.ReleaseBooleanArrayElements(jarr, jels, jni.JNI_ABORT)
                jenv.ReleaseBooleanArrayElements(jarr_ret, jels_ret)
            except Exception as exc:
                jenv.ReleaseBooleanArrayElements(jarr_ret, jels_ret, jni.JNI_ABORT)
                raise exc
            return self.jvm.JArray(jenv, jarr_ret)

    def getCharSlice(self, start: int, stop: int, step: int) -> JArray:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            jarr_ret = jenv.NewCharArray(size)
            jels_ret = jenv.GetCharArrayElements(jarr_ret)
            try:
                if step == 1:
                    jenv.GetCharArrayRegion(jarr, start, size, jels_ret)
                else:
                    jels = jenv.GetCharArrayElements(jarr)
                    try:
                        for ix, idx in enumerate(range(start, stop, step)):
                            jels_ret[ix] = jels[idx]
                    finally:
                        jenv.ReleaseCharArrayElements(jarr, jels, jni.JNI_ABORT)
                jenv.ReleaseCharArrayElements(jarr_ret, jels_ret)
            except Exception as exc:
                jenv.ReleaseCharArrayElements(jarr_ret, jels_ret, jni.JNI_ABORT)
                raise exc
            return self.jvm.JArray(jenv, jarr_ret)

    def getByteSlice(self, start: int, stop: int, step: int) -> JArray:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            jarr_ret = jenv.NewByteArray(size)
            jels_ret = jenv.GetByteArrayElements(jarr_ret)
            try:
                if step == 1:
                    jenv.GetByteArrayRegion(jarr, start, size, jels_ret)
                else:
                    jels = jenv.GetByteArrayElements(jarr)
                    try:
                        for ix, idx in enumerate(range(start, stop, step)):
                            jels_ret[ix] = jels[idx]
                    finally:
                        jenv.ReleaseByteArrayElements(jarr, jels, jni.JNI_ABORT)
                jenv.ReleaseByteArrayElements(jarr_ret, jels_ret)
            except Exception as exc:
                jenv.ReleaseByteArrayElements(jarr_ret, jels_ret, jni.JNI_ABORT)
                raise exc
            return self.jvm.JArray(jenv, jarr_ret)

    def getShortSlice(self, start: int, stop: int, step: int) -> JArray:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            jarr_ret = jenv.NewShortArray(size)
            jels_ret = jenv.GetShortArrayElements(jarr_ret)
            try:
                if step == 1:
                    jenv.GetShortArrayRegion(jarr, start, size, jels_ret)
                else:
                    jels = jenv.GetShortArrayElements(jarr)
                    try:
                        for ix, idx in enumerate(range(start, stop, step)):
                            jels_ret[ix] = jels[idx]
                    finally:
                        jenv.ReleaseShortArrayElements(jarr, jels, jni.JNI_ABORT)
                jenv.ReleaseShortArrayElements(jarr_ret, jels_ret)
            except Exception as exc:
                jenv.ReleaseShortArrayElements(jarr_ret, jels_ret, jni.JNI_ABORT)
                raise exc
            return self.jvm.JArray(jenv, jarr_ret)

    def getIntSlice(self, start: int, stop: int, step: int) -> JArray:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            jarr_ret = jenv.NewIntArray(size)
            jels_ret = jenv.GetIntArrayElements(jarr_ret)
            try:
                if step == 1:
                    jenv.GetIntArrayRegion(jarr, start, size, jels_ret)
                else:
                    jels = jenv.GetIntArrayElements(jarr)
                    try:
                        for ix, idx in enumerate(range(start, stop, step)):
                            jels_ret[ix] = jels[idx]
                    finally:
                        jenv.ReleaseIntArrayElements(jarr, jels, jni.JNI_ABORT)
                jenv.ReleaseIntArrayElements(jarr_ret, jels_ret)
            except Exception as exc:
                jenv.ReleaseIntArrayElements(jarr_ret, jels_ret, jni.JNI_ABORT)
                raise exc
            return self.jvm.JArray(jenv, jarr_ret)

    def getLongSlice(self, start: int, stop: int, step: int) -> JArray:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            jarr_ret = jenv.NewLongArray(size)
            jels_ret = jenv.GetLongArrayElements(jarr_ret)
            try:
                if step == 1:
                    jenv.GetLongArrayRegion(jarr, start, size, jels_ret)
                else:
                    jels = jenv.GetLongArrayElements(jarr)
                    try:
                        for ix, idx in enumerate(range(start, stop, step)):
                            jels_ret[ix] = jels[idx]
                    finally:
                        jenv.ReleaseLongArrayElements(jarr, jels, jni.JNI_ABORT)
                jenv.ReleaseLongArrayElements(jarr_ret, jels_ret)
            except Exception as exc:
                jenv.ReleaseLongArrayElements(jarr_ret, jels_ret, jni.JNI_ABORT)
                raise exc
            return self.jvm.JArray(jenv, jarr_ret)

    def getFloatSlice(self, start: int, stop: int, step: int) -> JArray:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            jarr_ret = jenv.NewFloatArray(size)
            jels_ret = jenv.GetFloatArrayElements(jarr_ret)
            try:
                if step == 1:
                    jenv.GetFloatArrayRegion(jarr, start, size, jels_ret)
                else:
                    jels = jenv.GetFloatArrayElements(jarr)
                    try:
                        for ix, idx in enumerate(range(start, stop, step)):
                            jels_ret[ix] = jels[idx]
                    finally:
                        jenv.ReleaseFloatArrayElements(jarr, jels, jni.JNI_ABORT)
                jenv.ReleaseFloatArrayElements(jarr_ret, jels_ret)
            except Exception as exc:
                jenv.ReleaseFloatArrayElements(jarr_ret, jels_ret, jni.JNI_ABORT)
                raise exc
            return self.jvm.JArray(jenv, jarr_ret)

    def getDoubleSlice(self, start: int, stop: int, step: int) -> JArray:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            jarr_ret = jenv.NewDoubleArray(size)
            jels_ret = jenv.GetDoubleArrayElements(jarr_ret)
            try:
                if step == 1:
                    jenv.GetDoubleArrayRegion(jarr, start, size, jels_ret)
                else:
                    jels = jenv.GetDoubleArrayElements(jarr)
                    try:
                        for ix, idx in enumerate(range(start, stop, step)):
                            jels_ret[ix] = jels[idx]
                    finally:
                        jenv.ReleaseDoubleArrayElements(jarr, jels, jni.JNI_ABORT)
                jenv.ReleaseDoubleArrayElements(jarr_ret, jels_ret)
            except Exception as exc:
                jenv.ReleaseDoubleArrayElements(jarr_ret, jels_ret, jni.JNI_ABORT)
                raise exc
            return self.jvm.JArray(jenv, jarr_ret)

    def getStringSlice(self, start: int, stop: int, step: int) -> JArray:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            jarr_ret = jenv.NewObjectArray(size, jvm.String.Class)
            with JFrame(jenv) as jfrm:
                for ix, idx in enumerate(range(start, stop, step)):
                    if not (ix % 256): jfrm.reset(256)
                    jobj = jenv.GetObjectArrayElement(jarr, idx)
                    jenv.SetObjectArrayElement(jarr_ret, ix, jobj)
            return self.jvm.JArray(jenv, jarr_ret)

    def getObjectSlice(self, start: int, stop: int, step: int) -> JArray:
        """???."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            jarr_ret = jenv.NewObjectArray(size, jvm.Object.Class)
            with JFrame(jenv) as jfrm:
                for ix, idx in enumerate(range(start, stop, step)):
                    if not (ix % 256): jfrm.reset(256)
                    jobj = jenv.GetObjectArrayElement(jarr, idx)
                    jenv.SetObjectArrayElement(jarr_ret, ix, jobj)
            return self.jvm.JArray(jenv, jarr_ret)

    def setBooleanSlice(self, start: int, stop: int, step: int, val: Sequence[bool]):
        """???."""
        with self.jvm as (jvm, jenv):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            if step == 1 and is_memview(val) and val.itemsize == jni.sizeof(jni.jboolean):
                val = val.as_ctypes if isinstance(val, memview) else memview(val).as_ctypes
                jenv.SetBooleanArrayRegion(jarr, start, size,
                                           jni.cast(val, jni.POINTER(jni.jboolean)))
            else:
                if is_memview(val): val = val.obj
                jels = jenv.GetBooleanArrayElements(jarr)
                try:
                    for ix, idx in enumerate(range(start, stop, step)):
                        jels[idx] = val[ix]
                    jenv.ReleaseBooleanArrayElements(jarr, jels)
                except Exception as exc:
                    jenv.ReleaseBooleanArrayElements(jarr, jels, jni.JNI_ABORT)
                    raise exc

    def setCharSlice(self, start: int, stop: int, step: int, val: Sequence[str] | str):
        """???."""
        with self.jvm as (jvm, jenv):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            if step == 1 and is_memview(val) and val.itemsize == jni.sizeof(jni.jchar):
                val = val.as_ctypes if isinstance(val, memview) else memview(val).as_ctypes
                jenv.SetCharArrayRegion(jarr, start, size, jni.cast(val, jni.POINTER(jni.jchar)))
            else:
                if is_memview(val): val = val.obj
                jels = jenv.GetCharArrayElements(jarr)
                try:
                    if isinstance(val, str) and step == 1 and JArray._jchar_equiv_unicode:
                        print("UUUUUUUUUUUUUUUUU")
                        jni.memmove(jni.byref(jels.contents, start * jni.sizeof(jni.jchar)),
                                    val,  JArray.size(start, stop) * jni.sizeof(jni.jchar))
                    else:
                        for ix, idx in enumerate(range(start, stop, step)):
                            jels[idx] = val[ix]
                    jenv.ReleaseCharArrayElements(jarr, jels)
                except Exception as exc:
                    jenv.ReleaseCharArrayElements(jarr, jels, jni.JNI_ABORT)
                    raise exc

    def setByteSlice(self, start: int, stop: int, step: int,
                     val: Sequence[int | bytes] | bytes | bytearray):
        """???."""
        with self.jvm as (jvm, jenv):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            if step == 1 and is_memview(val) and val.itemsize == jni.sizeof(jni.jbyte):
                val = val.as_ctypes if isinstance(val, memview) else memview(val).as_ctypes
                jenv.SetByteArrayRegion(jarr, start, size, jni.cast(val, jni.POINTER(jni.jbyte)))
            else:
                if is_memview(val): val = val.obj
                jels = jenv.GetByteArrayElements(jarr)
                try:
                    if isinstance(val, (bytes, bytearray)):
                        if step == 1 and JArray._jbyte_equiv_byte:
                            if isinstance(val, bytearray):
                                val = jni.from_buffer(val)
                            # print(("RRRRRRRRRRRRRRRRRR",
                            #        type(jels), type(jels.contents), type(val)))
                            jni.memmove(jni.byref(jels.contents, start), val,
                                        JArray.size(start, stop))
                        else:
                            for ix, idx in enumerate(range(start, stop, step)):
                                jels[idx] = val[ix]
                    else:
                        for ix, idx in enumerate(range(start, stop, step)):
                            v = val[ix]
                            jels[idx] = v[0] if isinstance(v, bytes) else v
                    jenv.ReleaseByteArrayElements(jarr, jels)
                except Exception as exc:
                    jenv.ReleaseByteArrayElements(jarr, jels, jni.JNI_ABORT)
                    raise exc

    def setShortSlice(self, start: int, stop: int, step: int, val: Sequence[int]):
        """???."""
        with self.jvm as (jvm, jenv):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            if step == 1 and is_memview(val) and val.itemsize == jni.sizeof(jni.jshort):
                val = val.as_ctypes if isinstance(val, memview) else memview(val).as_ctypes
                jenv.SetShortArrayRegion(jarr, start, size, jni.cast(val, jni.POINTER(jni.jshort)))
            else:
                if is_memview(val): val = val.obj
                jels = jenv.GetShortArrayElements(jarr)
                try:
                    for ix, idx in enumerate(range(start, stop, step)):
                        jels[idx] = val[ix]
                    jenv.ReleaseShortArrayElements(jarr, jels)
                except Exception as exc:
                    jenv.ReleaseShortArrayElements(jarr, jels, jni.JNI_ABORT)
                    raise exc

    def setIntSlice(self, start: int, stop: int, step: int, val: Sequence[int]):
        """???."""
        with self.jvm as (jvm, jenv):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            if step == 1 and is_memview(val) and val.itemsize == jni.sizeof(jni.jint):
                val = val.as_ctypes if isinstance(val, memview) else memview(val).as_ctypes
                jenv.SetIntArrayRegion(jarr, start, size, jni.cast(val, jni.POINTER(jni.jint)))
            else:
                if is_memview(val): val = val.obj
                jels = jenv.GetIntArrayElements(jarr)
                try:
                    for ix, idx in enumerate(range(start, stop, step)):
                        jels[idx] = val[ix]
                    jenv.ReleaseIntArrayElements(jarr, jels)
                except Exception as exc:
                    jenv.ReleaseIntArrayElements(jarr, jels, jni.JNI_ABORT)
                    raise exc

    def setLongSlice(self, start: int, stop: int, step: int, val: Sequence[int]):
        """???."""
        with self.jvm as (jvm, jenv):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            if step == 1 and is_memview(val) and val.itemsize == jni.sizeof(jni.jlong):
                val = val.as_ctypes if isinstance(val, memview) else memview(val).as_ctypes
                jenv.SetLongArrayRegion(jarr, start, size, jni.cast(val, jni.POINTER(jni.jlong)))
            else:
                if is_memview(val): val = val.obj
                jels = jenv.GetLongArrayElements(jarr)
                try:
                    for ix, idx in enumerate(range(start, stop, step)):
                        jels[idx] = val[ix]
                    jenv.ReleaseLongArrayElements(jarr, jels)
                except Exception as exc:
                    jenv.ReleaseLongArrayElements(jarr, jels, jni.JNI_ABORT)
                    raise exc

    def setFloatSlice(self, start: int, stop: int, step: int, val: Sequence[float]):
        """???."""
        with self.jvm as (jvm, jenv):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            if step == 1 and is_memview(val) and val.itemsize == jni.sizeof(jni.jfloat):
                val = val.as_ctypes if isinstance(val, memview) else memview(val).as_ctypes
                jenv.SetFloatArrayRegion(jarr, start, size, jni.cast(val, jni.POINTER(jni.jfloat)))
            else:
                if is_memview(val): val = val.obj
                jels = jenv.GetFloatArrayElements(jarr)
                try:
                    for ix, idx in enumerate(range(start, stop, step)):
                        jels[idx] = val[ix]
                    jenv.ReleaseFloatArrayElements(jarr, jels)
                except Exception as exc:
                    jenv.ReleaseFloatArrayElements(jarr, jels, jni.JNI_ABORT)
                    raise exc

    def setDoubleSlice(self, start: int, stop: int, step: int, val: Sequence[float]):
        """???."""
        with self.jvm as (jvm, jenv):
            size = JArray.size(start, stop, step)
            jarr = self._jobj
            if step == 1 and is_memview(val) and val.itemsize == jni.sizeof(jni.jdouble):
                val = val.as_ctypes if isinstance(val, memview) else memview(val).as_ctypes
                jenv.SetDoubleArrayRegion(jarr, start, size,
                                          jni.cast(val, jni.POINTER(jni.jdouble)))
            else:
                if is_memview(val): val = val.obj
                jels = jenv.GetDoubleArrayElements(jarr)
                try:
                    for ix, idx in enumerate(range(start, stop, step)):
                        jels[idx] = val[ix]
                    jenv.ReleaseDoubleArrayElements(jarr, jels)
                except Exception as exc:
                    jenv.ReleaseDoubleArrayElements(jarr, jels, jni.JNI_ABORT)
                    raise exc

    def setStringSlice(self, start: int, stop: int, step: int, val: Sequence[str | None]):
        """???."""
        with self.jvm as (jvm, jenv):
            jarr = self._jobj
            with JFrame(jenv) as jfrm:
                for ix, idx in enumerate(range(start, stop, step)):
                    if not (ix % 256): jfrm.reset(256)
                    elem = val[ix]
                    if elem is None:
                        jstr = None
                    else:
                        jchars, size, jbuf = str2jchars(elem)
                        jstr = jenv.NewString(jchars, size)
                    jenv.SetObjectArrayElement(jarr, idx, jstr)

    def setObjectSlice(self, start: int, stop: int, step: int, val: Sequence[JObject | None]):
        """???."""
        with self.jvm as (jvm, jenv):
            jarr = self._jobj
            for ix, idx in enumerate(range(start, stop, step)):
                obj = val[ix]
                jenv.SetObjectArrayElement(jarr, idx, obj.handle if obj is not None else None)

    def getBooleanBuffer(self) -> NamedTuple:
        """???."""
        with self.jvm as (jvm, jenv):
            is_copy = jni.obj(jni.jboolean)
            return JArrayBuffer(jenv.GetBooleanArrayElements(self._jobj, is_copy),
                                jni.sizeof(jni.jboolean), b"B", bool(is_copy))

    def getCharBuffer(self) -> NamedTuple:
        """???."""
        with self.jvm as (jvm, jenv):
            is_copy = jni.obj(jni.jboolean)
            return JArrayBuffer(jenv.GetCharArrayElements(self._jobj, is_copy),
                                jni.sizeof(jni.jchar), b"H", bool(is_copy))

    def getByteBuffer(self) -> NamedTuple:
        """???."""
        with self.jvm as (jvm, jenv):
            is_copy = jni.obj(jni.jboolean)
            return JArrayBuffer(jenv.GetByteArrayElements(self._jobj, is_copy),
                                jni.sizeof(jni.jbyte), b"b", bool(is_copy))

    def getShortBuffer(self) -> NamedTuple:
        """???."""
        with self.jvm as (jvm, jenv):
            is_copy = jni.obj(jni.jboolean)
            return JArrayBuffer(jenv.GetShortArrayElements(self._jobj, is_copy),
                                jni.sizeof(jni.jshort), b"h", bool(is_copy))

    def getIntBuffer(self) -> NamedTuple:
        """???."""
        with self.jvm as (jvm, jenv):
            is_copy = jni.obj(jni.jboolean)
            return JArrayBuffer(jenv.GetIntArrayElements(self._jobj, is_copy),
                                jni.sizeof(jni.jint), b"i", bool(is_copy))

    def getLongBuffer(self) -> NamedTuple:
        """???."""
        with self.jvm as (jvm, jenv):
            is_copy = jni.obj(jni.jboolean)
            return JArrayBuffer(jenv.GetLongArrayElements(self._jobj, is_copy),
                                jni.sizeof(jni.jlong), b"q", bool(is_copy))

    def getFloatBuffer(self) -> NamedTuple:
        """???."""
        with self.jvm as (jvm, jenv):
            is_copy = jni.obj(jni.jboolean)
            return JArrayBuffer(jenv.GetFloatArrayElements(self._jobj, is_copy),
                                jni.sizeof(jni.jfloat), b"f", bool(is_copy))

    def getDoubleBuffer(self) -> NamedTuple:
        """???."""
        with self.jvm as (jvm, jenv):
            is_copy = jni.obj(jni.jboolean)
            return JArrayBuffer(jenv.GetDoubleArrayElements(self._jobj, is_copy),
                                jni.sizeof(jni.jdouble), b"d", bool(is_copy))

    def releaseBooleanBuffer(self, buf: object, mode: bool | None = None):
        """???."""
        with self.jvm as (jvm, jenv):
            jenv.ReleaseBooleanArrayElements(self._jobj, jni.cast(buf, jni.POINTER(jni.jboolean)),
                                             0 if mode is None else
                                             jni.JNI_COMMIT if mode else jni.JNI_ABORT)

    def releaseCharBuffer(self, buf: object, mode: bool | None = None):
        """???."""
        with self.jvm as (jvm, jenv):
            jenv.ReleaseCharArrayElements(self._jobj, jni.cast(buf, jni.POINTER(jni.jchar)),
                                          0 if mode is None else
                                          jni.JNI_COMMIT if mode else jni.JNI_ABORT)

    def releaseByteBuffer(self, buf: object, mode: bool | None = None):
        """???."""
        with self.jvm as (jvm, jenv):
            jenv.ReleaseByteArrayElements(self._jobj, jni.cast(buf, jni.POINTER(jni.jbyte)),
                                          0 if mode is None else
                                          jni.JNI_COMMIT if mode else jni.JNI_ABORT)

    def releaseShortBuffer(self, buf: object, mode: bool | None = None):
        """???."""
        with self.jvm as (jvm, jenv):
            jenv.ReleaseShortArrayElements(self._jobj, jni.cast(buf, jni.POINTER(jni.jshort)),
                                           0 if mode is None else
                                           jni.JNI_COMMIT if mode else jni.JNI_ABORT)

    def releaseIntBuffer(self, buf: object, mode: bool | None = None):
        """???."""
        with self.jvm as (jvm, jenv):
            jenv.ReleaseIntArrayElements(self._jobj, jni.cast(buf, jni.POINTER(jni.jint)),
                                         0 if mode is None else
                                         jni.JNI_COMMIT if mode else jni.JNI_ABORT)

    def releaseLongBuffer(self, buf: object, mode: bool | None = None):
        """???."""
        with self.jvm as (jvm, jenv):
            jenv.ReleaseLongArrayElements(self._jobj, jni.cast(buf, jni.POINTER(jni.jlong)),
                                          0 if mode is None else
                                          jni.JNI_COMMIT if mode else jni.JNI_ABORT)

    def releaseFloatBuffer(self, buf: object, mode: bool | None = None):
        """???."""
        with self.jvm as (jvm, jenv):
            jenv.ReleaseFloatArrayElements(self._jobj, jni.cast(buf, jni.POINTER(jni.jfloat)),
                                           0 if mode is None else
                                           jni.JNI_COMMIT if mode else jni.JNI_ABORT)

    def releaseDoubleBuffer(self, buf: object, mode: bool | None = None):
        """???."""
        with self.jvm as (jvm, jenv):
            jenv.ReleaseDoubleArrayElements(self._jobj, jni.cast(buf, jni.POINTER(jni.jdouble)),
                                            0 if mode is None else
                                            jni.JNI_COMMIT if mode else jni.JNI_ABORT)


from .jclass  import JClass   # noqa: E402
from .jobject import JObject  # noqa: E402
