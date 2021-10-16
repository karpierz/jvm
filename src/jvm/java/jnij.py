# Copyright (c) 2004-2022 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import jni
from ..lib import obj

from ..jframe import JFrame


class jnij(obj):

    def dispose(self, jenv: jni.JNIEnv):
        if jenv is not None and hasattr(self, "Class"):
            jenv.DeleteGlobalRef(self.Class)

class java_array(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 8):
            self.BooleanArray1Class = jni.cast(jenv.NewGlobalRef(jenv.FindClass(b"[Z")), jni.jclass)
            self.CharArray1Class    = jni.cast(jenv.NewGlobalRef(jenv.FindClass(b"[C")), jni.jclass)
            self.ByteArray1Class    = jni.cast(jenv.NewGlobalRef(jenv.FindClass(b"[B")), jni.jclass)
            self.ShortArray1Class   = jni.cast(jenv.NewGlobalRef(jenv.FindClass(b"[S")), jni.jclass)
            self.IntArray1Class     = jni.cast(jenv.NewGlobalRef(jenv.FindClass(b"[I")), jni.jclass)
            self.LongArray1Class    = jni.cast(jenv.NewGlobalRef(jenv.FindClass(b"[J")), jni.jclass)
            self.FloatArray1Class   = jni.cast(jenv.NewGlobalRef(jenv.FindClass(b"[F")), jni.jclass)
            self.DoubleArray1Class  = jni.cast(jenv.NewGlobalRef(jenv.FindClass(b"[D")), jni.jclass)

    def dispose(self, jenv: jni.JNIEnv):
        if jenv is not None:
            jenv.DeleteGlobalRef(self.BooleanArray1Class)
            jenv.DeleteGlobalRef(self.CharArray1Class)
            jenv.DeleteGlobalRef(self.ByteArray1Class)
            jenv.DeleteGlobalRef(self.ShortArray1Class)
            jenv.DeleteGlobalRef(self.IntArray1Class)
            jenv.DeleteGlobalRef(self.LongArray1Class)
            jenv.DeleteGlobalRef(self.FloatArray1Class)
            jenv.DeleteGlobalRef(self.DoubleArray1Class)

class java_lang(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 14):
            jcls = jenv.FindClass(b"java/lang/Exception")
            self.Exception = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/lang/RuntimeException")
            self.RuntimeException = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/lang/ClassNotFoundException")
            self.ClassNotFoundException = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/lang/IndexOutOfBoundsException")
            self.IndexOutOfBoundsException = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/lang/ClassCastException")
            self.ClassCastException = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/lang/IllegalArgumentException")
            self.IllegalArgumentException = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/lang/ArithmeticException")
            self.ArithmeticException = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/lang/IllegalStateException")
            self.IllegalStateException = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/lang/Error")
            self.Error = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/lang/OutOfMemoryError")
            self.OutOfMemoryError = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/lang/NoClassDefFoundError")
            self.NoClassDefFoundError = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/lang/NoSuchMethodError")
            self.NoSuchMethodError = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/lang/UnsupportedOperationException")
            self.UnsupportedOperationException = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/lang/AssertionError")
            self.AssertionError = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)

    def dispose(self, jenv: jni.JNIEnv):
        if jenv is not None:
            jenv.DeleteGlobalRef(self.Exception)
            jenv.DeleteGlobalRef(self.RuntimeException)
            jenv.DeleteGlobalRef(self.ClassNotFoundException)
            jenv.DeleteGlobalRef(self.IndexOutOfBoundsException)
            jenv.DeleteGlobalRef(self.ClassCastException)
            jenv.DeleteGlobalRef(self.IllegalArgumentException)
            jenv.DeleteGlobalRef(self.ArithmeticException)
            jenv.DeleteGlobalRef(self.IllegalStateException)
            jenv.DeleteGlobalRef(self.Error)
            jenv.DeleteGlobalRef(self.OutOfMemoryError)
            jenv.DeleteGlobalRef(self.NoClassDefFoundError)
            jenv.DeleteGlobalRef(self.NoSuchMethodError)
            jenv.DeleteGlobalRef(self.UnsupportedOperationException)
            jenv.DeleteGlobalRef(self.AssertionError)

class java_io(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 4):
            jcls = jenv.FindClass(b"java/io/IOException")
            self.IOException = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/io/EOFException")
            self.EOFException = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/io/IOError")
            self.IOError = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/io/FileNotFoundException")
            self.FileNotFoundException = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)

    def dispose(self, jenv: jni.JNIEnv):
        if jenv is not None:
            jenv.DeleteGlobalRef(self.IOException)
            jenv.DeleteGlobalRef(self.EOFException)
            jenv.DeleteGlobalRef(self.IOError)
            jenv.DeleteGlobalRef(self.FileNotFoundException)

