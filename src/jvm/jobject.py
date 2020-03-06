# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Union, Tuple

from public import public
import jni
from .lib import memoryview as memview

from .jconstants  import EJavaType
from .jframe      import JFrame
from .jobjectbase import JObjectBase
from .jclass      import JClass
from ._util       import str2jchars


@public
class JObject(JObjectBase):

    """Object"""

    __slots__ = ()

    @classmethod
    def fromObject(cls, jobj: Optional['JObjectBase']) -> Optional['JObject']:

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JObject(jenv, jobj.handle) if jobj is not None else None

    @classmethod
    def newBoolean(cls, val: bool) -> Optional['JObject']:

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jval = jni.new_array(jni.jvalue, 1)
            jval[0].z = val
            jobj = jenv.CallStaticObjectMethod(jvm.Boolean.Class,
                                               jvm.Boolean.valueOf, jval)
            return cls.jvm.JObject(jenv, jobj) if jobj else None

    @classmethod
    def newCharacter(cls, val: str) -> Optional['JObject']:

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jval = jni.new_array(jni.jvalue, 1)
            jval[0].c = val[0]
            jobj = jenv.CallStaticObjectMethod(jvm.Character.Class,
                                               jvm.Character.valueOf, jval)
            return cls.jvm.JObject(jenv, jobj) if jobj else None

    @classmethod
    def newByte(cls, val: int) -> Optional['JObject']:

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jval = jni.new_array(jni.jvalue, 1)
            jval[0].b = val
            jobj = jenv.CallStaticObjectMethod(jvm.Byte.Class,
                                               jvm.Byte.valueOf, jval)
            return cls.jvm.JObject(jenv, jobj) if jobj else None

    @classmethod
    def newShort(cls, val: int) -> Optional['JObject']:

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jval = jni.new_array(jni.jvalue, 1)
            jval[0].s = val
            jobj = jenv.CallStaticObjectMethod(jvm.Short.Class,
                                               jvm.Short.valueOf, jval)
            return cls.jvm.JObject(jenv, jobj) if jobj else None

    @classmethod
    def newInteger(cls, val: int) -> Optional['JObject']:

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jval = jni.new_array(jni.jvalue, 1)
            jval[0].i = val
            jobj = jenv.CallStaticObjectMethod(jvm.Integer.Class,
                                               jvm.Integer.valueOf, jval)
            return cls.jvm.JObject(jenv, jobj) if jobj else None

    @classmethod
    def newLong(cls, val: int) -> Optional['JObject']:

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jval = jni.new_array(jni.jvalue, 1)
            jval[0].j = val
            jobj = jenv.CallStaticObjectMethod(jvm.Long.Class,
                                               jvm.Long.valueOf, jval)
            return cls.jvm.JObject(jenv, jobj) if jobj else None

    @classmethod
    def newFloat(cls, val: float) -> Optional['JObject']:

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jval = jni.new_array(jni.jvalue, 1)
            jval[0].f = val
            jobj = jenv.CallStaticObjectMethod(jvm.Float.Class,
                                               jvm.Float.valueOf, jval)
            return cls.jvm.JObject(jenv, jobj) if jobj else None

    @classmethod
    def newDouble(cls, val: float) -> Optional['JObject']:

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jval = jni.new_array(jni.jvalue, 1)
            jval[0].d = val
            jobj = jenv.CallStaticObjectMethod(jvm.Double.Class,
                                               jvm.Double.valueOf, jval)
            return cls.jvm.JObject(jenv, jobj) if jobj else None

    @classmethod
    def newString(cls, val: str) -> Optional['JObject']:

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jchars, size, jbuf = str2jchars(val)
            jstr = jenv.NewString(jchars, size)
            return cls.jvm.JObject(jenv, jstr) if jstr else None

    @classmethod
    def newDirectByteBuffer(cls, val: Union[bytes, bytearray, memoryview, memview]) -> Optional['JObject']:

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            if isinstance(val, memview):
                val = val.as_ctypes
            elif isinstance(val, memoryview):
                val = memview(val).as_ctypes
            jobj = jenv.NewDirectByteBuffer(val, len(val))
            return cls.jvm.JObject(jenv, jobj) if jobj else None

    def asClass(self, own: bool=True) -> JClass:

        with self.jvm as (jvm, jenv):
            return self.jvm.JClass(jenv, self._jobj, own=own)

    def asArray(self, javaType: Optional[EJavaType]=None, own: bool=True) -> 'JArray':

        with self.jvm as (jvm, jenv):
            return self.jvm.JArray(jenv, self._jobj, own=own)

    def booleanValue(self) -> bool:

        with self.jvm as (jvm, jenv):
            # if not jenv.IsInstanceOf(self._jobj, jvm.Boolean.Class):
            #     # TODO raise an error
            #     raise Exception()
            return jenv.CallBooleanMethod(self._jobj, jvm.Boolean.booleanValue)

    def charValue(self) -> str:

        with self.jvm as (jvm, jenv):
            # if not jenv.IsInstanceOf(self._jobj, jvm.Character.Class):
            #     # TODO raise an error
            #     raise Exception()
            return jenv.CallCharMethod(self._jobj, jvm.Character.charValue)

    def byteValue(self) -> int:

        with self.jvm as (jvm, jenv):
            # if not jenv.IsInstanceOf(self._jobj, jvm.Number.Class):
            #     # TODO raise an error
            #     raise Exception()
            return jenv.CallByteMethod(self._jobj, jvm.Number.byteValue)

    def shortValue(self) -> int:

        with self.jvm as (jvm, jenv):
            # if not jenv.IsInstanceOf(self._jobj, jvm.Number.Class):
            #     # TODO raise an error
            #     raise Exception()
            return jenv.CallShortMethod(self._jobj, jvm.Number.shortValue)

    def intValue(self) -> int:

        with self.jvm as (jvm, jenv):
            # if not jenv.IsInstanceOf(self._jobj, jvm.Number.Class):
            #     # TODO raise an error
            #     raise Exception()
            return jenv.CallIntMethod(self._jobj, jvm.Number.intValue)

    def longValue(self) -> int:

        with self.jvm as (jvm, jenv):
            # if not jenv.IsInstanceOf(self._jobj, jvm.Number.Class):
            #     # TODO raise an error
            #     raise Exception()
            return jenv.CallLongMethod(self._jobj, jvm.Number.longValue)

    def floatValue(self) -> float:

        with self.jvm as (jvm, jenv):
            # if not jenv.IsInstanceOf(self._jobj, jvm.Number.Class):
            #     # TODO raise an error
            #     raise Exception()
            return jenv.CallFloatMethod(self._jobj, jvm.Number.floatValue)

    def doubleValue(self) -> float:

        with self.jvm as (jvm, jenv):
            # if not jenv.IsInstanceOf(self._jobj, jvm.Number.Class):
            #     # TODO raise an error
            #     raise Exception()
            return jenv.CallDoubleMethod(self._jobj, jvm.Number.doubleValue)

    def stringValue(self) -> str:

        jstr = self.toString()
        return jstr if jstr is not None else "null"  # !!! v1.x
        # return jstr                                # !!! v2.x

    @classmethod
    def minmaxByteValue(cls) -> Tuple[int, int]:

        with cls.jvm as (jvm, jenv):
            return jvm.Byte.MIN_VALUE, jvm.Byte.MAX_VALUE

    @classmethod
    def minmaxShortValue(cls) -> Tuple[int, int]:

        with cls.jvm as (jvm, jenv):
            return jvm.Short.MIN_VALUE, jvm.Short.MAX_VALUE

    @classmethod
    def minmaxIntValue(cls) -> Tuple[int, int]:

        with cls.jvm as (jvm, jenv):
            return jvm.Integer.MIN_VALUE, jvm.Integer.MAX_VALUE

    @classmethod
    def minmaxLongValue(cls) -> Tuple[int, int]:

        with cls.jvm as (jvm, jenv):
            return jvm.Long.MIN_VALUE, jvm.Long.MAX_VALUE

    @classmethod
    def minmaxFloatValue(cls) -> Tuple[float, float]:

        with cls.jvm as (jvm, jenv):
            return jvm.Float.MIN_VALUE, jvm.Float.MAX_VALUE

    @classmethod
    def minmaxDoubleValue(cls) -> Tuple[float, float]:

        with cls.jvm as (jvm, jenv):
            return jvm.Double.MIN_VALUE, jvm.Double.MAX_VALUE
