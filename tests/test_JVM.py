# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import unittest
import sys
NoneType = type(None)

import jni
from jvm.jconstants import EJavaType
from jvm.jstring    import JString


class JVMTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from . import jvm
        cls.jvm = jvm

    def test_JVM(self):

        from jvm import JVM

        with self.assertRaisesRegex(RuntimeError, "First paramter must be a string"):
            jvm = JVM(123)

        with self.assertRaisesRegex(RuntimeError,
                                    "Unable to load DLL \[non_existent_dll\], error = .+"):
            jvm = JVM("non_existent_dll")

        pass  # TODO

    def test__JVM(self):

        self.assertEqual(self.jvm._jvm.Byte.MIN_VALUE,    -128)
        self.assertEqual(self.jvm._jvm.Byte.MAX_VALUE,    127)
        self.assertEqual(self.jvm._jvm.Short.MIN_VALUE,   -32768)
        self.assertEqual(self.jvm._jvm.Short.MAX_VALUE,   32767)
        self.assertEqual(self.jvm._jvm.Integer.MIN_VALUE, -2147483648)
        self.assertEqual(self.jvm._jvm.Integer.MAX_VALUE, 2147483647)
        self.assertEqual(self.jvm._jvm.Long.MIN_VALUE,    -9223372036854775808)
        self.assertEqual(self.jvm._jvm.Long.MAX_VALUE,    9223372036854775807)
        self.assertEqual(self.jvm._jvm.Float.MIN_VALUE,   1.401298464324817e-45)
        self.assertEqual(self.jvm._jvm.Float.MAX_VALUE,   3.4028234663852886e+38)
        self.assertEqual(self.jvm._jvm.Double.MIN_VALUE,  5e-324)
        self.assertEqual(self.jvm._jvm.Double.MAX_VALUE,  1.7976931348623157e+308)

        pass  # TODO

    def test_JClassLoader(self):

        cloader = self.jvm.JClassLoader.getSystemClassLoader()
        self.assertIsInstance(cloader, self.jvm.JClassLoader)

        packages = cloader.getPackages()
        self.assertIsInstance(packages, tuple)
        for jpackage in packages:
            self._check_jpackage(jpackage)

        package_name = "java.lang"

        jpackage = cloader.getPackage(package_name)
        self._check_jpackage(jpackage,
                             name=package_name,
                             is_sealed=False)

        #jclass_name = "org.python.jsr223.PyScriptEngine"
        #jclass_name = "org.python.util.ClassEnquirer"
        #jclass_name = "java.lang.Object"

        # jclass = cloader.findClass(jclass_name)
        # self.assertIsInstance(jclass, self.jvm.JClass)
        # self._check_jclass(jclass,
        #                    name=jclass_name,
        #                    canonical_name=jclass_name,
        #                    simple_name=jclass_name.rpartition(".")[-1],
        #                    is_interface=False,
        #                    is_enum=False,
        #                    is_primitive=False,
        #                    is_annotation=False,
        #                    is_anonymous_class=False,
        #                    is_local_class=False,
        #                    is_member_class=False,
        #                    is_array=False)

        jclass_name = "nonexistent.package.and.Class"

        with self.assertRaisesRegex(self.jvm.JavaException,
                                    "Java exception java.lang.ClassNotFoundException occurred: "
                                    + jclass_name):
            jclass = cloader.findClass(jclass_name)

        jclass_name = "java.lang.String"

        jclass = cloader.findSystemClass(jclass_name)
        self.assertIsInstance(jclass, self.jvm.JClass)
        self._check_jclass(jclass,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           signature="L"+jclass_name.replace('.','/')+";",
                           is_interface=False,
                           is_enum=False,
                           is_primitive=False,
                           is_annotation=False,
                           is_anonymous_class=False,
                           is_local_class=False,
                           is_member_class=False,
                           is_array=False)

        jclass_name = "nonexistent.package.and.Class"

        with self.assertRaisesRegex(self.jvm.JavaException,
                                    "Java exception java.lang.ClassNotFoundException occurred: "
                                    + jclass_name):
            jclass = cloader.findSystemClass(jclass_name)

        jclass_name = "java.lang.Object"

        jclass = cloader.findLoadedClass(jclass_name)
        self._check_jclass(jclass,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           signature="L"+jclass_name.replace('.','/')+";",
                           is_interface=False,
                           is_enum=False,
                           is_primitive=False,
                           is_annotation=False,
                           is_anonymous_class=False,
                           is_local_class=False,
                           is_member_class=False,
                           is_array=False)

        jclass_name = "nonexistent.package.and.Class"

        jclass = cloader.findLoadedClass(jclass_name)
        self.assertIsNone(jclass)

        jclass_name = "org.python.util.ClassEnquirer"

        jclass = cloader.findLoadedClass(jclass_name)
        #self.assertIsNone(jclass)
        #def loadClass(self, name: str) -> Optional[JClass]:

    def test_JPackage(self):

        packages = self.jvm.JPackage.getPackages()
        self.assertIsInstance(packages, tuple)
        for jpackage in packages:
            self._check_jpackage(jpackage)

        package_name = "java.lang"

        jpackage = self.jvm.JPackage.getPackage(package_name)
        self._check_jpackage(jpackage,
                             name=package_name,
                             is_sealed=False)

    def test_JClass(self):

        jclass_name = "org.python.jsr223.PyScriptEngine"

        jclass = self.jvm.JClass.forName(jclass_name)
        self._check_jclass(jclass,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           signature="L"+jclass_name.replace('.','/')+";",
                           is_interface=False,
                           is_enum=False,
                           is_primitive=False,
                           is_annotation=False,
                           is_anonymous_class=False,
                           is_local_class=False,
                           is_member_class=False,
                           is_array=False)

        jclass_name = "java.lang.String"

        jclass = self.jvm.JClass.forName(jclass_name)
        self._check_jclass(jclass,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           is_array=False)

        # from JObjectBase

        str_value = str(jclass)
        self.assertIsInstance(str_value, str)
        self.assertEqual(str_value, jclass.toString())

        is_equals = jclass.equals(jclass)
        self.assertIsInstance(is_equals, bool)
        self.assertTrue(is_equals)
        jclass2 = self.jvm.JClass.forName(jclass_name)
        is_equals = jclass.equals(jclass2)
        self.assertIsInstance(is_equals, bool)
        self.assertTrue(is_equals)
        jclass2 = jclass.asObject(own=False).asClass(own=False)
        is_equals = jclass.equals(jclass2)
        self.assertIsInstance(is_equals, bool)
        self.assertTrue(is_equals)
        jclass2 = self.jvm.JClass.forName("java.lang.Integer")
        is_equals = jclass.equals(jclass2)
        self.assertIsInstance(is_equals, bool)
        self.assertFalse(is_equals)
        is_equals = jclass.equals(None)
        self.assertIsInstance(is_equals, bool)
        self.assertFalse(is_equals)
        is_equals = jclass.equals(111)
        self.assertIsInstance(is_equals, bool)
        self.assertFalse(is_equals)
        is_equals = jclass.equals("xxx")
        self.assertIsInstance(is_equals, bool)
        self.assertFalse(is_equals)

        # from JClass

        jclass = self.jvm.JClass.getVoidClass()
        self._check_jclass(jclass,
                           name="void",
                           canonical_name="void",
                           simple_name="void",
                           is_array=False)

        jclass = self.jvm.JClass.getBooleanClass()
        self._check_jclass(jclass,
                           name="boolean",
                           canonical_name="boolean",
                           simple_name="boolean",
                           is_array=False)

        jclass = self.jvm.JClass.getCharClass()
        self._check_jclass(jclass,
                           name="char",
                           canonical_name="char",
                           simple_name="char",
                           is_array=False)

        jclass = self.jvm.JClass.getByteClass()
        self._check_jclass(jclass,
                           name="byte",
                           canonical_name="byte",
                           simple_name="byte",
                           is_array=False)

        jclass = self.jvm.JClass.getShortClass()
        self._check_jclass(jclass,
                           name="short",
                           canonical_name="short",
                           simple_name="short",
                           is_array=False)

        jclass = self.jvm.JClass.getIntClass()
        self._check_jclass(jclass,
                           name="int",
                           canonical_name="int",
                           simple_name="int",
                           is_array=False)

        jclass = self.jvm.JClass.getLongClass()
        self._check_jclass(jclass,
                           name="long",
                           canonical_name="long",
                           simple_name="long",
                           is_array=False)

        jclass = self.jvm.JClass.getFloatClass()
        self._check_jclass(jclass,
                           name="float",
                           canonical_name="float",
                           simple_name="float",
                           is_array=False)

        jclass = self.jvm.JClass.getDoubleClass()
        self._check_jclass(jclass,
                           name="double",
                           canonical_name="double",
                           simple_name="double",
                           is_array=False)

        jclass = self.jvm.JClass.getStringClass()
        self._check_jclass(jclass,
                           name="java.lang.String",
                           canonical_name="java.lang.String",
                           simple_name="String",
                           is_array=False)

        jclass = self.jvm.JClass.getClassClass()
        self._check_jclass(jclass,
                           name="java.lang.Class",
                           canonical_name="java.lang.Class",
                           simple_name="Class",
                           is_array=False)

        jclass = self.jvm.JClass.getBooleanObjectClass()
        self._check_jclass(jclass,
                           name="java.lang.Boolean",
                           canonical_name="java.lang.Boolean",
                           simple_name="Boolean",
                           is_array=False)

        jclass = self.jvm.JClass.getCharObjectClass()
        self._check_jclass(jclass,
                           name="java.lang.Character",
                           canonical_name="java.lang.Character",
                           simple_name="Character",
                           is_array=False)

        jclass = self.jvm.JClass.getByteObjectClass()
        self._check_jclass(jclass,
                           name="java.lang.Byte",
                           canonical_name="java.lang.Byte",
                           simple_name="Byte",
                           is_array=False)

        jclass = self.jvm.JClass.getShortObjectClass()
        self._check_jclass(jclass,
                           name="java.lang.Short",
                           canonical_name="java.lang.Short",
                           simple_name="Short",
                           is_array=False)

        jclass = self.jvm.JClass.getIntObjectClass()
        self._check_jclass(jclass,
                           name="java.lang.Integer",
                           canonical_name="java.lang.Integer",
                           simple_name="Integer",
                           is_array=False)

        jclass = self.jvm.JClass.getLongObjectClass()
        self._check_jclass(jclass,
                           name="java.lang.Long",
                           canonical_name="java.lang.Long",
                           simple_name="Long",
                           is_array=False)

        jclass = self.jvm.JClass.getFloatObjectClass()
        self._check_jclass(jclass,
                           name="java.lang.Float",
                           canonical_name="java.lang.Float",
                           simple_name="Float",
                           is_array=False)

        jclass = self.jvm.JClass.getDoubleObjectClass()
        self._check_jclass(jclass,
                           name="java.lang.Double",
                           canonical_name="java.lang.Double",
                           simple_name="Double",
                           is_array=False)

        for ndims in (1, 2, 5, 14, 152):
            ndims_sparents = ndims * "["
            ndims_dparents = ndims * "[]"

            jclass = self.jvm.JClass.getBooleanArrayClass(ndims)
            self._check_jclass(jclass,
                               name=ndims_sparents + "Z",
                               canonical_name="boolean" + ndims_dparents,
                               simple_name="boolean" + ndims_dparents,
                               is_array=True)

            jclass = self.jvm.JClass.getCharArrayClass(ndims)
            self._check_jclass(jclass,
                               name=ndims_sparents + "C",
                               canonical_name="char" + ndims_dparents,
                               simple_name="char" + ndims_dparents,
                               is_array=True)

            jclass = self.jvm.JClass.getByteArrayClass(ndims)
            self._check_jclass(jclass,
                               name=ndims_sparents + "B",
                               canonical_name="byte" + ndims_dparents,
                               simple_name="byte" + ndims_dparents,
                               is_array=True)

            jclass = self.jvm.JClass.getShortArrayClass(ndims)
            self._check_jclass(jclass,
                               name=ndims_sparents + "S",
                               canonical_name="short" + ndims_dparents,
                               simple_name="short" + ndims_dparents,
                               is_array=True)

            jclass = self.jvm.JClass.getIntArrayClass(ndims)
            self._check_jclass(jclass,
                               name=ndims_sparents + "I",
                               canonical_name="int" + ndims_dparents,
                               simple_name="int" + ndims_dparents,
                               is_array=True)

            jclass = self.jvm.JClass.getLongArrayClass(ndims)
            self._check_jclass(jclass,
                               name=ndims_sparents + "J",
                               canonical_name="long" + ndims_dparents,
                               simple_name="long" + ndims_dparents,
                               is_array=True)

            jclass = self.jvm.JClass.getFloatArrayClass(ndims)
            self._check_jclass(jclass,
                               name=ndims_sparents + "F",
                               canonical_name="float" + ndims_dparents,
                               simple_name="float" + ndims_dparents,
                               is_array=True)

            jclass = self.jvm.JClass.getDoubleArrayClass(ndims)
            self._check_jclass(jclass,
                               name=ndims_sparents + "D",
                               canonical_name="double" + ndims_dparents,
                               simple_name="double" + ndims_dparents,
                               is_array=True)

            jclass = self.jvm.JClass.getStringArrayClass(ndims)
            self._check_jclass(jclass,
                               name=ndims_sparents + "Ljava.lang.String;",
                               canonical_name="java.lang.String" + ndims_dparents,
                               simple_name="String" + ndims_dparents,
                               is_array=True)

            jclass = self.jvm.JClass.getObjectArrayClass("java.lang.StringBuilder", ndims)
            self._check_jclass(jclass,
                               name=ndims_sparents + "Ljava.lang.StringBuilder;",
                               canonical_name="java.lang.StringBuilder" + ndims_dparents,
                               simple_name="StringBuilder" + ndims_dparents,
                               is_array=True)

        jclass  = self.jvm.JClass.forName(jclass_name)
        jclass2 = self.jvm.JClass.forName(jclass_name)
        jclass3 = jclass.asObject(own=False).asClass(own=False)
        jclass4 = self.jvm.JClass.forName("java.lang.Integer")
        self.assertIsInstance(jclass,  self.jvm.JClass)
        self.assertIsInstance(jclass2, self.jvm.JClass)
        self.assertIsInstance(jclass3, self.jvm.JClass)
        self.assertIsInstance(jclass4, self.jvm.JClass)
        self.assertEqual(jclass,     jclass)
        self.assertEqual(jclass,     jclass2)
        self.assertEqual(jclass,     jclass3)
        self.assertNotEqual(jclass,  jclass4)
        self.assertNotEqual(jclass2, jclass4)
        self.assertNotEqual(jclass3, jclass4)
        self.assertNotEqual(jclass,  None)
        self.assertNotEqual(jclass,  111)
        self.assertNotEqual(jclass,  "xxx")

        hash_value = hash(jclass)
        self.assertEqual(hash_value, jclass.hashCode())

        jobj = jclass.asObject(own=False)
        self.assertIsInstance(jobj, self.jvm.JObject)
        jobj = jclass.asObject(own=True)
        self.assertIsInstance(jobj, self.jvm.JObject)
        jobj = jclass.asObject()
        self.assertIsInstance(jobj, self.jvm.JObject)

        subjclass_name = "java.lang.Object"
        jsubcls = self.jvm.JClass.forName(subjclass_name)
        self._check_jclass(jsubcls,
                           name=subjclass_name,
                           canonical_name=subjclass_name,
                           simple_name=subjclass_name.rpartition(".")[-1],
                           is_array=False)
        subclass = jclass.asSubclass(jsubcls)
        self._check_jclass(subclass,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           is_array=False)

        cloader = jclass.getClassLoader()
        self.assertIsInstance(cloader, (self.jvm.JClassLoader, NoneType))

        package = jclass.getPackage()
        self.assertIsInstance(package, (self.jvm.JPackage, NoneType))

        modifiers = jclass.getModifiersSet()
        self.assertIsInstance(modifiers, frozenset)
        for item in modifiers:
            self.assertIsInstance(item, int)

        raw_modifiers = jclass.getModifiers()
        self.assertIsInstance(raw_modifiers, int)

        #@staticmethod
        #def convertModifiers(modif: JModifiers) -> FrozenSet[int]:
        #
        #    res = set()
        #    if modif.isPublic:    res.add(EJavaModifiers.PUBLIC)
        #    if modif.isProtected: res.add(EJavaModifiers.PROTECTED)
        #    if modif.isFinal:     res.add(EJavaModifiers.FINAL)
        #    if modif.isStatic:    res.add(EJavaModifiers.STATIC)
        #    if modif.isAbstract:  res.add(EJavaModifiers.ABSTRACT)
        #    return res

        component_class = jclass.getComponentType()
        self.assertIsInstance(component_class, (self.jvm.JClass, NoneType))

        subjclass_name = "java.lang.Object"
        jsubcls = self.jvm.JClass.forName(subjclass_name)
        self._check_jclass(jsubcls,
                           name=subjclass_name,
                           canonical_name=subjclass_name,
                           simple_name=subjclass_name.rpartition(".")[-1],
                           is_array=False)
        is_a = jsubcls.isAssignableFrom(jclass)
        self.assertIs(type(is_a), bool)

        #obj: JObjectBase
        jobj = self.jvm.JObject.newString("STRING")
        is_a = jclass.isInstance(jobj)
        self.assertIs(type(is_a), bool)

        is_a = jclass.isThrowable()
        self.assertIs(type(is_a), bool)
        is_a = jclass.isException()
        self.assertIs(type(is_a), bool)

        super_class = jclass.getSuperclass()
        self.assertIsInstance(super_class, (self.jvm.JClass, NoneType))

        interfaces = jclass.getInterfaces()
        self.assertIsInstance(interfaces, tuple)
        for item in interfaces:
            self.assertIsInstance(item, self.jvm.JClass)

        classes = jclass.getDeclaredClasses()
        self.assertIsInstance(classes, tuple)
        for item in classes:
            self.assertIsInstance(item, self.jvm.JClass)

        constructors = jclass.getDeclaredConstructors()
        self.assertIsInstance(constructors, tuple)
        for item in constructors:
            self.assertIsInstance(item, self.jvm.JConstructor)

        constructors = jclass.getConstructors()
        self.assertIsInstance(constructors, tuple)
        for item in constructors:
            self.assertIsInstance(item, self.jvm.JConstructor)

        decl_field_name = "CASE_INSENSITIVE_ORDER"
        field_name      = "CASE_INSENSITIVE_ORDER"

        field = jclass.getDeclaredField(decl_field_name)
        self.assertIsInstance(field, self.jvm.JField)

        fields = jclass.getDeclaredFields()
        self.assertIsInstance(fields, tuple)
        for item in fields:
            self.assertIsInstance(item, self.jvm.JField)

        field = jclass.getField(field_name)
        self.assertIsInstance(field, self.jvm.JField)

        fields = jclass.getFields()
        self.assertIsInstance(fields, tuple)
        for item in fields:
            self.assertIsInstance(item, self.jvm.JField)

        methods = jclass.getDeclaredMethods()
        self.assertIsInstance(methods, tuple)
        for item in methods:
            self.assertIsInstance(item, self.jvm.JMethod)

        methods = jclass.getMethods()
        self.assertIsInstance(methods, tuple)
        for item in methods:
            self.assertIsInstance(item, self.jvm.JMethod)

        descriptors = jclass.getPropertyDescriptors()
        self.assertIsInstance(descriptors, tuple)
        for item in descriptors:
            self.assertIsInstance(item, self.jvm.JPropertyDescriptor)

        enclosing_class = jclass.getEnclosingClass()
        self.assertIsInstance(enclosing_class, (self.jvm.JClass, NoneType))

        enclosing_constructor = jclass.getEnclosingConstructor()
        self.assertIsInstance(enclosing_constructor, (self.jvm.JConstructor, NoneType))

        enclosing_method = jclass.getEnclosingMethod()
        self.assertIsInstance(enclosing_method, (self.jvm.JMethod, NoneType))

        jobject = jclass.newInstance()
        self.assertIsNotNone(jobject)
        self.assertIsInstance(jobject, self.jvm.JObject)
        self.assertEqual(jobject.getClass().getName(), jclass_name)
        self.assertEqual(jobject.toString(), u"")

    def test_JField(self):

        jclass_name = "java.lang.String"

        jclass = self.jvm.JClass.forName(jclass_name)
        self._check_jclass(jclass,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           is_array=False)

        decl_field_name = "CASE_INSENSITIVE_ORDER"

        field = jclass.getDeclaredField(decl_field_name)
        self.assertIsInstance(field, self.jvm.JField)

        # from JMember

        decl_class = field.getDeclaringClass()
        self._check_jclass(decl_class,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           is_array=False)

        modifiers = field.getModifiersSet()
        self.assertIsInstance(modifiers, frozenset)
        for item in modifiers:
            self.assertIsInstance(item, int)

        raw_modifiers = field.getModifiers()
        self.assertIsInstance(raw_modifiers, int)

        name = field.getName()
        self.assertIsInstance(name, str)
        self.assertEqual(name, decl_field_name)

        # from JField

        field_type = field.getType()
        self.assertIsInstance(field_type, self.jvm.JClass)

        signature = field.getSignature()
        self.assertIsInstance(signature, str)

        is_a = field.isEnumConstant()
        self.assertIs(type(is_a), bool)

        decl_field_name = "FILL"
        jclass_name = "java.awt.font.ShapeGraphicAttribute"
        jclass = self.jvm.JClass.forName(jclass_name)
        field = jclass.getDeclaredField(decl_field_name)
        self.assertIsInstance(field, self.jvm.JField)
        value = field.getStaticBoolean(jclass)
        self.assertIsInstance(value, bool)

        decl_field_name = "MAX_VALUE"

        jclass_name = "java.lang.Character"
        jclass = self.jvm.JClass.forName(jclass_name)
        field = jclass.getDeclaredField(decl_field_name)
        self.assertIsInstance(field, self.jvm.JField)
        value = field.getStaticChar(jclass)
        self.assertIsInstance(value, str)
        self.assertEqual(len(value), 1)

        jclass_name = "java.lang.Byte"
        jclass = self.jvm.JClass.forName(jclass_name)
        field = jclass.getDeclaredField(decl_field_name)
        self.assertIsInstance(field, self.jvm.JField)
        value = field.getStaticByte(jclass)
        self.assertIsInstance(value, int)

        jclass_name = "java.lang.Short"
        jclass = self.jvm.JClass.forName(jclass_name)
        field = jclass.getDeclaredField(decl_field_name)
        self.assertIsInstance(field, self.jvm.JField)
        value = field.getStaticShort(jclass)
        self.assertIsInstance(value, int)

        jclass_name = "java.lang.Integer"
        jclass = self.jvm.JClass.forName(jclass_name)
        field = jclass.getDeclaredField(decl_field_name)
        self.assertIsInstance(field, self.jvm.JField)
        value = field.getStaticInt(jclass)
        self.assertIsInstance(value, int)

        jclass_name = "java.lang.Long"
        jclass = self.jvm.JClass.forName(jclass_name)
        field = jclass.getDeclaredField(decl_field_name)
        self.assertIsInstance(field, self.jvm.JField)
        value = field.getStaticLong(jclass)
        self.assertIsInstance(value, int)

        jclass_name = "java.lang.Float"
        jclass = self.jvm.JClass.forName(jclass_name)
        field = jclass.getDeclaredField(decl_field_name)
        self.assertIsInstance(field, self.jvm.JField)
        value = field.getStaticFloat(jclass)
        self.assertIsInstance(value, float)

        jclass_name = "java.lang.Double"
        jclass = self.jvm.JClass.forName(jclass_name)
        field = jclass.getDeclaredField(decl_field_name)
        self.assertIsInstance(field, self.jvm.JField)
        value = field.getStaticDouble(jclass)
        self.assertIsInstance(value, float)

        decl_field_name = "ENGINE"
        jclass_name = "javax.script.ScriptEngine"
        jclass = self.jvm.JClass.forName(jclass_name)
        field = jclass.getDeclaredField(decl_field_name)
        self.assertIsInstance(field, self.jvm.JField)
        value = field.getStaticString(jclass)
        self.assertIsInstance(value, str)

        decl_field_name = "TRUE"
        jclass_name = "java.lang.Boolean"
        jclass = self.jvm.JClass.forName(jclass_name)
        field = jclass.getDeclaredField(decl_field_name)
        self.assertIsInstance(field, self.jvm.JField)
        value = field.getStaticObject(jclass)
        self.assertIsInstance(value, self.jvm.JObject)

        #this: JObject
        #value = field.getBoolean(this)
        #self.assertIsInstance(value, bool)

        #this: JObject
        #value = field.getChar(this)
        #self.assertIsInstance(value, str)
        #self.assertEqual(len(value), 1)

        #this: JObject
        #value = field.getByte(this)
        #self.assertIsInstance(value, int)

        #this: JObject
        #value = field.getShort(this)
        #self.assertIsInstance(value, int)

        #this: JObject
        #value = field.getInt(this)
        #self.assertIsInstance(value, int)

        #this: JObject
        #value = field.getLong(this)
        #self.assertIsInstance(value, int)

        #this: JObject
        #value = field.getFloat(this)
        #self.assertIsInstance(value, float)

        #this: JObject
        #value = field.getDouble(this)
        #self.assertIsInstance(value, float)

        #this: JObject
        #value = field.getString(this)
        #self.assertIsInstance(value, (str, NoneType))

        #this: JObject
        #value = field.getObject(this)
        #self.assertIsInstance(value, (self.jvm.JObject, NoneType))

        #jclass: JClass, val: bool)
        #field.setStaticBoolean(jclass, val)

        #jclass: JClass, val: str)
        #field.setStaticChar(jclass, val)

        #jclass: JClass, val: int)
        #field.setStaticByte(jclass, val)

        #jclass: JClass, val: int)
        #field.setStaticShort(jclass, val)

        #jclass: JClass, val: int)
        #field.setStaticInt(jclass, val)

        #jclass: JClass, val: Union[int, long])
        #field.setStaticLong(jclass, val)

        #jclass: JClass, val: float)
        #field.setStaticFloat(jclass, val)

        #jclass: JClass, val: float)
        #field.setStaticDouble(jclass, val)

        #jclass: JClass, val: str)
        #field.setStaticString(jclass, val)

        #jclass: JClass, val: Optional[JObject])
        #field.setStaticObject(jclass, val)

        #this: JObject, val: bool)
        #field.setBoolean(this, val)

        #this: JObject, val: str)
        #field.setChar(this, val)

        #this: JObject, val: int)
        #field.setByte(this, val)

        #this: JObject, val: int)
        #field.setShort(this, val)

        #this: JObject, val: int)
        #field.setInt(this, val)

        #this: JObject, val: Union[int, long])
        #field.setLong(this, val)

        #this: JObject, val: float)
        #field.setFloat(this, val)

        #this: JObject, val: float)
        #field.setDouble(this, val)

        #this: JObject, val: Optional[str])
        #field.setString(this, val)

        #this: JObject, val: Optional[JObject])
        #field.setObject(this, val)

    def test_JArguments(self):

        jargs = self.jvm.JArguments(20)

        for val_expected in (True, False, 0, 1, 23, 34):
            #pos: int, val_expected: bool
            jargs.setBoolean(0, val_expected)
            val = jargs.arguments[0].z
            self.assertIsInstance(val, int)
            self.assertEqual(val, val_expected)
            jargs.arguments[10].z = val_expected
            jargs.argtypes[10]    = EJavaType.BOOLEAN
            val = jargs.arguments[10].z
            self.assertIsInstance(val, int)
            self.assertEqual(val, val_expected)

        for val_expected in (1.0, "1", "33.2", object()):
            with self.assertRaises(TypeError):
                jargs.setBoolean(0, val_expected)

        for val_expected in ("a", "B"):
            #pos: int, val_expected: str
            jargs.setChar(1, val_expected)
            val = jargs.arguments[1].c
            self.assertIsInstance(val, str)
            self.assertEqual(val, val_expected)
            jargs.arguments[11].c = val_expected
            jargs.argtypes[11]    = EJavaType.CHAR
            val = jargs.arguments[11].c
            self.assertIsInstance(jargs.arguments[11].c, str)
            self.assertEqual(val, val_expected)

        for val_expected in (1.0, 1):
            with self.assertRaises(TypeError):
                jargs.setChar(1, 1.0)

        for val_expected in (True, False, 0, 1, 23, 34):
            #pos: int, val_expected: int
            jargs.setByte(2, val_expected)
            val = jargs.arguments[2].b
            self.assertIsInstance(val, int)
            self.assertEqual(val, val_expected)
            jargs.arguments[12].b = val_expected
            jargs.argtypes[12]    = EJavaType.BYTE
            val = jargs.arguments[12].b
            self.assertIsInstance(val, int)
            self.assertEqual(val, val_expected)

        for val_expected in (1.0, "1", "33.2", object()):
            with self.assertRaises(TypeError):
                jargs.setByte(2, val_expected)

        for val_expected in (True, False, 0, 1, 23, 34):
            #pos: int, val_expected: int
            jargs.setShort(3, val_expected)
            val = jargs.arguments[3].s
            self.assertIsInstance(val, int)
            self.assertEqual(val, val_expected)
            jargs.arguments[13].s = val_expected
            jargs.argtypes[13]    = EJavaType.SHORT
            val = jargs.arguments[13].s
            self.assertIsInstance(val, int)
            self.assertEqual(val, val_expected)

        for val_expected in (1.0, "1", "33.2", object()):
            with self.assertRaises(TypeError):
                jargs.setShort(3, val_expected)

        for val_expected in (True, False, 0, 1, 23, 34):
            #pos: int, val_expected: int
            jargs.setInt(4, val_expected)
            val = jargs.arguments[4].i
            self.assertIsInstance(val, int)
            self.assertEqual(val, val_expected)
            jargs.arguments[14].i = val_expected
            jargs.argtypes[14]    = EJavaType.INT
            val = jargs.arguments[14].i
            self.assertIsInstance(val, int)
            self.assertEqual(val, val_expected)

        for val_expected in (1.0, "1", "33.2", object()):
            with self.assertRaises(TypeError):
                jargs.setInt(4, val_expected)

        for val_expected in (True, False, 0, 1, 23, 34, 2222222222222222, 9223372036854775807):
            #pos: int, val_expected: Union[int, long]
            jargs.setLong(5, val_expected)
            val = jargs.arguments[5].j
            self.assertIsInstance(val, int)
            self.assertEqual(val, val_expected)
            jargs.arguments[15].j = val_expected
            jargs.argtypes[15]    = EJavaType.LONG
            val = jargs.arguments[15].j
            self.assertIsInstance(val, int)
            self.assertEqual(val, val_expected)

        for val_expected in (1.0, "1", "33.2", object()):
            with self.assertRaises(TypeError):
                jargs.setLong(5, val_expected)

        for val_expected in (True, False, 0, 1, 23, 34, 2147483648, 3.44, 5.77):
            #pos: int, val_expected: float
            jargs.setFloat(6, val_expected)
            val = jargs.arguments[6].f
            self.assertIsInstance(val, float)
            self.assertAlmostEqual(val, val_expected, places=6)
            jargs.arguments[16].f = val_expected
            jargs.argtypes[16]    = EJavaType.FLOAT
            val = jargs.arguments[16].f
            self.assertIsInstance(val, float)
            self.assertAlmostEqual(val, val_expected, places=6)

        for val_expected in ("1", "33.2", object()):
            with self.assertRaises(TypeError):
                jargs.setFloat(6, val_expected)

        for val_expected in (True, False, 0, 1, 23, 34, 2222222222222222, 9223372036854776, 3.44, 5.77):
            #pos: int, val_expected: float
            jargs.setDouble(7, val_expected)
            val = jargs.arguments[7].d
            self.assertIsInstance(val, float)
            self.assertEqual(val, val_expected)
            jargs.arguments[17].d = val_expected
            jargs.argtypes[17]    = EJavaType.DOUBLE
            val = jargs.arguments[17].d
            self.assertIsInstance(val, float)
            self.assertEqual(val, val_expected)

        for val_expected in ("1", "33.2", object()):
            with self.assertRaises(TypeError):
                jargs.setDouble(7, val_expected)

        for val_expected in (None, "", "XXX"):
            #pos: int, val: Optional[str]
            jargs.setString(8, val_expected)
            val = jargs.arguments[8].l
            #self.assertIsInstance(val, float)
            #self.assertEqual(val, val_expected)
            #jargs.arguments[18].l = val_expected
            #jargs.argtypes[18]    = EJavaType.DOUBLE
            #val = jargs.arguments[18].l
            #self.assertIsInstance(val, float)
            #self.assertEqual(val, val_expected)

        for val_expected in (1, 33.2, True, object()):
            with self.assertRaises(TypeError):
                jargs.setString(8, val_expected)

        for val_expected in (None,):
            #pos: int, val: Optional[str]
            jargs.setObject(9, val_expected)
            val = jargs.arguments[9].l
            #self.assertIsInstance(val, float)
            #self.assertEqual(val, val_expected)
            #jargs.arguments[19].l = val_expected
            #jargs.argtypes[19]    = EJavaType.DOUBLE
            #val = jargs.arguments[19].l
            #self.assertIsInstance(val, float)
            #self.assertEqual(val, val_expected)

        for val_expected in (1, 33.2, True):
            with self.assertRaises(TypeError):
                jargs.setObject(9, val_expected)

        # TODO

    def test_JConstructor(self):

        jclass_name = "java.lang.String"

        jclass = self.jvm.JClass.forName(jclass_name)
        self._check_jclass(jclass,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           is_array=False)

        constructors = jclass.getDeclaredConstructors()
        self.assertIsInstance(constructors, tuple)
        for jctor in constructors:
            self.assertIsInstance(jctor, self.jvm.JConstructor)
        self.assertGreaterEqual(len(constructors), 15)

        ctor_signature = u"([BLjava/lang/String;)V"
        jctor = self._get_constructor(jclass, ctor_signature)
        # throws UnsupportedEncodingException

        # from JMember

        decl_class = jctor.getDeclaringClass()
        self._check_jclass(decl_class,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           is_array=False)

        modifiers = jctor.getModifiersSet()
        self.assertIsInstance(modifiers, frozenset)
        for item in modifiers:
            self.assertIsInstance(item, int)

        raw_modifiers = jctor.getModifiers()
        self.assertIsInstance(raw_modifiers, int)

        name = jctor.getName()
        self.assertIsInstance(name, str)
        self.assertEqual(name, "java.lang.String")

        # from JConstructor

        parameter_types = jctor.getParameterTypes()
        self.assertIsInstance(parameter_types, tuple)
        for item in parameter_types:
            self.assertIsInstance(item, self.jvm.JClass)

        exception_types = jctor.getExceptionTypes()
        self.assertIsInstance(exception_types, tuple)
        for item in exception_types:
            self.assertIsInstance(item, self.jvm.JClass)

        is_vrargs = jctor.isVarArgs()
        self.assertIs(type(is_vrargs), bool)
        self.assertFalse(is_vrargs)

        signature = jctor.getSignature()
        self.assertIsInstance(signature, str)
        self.assertEqual(signature, ctor_signature)

        ctor_signature = u"([CII)V"
        jctor = self._get_constructor(jclass, ctor_signature)

        # from JMember

        decl_class = jctor.getDeclaringClass()
        self._check_jclass(decl_class,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           is_array=False)

        modifiers = jctor.getModifiersSet()
        self.assertIsInstance(modifiers, frozenset)
        for item in modifiers:
            self.assertIsInstance(item, int)

        raw_modifiers = jctor.getModifiers()
        self.assertIsInstance(raw_modifiers, int)

        name = jctor.getName()
        self.assertIsInstance(name, str)
        self.assertEqual(name, "java.lang.String")

        # from JConstructor

        parameter_types = jctor.getParameterTypes()
        self.assertIsInstance(parameter_types, tuple)
        for item in parameter_types:
            self.assertIsInstance(item, self.jvm.JClass)

        exception_types = jctor.getExceptionTypes()
        self.assertIsInstance(exception_types, tuple)
        self.assertEqual(exception_types, ())

        is_vrargs = jctor.isVarArgs()
        self.assertIs(type(is_vrargs), bool)
        self.assertFalse(is_vrargs)

        signature = jctor.getSignature()
        self.assertIsInstance(signature, str)
        self.assertEqual(signature, ctor_signature)

        jargs = self.jvm.JArguments(3)
        jarray = self.jvm.JArray.newCharArray(8)
        jarray.setChar(0, 'T')
        jarray.setChar(1, 'h')
        jarray.setChar(2, 'e')
        jarray.setChar(3, 'A')
        jarray.setChar(4, 'r')
        jarray.setChar(5, 'r')
        jarray.setChar(6, 'a')
        jarray.setChar(7, 'y')
        jargs.setArray(0, jarray)
        jargs.setInt(1, 2)
        jargs.setInt(2, 4)
        jobject = jctor.newInstance(jargs)
        self.assertIsInstance(jobject, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobject)
        self.assertEqual(jobject.getClass().getName(), jclass_name)
        self.assertEqual(jobject.toString(), u"eArr")

    def test_JMethod(self):

        jclass_name = "java.lang.String"

        jclass = self.jvm.JClass.forName(jclass_name)
        self._check_jclass(jclass,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           is_array=False)

        methods = jclass.getDeclaredMethods()
        self.assertIsInstance(methods, tuple)
        for jmethod in methods:
            self.assertIsInstance(jmethod, self.jvm.JMethod)
        self.assertGreaterEqual(len(methods), 1)

        jmethod_name = u"getBytes"
        jmethod_signature = u"(Ljava/lang/String;)[B"
        jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        # throws UnsupportedEncodingException

        # from JMember

        decl_class = jmethod.getDeclaringClass()
        self._check_jclass(decl_class,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           is_array=False)

        modifiers = jmethod.getModifiersSet()
        self.assertIsInstance(modifiers, frozenset)
        for item in modifiers:
            self.assertIsInstance(item, int)

        raw_modifiers = jmethod.getModifiers()
        self.assertIsInstance(raw_modifiers, int)

        name = jmethod.getName()
        self.assertIsInstance(name, str)
        self.assertEqual(name, jmethod_name)

        # from JMethod

        return_type = jmethod.getReturnType()
        self.assertIsInstance(return_type, self.jvm.JClass)

        parameter_types = jmethod.getParameterTypes()
        self.assertIsInstance(parameter_types, tuple)
        for item in parameter_types:
            self.assertIsInstance(item, self.jvm.JClass)

        exception_types = jmethod.getExceptionTypes()
        self.assertIsInstance(exception_types, tuple)
        for item in exception_types:
            self.assertIsInstance(item, self.jvm.JClass)

        is_vrargs = jmethod.isVarArgs()
        self.assertIs(type(is_vrargs), bool)
        self.assertFalse(is_vrargs)

        signature = jmethod.getSignature()
        self.assertIsInstance(signature, str)
        self.assertEqual(signature, jmethod_signature)

        jmethod_name = u"codePointCount"
        jmethod_signature = u"(II)I"
        jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)

        # from JMember

        decl_class = jmethod.getDeclaringClass()
        self._check_jclass(decl_class,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           is_array=False)

        modifiers = jmethod.getModifiersSet()
        self.assertIsInstance(modifiers, frozenset)
        for item in modifiers:
            self.assertIsInstance(item, int)

        raw_modifiers = jmethod.getModifiers()
        self.assertIsInstance(raw_modifiers, int)

        name = jmethod.getName()
        self.assertIsInstance(name, str)
        self.assertEqual(name, jmethod_name)

        # from JMethod

        return_type = jmethod.getReturnType()
        self.assertIsInstance(return_type, self.jvm.JClass)

        parameter_types = jmethod.getParameterTypes()
        self.assertIsInstance(parameter_types, tuple)
        for item in parameter_types:
            self.assertIsInstance(item, self.jvm.JClass)

        exception_types = jmethod.getExceptionTypes()
        self.assertIsInstance(exception_types, tuple)
        self.assertEqual(exception_types, ())

        is_vrargs = jmethod.isVarArgs()
        self.assertIs(type(is_vrargs), bool)
        self.assertFalse(is_vrargs)

        signature = jmethod.getSignature()
        self.assertIsInstance(signature, str)
        self.assertEqual(signature, jmethod_signature)

        # Methods call

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #jargs.set???(0, jarray)
        #return_value = jmethod.callStaticVoid(jclass, jargs)
        #self.assertIsNone(return_value)

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callStaticBoolean(jclass, jargs)
        #self.assertIsInstance(return_value, bool)

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callStaticChar(jclass, jargs)
        #self.assertIsInstance(return_value, str)

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callStaticByte(jclass, jargs)
        #self.assertIsInstance(return_value, int)

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callStaticShort(jclass, jargs)
        #self.assertIsInstance(return_value, int)

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callStaticInt(jclass, jargs)
        #self.assertIsInstance(return_value, int)

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callStaticLong(jclass, jargs)
        #self.assertIsInstance(return_value, int)

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callStaticFloat(jclass, jargs)
        #self.assertIsInstance(return_value, float)

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callStaticDouble(jclass, jargs)
        #self.assertIsInstance(return_value, float)

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callStaticString(jclass, jargs)
        #self.assertIsInstance(return_value, (str, NoneType))

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callStaticObject(jclass, jargs)
        #self.assertIsInstance(return_value, (self.jvm.JObject, NoneType))

        ctor_signature = u"([CII)V"
        jctor = self._get_constructor(jclass, ctor_signature)

        jargs = self.jvm.JArguments(3)
        jarray = self.jvm.JArray.newCharArray(8)
        jarray.setChar(0, 'T')
        jarray.setChar(1, 'h')
        jarray.setChar(2, 'e')
        jarray.setChar(3, 'A')
        jarray.setChar(4, 'r')
        jarray.setChar(5, 'r')
        jarray.setChar(6, 'a')
        jarray.setChar(7, 'y')
        jargs.setArray(0, jarray)
        jargs.setInt(1, 2)
        jargs.setInt(2, 4)
        this = jctor.newInstance(jargs)
        self.assertIsInstance(this, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(this)
        self.assertEqual(this.getClass().getName(), jclass_name)
        self.assertEqual(this.toString(), u"eArr")

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callInstanceVoid(this, jargs)
        #self.assertIsNone(return_value)

        jmethod_name = u"isEmpty"
        jmethod_signature = u"()Z"
        jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        return_type = jmethod.getReturnType()
        self.assertEqual(return_type.getName(), "boolean")
        jargs = self.jvm.JArguments(0)
        return_value = jmethod.callInstanceBoolean(this, jargs)
        self.assertIsInstance(return_value, bool)
        self.assertFalse(return_value)

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callInstanceChar(this, jargs)
        #self.assertIsInstance(return_value, str)

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callInstanceByte(this, jargs)
        #self.assertIsInstance(return_value, int)

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callInstanceShort(this, jargs)
        #self.assertIsInstance(return_value, int)

        jmethod_name = u"length"
        jmethod_signature = u"()I"
        jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        return_type = jmethod.getReturnType()
        self.assertEqual(return_type.getName(), "int")
        jargs = self.jvm.JArguments(0)
        return_value = jmethod.callInstanceInt(this, jargs)
        self.assertIsInstance(return_value, int)
        self.assertEqual(return_value, 4)

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callInstanceLong(this, jargs)
        #self.assertIsInstance(return_value, int)

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callInstanceFloat(this, jargs)
        #self.assertIsInstance(return_value, float)

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callInstanceDouble(this, jargs)
        #self.assertIsInstance(return_value, float)

        jmethod_name = u"toUpperCase"
        jmethod_signature = u"()Ljava/lang/String;"
        jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        return_type = jmethod.getReturnType()
        self.assertEqual(return_type.getName(), "java.lang.String")
        jargs = self.jvm.JArguments(0)
        return_value = jmethod.callInstanceString(this, jargs)
        self.assertIsInstance(return_value, (str, NoneType))
        self.assertIsNotNone(return_value)
        self.assertEqual(return_value, u"EARR")

        #jmethod_name = u"???"
        #jmethod_signature = u"???"
        #jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        #return_type = jmethod.getReturnType()
        #self.assertEqual(return_type.getName(), "???")
        jargs = self.jvm.JArguments(0)
        #return_value = jmethod.callInstanceObject(this, jargs)
        #self.assertIsInstance(return_value, (self.jvm.JObject, NoneType))

    def test_JPropertyDescriptor(self):

        jclass_name = "java.lang.Throwable"

        jclass = self.jvm.JClass.forName(jclass_name)
        self._check_jclass(jclass,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           is_array=False)

        descriptors = jclass.getPropertyDescriptors()
        self.assertIsInstance(descriptors, tuple)
        for item in descriptors:
            self.assertIsInstance(item, self.jvm.JPropertyDescriptor)
        self.assertEqual(len(descriptors), 6)
        self.assertListEqual(sorted(item.getName() for item in descriptors),
                             sorted(("class", "cause", "localizedMessage",
                                     "message", "stackTrace", "suppressed")))

        # from JPropertyDescriptor

        prop_name = "localizedMessage"

        prop = next(item for item in descriptors if item.getName() == prop_name)

        hash_value = prop.hashCode()
        self.assertIsInstance(hash_value, int)

        name = prop.getName()
        self.assertIsInstance(name, str)
        self.assertEqual(name, prop_name)

        prop_type = prop.getPropertyType()
        self.assertIsNotNone(prop_type)
        self._check_jclass(prop_type,
                           name="java.lang.String",
                           canonical_name="java.lang.String",
                           simple_name="String",
                           is_array=False)

        read_method = prop.getReadMethod()
        self.assertIsInstance(read_method, (self.jvm.JMethod, NoneType))
        self.assertIsNotNone(read_method)
        self.assertEqual(read_method.getName(), "get" + prop_name[0].upper() + prop_name[1:])

        write_method = prop.getWriteMethod()
        self.assertIsInstance(write_method, (self.jvm.JMethod, NoneType))
        self.assertIsNone(write_method)

        prop_name = "stackTrace"

        prop = next(item for item in descriptors if item.getName() == prop_name)

        hash_value = prop.hashCode()
        self.assertIsInstance(hash_value, int)

        name = prop.getName()
        self.assertIsInstance(name, str)
        self.assertEqual(name, prop_name)

        prop_type = prop.getPropertyType()
        self.assertIsNotNone(prop_type)
        self._check_jclass(prop_type,
                           name="[Ljava.lang.StackTraceElement;",
                           canonical_name="java.lang.StackTraceElement[]",
                           simple_name="StackTraceElement[]",
                           is_array=True)

        read_method = prop.getReadMethod()
        self.assertIsInstance(read_method, (self.jvm.JMethod, NoneType))
        self.assertIsNotNone(read_method)
        self.assertEqual(read_method.getName(), "get" + prop_name[0].upper() + prop_name[1:])

        write_method = prop.getWriteMethod()
        self.assertIsInstance(write_method, (self.jvm.JMethod, NoneType))
        self.assertIsNotNone(write_method)
        self.assertEqual(write_method.getName(), "set" + prop_name[0].upper() + prop_name[1:])

    def test_JObject(self):

        # from JObjectBase

        from jvm.jvm import JVMException
        with self.assertRaises(JVMException):
            jobj = self.jvm.JObject(None, 0, own=False)
        del JVMException

        jobj = self.jvm.JObject.newString(u"ABCDEF")
        self.assertIsInstance(jobj, self.jvm.JObject)

        handle = jobj.handle
        self.assertIs(handle, jobj._jobj)

        jobj2 = self.jvm.JObject.fromObject(jobj)
        jobj3 = self.jvm.JObject.newInteger(1234)
        self.assertIsInstance(jobj2, self.jvm.JObject)
        self.assertIsInstance(jobj2, self.jvm.JObject)
        self.assertIsInstance(jobj3, self.jvm.JObject)
        self.assertEqual(jobj,     jobj)
        self.assertEqual(jobj,     jobj2)
        self.assertNotEqual(jobj,  jobj3)
        self.assertNotEqual(jobj2, jobj3)
        self.assertNotEqual(jobj,  None)
        self.assertNotEqual(jobj,  111)
        self.assertNotEqual(jobj,  "xxx")

        jclass = jobj.getClass()
        self.assertIsInstance(jclass, self.jvm.JClass)

        hash_value = hash(jobj)
        self.assertEqual(hash_value, jobj.hashCode())

        str_value = str(jobj)
        self.assertIsInstance(str_value, str)
        self.assertEqual(str_value, jobj.toString())

        hash_value = jobj.hashCode()
        self.assertIsInstance(hash_value, int)

        str_value = jobj.toString()
        self.assertIsInstance(str_value, (str, NoneType))
        self.assertIsNotNone(str_value)

        is_equals = jobj.equals(jobj)
        self.assertIsInstance(is_equals, bool)
        self.assertTrue(is_equals)
        jobj2 = self.jvm.JObject.fromObject(jobj)
        is_equals = jobj.equals(jobj2)
        self.assertIsInstance(is_equals, bool)
        self.assertTrue(is_equals)
        jobj2 = self.jvm.JObject.newString(u"ABCDEF")
        is_equals = jobj.equals(jobj2)
        self.assertIsInstance(is_equals, bool)
        self.assertTrue(is_equals)
        jobj2 = self.jvm.JObject.newInteger(1234)
        is_equals = jobj.equals(jobj2)
        self.assertIsInstance(is_equals, bool)
        self.assertFalse(is_equals)
        is_equals = jobj.equals(None)
        self.assertIsInstance(is_equals, bool)
        self.assertFalse(is_equals)
        is_equals = jobj.equals(111)
        self.assertIsInstance(is_equals, bool)
        self.assertFalse(is_equals)
        is_equals = jobj.equals("xxx")
        self.assertIsInstance(is_equals, bool)
        self.assertFalse(is_equals)

        # from JObject

        #jobj: Optional['JObjectBase'], ->Optional['JObject'] 
        #= self.jvm.JObject.fromObject(cls, jobj):
        #
        #    with cls.jvm as (jvm, jenv):
        #        return cls.jvm.JObject(jenv, jobj.handle) if jobj is not None else None

        #val: bool
        jobj = self.jvm.JObject.newBoolean(True)
        self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobj)
        jobj = self.jvm.JObject.newBoolean(False)
        self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobj)

        #val: str
        jobj = self.jvm.JObject.newCharacter(u"A")
        self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobj)

        #val: int
        jobj = self.jvm.JObject.newByte(66)
        self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobj)

        #val: int
        jobj = self.jvm.JObject.newShort(123)
        self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobj)

        #val: int
        jobj = self.jvm.JObject.newInteger(1234)
        self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobj)

        #val: Union[int, long]
        jobj = self.jvm.JObject.newLong(12345)
        self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobj)
        jobj = self.jvm.JObject.newLong(1234567)
        self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobj)

        #val: float
        jobj = self.jvm.JObject.newFloat(123.45)
        self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobj)

        #val: float
        jobj = self.jvm.JObject.newDouble(12345.67)
        self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobj)

        #val: str
        jobj = self.jvm.JObject.newString("STRING")
        self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobj)
        jobj = self.jvm.JObject.newString(u"STRING")
        self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobj)

        #val: Union[bytes, bytearray, memoryview, memview]
        jobj = self.jvm.JObject.newDirectByteBuffer(b"abcdefgh")
        self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobj)
        #jobj = self.jvm.JObject.newDirectByteBuffer(bytearray(b"abcdefgh"))
        #self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        #self.assertIsNotNone(jobj)
        jobj = self.jvm.JObject.newDirectByteBuffer(memoryview(b"abcdefgh"))
        self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobj)
        from jvm.lib import memoryview as memview
        jobj = self.jvm.JObject.newDirectByteBuffer(memview(b"abcdefgh"))
        del memview
        self.assertIsInstance(jobj, (self.jvm.JObject, NoneType))
        self.assertIsNotNone(jobj)

        jclass = jobj.asClass(own=True)
        self.assertIsInstance(jclass, self.jvm.JClass)
        jclass = jobj.asClass(own=False)
        self.assertIsInstance(jclass, self.jvm.JClass)
        jclass = jobj.asClass()
        self.assertIsInstance(jclass, self.jvm.JClass)

        #javaType: Optional[EJavaType], own: bool
        jarr = jobj.asArray(javaType=None, own=True)
        self.assertIsInstance(jarr, self.jvm.JArray)
        jarr = jobj.asArray(javaType=None, own=False)
        self.assertIsInstance(jarr, self.jvm.JArray)
        jarr = jobj.asArray(javaType=None)
        self.assertIsInstance(jarr, self.jvm.JArray)
        jarr = jobj.asArray()
        self.assertIsInstance(jarr, self.jvm.JArray)

        jobj = self.jvm.JObject.newBoolean(True)
        value = jobj.booleanValue()
        self.assertIsInstance(value, bool)

        jobj = self.jvm.JObject.newCharacter(u"A")
        value = jobj.charValue()
        self.assertIsInstance(value, str)
        self.assertEqual(len(value), 1)
        self.assertEqual(value, u"A")

        jobj = self.jvm.JObject.newByte(66)
        value = jobj.byteValue()
        self.assertIsInstance(value, int)
        self.assertEqual(value, 66)

        jobj = self.jvm.JObject.newShort(123)
        value = jobj.shortValue()
        self.assertIsInstance(value, int)
        self.assertEqual(value, 123)

        jobj = self.jvm.JObject.newInteger(1234)
        value = jobj.intValue()
        self.assertIsInstance(value, int)
        self.assertEqual(value, 1234)

        jobj = self.jvm.JObject.newLong(1234567)
        value = jobj.longValue()
        self.assertIsInstance(value, int)
        self.assertEqual(value, 1234567)

        jobj = self.jvm.JObject.newFloat(123.45)
        value = jobj.floatValue()
        self.assertIsInstance(value, float)
        self.assertAlmostEqual(value, 123.45, 5)

        jobj = self.jvm.JObject.newDouble(12345.67)
        value = jobj.doubleValue()
        self.assertIsInstance(value, float)
        self.assertAlmostEqual(value, 12345.67, 7)

        jobj = self.jvm.JObject.newString(u"STRING")
        value = jobj.stringValue()
        self.assertIsInstance(value, str)
        self.assertEqual(value, u"STRING")
        # return jstr if jstr is not None else u"null" #!!! v1.x

        values = self.jvm.JObject.minmaxByteValue()
        self.assertIsInstance(values, tuple)
        self.assertEqual(len(values), 2)
        min_val, max_val = values
        self.assertIsInstance(min_val, int)
        self.assertIsInstance(max_val, int)

        values = self.jvm.JObject.minmaxShortValue()
        self.assertIsInstance(values, tuple)
        self.assertEqual(len(values), 2)
        min_val, max_val = values
        self.assertIsInstance(min_val, int)
        self.assertIsInstance(max_val, int)

        values = self.jvm.JObject.minmaxIntValue()
        self.assertIsInstance(values, tuple)
        self.assertEqual(len(values), 2)
        min_val, max_val = values
        self.assertIsInstance(min_val, int)
        self.assertIsInstance(max_val, int)

        values = self.jvm.JObject.minmaxLongValue()
        self.assertIsInstance(values, tuple)
        self.assertEqual(len(values), 2)
        min_val, max_val = values
        self.assertIsInstance(min_val, int)
        self.assertIsInstance(max_val, int)

        values = self.jvm.JObject.minmaxFloatValue()
        self.assertIsInstance(values, tuple)
        self.assertEqual(len(values), 2)
        min_val, max_val = values
        self.assertIsInstance(min_val, float)
        self.assertIsInstance(max_val, float)

        values = self.jvm.JObject.minmaxDoubleValue()
        self.assertIsInstance(values, tuple)
        self.assertEqual(len(values), 2)
        min_val, max_val = values
        self.assertIsInstance(min_val, float)
        self.assertIsInstance(max_val, float)

    def test_JArray(self):
        pass  # TODO

    def test_JAnnotation(self):

        from jvm.jvm import JVMException
        with self.assertRaises(JVMException):
            jobj = self.jvm.JAnnotation(None, 0, own=False)
        del JVMException

        jclass_name = "java.security.Signer"

        jclass = self.jvm.JClass.forName(jclass_name)
        self._check_jclass(jclass,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           is_array=False)

        annotations = jclass.getDeclaredAnnotations()
        self.assertIsInstance(annotations, tuple)
        self.assertNotEqual(annotations, ())
        for jannotation in annotations:
            self.assertIsInstance(jannotation, self.jvm.JAnnotation)

        annotations = jclass.getAnnotations()
        self.assertIsInstance(annotations, tuple)
        self.assertNotEqual(annotations, ())
        for jannotation in annotations:
            self.assertIsInstance(jannotation, self.jvm.JAnnotation)

        annotations = jclass.getDeclaredAnnotations() + jclass.getAnnotations()
        for jannotation in annotations:

            hash_value = hash(jannotation)
            self.assertEqual(hash_value, jannotation.hashCode())

            str_value = str(jannotation)
            self.assertIsInstance(str_value, str)
            self.assertEqual(str_value, jannotation.toString())

            hash_value = jannotation.hashCode()
            self.assertIsInstance(hash_value, int)

            str_value = jannotation.toString()
            self.assertIsInstance(str_value, (str, NoneType))
            self.assertIsNotNone(str_value)

            is_equals = jannotation.equals(jannotation)
            self.assertIsInstance(is_equals, bool)
            self.assertTrue(is_equals)
            #jobj2 = self.jvm.JObject.fromObject(jobj)
            #is_equals = jobj.equals(jobj2)
            #self.assertIsInstance(is_equals, bool)
            #self.assertTrue(is_equals)
            jobj2 = self.jvm.JObject.newString(u"ABCDEF")
            is_equals = jannotation.equals(jobj2)
            self.assertIsInstance(is_equals, bool)
            self.assertFalse(is_equals)
            jobj2 = self.jvm.JObject.newInteger(1234)
            is_equals = jannotation.equals(jobj2)
            self.assertIsInstance(is_equals, bool)
            self.assertFalse(is_equals)
            is_equals = jannotation.equals(None)
            self.assertIsInstance(is_equals, bool)
            self.assertFalse(is_equals)
            is_equals = jannotation.equals(111)
            self.assertIsInstance(is_equals, bool)
            self.assertFalse(is_equals)
            is_equals = jannotation.equals("xxx")
            self.assertIsInstance(is_equals, bool)
            self.assertFalse(is_equals)

            jannotation_type = jannotation.annotationType()
            self.assertIsInstance(jannotation_type, self.jvm.JClass)
            self.assertEqual(jannotation_type.toString(),
                             "interface java.lang.Deprecated")

    def test_JMonitor(self):
        pass  # TODO

    def test_JProxy(self):
        pass  # TODO

    def test_JThread(self):

        thread = self.jvm.JThread.currentThread()
        self.assertIsInstance(thread, self.jvm.JThread)

        id = thread.getId()
        self.assertIsInstance(id, int)

        name = thread.getName()
        self.assertIsInstance(name, str)

        cloader = thread.getContextClassLoader()
        self.assertIsInstance(cloader, (self.jvm.JClassLoader, NoneType))

        #jcloader: Optional[JClassLoader]
        # thread.setContextClassLoader(jcloader)

        is_daemon = thread.isDaemon()
        self.assertIs(type(is_daemon), bool)

        is_alive = thread.isAlive()
        self.assertIs(type(is_alive), bool)

        is_interrupted = thread.isInterrupted()
        self.assertIs(type(is_interrupted), bool)

        # thread.start()

        # thread.join()

        # thread.interrupt()

        stack_trace = thread.getStackTrace()
        self.assertIsInstance(stack_trace, tuple)
        for item in stack_trace:
            self.assertIsInstance(item, self.jvm.JObject)

    def test_JReferenceQueue(self):

        jclass_name = "org.jt.ref.TestReferenceQueue"

        jclass = self.jvm.JClass.forName(jclass_name)
        self._check_jclass(jclass,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           is_array=False)

        py_object1 = object()
        py_object2 = object()
        py_object3 = object()

        jmethod_name = u"testReferenceQueue"
        jmethod_signature = u"([I)V"
        jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        return_type = jmethod.getReturnType()
        self.assertEqual(return_type.getName(), "void")
        jargs = self.jvm.JArguments(1)
        jarray = self.jvm.JArray.newIntArray(3)
        jarray.setInt(0, id(py_object1))
        jarray.setInt(1, id(py_object2))
        jarray.setInt(2, id(py_object3))
        jargs.setArray(0, jarray)
        return_value = jmethod.callStaticVoid(jclass, jargs)
        self.assertIsNone(return_value)

    def test_JException(self):
        pass  # TODO

    def test_JString(self):

        jclass_name = "org.jt.jvm.test.StringTest"

        jclass = self.jvm.JClass.forName(jclass_name)
        self._check_jclass(jclass,
                           name=jclass_name,
                           canonical_name=jclass_name,
                           simple_name=jclass_name.rpartition(".")[-1],
                           is_array=False)

        jfield_name = u"fieldStaticString"
        jfield = jclass.getDeclaredField(jfield_name)
        field_type = jfield.getType()
        self.assertEqual(field_type.getName(), "java.lang.String")

        jmethod_name = u"methodStaticString"
        jmethod_signature = u"()Ljava/lang/String;"
        jmethod = self._get_method(jclass, jmethod_name, jmethod_signature)
        return_type = jmethod.getReturnType()
        self.assertEqual(return_type.getName(), "java.lang.String")
        jargs = self.jvm.JArguments(0)
        return_value = jmethod.callStaticString(jclass, jargs)
        self.assertIsInstance(return_value, str)
        self.assertEqual(return_value, u"hello \U0001F30E!")

        #Test = jclass # autoclass('org.jnius.BasicsTest')
        #test = Test()
        #self.assertEquals(Test.fieldStaticString,    u"hello \U0001F30E!")
        #self.assertEquals(test.fieldString,          u"hello \U0001F30E!")
        #self.assertEquals(Test.methodStaticString(), u"hello \U0001F30E!")
        #self.assertEquals(test.methodString(),       u"hello \U0001F30E!")

        # Unicode charset:
        #
        # u"\u0000" - u"\uD7FF"
        # u"\uE000" - u"\uFFFF"
        # u"\U00010000" - u"\U0010FFFF"

        s = u""
        for x in range(0x0000, 0xD7FF + 1):
            s += chr(x)
        for x in range(0xE000, 0xFFFF + 1):
            s += chr(x)

        s = u""
        for x in range(0x00010000, min(0x0010FFFF, sys.maxunicode) + 1):
            s += chr(x)

        pass  # TODO

    @unittest.skip("jvm: crash!!!")
    def test_PythonInterpreter(self):

        jclass = self.jvm.JClass.forName("org.python.util.PythonInterpreter")
        jctor  = self._get_constructor(jclass, u"()V")

        jargs = self.jvm.JArguments(0)
        python = jctor.newInstance(jargs)
        #!!!print("@@@", dir(python))

    def _get_constructor(self, jclass, signature):

        constructors = jclass.getConstructors()
        self.assertIsInstance(constructors, tuple)
        for jctor in constructors:
            self.assertIsInstance(jctor, self.jvm.JConstructor)
        return next(jctor for jctor in constructors
                    if jctor.getSignature() == signature)

    def _get_method(self, jclass, name, signature, _print=False):

        methods = jclass.getMethods()
        self.assertIsInstance(methods, tuple)
        for jmethod in methods:
            self.assertIsInstance(jmethod, self.jvm.JMethod)
            if _print: print(jmethod.getName(), jmethod.getSignature())
        return next(jmethod for jmethod in methods
                    if jmethod.getName() == name and
                       jmethod.getSignature() == signature)

    def _check_jclass(self, jclass,
                      name=None,
                      canonical_name=None,
                      simple_name=None,
                      signature=None,
                      is_interface=None,
                      is_enum=None,
                      is_primitive=None,
                      is_annotation=None,
                      is_anonymous_class=None,
                      is_local_class=None,
                      is_member_class=None,
                      is_array=None):

        self.assertIsInstance(jclass, self.jvm.JClass)

        # from JObjectBase

        handle = jclass.handle
        self.assertIs(handle, jclass._jobj)

        hash_value = jclass.hashCode()
        self.assertIsInstance(hash_value, int)

        #jcls = jclass.getClass()
        #self.assertIsInstance(jcls, self.jvm.JClass)

        str_value = jclass.toString()
        self.assertIsInstance(str_value, (str, NoneType))
        self.assertIsNotNone(str_value)

        # from JClass

        jclass_name = jclass.getName()
        self.assertIsInstance(jclass_name, str)
        if name is not None:
            self.assertEqual(jclass_name, name)

        class_canonical_name = jclass.getCanonicalName()
        self.assertIsInstance(class_canonical_name, str)
        if canonical_name is not None:
            self.assertEqual(class_canonical_name, canonical_name)

        class_simple_name = jclass.getSimpleName()
        self.assertIsInstance(class_simple_name, str)
        if simple_name is not None:
            self.assertEqual(class_simple_name, simple_name)

        class_signature = jclass.getSignature()
        self.assertIsInstance(class_signature, str)
        if signature is not None:
            self.assertEqual(class_signature, signature)

        class_is_interface = jclass.isInterface()
        self.assertIs(type(class_is_interface), bool)
        if is_interface is not None:
            self.assertIs(class_is_interface, is_interface)

        class_is_enum = jclass.isEnum()
        self.assertIs(type(class_is_enum), bool)
        if is_enum is not None:
            self.assertIs(class_is_enum, is_enum)

        class_is_primitive = jclass.isPrimitive()
        self.assertIs(type(class_is_primitive), bool)
        if is_primitive is not None:
            self.assertIs(class_is_primitive, is_primitive)

        class_is_annotation = jclass.isAnnotation()
        self.assertIs(type(class_is_annotation), bool)
        if is_annotation is not None:
            self.assertIs(class_is_annotation, is_annotation)

        class_is_anonymous_class = jclass.isAnonymousClass()
        self.assertIs(type(class_is_anonymous_class), bool)
        if is_anonymous_class is not None:
            self.assertIs(class_is_anonymous_class, is_anonymous_class)

        class_is_local_class = jclass.isLocalClass()
        self.assertIs(type(class_is_local_class), bool)
        if is_local_class is not None:
            self.assertIs(class_is_local_class, is_local_class)

        class_is_member_class = jclass.isMemberClass()
        self.assertIs(type(class_is_member_class), bool)
        if is_member_class is not None:
            self.assertIs(class_is_member_class, is_member_class)

        class_is_array = jclass.isArray()
        self.assertIs(type(class_is_array), bool)
        if is_array is not None:
            self.assertIs(class_is_array, is_array)

    def _check_jpackage(self, jpackage,
                        name=None,
                        is_sealed=None):

        self.assertIsInstance(jpackage, (self.jvm.JPackage, NoneType))
        self.assertIsNotNone(jpackage)

        package_name = jpackage.getName()
        self.assertIsInstance(package_name, str)
        if name is not None:
            self.assertEqual(package_name, name)

        spec_title = jpackage.getSpecificationTitle()
        self.assertIsInstance(spec_title, (str, NoneType))

        spec_version = jpackage.getSpecificationVersion()
        self.assertIsInstance(spec_version, (str, NoneType))

        spec_vendor = jpackage.getSpecificationVendor()
        self.assertIsInstance(spec_vendor, (str, NoneType))

        spec_title = jpackage.getImplementationTitle()
        self.assertIsInstance(spec_title, (str, NoneType))

        impl_version = jpackage.getImplementationVersion()
        self.assertIsInstance(impl_version, (str, NoneType))

        spec_vendor = jpackage.getImplementationVendor()
        self.assertIsInstance(spec_vendor, (str, NoneType))

        package_is_sealed = jpackage.isSealed()
        self.assertIs(type(package_is_sealed), bool)
        if is_sealed is not None:
            self.assertIs(package_is_sealed, is_sealed)
