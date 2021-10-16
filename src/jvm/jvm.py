# Copyright (c) 2004-2022 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Tuple
from pathlib import Path
import os

import jni
from .lib import public
from .lib import obj
from .lib import const
from .lib import weakconst
from .lib import adict

from .jconstants import EStatusCode

INTERNAL_CLASSPATHS = [Path(__file__).resolve().parent/"java"]


@public
class JVM(obj):
    """Java Virtual Machine"""

    JNI_VERSION = jni.JNI_VERSION_1_6

    def createdJVMs(self) -> Tuple['_JVM', ...]:
        njvm = jni.new(jni.jsize)
        err = self._jvm.JNI.GetCreatedJavaVMs(None, 0, njvm)
        if err != jni.JNI_OK:
            raise jni.JNIException(err, info="JNI_GetCreatedJavaVMs")
        pjvm = jni.new_array(jni.POINTER(jni.JavaVM), njvm[0])
        err = self._jvm.JNI.GetCreatedJavaVMs(pjvm, len(pjvm), njvm)
        if err != jni.JNI_OK:
            raise jni.JNIException(err, info="JNI_GetCreatedJavaVMs")
        jvms = []
        for i in range(njvm[0]):
            jvm = _JVM()
            jvm.JNI    = self._jvm.JNI
            jvm.jnijvm = pjvm[0][i]
            jvms.append(jvm)
        return tuple(jvms)

    def __init__(self, dll_path: Optional[object] = None):

        def class_copy(cls, **dict):
            dict.update(__module__="jvm", __doc__=cls.__doc__, __slots__=())
            return type(cls.__name__, (cls,), dict)

        from .jthread         import JThread
        from .jpackage        import JPackage
        from .jclassloader    import JClassLoader
        from .jclass          import JClass
        from .jfield          import JField
        from .jconstructor    import JConstructor
        from .jmethod         import JMethod
        from .jarguments      import JArguments
        from .jpropdescriptor import JPropertyDescriptor
        from .jannotation     import JAnnotation
        from .jobject         import JObject
        from .jarray          import JArray
        from .jmonitor        import JMonitor
        from .jproxy          import JProxy
        from .jrefqueue       import JReferenceQueue
        from .jexception      import JException

        self.JThread             = class_copy(JThread,             jvm=weakconst(self))
        self.JPackage            = class_copy(JPackage,            jvm=weakconst(self))
        self.JClassLoader        = class_copy(JClassLoader,        jvm=weakconst(self))
        self.JClass              = class_copy(JClass,              jvm=weakconst(self))
        self.JField              = class_copy(JField,              jvm=weakconst(self))
        self.JConstructor        = class_copy(JConstructor,        jvm=weakconst(self))
        self.JMethod             = class_copy(JMethod,             jvm=weakconst(self))
        self.JArguments          = class_copy(JArguments,          jvm=weakconst(self))
        self.JPropertyDescriptor = class_copy(JPropertyDescriptor, jvm=weakconst(self))
        self.JAnnotation         = class_copy(JAnnotation,         jvm=weakconst(self))
        self.JObject             = class_copy(JObject,             jvm=weakconst(self))
        self.JArray              = class_copy(JArray,              jvm=weakconst(self))
        self.JMonitor            = class_copy(JMonitor,            jvm=weakconst(self))
        self.JProxy              = class_copy(JProxy,              jvm=weakconst(self))
        self.JReferenceQueue     = class_copy(JReferenceQueue,     jvm=weakconst(self))
        self.JException          = class_copy(JException,          jvm=weakconst(self))

        if_load = dll_path is not None

        self._jvm = None  # _JVM
        self.JavaException = None
        self.ExceptionsMap = {}
        try:
            # TODO: add the non-string parameters, for possible callbacks

            if if_load and not isinstance(dll_path, (str, os.PathLike)):
                raise JVMException(EStatusCode.EINVAL,
                                   "First parameter must be a string or os.PathLike type")
            self._jvm = _JVM()
            self._jvm.data.describe_exceptions = False
            try:
                self._jvm.JNI = jni.load(dll_path) if if_load else None
            except Exception as exc:
                raise JVMException(EStatusCode.UNKNOWN,
                                   f"Unable to load DLL [{dll_path}], error = {exc}") from None
            self._jvm._create()
        except Exception as exc:
            self.handleException(exc)

    def __del__(self):
        if not self._jvm: return
        try: self._jvm.jnijvm.DestroyJavaVM()
        except Exception: pass
        self._jvm.jnijvm = None
        try: self._jvm.JNI.dllclose()
        except Exception: pass
        self._jvm.JNI = None

    def __enter__(self):
        if self._jvm is None:
            raise JVMException(EStatusCode.EDETACHED,
                               "Unable to use JVM: thread detached from the VM")
        if self._jvm.jnijvm:
            penv = jni.obj(jni.POINTER(jni.JNIEnv))
            self._jvm.jnijvm.AttachCurrentThread(penv)
            return self._jvm, jni.JEnv(penv)
        else:
            return self._jvm, None

    def __exit__(self, exc_type, exc, exc_tb):
        del exc_type, exc_tb
        if exc: self.handleException(exc)
        return True

    def __iter__(self):
        return iter(self.__enter__())

    def start(self, *jvmoptions, **jvmargs): # -> Tuple['_JVM', jni.JNIEnv]:
        jvmoptions = tuple(["-Djava.class.path=" + os.pathsep.join(
                               [item.partition("=")[2] for item in jvmoptions
                                if item.lstrip().startswith("-Djava.class.path=")] +
                               [str(path) for path in INTERNAL_CLASSPATHS])] +
                           [item for item in jvmoptions
                            if not item.lstrip().startswith("-Djava.class.path=")])
        ignoreUnrecognized = jvmargs.get("ignoreUnrecognized", True)
        try:
            pjvm = jni.obj(jni.POINTER(jni.JavaVM))
            penv = jni.obj(jni.POINTER(jni.JNIEnv))
            jvm_args = jni.obj(jni.JavaVMInitArgs)
            jvm_args.version  = JVM.JNI_VERSION
            jvm_args.nOptions = len(jvmoptions)
            jvm_args.options  = joptions = jni.new_array(jni.JavaVMOption, jvm_args.nOptions)
            _keep = []
            for i, option in enumerate(jvmoptions):
                optionString = jni.new_cstr(option if isinstance(option, bytes)
                                            else str(option).encode("utf-8"))
                _keep.append(optionString)
                jvm_args.options[i].optionString = optionString
                jvm_args.options[i].extraInfo    = jni.NULL
            jvm_args.ignoreUnrecognized = jni.JNI_TRUE if ignoreUnrecognized else jni.JNI_FALSE
            err = self._jvm.JNI.CreateJavaVM(pjvm, penv, jvm_args)
            del _keep, joptions, jvm_args
            if err != jni.JNI_OK or jni.isNULL(pjvm):
                raise jni.JNIException(err if err != jni.JNI_OK else jni.JNI_ERR,
                                       info="JNI_CreateJavaVM")
            self._jvm.jnijvm = jni.JVM(pjvm)
            jenv = jni.JEnv(penv)
            try:
                self._jvm._initialize(jenv)
            except Exception as exc:
                try: self._jvm.jnijvm.DestroyJavaVM()
                except Exception: pass
                raise exc
            return self._jvm, jenv
        except Exception as exc:
            try:
                self.handleException(exc)
            finally:
                self._jvm.jnijvm = None

    def attach(self, pjvm: Optional[object] = None): # -> Tuple['_JVM', jni.JNIEnv]:
        if_bind = pjvm is not None
        try:
            if if_bind and not pjvm:
                raise JVMException(EStatusCode.EINVAL,
                                   "First parameter must be a JNI jvm handle")
            penv = jni.obj(jni.POINTER(jni.JNIEnv))
            if if_bind:
                self._jvm.jnijvm = jni.cast(pjvm, jni.POINTER(jni.JavaVM))[0]
                self._jvm.jnijvm.AttachCurrentThread(penv)
            else:
                self._jvm.jnijvm.GetEnv(penv, JVM.JNI_VERSION)
            jenv = jni.JEnv(penv)
            self._jvm._initialize(jenv)
            return self._jvm, jenv
        except Exception as exc:
            try:
                self.handleException(exc)
            finally:
                if if_bind:
                    self._jvm.jnijvm = None

    def shutdown(self):
        if self._jvm.jnijvm is None: return
        try:
            penv = jni.obj(jni.POINTER(jni.JNIEnv))
            self._jvm.jnijvm.AttachCurrentThread(penv)
            jenv = jni.JEnv(penv)
            self._jvm._dispose(jenv)
            self._jvm.jnijvm.DestroyJavaVM()
        except Exception as exc:
            try:
                self.handleException(exc)
            finally:
                self._jvm.jnijvm = None

    def isStarted(self) -> bool:
        # Check if the JVM environment has been initialized
        return self._jvm is not None and self._jvm.jnijvm is not None

    def attachThread(self, daemon: bool=False):
        try:
            penv = jni.obj(jni.POINTER(jni.JNIEnv))
            if not daemon:
                self._jvm.jnijvm.AttachCurrentThread(penv)
            else:
                self._jvm.jnijvm.AttachCurrentThreadAsDaemon(penv)
            return self._jvm, jni.JEnv(penv)
        except Exception as exc:
            self.handleException(exc)

    def detachThread(self):
        try:
            self._jvm.jnijvm.DetachCurrentThread()
        except Exception as exc:
            self.handleException(exc)

    def isThreadAttached(self) -> bool:
        try:
            penv = jni.obj(jni.POINTER(jni.JNIEnv))
            self._jvm.jnijvm.GetEnv(penv, JVM.JNI_VERSION)
        except jni.JNIException as exc:
            if exc.getError() == jni.JNI_EDETACHED:
                return False
            self.handleException(exc)
        except Exception as exc:
            self.handleException(exc)
        else:
            return not jni.isNULL(penv)

    def handleException(self, exc):
        try:
            raise exc
        except jni.Throwable as exc:
            self.JException.printDescribe()
            jexc = self.JException(exc)
            if self.JavaException and hasattr(self.JavaException, "__exception__"):
                raise self.JavaException.__exception__(jexc) from None
            else:
                classname = jexc.getClass().getName()
                message   = jexc.getMessage()
                if message is None: message = classname
                PyExc = self.JavaException or RuntimeError
                raise PyExc(f"Java exception {classname} occurred: {message}") from None
        except jni.JNIException as exc:
            PyExc = self.ExceptionsMap.get(exc.getError(),
                                           self.ExceptionsMap.get(EStatusCode.ERR, RuntimeError))
            raise PyExc(exc.getMessage()) from None
        except JVMException as exc:
            PyExc = self.ExceptionsMap.get(exc.args[0],
                                           self.ExceptionsMap.get(EStatusCode.ERR, RuntimeError))
            raise PyExc(exc.args[1]) from None
        except Exception:
            PyExc = self.ExceptionsMap.get(None)
            raise (PyExc(exc) if PyExc else exc) from None


