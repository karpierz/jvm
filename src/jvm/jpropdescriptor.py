# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

from .lib import public
from .lib import cached

from .jframe      import JFrame
from .jstring     import JString
from .jobjectbase import JObjectBase


@public
class JPropertyDescriptor(JObjectBase):
    """Java PropertyDescriptor"""

    __slots__ = ()

    @cached
    def getPropertyType(self) -> JClass | None:
        """Returns the Java type info for the property.

        Note that the Class object may describe primitive Java types such as int.
        This type is returned by the read method or is used as the parameter type
        of the write method. Returns null if the type is an indexed property that
        does not support non-indexed access.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.CallObjectMethod(self._jobj, jvm.PropertyDescriptor.getPropertyType)
            return self.jvm.JClass(jenv, jcls) if jcls else None

    @cached
    def getReadMethod(self) -> JMethod | None:
        """Gets the method that should be used to read the property value."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jmeth = jenv.CallObjectMethod(self._jobj, jvm.PropertyDescriptor.getReadMethod)
            return self.jvm.JMethod(jenv, jmeth) if jmeth else None

    @cached
    def getWriteMethod(self) -> JMethod | None:
        """Gets the method that should be used to write the property value."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jmeth = jenv.CallObjectMethod(self._jobj, jvm.PropertyDescriptor.getWriteMethod)
            return self.jvm.JMethod(jenv, jmeth) if jmeth else None

    @cached
    def hashCode(self) -> int:
        """Returns a hash code value for the object.

        See Object.hashCode() for a complete description.
        """
        with self.jvm as (jvm, jenv):
            return int(jenv.CallIntMethod(self._jobj, jvm.PropertyDescriptor.hashCode))

    # Below are inherited from java.beans.FeatureDescriptor.

    @cached
    def getName(self) -> str:
        """Gets the programmatic name of this feature."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jname = jenv.CallObjectMethod(self._jobj, jvm.PropertyDescriptor.getName)
            return JString(jenv, jname, own=False).str

    @cached
    def toString(self) -> str | None:
        """Returns a string representation of the object.

        See Object.toString() for a complete description.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jstr = jenv.CallObjectMethod(self._jobj, jvm.PropertyDescriptor.toString)
            return JString(jenv, jstr, own=False).str if jstr else None


from .jclass  import JClass   # noqa: E402
from .jmethod import JMethod  # noqa: E402
