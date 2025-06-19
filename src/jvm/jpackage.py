# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

from typing import Tuple

import jni
from .lib import public
from .lib import cached

from .jframe      import JFrame
from .jstring     import JString
from .jobjectbase import JObjectBase
from .jannotated  import JAnnotatedElement
from ._util       import str2jchars


@public
class JPackage(JObjectBase, JAnnotatedElement):
    """Java Package"""

    __slots__ = ()

    @classmethod
    def getPackage(cls, name: str) -> JPackage | None:
        """Find a package by name in the callers ClassLoader instance."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 2):
            jchars, size, jbuf = str2jchars(name)
            jname = jenv.NewString(jchars, size)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = jname  # noqa: E741
            jpkg = jenv.CallStaticObjectMethod(jvm.Package.Class,
                                               jvm.Package.getPackage,
                                               jargs)
            return cls.jvm.JPackage(jenv, jpkg) if jpkg else None

    @classmethod
    def getPackages(cls) -> Tuple[JPackage, ...]:
        """Get all the packages currently known for the caller's ClassLoader instance."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallStaticObjectMethod(jvm.Package.Class,
                                                        jvm.Package.getPackages),
                                                        jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(cls.jvm.JPackage(jenv, jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))

    @cached
    def getName(self) -> str:
        """Return the name of this package."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jname = jenv.CallObjectMethod(self._jobj, jvm.Package.getName)
            return JString(jenv, jname, own=False).str

    @cached
    def getSpecificationTitle(self) -> str:
        """Return the title of the specification that this package implements."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            titl = jenv.CallObjectMethod(self._jobj, jvm.Package.getSpecificationTitle)
            return JString(jenv, titl, own=False).str if titl else None

    @cached
    def getSpecificationVersion(self) -> str:
        """Returns the version number of the specification that this package implements.

        This version string must be a sequence of nonnegative decimal integers separated
        by "."'s and may have leading zeros. When version strings are compared the most
        significant numbers are compared.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            ver = jenv.CallObjectMethod(self._jobj, jvm.Package.getSpecificationVersion)
            return JString(jenv, ver, own=False).str if ver else None

    @cached
    def getSpecificationVendor(self) -> str:
        """Return the name of the organization, vendor, or company that owns \
        and maintains the specification of the classes that implement this package."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            vend = jenv.CallObjectMethod(self._jobj, jvm.Package.getSpecificationVendor)
            return JString(jenv, vend, own=False).str if vend else None

    @cached
    def getImplementationTitle(self) -> str:
        """Return the title of this package."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            titl = jenv.CallObjectMethod(self._jobj, jvm.Package.getImplementationTitle)
            return JString(jenv, titl, own=False).str if titl else None

    @cached
    def getImplementationVersion(self) -> str:
        """Return the version of this implementation.

        It consists of any string assigned by the vendor of this implementation and
        does not have any particular syntax specified or expected by the Java runtime.
        It may be compared for equality with other package version strings used for this
        implementation by this vendor for this package.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            ver = jenv.CallObjectMethod(self._jobj, jvm.Package.getImplementationVersion)
            return JString(jenv, ver, own=False).str if ver else None

    @cached
    def getImplementationVendor(self) -> str:
        """Returns the name of the organization, vendor or company that provided \
        this implementation."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            vend = jenv.CallObjectMethod(self._jobj, jvm.Package.getImplementationVendor)
            return JString(jenv, vend, own=False).str if vend else None

    @cached
    def isSealed(self) -> bool:
        """Returns True if this package is sealed."""
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Package.isSealed)
