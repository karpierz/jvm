# Copyright (c) 2004-2022 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Tuple, FrozenSet

import jni
from .lib import public
from .lib import cached

from .jconstants  import EJavaModifiers
from .jmodifiers  import JModifiers
from .jframe      import JFrame
from .jstring     import JString
from .jobjectbase import JObjectBase
from .jannotated  import JAnnotatedElement
from ._util       import str2jchars


@public
class JClass(JObjectBase, JAnnotatedElement):
    """Java Class"""

    __slots__ = ()

    name_trans  = bytes.maketrans(b"/.", b"./")
    name_utrans = bytes.maketrans(b"./", b"/.")

    @classmethod
    def forName(cls, name: str) -> 'JClass':
        """Returns the Class object associated with the class or interface
        with the given string name.
        """
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            name = name.encode("utf-8").translate(JClass.name_utrans)
            jcls = jenv.FindClass(name)
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getVoidClass(cls) -> 'JClass':
        """Returns the Class object of the primitive void type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Void.TYPE)

    @classmethod
    def getBooleanClass(cls) -> 'JClass':
        """Returns the Class object of the primitive boolean type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Boolean.TYPE)

    @classmethod
    def getCharClass(cls) -> 'JClass':
        """Returns the Class object of the primitive char type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Character.TYPE)

    @classmethod
    def getByteClass(cls) -> 'JClass':
        """Returns the Class object of the primitive byte type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Byte.TYPE)

    @classmethod
    def getShortClass(cls) -> 'JClass':
        """Returns the Class object of the primitive short type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Short.TYPE)

    @classmethod
    def getIntClass(cls) -> 'JClass':
        """Returns the Class object of the primitive int type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Integer.TYPE)

    @classmethod
    def getLongClass(cls) -> 'JClass':
        """Returns the Class object of the primitive long type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Long.TYPE)

    @classmethod
    def getFloatClass(cls) -> 'JClass':
        """Returns the Class object of the primitive float type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Float.TYPE)

    @classmethod
    def getDoubleClass(cls) -> 'JClass':
        """Returns the Class object of the primitive double type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Double.TYPE)

    @classmethod
    def getStringClass(cls) -> 'JClass':
        """Returns the Class object of java.lang.String type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.String.Class)

    @classmethod
    def getClassClass(cls) -> 'JClass':
        """Returns the Class object of java.lang.Class type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Class.Class)

    @classmethod
    def getBooleanObjectClass(cls) -> 'JClass':
        """Returns the Class object of java.lang.Boolean type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Boolean.Class)

    @classmethod
    def getCharObjectClass(cls) -> 'JClass':
        """Returns the Class object of java.lang.Character type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Character.Class)

    @classmethod
    def getByteObjectClass(cls) -> 'JClass':
        """Returns the Class object of java.lang.Byte type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Byte.Class)

    @classmethod
    def getShortObjectClass(cls) -> 'JClass':
        """Returns the Class object of java.lang.Short type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Short.Class)

    @classmethod
    def getIntObjectClass(cls) -> 'JClass':
        """Returns the Class object of java.lang.Integer type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Integer.Class)

    @classmethod
    def getLongObjectClass(cls) -> 'JClass':
        """Returns the Class object of java.lang.Long type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Long.Class)

    @classmethod
    def getFloatObjectClass(cls) -> 'JClass':
        """Returns the Class object of java.lang.Float type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Float.Class)

    @classmethod
    def getDoubleObjectClass(cls) -> 'JClass':
        """Returns the Class object of java.lang.Double type."""
        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Double.Class)

    @classmethod
    def getBooleanArrayClass(cls, ndims: int) -> 'JClass':
        """Returns the Class object of array of the primitive boolean type."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"Z")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getCharArrayClass(cls, ndims: int) -> 'JClass':
        """Returns the Class object of array of the primitive char type."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"C")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getByteArrayClass(cls, ndims: int) -> 'JClass':
        """Returns the Class object of array of the primitive byte type."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"B")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getShortArrayClass(cls, ndims: int) -> 'JClass':
        """Returns the Class object of array of the primitive short type."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"S")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getIntArrayClass(cls, ndims: int) -> 'JClass':
        """Returns the Class object of array of the primitive int type."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"I")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getLongArrayClass(cls, ndims: int) -> 'JClass':
        """Returns the Class object of array of the primitive long type."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"J")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getFloatArrayClass(cls, ndims: int) -> 'JClass':
        """Returns the Class object of array of the primitive float type."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"F")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getDoubleArrayClass(cls, ndims: int) -> 'JClass':
        """Returns the Class object of array of the primitive double type."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"D")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getStringArrayClass(cls, ndims: int) -> 'JClass':
        """Returns the Class object of array of java.lang.String type."""
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"Ljava/lang/String;")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getObjectArrayClass(cls, cname: str, ndims: int) -> 'JClass':
        """Returns the Class object associated with the array of class
        or interface with the given string name.
        """
        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            cname = cname.encode("utf-8").translate(JClass.name_utrans)
            jcls = jenv.FindClass(b"[" * ndims + b"L" + cname + b";")
            return cls.jvm.JClass(jenv, jcls)

    def __init__(self, jenv: jni.JNIEnv, jcls: jni.jclass, own: bool = True):
        super().__init__(jenv, jni.cast(jcls, jni.jclass), own=own)

    def __hash__(self):
        """Returns a hash code value for the object."""
        return super().__hash__()

    def __eq__(self, other):

        if self is other:
            return True

        if not isinstance(other, self.jvm.JClass):
            return NotImplemented

        if self._jobj == other.handle:
            return True  # pragma: no cover

        if self.hashCode() != other.hashCode():
            return False

        return True  # and self.getName() == other.getName()

    def __ne__(self, other):
        eq = self.__eq__(other)
        return NotImplemented if eq is NotImplemented else not eq

    def asObject(self, own: bool = True) -> 'JObject':

        with self.jvm as (jvm, jenv):
            return self.jvm.JObject(jenv, self._jobj, own=own)

    def asSubclass(self, jcls: 'JClass') -> 'JClass':
        """Casts this Class object to represent a subclass of the class
        represented by the specified class object.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = jcls.handle
            jccls = jenv.CallObjectMethod(self._jobj, jvm.Class.asSubclass, jargs)
            return self.jvm.JClass(jenv, jccls)

    @cached
    def getClassLoader(self) -> Optional['JClassLoader']:
        """Returns the class loader for the class."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcld = jenv.CallObjectMethod(self._jobj, jvm.Class.getClassLoader)
            return self.jvm.JClassLoader(jenv, jcld) if jcld else None

    @cached
    def getPackage(self) -> Optional['JPackage']:
        """Gets the package for this class."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jpkg = jenv.CallObjectMethod(self._jobj, jvm.Class.getPackage)
            return self.jvm.JPackage(jenv, jpkg) if jpkg else None

    @cached
    def getModifiers(self) -> int:
        """Returns the Java language modifiers for this class or interface,
        encoded in an integer.
        The JModifier class should be used to decode the modifiers in the integer.
        """
        with self.jvm as (jvm, jenv):
            jmodif = jenv.CallIntMethod(self._jobj, jvm.Class.getModifiers)
            return int(jmodif)

    @cached
    def getModifiersSet(self) -> FrozenSet[int]:
        """Returns the Java language modifiers for this class or interface,
        as a set of integers.
        The JModifier class should be used to decode the modifiers in the integer.
        """
        with self.jvm as (jvm, jenv):
            jmodif = jenv.CallIntMethod(self._jobj, jvm.Class.getModifiers)
            modif  = JModifiers(jvm, jenv, jmodif)
            return JClass.convertModifiers(modif)

    @staticmethod
    def convertModifiers(modif: JModifiers) -> FrozenSet[int]:
        res = set()
        if modif.isPublic:    res.add(EJavaModifiers.PUBLIC)
        if modif.isProtected: res.add(EJavaModifiers.PROTECTED)
        if modif.isFinal:     res.add(EJavaModifiers.FINAL)
        if modif.isStatic:    res.add(EJavaModifiers.STATIC)
        if modif.isAbstract:  res.add(EJavaModifiers.ABSTRACT)
        return frozenset(res)

    @cached
    def getName(self) -> str:
        """Returns the name of the entity (class, interface, array class,
        primitive type, or void) represented by this Class object, as a string.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jname = jenv.CallObjectMethod(self._jobj, jvm.Class.getName)
            return JString(jenv, jname, own=False).str

    @cached
    def getSimpleName(self) -> str:
        """Returns the simple name of the underlying class as given in the source code."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jname = jenv.CallObjectMethod(self._jobj, jvm.Class.getSimpleName)
            return JString(jenv, jname, own=False).str

    @cached
    def getCanonicalName(self) -> str:
        """Returns the canonical name of the underlying class as defined by the
        Java Language Specification.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jname = jenv.CallObjectMethod(self._jobj, jvm.Class.getCanonicalName)
            return JString(jenv, jname, own=False).str if jname else ""

    @cached
    def isInterface(self) -> bool:
        """Determines if the specified Class object represents an interface type."""
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isInterface)

    @cached
    def isEnum(self) -> bool:
        """Returns true if and only if this class was declared as an enum
        in the source code.
        """
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isEnum)

    @cached
    def isPrimitive(self) -> bool:
        """Returns true if and only if this class was declared as an enum
        in the source code.
        """
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isPrimitive)

    @cached
    def isAnnotation(self) -> bool:
        """Returns true if this Class object represents an annotation type."""
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isAnnotation)

    @cached
    def isAnonymousClass(self) -> bool:
        """Returns true if and only if the underlying class is an anonymous class."""
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isAnonymousClass)

    @cached
    def isLocalClass(self) -> bool:
        """Returns true if and only if the underlying class is a local class."""
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isLocalClass)

    @cached
    def isMemberClass(self) -> bool:
        """Returns true if and only if the underlying class is a member class."""
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isMemberClass)

    @cached
    def isArray(self) -> bool:
        """Determines if this Class object represents an array class."""
        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isArray)

    @cached
    def getComponentType(self) -> Optional['JClass']:
        """Returns the Class representing the component type of an array."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.CallObjectMethod(self._jobj, jvm.Class.getComponentType)
            return self.jvm.JClass(jenv, jcls) if jcls else None

    def isAssignableFrom(self, jcls: 'JClass') -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.IsAssignableFrom(jcls.handle, self._jobj)

    def isInstance(self, obj: JObjectBase) -> bool:
        """Determines if the specified Object is assignment-compatible with
        the object represented by this Class.
        """
        with self.jvm as (jvm, jenv):
            return jenv.IsInstanceOf(obj.handle, self._jobj)

    @cached
    def isThrowable(self) -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.IsAssignableFrom(self._jobj, jvm.Throwable.Class)

    def isException(self) -> bool: return self.isThrowable()

    @cached
    def getSuperclass(self) -> Optional['JClass']:
        """Returns the Class representing the superclass of the entity
        (class, interface, primitive type or void) represented by this Class.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.GetSuperclass(self._jobj)
            return self.jvm.JClass(jenv, jcls) if jcls else None

    @cached
    def getInterfaces(self) -> Tuple['JClass', ...]:
        """Determines the interfaces implemented by the class or interface
        represented by this object.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                  jvm.Class.getInterfaces),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JClass(jenv, jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))

    @cached
    def getDeclaredClasses(self) -> Tuple['JClass', ...]:
        """Returns an array of Class objects reflecting all the classes and interfaces
        declared as members of the class represented by this Class object.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                  jvm.Class.getDeclaredClasses),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JClass(jenv, jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))

    @cached
    def getDeclaredConstructors(self) -> Tuple['JConstructor', ...]:
        """Returns an array of Constructor objects reflecting all the constructors
        declared by the class represented by this Class object.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                  jvm.Class.getDeclaredConstructors),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JConstructor(jenv, jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))

    @cached
    def getConstructors(self) -> Tuple['JConstructor', ...]:
        """Returns an array containing Constructor objects reflecting all the
        public constructors of the class represented by this Class object.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                  jvm.Class.getConstructors),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JConstructor(jenv, jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))

    def getDeclaredField(self, name: str) -> 'JField':
        """Returns a Field object that reflects the specified declared field of the class
        or interface represented by this Class object.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 2):
            jchars, size, jbuf = str2jchars(name)
            jname = jenv.NewString(jchars, size)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = jname
            jfld = jenv.CallObjectMethod(self._jobj, jvm.Class.getDeclaredField, jargs)
            return self.jvm.JField(jenv, jfld)

    @cached
    def getDeclaredFields(self) -> Tuple['JField', ...]:
        """Returns an array of Field objects reflecting all the fields declared by
        the class or interface represented by this Class object.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                  jvm.Class.getDeclaredFields),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JField(jenv, jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))

    def getField(self, name: str) -> 'JField':
        """Returns a Field object that reflects the specified public member field
        of the class or interface represented by this Class object.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 2):
            jchars, size, jbuf = str2jchars(name)
            jname = jenv.NewString(jchars, size)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = jname
            jfld = jenv.CallObjectMethod(self._jobj, jvm.Class.getField, jargs)
            return self.jvm.JField(jenv, jfld)

    @cached
    def getFields(self) -> Tuple['JField', ...]:
        """Returns an array containing Field objects reflecting all the accessible
        public fields of the class or interface represented by this Class object.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                  jvm.Class.getFields),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JField(jenv, jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))

    @cached
    def getDeclaredMethods(self) -> Tuple['JMethod', ...]:
        """Returns an array containing Method objects reflecting all the declared methods
        of the class or interface represented by this Class object, including public,
        protected, default (package) access, and private methods, but excluding
        inherited methods.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                  jvm.Class.getDeclaredMethods),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JMethod(jenv, jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))

    @cached
    def getMethods(self) -> Tuple['JMethod', ...]:
        """Returns an array containing Method objects reflecting all the public methods
        of the class or interface represented by this Class object, including those
        declared by the class or interface and those inherited from superclasses
        and superinterfaces.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                  jvm.Class.getMethods),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JMethod(jenv, jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))

    @cached
    def getPropertyDescriptors(self) -> Tuple['JPropertyDescriptor', ...]:

        with self.jvm as (jvm, jenv), JFrame(jenv, 2):
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = self._jobj
            jbeanInfo = jenv.CallStaticObjectMethod(jvm.Introspector.Class,
                                                    jvm.Introspector.getBeanInfo, jargs)
            jarr = jni.cast(jenv.CallObjectMethod(jbeanInfo,
                                                  jvm.BeanInfo.getPropertyDescriptors),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JPropertyDescriptor(jenv,
                                                          jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))

    @cached
    def getEnclosingClass(self) -> Optional['JClass']:
        """Returns the immediately enclosing class of the underlying class."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.CallObjectMethod(self._jobj, jvm.Class.getEnclosingClass)
            return self.jvm.JClass(jenv, jcls) if jcls else None

    @cached
    def getEnclosingConstructor(self) -> Optional['JConstructor']:
        """If this Class object represents a local or anonymous class within a constructor,
        returns a Constructor object representing the immediately enclosing constructor
        of the underlying class.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jctor = jenv.CallObjectMethod(self._jobj, jvm.Class.getEnclosingConstructor)
            return self.jvm.JConstructor(jenv, jctor) if jctor else None

    @cached
    def getEnclosingMethod(self) -> Optional['JMethod']:
        """If this Class object represents a local or anonymous class within a method,
        returns a Method object representing the immediately enclosing method
        of the underlying class.
        """
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jmeth = jenv.CallObjectMethod(self._jobj, jvm.Class.getEnclosingMethod)
            return self.jvm.JMethod(jenv, jmeth) if jmeth else None

    def newInstance(self) -> 'JObject':
        """Creates a new instance of the class represented by this Class object."""
        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jobj = jenv.CallObjectMethod(self._jobj, jvm.Class.newInstance)
            return self.jvm.JObject(jenv, jobj)

    @cached
    def getSignature(self) -> str:
        """Returns the class signature."""
        name = self.getName()
        signature = JClass.__signatures.get(name)
        if signature is None:
            if name.startswith("["):
                signature = name.replace(".", "/")
            else:
                signature = "L" + name.replace(".", "/") + ";"
        return signature

    __signatures = {
        "void":    "V",
        "boolean": "Z",
        "char":    "C",
        "byte":    "B",
        "short":   "S",
        "int":     "I",
        "long":    "J",
        "float":   "F",
        "double":  "D",
    }