class java_nio(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 7):
            jcls = jenv.FindClass(b"java/nio/ByteBuffer")
            self.ByteBufferClass  = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.ByteBuffer_order = jenv.GetMethodID(jcls, b"order", b"()Ljava/nio/ByteOrder;")
            jcls = jenv.FindClass(b"java/nio/ShortBuffer")
            self.ShortBufferClass  = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.ShortBuffer_order = jenv.GetMethodID(jcls, b"order", b"()Ljava/nio/ByteOrder;")
            jcls = jenv.FindClass(b"java/nio/IntBuffer")
            self.IntBufferClass  = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.IntBuffer_order = jenv.GetMethodID(jcls, b"order", b"()Ljava/nio/ByteOrder;")
            jcls = jenv.FindClass(b"java/nio/LongBuffer")
            self.LongBufferClass  = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.LongBuffer_order = jenv.GetMethodID(jcls, b"order", b"()Ljava/nio/ByteOrder;")
            jcls = jenv.FindClass(b"java/nio/FloatBuffer")
            self.FloatBufferClass  = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.FloatBuffer_order = jenv.GetMethodID(jcls, b"order", b"()Ljava/nio/ByteOrder;")
            jcls = jenv.FindClass(b"java/nio/DoubleBuffer")
            self.DoubleBufferClass  = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.DoubleBuffer_order = jenv.GetMethodID(jcls, b"order", b"()Ljava/nio/ByteOrder;")
            jcls = jenv.FindClass(b"java/nio/ByteOrder");
            self.ByteOrderClass = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.ByteOrder_nativeOrder = jenv.GetStaticMethodID(jcls, b"nativeOrder", b"()Ljava/nio/ByteOrder;")

    def dispose(self, jenv: jni.JNIEnv):
        if jenv is not None:
            jenv.DeleteGlobalRef(self.ByteBufferClass)
            jenv.DeleteGlobalRef(self.ShortBufferClass)
            jenv.DeleteGlobalRef(self.IntBufferClass)
            jenv.DeleteGlobalRef(self.LongBufferClass)
            jenv.DeleteGlobalRef(self.FloatBufferClass)
            jenv.DeleteGlobalRef(self.DoubleBufferClass)
            jenv.DeleteGlobalRef(self.ByteOrderClass)

class java_util(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 9):
            jcls = jenv.FindClass(b"java/util/List")
            self.ListClass    = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.List_addAll  = jenv.GetMethodID(jcls, b"addAll",  b"(Ljava/util/Collection;)Z")
            self.List_add     = jenv.GetMethodID(jcls, b"add",     b"(Ljava/lang/Object;)Z")
            self.List_get     = jenv.GetMethodID(jcls, b"get",     b"(I)Ljava/lang/Object;")
            self.List_set     = jenv.GetMethodID(jcls, b"set",     b"(ILjava/lang/Object;)Ljava/lang/Object;")
            self.List_remove  = jenv.GetMethodID(jcls, b"remove",  b"(I)Ljava/lang/Object;")
            self.List_clear   = jenv.GetMethodID(jcls, b"clear",   b"()V")
            self.List_subList = jenv.GetMethodID(jcls, b"subList", b"(II)Ljava/util/List;")
            jcls = jenv.FindClass(b"java/util/Set")
            self.SetClass = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            jcls = jenv.FindClass(b"java/util/Map")
            self.MapClass        = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.Map_size        = jenv.GetMethodID(jcls, b"size",        b"()I")
            self.Map_containsKey = jenv.GetMethodID(jcls, b"containsKey", b"(Ljava/lang/Object;)Z")
            self.Map_get         = jenv.GetMethodID(jcls, b"get",         b"(Ljava/lang/Object;)Ljava/lang/Object;")
            self.Map_put         = jenv.GetMethodID(jcls, b"put",         b"(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;")
            self.Map_remove      = jenv.GetMethodID(jcls, b"remove",      b"(Ljava/lang/Object;)Ljava/lang/Object;")
            self.Map_clear       = jenv.GetMethodID(jcls, b"clear",       b"()V")
            self.Map_keySet      = jenv.GetMethodID(jcls, b"keySet",      b"()Ljava/util/Set;")
            self.Map_entrySet    = jenv.GetMethodID(jcls, b"entrySet",    b"()Ljava/util/Set;")
            jcls = jenv.FindClass(b"java/util/Map$Entry")
            self.MapEntryClass     = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.MapEntry_getKey   = jenv.GetMethodID(jcls, b"getKey",   b"()Ljava/lang/Object;")
            self.MapEntry_getValue = jenv.GetMethodID(jcls, b"getValue", b"()Ljava/lang/Object;")
            jcls = jenv.FindClass(b"java/util/Iterator")
            self.IteratorClass    = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.Iterator_hasNext = jenv.GetMethodID(jcls, b"hasNext", b"()Z")
            self.Iterator_next    = jenv.GetMethodID(jcls, b"next",    b"()Ljava/lang/Object;")
            jcls = jenv.FindClass(b"java/util/Collection")
            self.CollectionClass     = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.Collection_size     = jenv.GetMethodID(jcls, b"size",     b"()I")
            self.Collection_contains = jenv.GetMethodID(jcls, b"contains", b"(Ljava/lang/Object;)Z")
            self.Collection_iterator = jenv.GetMethodID(jcls, b"iterator", b"()Ljava/util/Iterator;")
            jcls = jenv.FindClass(b"java/util/Collections")
            self.CollectionsClass             = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.Collections_unmodifiableList = jenv.GetStaticMethodID(jcls, b"unmodifiableList", b"(Ljava/util/List;)Ljava/util/List;")
            jcls = jenv.FindClass(b"java/util/ArrayList")
            self.ArrayListClass          = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.ArrayListConstructorInt = jenv.GetMethodID(jcls, b"<init>", b"(I)V")
            self.ArrayList_add           = jenv.GetMethodID(jcls, b"add",    b"(Ljava/lang/Object;)Z")
            jcls = jenv.FindClass(b"java/util/HashMap")
            self.HashMapClass          = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.HashMapConstructorInt = jenv.GetMethodID(jcls, b"<init>", b"(I)V")
            self.HashMap_put           = jenv.GetMethodID(jcls, b"put",    b"(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;")

    def dispose(self, jenv: jni.JNIEnv):
        if jenv is not None:
            jenv.DeleteGlobalRef(self.ListClass)
            jenv.DeleteGlobalRef(self.MapEntryClass)
            jenv.DeleteGlobalRef(self.MapClass)
            jenv.DeleteGlobalRef(self.IteratorClass)
            jenv.DeleteGlobalRef(self.CollectionClass)
            jenv.DeleteGlobalRef(self.ArrayListClass)
            jenv.DeleteGlobalRef(self.CollectionsClass)
            jenv.DeleteGlobalRef(self.HashMapClass)