@public
class _JVM(obj):

    __slots__ = ('JNI', 'jnijvm', 'data') + \
                ('java_array', 'java_lang', 'java_io', 'java_nio', 'java_util',
                 'System', 'Thread', 'Package', 'ClassLoader', 'Class', 'Throwable',
                 'StackTraceElement', 'AutoCloseable', 'Comparable', 'Iterable', 'Introspector',
                 'BeanInfo', 'PropertyDescriptor', 'Annotation', 'AnnotatedElement', 'Modifier',
                 'Member', 'Field', 'Constructor', 'Method', 'Proxy', 'Void', 'Boolean',
                 'Character', 'Byte', 'Short', 'Integer', 'Long', 'Float', 'Double', 'Number',
                 'String', 'Object', 'StringWriter', 'PrintWriter') + \
                ('jt_reflect_ProxyHandler', 'jt_ref_Reference', 'jt_ref_ReferenceQueue') + \
                ('PyVersion', 'PyException', 'PyObject', 'PyModule', 'PyClass',
                 'PyClassEnquirer', 'PythonInterpreter', 'PyScriptEngineFactory', 'PyScriptEngine')

    def __init__(self):
        super().__init__()
        self.JNI    = None  # jni.JNI
        self.jnijvm = None  # jni.JavaVM
        self.data   = adict()

    def _create(self):

        from .java import jnij

        self.java_array         = jnij.java_array()
        self.java_lang          = jnij.java_lang()
        self.java_io            = jnij.java_io()
        self.java_nio           = jnij.java_nio()
        self.java_util          = jnij.java_util()
        self.System             = jnij.java_lang_System()
        self.Thread             = jnij.java_lang_Thread()
        self.Package            = jnij.java_lang_Package()
        self.ClassLoader        = jnij.java_lang_ClassLoader()
        self.Class              = jnij.java_lang_Class()
        self.Throwable          = jnij.java_lang_Throwable()
        self.StackTraceElement  = jnij.java_lang_StackTraceElement()
        self.AutoCloseable      = jnij.java_lang_AutoCloseable()
        self.Comparable         = jnij.java_lang_Comparable()
        self.Iterable           = jnij.java_lang_Iterable()
        self.Introspector       = jnij.java_beans_Introspector()
        self.BeanInfo           = jnij.java_beans_BeanInfo()
        self.PropertyDescriptor = jnij.java_beans_PropertyDescriptor()
        self.Annotation         = jnij.java_lang_annotation_Annotation()
        self.AnnotatedElement   = jnij.java_lang_reflect_AnnotatedElement()
        self.Modifier           = jnij.java_lang_reflect_Modifier()
        self.Member             = jnij.java_lang_reflect_Member()
        self.Field              = jnij.java_lang_reflect_Field()
        self.Constructor        = jnij.java_lang_reflect_Constructor()
        self.Method             = jnij.java_lang_reflect_Method()
        self.Proxy              = jnij.java_lang_reflect_Proxy()
        self.Void               = jnij.java_lang_Void()
        self.Boolean            = jnij.java_lang_Boolean()
        self.Character          = jnij.java_lang_Character()
        self.Byte               = jnij.java_lang_Byte()
        self.Short              = jnij.java_lang_Short()
        self.Integer            = jnij.java_lang_Integer()
        self.Long               = jnij.java_lang_Long()
        self.Float              = jnij.java_lang_Float()
        self.Double             = jnij.java_lang_Double()
        self.Number             = jnij.java_lang_Number()
        self.String             = jnij.java_lang_String()
        self.Object             = jnij.java_lang_Object()
        self.StringWriter       = jnij.java_io_StringWriter()
        self.PrintWriter        = jnij.java_io_PrintWriter()

        from .java import jnijt

        self.jt_reflect_ProxyHandler = jnijt.jt_reflect_ProxyHandler()
        self.jt_ref_Reference        = jnijt.jt_ref_Reference()
        self.jt_ref_ReferenceQueue   = jnijt.jt_ref_ReferenceQueue()

        from .java import jnipy

        self.PyVersion             = jnipy.Version()
        self.PyException           = jnipy.PyException()
        self.PyObject              = jnipy.PyObject()
        self.PyModule              = jnipy.PyModule()
        self.PyClass               = jnipy.PyClass()
        self.PyClassEnquirer       = jnipy.ClassEnquirer()
        self.PythonInterpreter     = jnipy.PythonInterpreter()
        self.PyScriptEngineFactory = jnipy.PyScriptEngineFactory()
        self.PyScriptEngine        = jnipy.PyScriptEngine()

    def _initialize(self, jenv: jni.JNIEnv):

        self.java_array.initialize(jenv)
        self.java_lang.initialize(jenv)
        self.java_io.initialize(jenv)
        self.java_nio.initialize(jenv)
        self.java_util.initialize(jenv)
        self.System.initialize(jenv)
        self.Thread.initialize(jenv)
        self.Package.initialize(jenv)
        self.ClassLoader.initialize(jenv)
        self.Class.initialize(jenv)
        self.Throwable.initialize(jenv)
        self.StackTraceElement.initialize(jenv)
        self.AutoCloseable.initialize(jenv)
        self.Comparable.initialize(jenv)
        self.Iterable.initialize(jenv)
        self.Introspector.initialize(jenv)
        self.BeanInfo.initialize(jenv)
        self.PropertyDescriptor.initialize(jenv)
        self.Annotation.initialize(jenv)
        self.AnnotatedElement.initialize(jenv)
        self.Modifier.initialize(jenv)
        self.Member.initialize(jenv)
        self.Field.initialize(jenv)
        self.Constructor.initialize(jenv)
        self.Method.initialize(jenv)
        self.Proxy.initialize(jenv)
        self.Void.initialize(jenv)
        self.Boolean.initialize(jenv)
        self.Character.initialize(jenv)
        self.Byte.initialize(jenv)
        self.Short.initialize(jenv)
        self.Integer.initialize(jenv)
        self.Long.initialize(jenv)
        self.Float.initialize(jenv)
        self.Double.initialize(jenv)
        self.Number.initialize(jenv)
        self.String.initialize(jenv)
        self.Object.initialize(jenv)
        self.StringWriter.initialize(jenv)
        self.PrintWriter.initialize(jenv)

        self.jt_reflect_ProxyHandler.initialize(jenv)
        self.jt_ref_Reference.initialize(jenv)
        self.jt_ref_ReferenceQueue.initialize(jenv)

        self.PyVersion.initialize(jenv)
        self.PyException.initialize(jenv)
        self.PyObject.initialize(jenv)
        self.PyModule.initialize(jenv)
        self.PyClass.initialize(jenv)
        self.PyClassEnquirer.initialize(jenv)
        self.PythonInterpreter.initialize(jenv)
        self.PyScriptEngineFactory.initialize(jenv)
        self.PyScriptEngine.initialize(jenv)

    def _dispose(self, jenv: jni.JNIEnv):

        self.java_array.dispose(jenv)
        self.java_lang.dispose(jenv)
        self.java_io.dispose(jenv)
        self.java_nio.dispose(jenv)
        self.java_util.dispose(jenv)
        self.System.dispose(jenv)
        self.Thread.dispose(jenv)
        self.Package.dispose(jenv)
        self.ClassLoader.dispose(jenv)
        self.Class.dispose(jenv)
        self.Throwable.dispose(jenv)
        self.StackTraceElement.dispose(jenv)
        self.AutoCloseable.dispose(jenv)
        self.Comparable.dispose(jenv)
        self.Iterable.dispose(jenv)
        self.Introspector.dispose(jenv)
        self.BeanInfo.dispose(jenv)
        self.PropertyDescriptor.dispose(jenv)
        self.Annotation.dispose(jenv)
        self.AnnotatedElement.dispose(jenv)
        self.Modifier.dispose(jenv)
        self.Member.dispose(jenv)
        self.Field.dispose(jenv)
        self.Constructor.dispose(jenv)
        self.Method.dispose(jenv)
        self.Proxy.dispose(jenv)
        self.Void.dispose(jenv)
        self.Boolean.dispose(jenv)
        self.Character.dispose(jenv)
        self.Byte.dispose(jenv)
        self.Short.dispose(jenv)
        self.Integer.dispose(jenv)
        self.Long.dispose(jenv)
        self.Float.dispose(jenv)
        self.Double.dispose(jenv)
        self.Number.dispose(jenv)
        self.String.dispose(jenv)
        self.Object.dispose(jenv)
        self.StringWriter.dispose(jenv)
        self.PrintWriter.dispose(jenv)

        self.jt_reflect_ProxyHandler.dispose(jenv)
        self.jt_ref_Reference.dispose(jenv)
        self.jt_ref_ReferenceQueue.dispose(jenv)

        self.PyVersion.dispose(jenv)
        self.PyException.dispose(jenv)
        self.PyObject.dispose(jenv)
        self.PyModule.dispose(jenv)
        self.PyClass.dispose(jenv)
        self.PyClassEnquirer.dispose(jenv)
        self.PythonInterpreter.dispose(jenv)
        self.PyScriptEngineFactory.dispose(jenv)
        self.PyScriptEngine.dispose(jenv)


@public
class JVMException(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
