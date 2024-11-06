# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Union

import jni
from .lib import public
from .lib import cached

from .jframe     import JFrame
from .jmember    import JMember
from .jannotated import JAnnotatedElement
from .jclass     import JClass
from .jstring    import JString
from .jobject    import JObject
from ._util      import str2jchars


@public
class JField(JMember, JAnnotatedElement):
    """Java Field"""

    __slots__ = ()

    @cached
    def _jfid(self, jenv: jni.JNIEnv):
        return jenv.FromReflectedField(self._jobj)

    @cached
    def getType(self) -> JClass:
        """Returns a Class object that identifies the declared type for the field
        represented by this Field object.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.CallObjectMethod(self._jobj, jvm.Field.getType)
            return self.jvm.JClass(jenv, jcls)

    @cached
    def isEnumConstant(self) -> bool:
        """Returns True if this field represents an element of an enumerated type;
        returns False otherwise.
        """
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Field.isEnumConstant)

    def getStaticBoolean(self, jcls: JClass) -> bool:
        """Gets the value of a static boolean field."""
        with self.jvm as (jvm, jenv):
            return jenv.GetStaticBooleanField(jcls.handle, self._jfid(jenv))

    def getStaticChar(self, jcls: JClass) -> str:
        """Gets the value of a static field of type char or of another
        primitive type convertible to type char via a widening conversion.
        """
        with self.jvm as (jvm, jenv):
            return jenv.GetStaticCharField(jcls.handle, self._jfid(jenv))

    def getStaticByte(self, jcls: JClass) -> int:
        """Gets the value of a static byte field."""
        with self.jvm as (jvm, jenv):
            return jenv.GetStaticByteField(jcls.handle, self._jfid(jenv))

    def getStaticShort(self, jcls: JClass) -> int:
        """Gets the value of a static field of type short or of another
        primitive type convertible to type short via a widening conversion.
        """
        with self.jvm as (jvm, jenv):
            return jenv.GetStaticShortField(jcls.handle, self._jfid(jenv))

    def getStaticInt(self, jcls: JClass) -> int:
        """Gets the value of a static field of type int or of another
        primitive type convertible to type int via a widening conversion.
        """
        with self.jvm as (jvm, jenv):
            return jenv.GetStaticIntField(jcls.handle, self._jfid(jenv))

    def getStaticLong(self, jcls: JClass) -> int:
        """Gets the value of a static field of type long or of another
        primitive type convertible to type long via a widening conversion.
        """
        with self.jvm as (jvm, jenv):
            return jenv.GetStaticLongField(jcls.handle, self._jfid(jenv))

    def getStaticFloat(self, jcls: JClass) -> float:
        """Gets the value of a static field of type float or of another
        primitive type convertible to type float via a widening conversion.
        """
        with self.jvm as (jvm, jenv):
            return jenv.GetStaticFloatField(jcls.handle, self._jfid(jenv))

    def getStaticDouble(self, jcls: JClass) -> float:
        """Gets the value of a static field of type double or of another
        primitive type convertible to type double via a widening conversion.
        """
        with self.jvm as (jvm, jenv):
            return jenv.GetStaticDoubleField(jcls.handle, self._jfid(jenv))

    def getStaticString(self, jcls: JClass) -> Optional[str]:
        """Returns the value of a static field represented by this Field,
        on the specified class argument, as a String.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jstr = jenv.GetStaticObjectField(jcls.handle, self._jfid(jenv))
            return JString(jenv, jstr, own=False).str if jstr else None

    def getStaticObject(self, jcls: JClass) -> Optional[JObject]:
        """Returns the value of a static field represented by this Field,
        on the specified class argument, as an Object.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jobj = jenv.GetStaticObjectField(jcls.handle, self._jfid(jenv))
            return self.jvm.JObject(jenv, jobj) if jobj else None

    def setStaticBoolean(self, jcls: JClass, val: bool):
        """Sets the value of a static field as a boolean on the specified
        class.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetStaticBooleanField(jcls.handle, self._jfid(jenv), val)

    def setStaticChar(self, jcls: JClass, val: str):
        """Sets the value of a static field as a char on the specified
        class.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetStaticCharField(jcls.handle, self._jfid(jenv), val)

    def setStaticByte(self, jcls: JClass, val: int):
        """Sets the value of a static field as a byte on the specified
        class.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetStaticByteField(jcls.handle, self._jfid(jenv), val)

    def setStaticShort(self, jcls: JClass, val: int):
        """Sets the value of a static field as a short on the specified
        class.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetStaticShortField(jcls.handle, self._jfid(jenv), val)

    def setStaticInt(self, jcls: JClass, val: int):
        """Sets the value of a static field as an int on the specified
        class.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetStaticIntField(jcls.handle, self._jfid(jenv), val)

    def setStaticLong(self, jcls: JClass, val: int):
        """Sets the value of a static field as a long on the specified
        class.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetStaticLongField(jcls.handle, self._jfid(jenv), val)

    def setStaticFloat(self, jcls: JClass, val: float):
        """Sets the value of a static field as a float on the specified
        class.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetStaticFloatField(jcls.handle, self._jfid(jenv), val)

    def setStaticDouble(self, jcls: JClass, val: float):
        """Sets the value of a static field as a double on the specified
        class.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetStaticDoubleField(jcls.handle, self._jfid(jenv), val)

    def setStaticString(self, jcls: JClass, val: str):
        """Sets the value of a static field represented by this Field,
        on the specified class argument to the specified new String value.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            if val is None:
                jstr = None
            else:
                jchars, size, jbuf = str2jchars(val)
                jstr = jenv.NewString(jchars, size)
            jenv.SetStaticObjectField(jcls.handle, self._jfid(jenv), jstr)

    def setStaticObject(self, jcls: JClass, val: Optional[JObject]):
        """Sets the value of a static field represented by this Field,
        on the specified class argument to the specified new Object value.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetStaticObjectField(jcls.handle, self._jfid(jenv),
                                      val.handle if val is not None else None)

    def getBoolean(self, this: JObject) -> bool:
        """Gets the value of an instance boolean field."""
        with self.jvm as (jvm, jenv):
            return jenv.GetBooleanField(this.handle, self._jfid(jenv))

    def getChar(self, this: JObject) -> str:
        """Gets the value of an instance field of type char or of another
        primitive type convertible to type char via a widening conversion.
        """
        with self.jvm as (jvm, jenv):
            return jenv.GetCharField(this.handle, self._jfid(jenv))

    def getByte(self, this: JObject) -> int:
        """Gets the value of an instance byte field."""
        with self.jvm as (jvm, jenv):
            return jenv.GetByteField(this.handle, self._jfid(jenv))

    def getShort(self, this: JObject) -> int:
        """Gets the value of an instance field of type short or of another
        primitive type convertible to type short via a widening conversion.
        """
        with self.jvm as (jvm, jenv):
            return jenv.GetShortField(this.handle, self._jfid(jenv))

    def getInt(self, this: JObject) -> int:
        """Gets the value of an instance field of type int or of another
        primitive type convertible to type int via a widening conversion.
        """
        with self.jvm as (jvm, jenv):
            return jenv.GetIntField(this.handle, self._jfid(jenv))

    def getLong(self, this: JObject) -> int:
        """Gets the value of an instance field of type long or of another
        primitive type convertible to type long via a widening conversion.
        """
        with self.jvm as (jvm, jenv):
            return jenv.GetLongField(this.handle, self._jfid(jenv))

    def getFloat(self, this: JObject) -> float:
        """Gets the value of an instance field of type float or of another
        primitive type convertible to type float via a widening conversion.
        """
        with self.jvm as (jvm, jenv):
            return jenv.GetFloatField(this.handle, self._jfid(jenv))

    def getDouble(self, this: JObject) -> float:
        """Gets the value of an instance field of type double or of another
        primitive type convertible to type double via a widening conversion.
        """
        with self.jvm as (jvm, jenv):
            return jenv.GetDoubleField(this.handle, self._jfid(jenv))

    def getString(self, this: JObject) -> Optional[str]:
        """Returns the value of an instance field represented by this Field,
        on the specified object argument, as a String.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jstr = jenv.GetObjectField(this.handle, self._jfid(jenv))
            return JString(jenv, jstr, own=False).str if jstr else None

    def getObject(self, this: JObject) -> Optional[JObject]:
        """Returns the value of an instance field represented by this Field,
        on the specified object argument, as an Object.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jobj = jenv.GetObjectField(this.handle, self._jfid(jenv))
            return self.jvm.JObject(jenv, jobj) if jobj else None

    def setBoolean(self, this: JObject, val: bool):
        """Sets the value of an instance field as a boolean on the specified
        object.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetBooleanField(this.handle, self._jfid(jenv), val)

    def setChar(self, this: JObject, val: str):
        """Sets the value of an instance field as a char on the specified
        object.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetCharField(this.handle, self._jfid(jenv), val)

    def setByte(self, this: JObject, val: int):
        """Sets the value of an instance field as a byte on the specified
        object.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetByteField(this.handle, self._jfid(jenv), val)

    def setShort(self, this: JObject, val: int):
        """Sets the value of an instance field as a short on the specified
        object.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetShortField(this.handle, self._jfid(jenv), val)

    def setInt(self, this: JObject, val: int):
        """Sets the value of an instance field as an int on the specified
        object.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetIntField(this.handle, self._jfid(jenv), val)

    def setLong(self, this: JObject, val: int):
        """Sets the value of an instance field as a long on the specified
        object.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetLongField(this.handle, self._jfid(jenv), val)

    def setFloat(self, this: JObject, val: float):
        """Sets the value of an instance field as a float on the specified
        object.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetFloatField(this.handle, self._jfid(jenv), val)

    def setDouble(self, this: JObject, val: float):
        """Sets the value of an instance field as a double on the specified
        object.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetDoubleField(this.handle, self._jfid(jenv), val)

    def setString(self, this: JObject, val: Optional[str]):
        """Sets the value of an instance field represented by this Field,
        on the specified object argument to the specified new String value.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            if val is None:
                jstr = None
            else:
                jchars, size, jbuf = str2jchars(val)
                jstr = jenv.NewString(jchars, size)
            jenv.SetObjectField(this.handle, self._jfid(jenv), jstr)

    def setObject(self, this: JObject, val: Optional[JObject]):
        """Sets the value of an instance field represented by this Field,
        on the specified object argument to the specified new Object value.
        """
        with self.jvm as (jvm, jenv):
            jenv.SetObjectField(this.handle, self._jfid(jenv),
                                val.handle if val is not None else None)

    # Helpers

    @cached
    def getSignature(self) -> str:
        """Returns the field signature."""
        return self.getType().getSignature()
