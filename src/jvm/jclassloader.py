# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Tuple

from public import public
import jni

from .jframe      import JFrame
from .jobjectbase import JObjectBase
from .jpackage    import JPackage
from .jclass      import JClass
from ._util       import str2jchars


@public
class JClassLoader(JObjectBase):

    """Java ClassLoader"""

    __slots__ = ()

    @classmethod
    def getSystemClassLoader(cls) -> Optional['JClassLoader']:
        """Returns the system class loader for delegation.
        This is the default delegation parent for new ClassLoader instances,
        and is typically the class loader used to start the application.
        This method is first invoked early in the runtime's startup sequence,
        at which point it creates the system class loader and sets it
        as the context class loader of the invoking Thread.
        The default system class loader is an implementation-dependent instance
        of this class."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcld = jenv.CallStaticObjectMethod(jvm.ClassLoader.Class,
                                               jvm.ClassLoader.getSystemClassLoader)
            return cls.jvm.JClassLoader(jenv, jcld) if jcld else None

    def loadClass(self, name: str) -> JClass:
        """Loads the class with the specified binary name.
        This method searches for classes in the same manner as the loadClass(String, boolean)
        method. It is invoked by the Java virtual machine to resolve class references.
        Invoking this method is equivalent to invoking loadClass(name, false)."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 2):
            jchars, size, jbuf = str2jchars(name)
            jname = jenv.NewString(jchars, size)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = jname
            jcls = jenv.CallObjectMethod(self._jobj, jvm.ClassLoader.loadClass, jargs)
            return self.jvm.JClass(jenv, jcls)

    def getPackage(self, name: str) -> Optional[JPackage]:
        """Returns a Package that has been defined by this class loader or any of
        its ancestors."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 2):
            jchars, size, jbuf = str2jchars(name)
            jname = jenv.NewString(jchars, size)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = jname
            jpkg = jenv.CallObjectMethod(self._jobj, jvm.ClassLoader.getPackage, jargs)
            return self.jvm.JPackage(jenv, jpkg) if jpkg else None

    def getPackages(self) -> Tuple[JPackage, ...]:
        """Returns all of the Packages defined by this class loader and its ancestors."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                  jvm.ClassLoader.getPackages),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JPackage(jenv, jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))

    def findClass(self, name: str) -> JClass:

        with self.jvm as (jvm, jenv), JFrame(jenv, 2):
            jchars, size, jbuf = str2jchars(name)
            jname = jenv.NewString(jchars, size)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = jname
            jcls = jenv.CallObjectMethod(self._jobj, jvm.ClassLoader.findClass, jargs)
            return self.jvm.JClass(jenv, jcls)

    def findSystemClass(self, name: str) -> JClass:

        with self.jvm as (jvm, jenv), JFrame(jenv, 2):
            jchars, size, jbuf = str2jchars(name)
            jname = jenv.NewString(jchars, size)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = jname
            jcls = jenv.CallObjectMethod(self._jobj, jvm.ClassLoader.findSystemClass, jargs)
            return self.jvm.JClass(jenv, jcls)

    def findLoadedClass(self, name: str) -> Optional[JClass]:

        with self.jvm as (jvm, jenv), JFrame(jenv, 2):
            jchars, size, jbuf = str2jchars(name)
            jname = jenv.NewString(jchars, size)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = jname
            jcls = jenv.CallObjectMethod(self._jobj, jvm.ClassLoader.findLoadedClass, jargs)
            return self.jvm.JClass(jenv, jcls) if jcls else None
