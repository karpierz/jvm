# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Tuple, FrozenSet

from public import public
import jni
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

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            name = name.encode("utf-8").translate(JClass.name_utrans)
            jcls = jenv.FindClass(name)
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getVoidClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Void.TYPE)

    @classmethod
    def getBooleanClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Boolean.TYPE)

    @classmethod
    def getCharClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Character.TYPE)

    @classmethod
    def getByteClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Byte.TYPE)

    @classmethod
    def getShortClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Short.TYPE)

    @classmethod
    def getIntClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Integer.TYPE)

    @classmethod
    def getLongClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Long.TYPE)

    @classmethod
    def getFloatClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Float.TYPE)

    @classmethod
    def getDoubleClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Double.TYPE)

    @classmethod
    def getStringClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.String.Class)

    @classmethod
    def getClassClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Class.Class)

    @classmethod
    def getBooleanObjectClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Boolean.Class)

    @classmethod
    def getCharObjectClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Character.Class)

    @classmethod
    def getByteObjectClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Byte.Class)

    @classmethod
    def getShortObjectClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Short.Class)

    @classmethod
    def getIntObjectClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Integer.Class)

    @classmethod
    def getLongObjectClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Long.Class)

    @classmethod
    def getFloatObjectClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Float.Class)

    @classmethod
    def getDoubleObjectClass(cls) -> 'JClass':

        with cls.jvm as (jvm, jenv):
            return cls.jvm.JClass(jenv, jvm.Double.Class)

    @classmethod
    def getBooleanArrayClass(cls, ndims: int) -> 'JClass':

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"Z")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getCharArrayClass(cls, ndims: int) -> 'JClass':

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"C")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getByteArrayClass(cls, ndims: int) -> 'JClass':

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"B")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getShortArrayClass(cls, ndims: int) -> 'JClass':

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"S")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getIntArrayClass(cls, ndims: int) -> 'JClass':

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"I")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getLongArrayClass(cls, ndims: int) -> 'JClass':

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"J")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getFloatArrayClass(cls, ndims: int) -> 'JClass':

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"F")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getDoubleArrayClass(cls, ndims: int) -> 'JClass':

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"D")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getStringArrayClass(cls, ndims: int) -> 'JClass':

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.FindClass(b"[" * ndims + b"Ljava/lang/String;")
            return cls.jvm.JClass(jenv, jcls)

    @classmethod
    def getObjectArrayClass(cls, cname: str, ndims: int) -> 'JClass':

        with cls.jvm as (jvm, jenv), JFrame(jenv, 1):
            cname = cname.encode("utf-8").translate(JClass.name_utrans)
            jcls = jenv.FindClass(b"[" * ndims + b"L" + cname + b";")
            return cls.jvm.JClass(jenv, jcls)

    def __init__(self, jenv: jni.JNIEnv, jcls: jni.jclass, own: bool=True):
        super().__init__(jenv, jni.cast(jcls, jni.jclass), own=own)

    def __hash__(self):
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

    def asObject(self, own: bool=True) -> 'JObject':

        with self.jvm as (jvm, jenv):
            return self.jvm.JObject(jenv, self._jobj, own=own)

    def asSubclass(self, jcls: 'JClass') -> 'JClass':

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = jcls.handle
            jccls = jenv.CallObjectMethod(self._jobj, jvm.Class.asSubclass, jargs)
            return self.jvm.JClass(jenv, jccls)

    @cached
    def getClassLoader(self) -> Optional['JClassLoader']:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcld = jenv.CallObjectMethod(self._jobj, jvm.Class.getClassLoader)
            return self.jvm.JClassLoader(jenv, jcld) if jcld else None

    @cached
    def getPackage(self) -> Optional['JPackage']:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jpkg = jenv.CallObjectMethod(self._jobj, jvm.Class.getPackage)
            return self.jvm.JPackage(jenv, jpkg) if jpkg else None

    @cached
    def getModifiers(self) -> int:

        with self.jvm as (jvm, jenv):
            jmodif = jenv.CallIntMethod(self._jobj, jvm.Class.getModifiers)
            return int(jmodif)

    @cached
    def getModifiersSet(self) -> FrozenSet[int]:

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

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jname = jenv.CallObjectMethod(self._jobj, jvm.Class.getName)
            return JString(jenv, jname, own=False).str

    @cached
    def getSimpleName(self) -> str:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jname = jenv.CallObjectMethod(self._jobj, jvm.Class.getSimpleName)
            return JString(jenv, jname, own=False).str

    @cached
    def getCanonicalName(self) -> str:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jname = jenv.CallObjectMethod(self._jobj, jvm.Class.getCanonicalName)
            return JString(jenv, jname, own=False).str if jname else ""

    @cached
    def getSignature(self) -> str:

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

    @cached
    def isInterface(self) -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isInterface)

    @cached
    def isEnum(self) -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isEnum)

    @cached
    def isPrimitive(self) -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isPrimitive)

    @cached
    def isAnnotation(self) -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isAnnotation)

    @cached
    def isAnonymousClass(self) -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isAnonymousClass)

    @cached
    def isLocalClass(self) -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isLocalClass)

    @cached
    def isMemberClass(self) -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isMemberClass)

    @cached
    def isArray(self) -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(self._jobj, jvm.Class.isArray)

    @cached
    def getComponentType(self) -> Optional['JClass']:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.CallObjectMethod(self._jobj, jvm.Class.getComponentType)
            return self.jvm.JClass(jenv, jcls) if jcls else None

    def isAssignableFrom(self, jcls: 'JClass') -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.IsAssignableFrom(jcls.handle, self._jobj)

    def isInstance(self, obj: JObjectBase) -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.IsInstanceOf(obj.handle, self._jobj)

    @cached
    def isThrowable(self) -> bool:

        with self.jvm as (jvm, jenv):
            return jenv.IsAssignableFrom(self._jobj, jvm.Throwable.Class)

    def isException(self) -> bool: return self.isThrowable()

    @cached
    def getSuperclass(self) -> Optional['JClass']:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.GetSuperclass(self._jobj)
            return self.jvm.JClass(jenv, jcls) if jcls else None

    @cached
    def getInterfaces(self) -> Tuple['JClass', ...]:

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

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                  jvm.Class.getConstructors),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JConstructor(jenv, jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))

    def getDeclaredField(self, name: str) -> 'JField':

        with self.jvm as (jvm, jenv), JFrame(jenv, 2):
            jchars, size, jbuf = str2jchars(name)
            jname = jenv.NewString(jchars, size)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = jname
            jfld = jenv.CallObjectMethod(self._jobj, jvm.Class.getDeclaredField, jargs)
            return self.jvm.JField(jenv, jfld)

    @cached
    def getDeclaredFields(self) -> Tuple['JField', ...]:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jarr = jni.cast(jenv.CallObjectMethod(self._jobj,
                                                  jvm.Class.getDeclaredFields),
                                                  jni.jobjectArray)
            jlen = jenv.GetArrayLength(jarr)
            with JFrame(jenv, jlen):
                return tuple(self.jvm.JField(jenv, jenv.GetObjectArrayElement(jarr, idx))
                             for idx in range(jlen))

    def getField(self, name: str) -> 'JField':

        with self.jvm as (jvm, jenv), JFrame(jenv, 2):
            jchars, size, jbuf = str2jchars(name)
            jname = jenv.NewString(jchars, size)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = jname
            jfld = jenv.CallObjectMethod(self._jobj, jvm.Class.getField, jargs)
            return self.jvm.JField(jenv, jfld)

    @cached
    def getFields(self) -> Tuple['JField', ...]:

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

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jcls = jenv.CallObjectMethod(self._jobj, jvm.Class.getEnclosingClass)
            return self.jvm.JClass(jenv, jcls) if jcls else None

    @cached
    def getEnclosingConstructor(self) -> Optional['JConstructor']:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jctor = jenv.CallObjectMethod(self._jobj, jvm.Class.getEnclosingConstructor)
            return self.jvm.JConstructor(jenv, jctor) if jctor else None

    @cached
    def getEnclosingMethod(self) -> Optional['JMethod']:

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jmeth = jenv.CallObjectMethod(self._jobj, jvm.Class.getEnclosingMethod)
            return self.jvm.JMethod(jenv, jmeth) if jmeth else None

    def newInstance(self) -> 'JObject':

        with self.jvm as (jvm, jenv), JFrame(jenv, 1):
            jobj = jenv.CallObjectMethod(self._jobj, jvm.Class.newInstance)
            return self.jvm.JObject(jenv, jobj)
