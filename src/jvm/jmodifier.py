# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

import jni
from .lib import public
from .lib import classproperty

from .jobjectbase import JObjectBase


@public
class JModifier(JObjectBase):

    @classproperty
    def PUBLIC(cls) -> int:  # noqa: N805
        """The int value representing the public modifier."""
        with cls.jvm as (jvm, jenv):
            return jvm.Modifier.PUBLIC

    @classproperty
    def PROTECTED(cls) -> int:  # noqa: N805
        """The int value representing the protected modifier."""
        with cls.jvm as (jvm, jenv):
            return jvm.Modifier.PROTECTED

    @classproperty
    def PRIVATE(cls) -> int:  # noqa: N805
        """The int value representing the private modifier."""
        with cls.jvm as (jvm, jenv):
            return jvm.Modifier.PRIVATE

    @classproperty
    def FINAL(cls) -> int:  # noqa: N805
        """The int value representing the final modifier."""
        with cls.jvm as (jvm, jenv):
            return jvm.Modifier.FINAL

    @classproperty
    def STATIC(cls) -> int:  # noqa: N805
        """The int value representing the static modifier."""
        with cls.jvm as (jvm, jenv):
            return jvm.Modifier.STATIC

    @classproperty
    def ABSTRACT(cls) -> int:  # noqa: N805
        """The int value representing the abstract modifier."""
        with cls.jvm as (jvm, jenv):
            return jvm.Modifier.ABSTRACT

    @classproperty
    def INTERFACE(cls) -> int:  # noqa: N805
        """The int value representing the interface modifier."""
        with cls.jvm as (jvm, jenv):
            return jvm.Modifier.INTERFACE

    @classproperty
    def NATIVE(cls) -> int:  # noqa: N805
        """The int value representing the native modifier."""
        with cls.jvm as (jvm, jenv):
            return jvm.Modifier.NATIVE

    @classproperty
    def STRICT(cls) -> int:  # noqa: N805
        """The int value representing the strictfp modifier."""
        with cls.jvm as (jvm, jenv):
            return jvm.Modifier.STRICT

    @classproperty
    def SYNCHRONIZED(cls) -> int:  # noqa: N805
        """The int value representing the synchronized modifier."""
        with cls.jvm as (jvm, jenv):
            return jvm.Modifier.SYNCHRONIZED

    @classproperty
    def TRANSIENT(cls) -> int:  # noqa: N805
        """The int value representing the transient modifier."""
        with cls.jvm as (jvm, jenv):
            return jvm.Modifier.TRANSIENT

    @classproperty
    def VOLATILE(cls) -> int:  # noqa: N805
        """The int value representing the volatile modifier."""
        with cls.jvm as (jvm, jenv):
            return jvm.Modifier.VOLATILE

    @classmethod
    def isPublic(cls, modif: int) -> bool:
        """Return True if the integer argument includes the public modifier, \
        False otherwise."""
        with cls.jvm as (jvm, jenv):
            jmod = jni.new_array(jni.jvalue, 1)
            jmod[0].i = modif
            return jenv.CallStaticBooleanMethod(jvm.Modifier.Class,
                                                jvm.Modifier.isPublic, jmod)

    @classmethod
    def isProtected(cls, modif: int) -> bool:
        """Return True if the integer argument includes the protected modifier, \
        False otherwise."""
        with cls.jvm as (jvm, jenv):
            jmod = jni.new_array(jni.jvalue, 1)
            jmod[0].i = modif
            return jenv.CallStaticBooleanMethod(jvm.Modifier.Class,
                                                jvm.Modifier.isProtected, jmod)

    @classmethod
    def isPrivate(cls, modif: int) -> bool:
        """Return True if the integer argument includes the private modifier, \
        False otherwise."""
        with cls.jvm as (jvm, jenv):
            jmod = jni.new_array(jni.jvalue, 1)
            jmod[0].i = modif
            return jenv.CallStaticBooleanMethod(jvm.Modifier.Class,
                                                jvm.Modifier.isPrivate, jmod)

    @classmethod
    def isFinal(cls, modif: int) -> bool:
        """Return True if the integer argument includes the final modifier, \
        False otherwise."""
        with cls.jvm as (jvm, jenv):
            jmod = jni.new_array(jni.jvalue, 1)
            jmod[0].i = modif
            return jenv.CallStaticBooleanMethod(jvm.Modifier.Class,
                                                jvm.Modifier.isFinal, jmod)

    @classmethod
    def isStatic(cls, modif: int) -> bool:
        """Return True if the integer argument includes the static modifier, \
        False otherwise."""
        with cls.jvm as (jvm, jenv):
            jmod = jni.new_array(jni.jvalue, 1)
            jmod[0].i = modif
            return jenv.CallStaticBooleanMethod(jvm.Modifier.Class,
                                                jvm.Modifier.isStatic, jmod)

    @classmethod
    def isAbstract(cls, modif: int) -> bool:
        """Return True if the integer argument includes the abstract modifier, \
        False otherwise."""
        with cls.jvm as (jvm, jenv):
            jmod = jni.new_array(jni.jvalue, 1)
            jmod[0].i = modif
            return jenv.CallStaticBooleanMethod(jvm.Modifier.Class,
                                                jvm.Modifier.isAbstract, jmod)

    @classmethod
    def isInterface(cls, modif: int) -> bool:
        """Return True if the integer argument includes the interface modifier, \
        False otherwise."""
        with cls.jvm as (jvm, jenv):
            jmod = jni.new_array(jni.jvalue, 1)
            jmod[0].i = modif
            return jenv.CallStaticBooleanMethod(jvm.Modifier.Class,
                                                jvm.Modifier.isInterface, jmod)

    @classmethod
    def isNative(cls, modif: int) -> bool:
        """Return True if the integer argument includes the native modifier, \
        False otherwise."""
        with cls.jvm as (jvm, jenv):
            jmod = jni.new_array(jni.jvalue, 1)
            jmod[0].i = modif
            return jenv.CallStaticBooleanMethod(jvm.Modifier.Class,
                                                jvm.Modifier.isNative, jmod)

    @classmethod
    def isStrict(cls, modif: int) -> bool:
        """Return True if the integer argument includes the strictfp modifier, \
        False otherwise."""
        with cls.jvm as (jvm, jenv):
            jmod = jni.new_array(jni.jvalue, 1)
            jmod[0].i = modif
            return jenv.CallStaticBooleanMethod(jvm.Modifier.Class,
                                                jvm.Modifier.isStrict, jmod)

    @classmethod
    def isSynchronized(cls, modif: int) -> bool:
        """Return True if the integer argument includes the synchronized modifier, \
        False otherwise."""
        with cls.jvm as (jvm, jenv):
            jmod = jni.new_array(jni.jvalue, 1)
            jmod[0].i = modif
            return jenv.CallStaticBooleanMethod(jvm.Modifier.Class,
                                                jvm.Modifier.isSynchronized, jmod)

    @classmethod
    def isTransient(cls, modif: int) -> bool:
        """Return True if the integer argument includes the transient modifier, \
        False otherwise."""
        with cls.jvm as (jvm, jenv):
            jmod = jni.new_array(jni.jvalue, 1)
            jmod[0].i = modif
            return jenv.CallStaticBooleanMethod(jvm.Modifier.Class,
                                                jvm.Modifier.isTransient, jmod)

    @classmethod
    def isVolatile(cls, modif: int) -> bool:
        """Return True if the integer argument includes the volatile modifier, \
        False otherwise."""
        with cls.jvm as (jvm, jenv):
            jmod = jni.new_array(jni.jvalue, 1)
            jmod[0].i = modif
            return jenv.CallStaticBooleanMethod(jvm.Modifier.Class,
                                                jvm.Modifier.isVolatile, jmod)