class java_lang_System(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/System")
            self.Class            = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.identityHashCode = jenv.GetStaticMethodID(jcls, b"identityHashCode", b"(Ljava/lang/Object;)I")
            self.getProperty      = jenv.GetStaticMethodID(jcls, b"getProperty",      b"(Ljava/lang/String;)Ljava/lang/String;")
            self.setProperty      = jenv.GetStaticMethodID(jcls, b"setProperty",      b"(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;")
            self.clearProperty    = jenv.GetStaticMethodID(jcls, b"clearProperty",    b"(Ljava/lang/String;)Ljava/lang/String;")
            self.loadLibrary      = jenv.GetStaticMethodID(jcls, b"loadLibrary",      b"(Ljava/lang/String;)V")
            self.runFinalization  = jenv.GetStaticMethodID(jcls, b"runFinalization",  b"()V")

class java_lang_Thread(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/Thread")
            self.Class                 = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.currentThread         = jenv.GetStaticMethodID(jcls, b"currentThread",   b"()Ljava/lang/Thread;")
            self.getId                 = jenv.GetMethodID(jcls, b"getId",                 b"()J")
            self.getName               = jenv.GetMethodID(jcls, b"getName",               b"()Ljava/lang/String;")
            self.getContextClassLoader = jenv.GetMethodID(jcls, b"getContextClassLoader", b"()Ljava/lang/ClassLoader;")
            self.setContextClassLoader = jenv.GetMethodID(jcls, b"setContextClassLoader", b"(Ljava/lang/ClassLoader;)V")
            self.isDaemon              = jenv.GetMethodID(jcls, b"isDaemon",              b"()Z")
            self.isAlive               = jenv.GetMethodID(jcls, b"isAlive",               b"()Z")
            self.isInterrupted         = jenv.GetMethodID(jcls, b"isInterrupted",         b"()Z")
            self.start                 = jenv.GetMethodID(jcls, b"start",                 b"()V")
            self.join                  = jenv.GetMethodID(jcls, b"join",                  b"()V")
            self.interrupt             = jenv.GetMethodID(jcls, b"interrupt",             b"()V")
            self.getStackTrace         = jenv.GetMethodID(jcls, b"getStackTrace",         b"()[Ljava/lang/StackTraceElement;")

class java_lang_Package(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/Package")
            self.Class                    = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.getPackage               = jenv.GetStaticMethodID(jcls, b"getPackage",         b"(Ljava/lang/String;)Ljava/lang/Package;")
            self.getPackages              = jenv.GetStaticMethodID(jcls, b"getPackages",        b"()[Ljava/lang/Package;")
            self.getName                  = jenv.GetMethodID(jcls, b"getName",                  b"()Ljava/lang/String;")
            self.getSpecificationTitle    = jenv.GetMethodID(jcls, b"getSpecificationTitle",    b"()Ljava/lang/String;")
            self.getSpecificationVersion  = jenv.GetMethodID(jcls, b"getSpecificationVersion",  b"()Ljava/lang/String;")
            self.getSpecificationVendor   = jenv.GetMethodID(jcls, b"getSpecificationVendor",   b"()Ljava/lang/String;")
            self.getImplementationTitle   = jenv.GetMethodID(jcls, b"getImplementationTitle",   b"()Ljava/lang/String;")
            self.getImplementationVersion = jenv.GetMethodID(jcls, b"getImplementationVersion", b"()Ljava/lang/String;")
            self.getImplementationVendor  = jenv.GetMethodID(jcls, b"getImplementationVendor",  b"()Ljava/lang/String;")
            self.isSealed                 = jenv.GetMethodID(jcls, b"isSealed",                 b"()Z")

class java_lang_ClassLoader(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/ClassLoader")
            self.Class                = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.getSystemClassLoader = jenv.GetStaticMethodID(jcls, b"getSystemClassLoader", b"()Ljava/lang/ClassLoader;")
            self.getParent            = jenv.GetMethodID(jcls,       b"getParent",            b"()Ljava/lang/ClassLoader;")
            self.getPackage           = jenv.GetMethodID(jcls,       b"getPackage",           b"(Ljava/lang/String;)Ljava/lang/Package;")
            self.getPackages          = jenv.GetMethodID(jcls,       b"getPackages",          b"()[Ljava/lang/Package;")
            self.findClass            = jenv.GetMethodID(jcls,       b"findClass",            b"(Ljava/lang/String;)Ljava/lang/Class;")
            self.findLoadedClass      = jenv.GetMethodID(jcls,       b"findLoadedClass",      b"(Ljava/lang/String;)Ljava/lang/Class;")
            self.findSystemClass      = jenv.GetMethodID(jcls,       b"findSystemClass",      b"(Ljava/lang/String;)Ljava/lang/Class;")
            self.loadClass            = jenv.GetMethodID(jcls,       b"loadClass",            b"(Ljava/lang/String;)Ljava/lang/Class;")
            self.definePackage        = jenv.GetMethodID(jcls,       b"definePackage",        b"(Ljava/lang/String;"
                                                                                              b"Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;"
                                                                                              b"Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;"
                                                                                              b"Ljava/net/URL;)Ljava/lang/Package;")
            self.defineClass          = jenv.GetMethodID(jcls,       b"defineClass",          b"(Ljava/lang/String;[BII)Ljava/lang/Class;")
            self.getResource          = jenv.GetMethodID(jcls,       b"getResource",          b"(Ljava/lang/String;)Ljava/net/URL;")
            self.getResources         = jenv.GetMethodID(jcls,       b"getResources",         b"(Ljava/lang/String;)Ljava/util/Enumeration;")
            self.getSystemResource    = jenv.GetStaticMethodID(jcls, b"getSystemResource",    b"(Ljava/lang/String;)Ljava/net/URL;")
            self.getSystemResources   = jenv.GetStaticMethodID(jcls, b"getSystemResources",   b"(Ljava/lang/String;)Ljava/util/Enumeration;")
            self.findLibrary          = jenv.GetMethodID(jcls,       b"findLibrary",          b"(Ljava/lang/String;)Ljava/lang/String;")

class java_lang_Class(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/Class")
            self.Class                   = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.forName                 = jenv.GetStaticMethodID(jcls, b"forName",           b"(Ljava/lang/String;ZLjava/lang/ClassLoader;)Ljava/lang/Class;")
            self.asSubclass              = jenv.GetMethodID(jcls, b"asSubclass",              b"(Ljava/lang/Class;)Ljava/lang/Class;")
            self.getClassLoader          = jenv.GetMethodID(jcls, b"getClassLoader",          b"()Ljava/lang/ClassLoader;")
            self.getPackage              = jenv.GetMethodID(jcls, b"getPackage",              b"()Ljava/lang/Package;")
            self.getName                 = jenv.GetMethodID(jcls, b"getName",                 b"()Ljava/lang/String;")
            self.getSimpleName           = jenv.GetMethodID(jcls, b"getSimpleName",           b"()Ljava/lang/String;")
            self.getCanonicalName        = jenv.GetMethodID(jcls, b"getCanonicalName",        b"()Ljava/lang/String;")
            self.getComponentType        = jenv.GetMethodID(jcls, b"getComponentType",        b"()Ljava/lang/Class;")
            self.getModifiers            = jenv.GetMethodID(jcls, b"getModifiers",            b"()I")
            self.getSuperclass           = jenv.GetMethodID(jcls, b"getSuperclass",           b"()Ljava/lang/Class;")
            self.getInterfaces           = jenv.GetMethodID(jcls, b"getInterfaces",           b"()[Ljava/lang/Class;")
            self.getDeclaredClasses      = jenv.GetMethodID(jcls, b"getDeclaredClasses",      b"()[Ljava/lang/Class;")
            self.getDeclaredConstructors = jenv.GetMethodID(jcls, b"getDeclaredConstructors", b"()[Ljava/lang/reflect/Constructor;")
            self.getDeclaredField        = jenv.GetMethodID(jcls, b"getDeclaredField",        b"(Ljava/lang/String;)Ljava/lang/reflect/Field;")
            self.getDeclaredFields       = jenv.GetMethodID(jcls, b"getDeclaredFields",       b"()[Ljava/lang/reflect/Field;")
            self.getDeclaredMethods      = jenv.GetMethodID(jcls, b"getDeclaredMethods",      b"()[Ljava/lang/reflect/Method;")
            self.getClasses              = jenv.GetMethodID(jcls, b"getClasses",              b"()[Ljava/lang/Class;")
            self.getConstructors         = jenv.GetMethodID(jcls, b"getConstructors",         b"()[Ljava/lang/reflect/Constructor;")
            self.getField                = jenv.GetMethodID(jcls, b"getField",                b"(Ljava/lang/String;)Ljava/lang/reflect/Field;")
            self.getFields               = jenv.GetMethodID(jcls, b"getFields",               b"()[Ljava/lang/reflect/Field;")
            self.getMethods              = jenv.GetMethodID(jcls, b"getMethods",              b"()[Ljava/lang/reflect/Method;")
            self.getEnclosingClass       = jenv.GetMethodID(jcls, b"getEnclosingClass",       b"()Ljava/lang/Class;")
            self.getEnclosingConstructor = jenv.GetMethodID(jcls, b"getEnclosingConstructor", b"()Ljava/lang/reflect/Constructor;")
            self.getEnclosingMethod      = jenv.GetMethodID(jcls, b"getEnclosingMethod",      b"()Ljava/lang/reflect/Method;")
            self.isAssignableFrom        = jenv.GetMethodID(jcls, b"isAssignableFrom",        b"(Ljava/lang/Class;)Z")
            self.isInstance              = jenv.GetMethodID(jcls, b"isInstance",              b"(Ljava/lang/Object;)Z")
            self.isAnnotation            = jenv.GetMethodID(jcls, b"isAnnotation",            b"()Z")
            self.isInterface             = jenv.GetMethodID(jcls, b"isInterface",             b"()Z")
            self.isEnum                  = jenv.GetMethodID(jcls, b"isEnum",                  b"()Z")
            self.isArray                 = jenv.GetMethodID(jcls, b"isArray",                 b"()Z")
            self.isAnonymousClass        = jenv.GetMethodID(jcls, b"isAnonymousClass",        b"()Z")
            self.isLocalClass            = jenv.GetMethodID(jcls, b"isLocalClass",            b"()Z")
            self.isMemberClass           = jenv.GetMethodID(jcls, b"isMemberClass",           b"()Z")
            self.isPrimitive             = jenv.GetMethodID(jcls, b"isPrimitive",             b"()Z")
            self.isSynthetic             = jenv.GetMethodID(jcls, b"isSynthetic",             b"()Z")
            self.newInstance             = jenv.GetMethodID(jcls, b"newInstance",             b"()Ljava/lang/Object;")

class java_lang_Throwable(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/Throwable")
            self.Class               = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.getMessage          = jenv.GetMethodID(jcls, b"getMessage",          b"()Ljava/lang/String;")
            self.getLocalizedMessage = jenv.GetMethodID(jcls, b"getLocalizedMessage", b"()Ljava/lang/String;")
            self.getCause            = jenv.GetMethodID(jcls, b"getCause",            b"()Ljava/lang/Throwable;")
            self.getStackTrace       = jenv.GetMethodID(jcls, b"getStackTrace",       b"()[Ljava/lang/StackTraceElement;")
            self.setStackTrace       = jenv.GetMethodID(jcls, b"setStackTrace",       b"([Ljava/lang/StackTraceElement;)V")
            self.printStackTrace     = jenv.GetMethodID(jcls, b"printStackTrace",     b"(Ljava/io/PrintWriter;)V")

class java_lang_StackTraceElement(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/StackTraceElement")
            self.Class       = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.Constructor = jenv.GetMethodID(jcls, b"<init>", b"(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;I)V")

class java_lang_AutoCloseable(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/AutoCloseable")
            self.Class = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.close = jenv.GetMethodID(jcls, b"close", b"()V")

class java_lang_Comparable(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/Comparable")
            self.Class     = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.compareTo = jenv.GetMethodID(jcls, b"compareTo", b"(Ljava/lang/Object;)I")

class java_lang_Iterable(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/Iterable")
            self.Class    = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.iterator = jenv.GetMethodID(jcls, b"iterator", b"()Ljava/util/Iterator;")

class java_beans_Introspector(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/beans/Introspector")
            self.Class       = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.getBeanInfo = jenv.GetStaticMethodID(jcls, b"getBeanInfo", b"(Ljava/lang/Class;)Ljava/beans/BeanInfo;")

class java_beans_BeanInfo(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/beans/BeanInfo")
            self.Class                  = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.getPropertyDescriptors = jenv.GetMethodID(jcls, b"getPropertyDescriptors", b"()[Ljava/beans/PropertyDescriptor;")

class java_beans_PropertyDescriptor(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 2):
            jfcls = jenv.FindClass(b"java/beans/FeatureDescriptor")
            jcls  = jenv.FindClass(b"java/beans/PropertyDescriptor")
            self.Class           = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.hashCode        = jenv.GetMethodID(jcls,  b"hashCode",        b"()I")
            self.toString        = jenv.GetMethodID(jcls,  b"toString",        b"()Ljava/lang/String;")
            self.getName         = jenv.GetMethodID(jfcls, b"getName",         b"()Ljava/lang/String;")
            self.getPropertyType = jenv.GetMethodID(jcls,  b"getPropertyType", b"()Ljava/lang/Class;")
            self.getReadMethod   = jenv.GetMethodID(jcls,  b"getReadMethod",   b"()Ljava/lang/reflect/Method;")
            self.getWriteMethod  = jenv.GetMethodID(jcls,  b"getWriteMethod",  b"()Ljava/lang/reflect/Method;")
            self.setReadMethod   = jenv.GetMethodID(jcls,  b"setReadMethod",   b"(Ljava/lang/reflect/Method;)V")
            self.setWriteMethod  = jenv.GetMethodID(jcls,  b"setWriteMethod",  b"(Ljava/lang/reflect/Method;)V")

class java_lang_annotation_Annotation(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/annotation/Annotation")
            self.Class          = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.annotationType = jenv.GetMethodID(jcls, b"annotationType", b"()Ljava/lang/Class;")
            self.hashCode       = jenv.GetMethodID(jcls, b"hashCode", b"()I")
            self.toString       = jenv.GetMethodID(jcls, b"toString", b"()Ljava/lang/String;")
            self.equals         = jenv.GetMethodID(jcls, b"equals",   b"(Ljava/lang/Object;)Z")

class java_lang_reflect_AnnotatedElement(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/reflect/AnnotatedElement")
            self.Class                  = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.getDeclaredAnnotations = jenv.GetMethodID(jcls, b"getDeclaredAnnotations", b"()[Ljava/lang/annotation/Annotation;")
            self.getAnnotations         = jenv.GetMethodID(jcls, b"getAnnotations",         b"()[Ljava/lang/annotation/Annotation;")
            self.getAnnotation          = jenv.GetMethodID(jcls, b"getAnnotation",          b"(Ljava/lang/Class;)Ljava/lang/annotation/Annotation;")
            self.isAnnotationPresent    = jenv.GetMethodID(jcls, b"isAnnotationPresent",    b"(Ljava/lang/Class;)Z")

class java_lang_reflect_Modifier(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/reflect/Modifier")
            self.Class          = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.PUBLIC         = jenv.GetStaticIntField(jcls, jenv.GetStaticFieldID(jcls, b"PUBLIC",       b"I"))
            self.PROTECTED      = jenv.GetStaticIntField(jcls, jenv.GetStaticFieldID(jcls, b"PROTECTED",    b"I"))
            self.PRIVATE        = jenv.GetStaticIntField(jcls, jenv.GetStaticFieldID(jcls, b"PRIVATE",      b"I"))
            self.FINAL          = jenv.GetStaticIntField(jcls, jenv.GetStaticFieldID(jcls, b"FINAL",        b"I"))
            self.STATIC         = jenv.GetStaticIntField(jcls, jenv.GetStaticFieldID(jcls, b"STATIC",       b"I"))
            self.ABSTRACT       = jenv.GetStaticIntField(jcls, jenv.GetStaticFieldID(jcls, b"ABSTRACT",     b"I"))
            self.INTERFACE      = jenv.GetStaticIntField(jcls, jenv.GetStaticFieldID(jcls, b"INTERFACE",    b"I"))
            self.NATIVE         = jenv.GetStaticIntField(jcls, jenv.GetStaticFieldID(jcls, b"NATIVE",       b"I"))
            self.STRICT         = jenv.GetStaticIntField(jcls, jenv.GetStaticFieldID(jcls, b"STRICT",       b"I"))
            self.SYNCHRONIZED   = jenv.GetStaticIntField(jcls, jenv.GetStaticFieldID(jcls, b"SYNCHRONIZED", b"I"))
            self.TRANSIENT      = jenv.GetStaticIntField(jcls, jenv.GetStaticFieldID(jcls, b"TRANSIENT",    b"I"))
            self.VOLATILE       = jenv.GetStaticIntField(jcls, jenv.GetStaticFieldID(jcls, b"VOLATILE",     b"I"))
            self.isAbstract     = jenv.GetStaticMethodID(jcls, b"isAbstract",     b"(I)Z")
            self.isFinal        = jenv.GetStaticMethodID(jcls, b"isFinal",        b"(I)Z")
            self.isInterface    = jenv.GetStaticMethodID(jcls, b"isInterface",    b"(I)Z")
            self.isNative       = jenv.GetStaticMethodID(jcls, b"isNative",       b"(I)Z")
            self.isPrivate      = jenv.GetStaticMethodID(jcls, b"isPrivate",      b"(I)Z")
            self.isProtected    = jenv.GetStaticMethodID(jcls, b"isProtected",    b"(I)Z")
            self.isPublic       = jenv.GetStaticMethodID(jcls, b"isPublic",       b"(I)Z")
            self.isStatic       = jenv.GetStaticMethodID(jcls, b"isStatic",       b"(I)Z")
            self.isStrict       = jenv.GetStaticMethodID(jcls, b"isStrict",       b"(I)Z")
            self.isSynchronized = jenv.GetStaticMethodID(jcls, b"isSynchronized", b"(I)Z")
            self.isTransient    = jenv.GetStaticMethodID(jcls, b"isTransient",    b"(I)Z")
            self.isVolatile     = jenv.GetStaticMethodID(jcls, b"isVolatile",     b"(I)Z")
            self.toString       = jenv.GetStaticMethodID(jcls, b"toString",       b"(I)Ljava/lang/String;")

class java_lang_reflect_Member(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/reflect/Member")
            self.Class             = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.getName           = jenv.GetMethodID(jcls, b"getName",           b"()Ljava/lang/String;")
            self.getModifiers      = jenv.GetMethodID(jcls, b"getModifiers",      b"()I")
            self.getDeclaringClass = jenv.GetMethodID(jcls, b"getDeclaringClass", b"()Ljava/lang/Class;")
            self.isSynthetic       = jenv.GetMethodID(jcls, b"isSynthetic",       b"()Z")

class java_lang_reflect_Field(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/reflect/Field")
            self.Class          = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.getType        = jenv.GetMethodID(jcls, b"getType",        b"()Ljava/lang/Class;")
            self.isEnumConstant = jenv.GetMethodID(jcls, b"isEnumConstant", b"()Z")

class java_lang_reflect_Constructor(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/reflect/Constructor")
            self.Class             = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.getParameterTypes = jenv.GetMethodID(jcls, b"getParameterTypes", b"()[Ljava/lang/Class;")
            self.getExceptionTypes = jenv.GetMethodID(jcls, b"getExceptionTypes", b"()[Ljava/lang/Class;")
            self.isVarArgs         = jenv.GetMethodID(jcls, b"isVarArgs",         b"()Z")

class java_lang_reflect_Method(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/reflect/Method")
            self.Class             = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.getReturnType     = jenv.GetMethodID(jcls, b"getReturnType",     b"()Ljava/lang/Class;")
            self.getParameterTypes = jenv.GetMethodID(jcls, b"getParameterTypes", b"()[Ljava/lang/Class;")
            self.getExceptionTypes = jenv.GetMethodID(jcls, b"getExceptionTypes", b"()[Ljava/lang/Class;")
            self.isVarArgs         = jenv.GetMethodID(jcls, b"isVarArgs",         b"()Z")
            self.isBridge          = jenv.GetMethodID(jcls, b"isBridge",          b"()Z")
            self.toGenericString   = jenv.GetMethodID(jcls, b"toGenericString",   b"()Ljava/lang/String;")

class java_lang_reflect_Proxy(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/reflect/Proxy")
            self.Class                = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.getProxyClass        = jenv.GetStaticMethodID(jcls, b"getProxyClass",
                                                               b"(Ljava/lang/ClassLoader;[Ljava/lang/Class;)Ljava/lang/Class;")
            self.isProxyClass         = jenv.GetStaticMethodID(jcls, b"isProxyClass", b"(Ljava/lang/Class;)Z")
            self.newProxyInstance     = jenv.GetStaticMethodID(jcls, b"newProxyInstance",
                                                               b"(Ljava/lang/ClassLoader;[Ljava/lang/Class;"
                                                               b"Ljava/lang/reflect/InvocationHandler;)Ljava/lang/Object;")
            self.getInvocationHandler = jenv.GetStaticMethodID(jcls, b"getInvocationHandler",
                                                               b"(Ljava/lang/Object;)Ljava/lang/reflect/InvocationHandler;")

class java_lang_Number(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/Number")
            self.Class       = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.byteValue   = jenv.GetMethodID(jcls, b"byteValue",   b"()B")
            self.shortValue  = jenv.GetMethodID(jcls, b"shortValue",  b"()S")
            self.intValue    = jenv.GetMethodID(jcls, b"intValue",    b"()I")
            self.longValue   = jenv.GetMethodID(jcls, b"longValue",   b"()J")
            self.floatValue  = jenv.GetMethodID(jcls, b"floatValue",  b"()F")
            self.doubleValue = jenv.GetMethodID(jcls, b"doubleValue", b"()D")

class jnijprim(jnij):

    def dispose(self, jenv: jni.JNIEnv):
        if jenv is not None:
            jenv.DeleteGlobalRef(self.Class)
            jenv.DeleteGlobalRef(self.TYPE)

class java_lang_Void(jnijprim):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 2):
            jcls = jenv.FindClass(b"java/lang/Void")
            TYPE = jenv.GetStaticObjectField(jcls, jenv.GetStaticFieldID(jcls, b"TYPE", b"Ljava/lang/Class;"))
            self.Class = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.TYPE  = jni.cast(jenv.NewGlobalRef(TYPE), jni.jclass)

class java_lang_Boolean(jnijprim):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 2):
            jcls = jenv.FindClass(b"java/lang/Boolean")
            TYPE = jenv.GetStaticObjectField(jcls, jenv.GetStaticFieldID(jcls, b"TYPE", b"Ljava/lang/Class;"))
            self.Class        = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.TYPE         = jni.cast(jenv.NewGlobalRef(TYPE), jni.jclass)
            self.Constructor  = jenv.GetMethodID      (jcls, b"<init>",       b"(Z)V")
            self.valueOf      = jenv.GetStaticMethodID(jcls, b"valueOf",      b"(Z)Ljava/lang/Boolean;")
            self.booleanValue = jenv.GetMethodID      (jcls, b"booleanValue", b"()Z")

class java_lang_Character(jnijprim):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 2):
            jcls = jenv.FindClass(b"java/lang/Character")
            TYPE = jenv.GetStaticObjectField(jcls, jenv.GetStaticFieldID(jcls, b"TYPE", b"Ljava/lang/Class;"))
            self.Class       = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.TYPE        = jni.cast(jenv.NewGlobalRef(TYPE), jni.jclass)
            self.Constructor = jenv.GetMethodID      (jcls, b"<init>",    b"(C)V")
            self.valueOf     = jenv.GetStaticMethodID(jcls, b"valueOf",   b"(C)Ljava/lang/Character;")
            self.charValue   = jenv.GetMethodID      (jcls, b"charValue", b"()C")

class java_lang_Byte(jnijprim):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 2):
            jcls = jenv.FindClass(b"java/lang/Byte")
            TYPE = jenv.GetStaticObjectField(jcls, jenv.GetStaticFieldID(jcls, b"TYPE", b"Ljava/lang/Class;"))
            self.Class       = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.TYPE        = jni.cast(jenv.NewGlobalRef(TYPE), jni.jclass)
            self.Constructor = jenv.GetMethodID      (jcls, b"<init>",  b"(B)V")
            self.valueOf     = jenv.GetStaticMethodID(jcls, b"valueOf", b"(B)Ljava/lang/Byte;")
            self.MIN_VALUE   = jenv.GetStaticByteField(jcls, jenv.GetStaticFieldID(jcls, b"MIN_VALUE", b"B"))
            self.MAX_VALUE   = jenv.GetStaticByteField(jcls, jenv.GetStaticFieldID(jcls, b"MAX_VALUE", b"B"))

class java_lang_Short(jnijprim):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 2):
            jcls = jenv.FindClass(b"java/lang/Short")
            TYPE = jenv.GetStaticObjectField(jcls, jenv.GetStaticFieldID(jcls, b"TYPE", b"Ljava/lang/Class;"))
            self.Class       = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.TYPE        = jni.cast(jenv.NewGlobalRef(TYPE), jni.jclass)
            self.Constructor = jenv.GetMethodID      (jcls, b"<init>",  b"(S)V")
            self.valueOf     = jenv.GetStaticMethodID(jcls, b"valueOf", b"(S)Ljava/lang/Short;")
            self.MIN_VALUE   = jenv.GetStaticShortField(jcls, jenv.GetStaticFieldID(jcls, b"MIN_VALUE", b"S"))
            self.MAX_VALUE   = jenv.GetStaticShortField(jcls, jenv.GetStaticFieldID(jcls, b"MAX_VALUE", b"S"))
            # Some JVM's incorrectly return positive values
            if self.MIN_VALUE > 0: self.MIN_VALUE = -self.MIN_VALUE

class java_lang_Integer(jnijprim):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 2):
            jcls = jenv.FindClass(b"java/lang/Integer")
            TYPE = jenv.GetStaticObjectField(jcls, jenv.GetStaticFieldID(jcls, b"TYPE", b"Ljava/lang/Class;"))
            self.Class       = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.TYPE        = jni.cast(jenv.NewGlobalRef(TYPE), jni.jclass)
            self.Constructor = jenv.GetMethodID      (jcls, b"<init>",  b"(I)V")
            self.valueOf     = jenv.GetStaticMethodID(jcls, b"valueOf", b"(I)Ljava/lang/Integer;")
            self.MIN_VALUE   = jenv.GetStaticIntField(jcls, jenv.GetStaticFieldID(jcls, b"MIN_VALUE", b"I"))
            self.MAX_VALUE   = jenv.GetStaticIntField(jcls, jenv.GetStaticFieldID(jcls, b"MAX_VALUE", b"I"))
            # Some JVM's incorrectly return positive values
            if self.MIN_VALUE > 0: self.MIN_VALUE = -self.MIN_VALUE

class java_lang_Long(jnijprim):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 2):
            jcls = jenv.FindClass(b"java/lang/Long")
            TYPE = jenv.GetStaticObjectField(jcls, jenv.GetStaticFieldID(jcls, b"TYPE", b"Ljava/lang/Class;"))
            self.Class       = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.TYPE        = jni.cast(jenv.NewGlobalRef(TYPE), jni.jclass)
            self.Constructor = jenv.GetMethodID      (jcls, b"<init>",  b"(J)V")
            self.valueOf     = jenv.GetStaticMethodID(jcls, b"valueOf", b"(J)Ljava/lang/Long;")
            self.MIN_VALUE   = jenv.GetStaticLongField(jcls, jenv.GetStaticFieldID(jcls, b"MIN_VALUE", b"J"))
            self.MAX_VALUE   = jenv.GetStaticLongField(jcls, jenv.GetStaticFieldID(jcls, b"MAX_VALUE", b"J"))
            # Some JVM's incorrectly return positive values
            if self.MIN_VALUE > 0: self.MIN_VALUE = -self.MIN_VALUE

class java_lang_Float(jnijprim):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 2):
            jcls = jenv.FindClass(b"java/lang/Float")
            TYPE = jenv.GetStaticObjectField(jcls, jenv.GetStaticFieldID(jcls, b"TYPE", b"Ljava/lang/Class;"))
            self.Class       = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.TYPE        = jni.cast(jenv.NewGlobalRef(TYPE), jni.jclass)
            self.Constructor = jenv.GetMethodID      (jcls, b"<init>",  b"(F)V")
            self.valueOf     = jenv.GetStaticMethodID(jcls, b"valueOf", b"(F)Ljava/lang/Float;")
            self.MIN_VALUE   = jenv.GetStaticFloatField(jcls, jenv.GetStaticFieldID(jcls, b"MIN_VALUE", b"F"))
            self.MAX_VALUE   = jenv.GetStaticFloatField(jcls, jenv.GetStaticFieldID(jcls, b"MAX_VALUE", b"F"))

class java_lang_Double(jnijprim):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 2):
            jcls = jenv.FindClass(b"java/lang/Double")
            TYPE = jenv.GetStaticObjectField(jcls, jenv.GetStaticFieldID(jcls, b"TYPE", b"Ljava/lang/Class;"))
            self.Class       = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.TYPE        = jni.cast(jenv.NewGlobalRef(TYPE), jni.jclass)
            self.Constructor = jenv.GetMethodID      (jcls, b"<init>",  b"(D)V")
            self.valueOf     = jenv.GetStaticMethodID(jcls, b"valueOf", b"(D)Ljava/lang/Double;")
            self.MIN_VALUE   = jenv.GetStaticDoubleField(jcls, jenv.GetStaticFieldID(jcls, b"MIN_VALUE", b"D"))
            self.MAX_VALUE   = jenv.GetStaticDoubleField(jcls, jenv.GetStaticFieldID(jcls, b"MAX_VALUE", b"D"))

class java_lang_String(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/String")
            self.Class                = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.ConstructorFromBytes = jenv.GetMethodID(jcls, b"<init>",   b"([BLjava/lang/String;)V")
            self.getBytes             = jenv.GetMethodID(jcls, b"getBytes", b"(Ljava/lang/String;)[B")

class java_lang_Object(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/lang/Object")
            self.Class    = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.getClass = jenv.GetMethodID(jcls, b"getClass", b"()Ljava/lang/Class;")
            self.hashCode = jenv.GetMethodID(jcls, b"hashCode", b"()I")
            self.toString = jenv.GetMethodID(jcls, b"toString", b"()Ljava/lang/String;")
            self.equals   = jenv.GetMethodID(jcls, b"equals",   b"(Ljava/lang/Object;)Z")

class java_io_StringWriter(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/io/StringWriter")
            self.Class       = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
            self.Constructor = jenv.GetMethodID(jcls, b"<init>", b"()V")

class java_io_PrintWriter(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        with JFrame(jenv, 1):
            jcls = jenv.FindClass(b"java/io/PrintWriter")
            self.Class       = jni.cast(jenv.NewGlobalRef(jcls),  jni.jclass)
            self.Constructor = jenv.GetMethodID(jcls, b"<init>", b"(Ljava/io/Writer;)V")
            self.flush       = jenv.GetMethodID(jcls, b"flush",  b"()V")
