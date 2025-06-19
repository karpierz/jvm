# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

from typing import FrozenSet

from .lib import public
from .lib import cached

from .jframe      import JFrame
from .jmodifiers  import JModifiers
from .jstring     import JString
from .jobjectbase import JObjectBase


@public
class JMember(JObjectBase):
    """Java Member"""

    __slots__ = ()

    @cached
    def getDeclaringClass(self) -> JClass:  # noqa: F821 # !!!
        """Returns the Class object representing the class or interface \
        that declares the member or constructor represented by this Member."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.CallObjectMethod(self._jobj, jvm.Member.getDeclaringClass)
            return self.jvm.JClass(jenv, jcls)

    @cached
    def getName(self) -> str:
        """Returns the simple name of the underlying member or constructor \
        represented by this Member."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jname = jenv.CallObjectMethod(self._jobj, jvm.Member.getName)
            return JString(jenv, jname, own=False).str

    @cached
    def getModifiers(self) -> int:
        """Returns the Java language modifiers for the member or constructor \
        represented by this Member, as an integer.

        The JModifier class should be used to decode the modifiers in the integer.
        """
        with self.jvm as (jvm, jenv):
            jmodif = jenv.CallIntMethod(self._jobj, jvm.Member.getModifiers)
            return int(jmodif)

    @cached
    def getModifiersSet(self) -> FrozenSet[int]:
        """Returns the Java language modifiers for the member or constructor \
        represented by this Member, as a set of integers.

        The JModifier class should be used to decode the modifiers in the integer.
        """
        with self.jvm as (jvm, jenv):
            jmodif = jenv.CallIntMethod(self._jobj, jvm.Member.getModifiers)
            modif  = JModifiers(jvm, jenv, jmodif)
            return self.jvm.JClass.convertModifiers(modif)

    @cached
    def isSynthetic(self) -> bool:
        """Returns True if this member was introduced by the compiler; \
        returns False otherwise."""
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Member.isSynthetic)


# from .jclass import JClass  # noqa: E402
