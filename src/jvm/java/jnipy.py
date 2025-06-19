# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

import jni

from . import registerClass
from .jnij import jnij


class Version(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        from .org.python import Version
        registerClass(jenv, "org.python.Version", Version)

class PyException(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        from .org.python.core import PyException
        registerClass(jenv, "org.python.core.PyException", PyException)

class PyObject(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        from .org.python.core import PyObject
        registerClass(jenv, "org.python.core.PyObject", PyObject)

class PyModule(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        from .org.python.core import PyModule
        registerClass(jenv, "org.python.core.PyModule", PyModule)

class PyClass(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        from .org.python.core import PyClass
        registerClass(jenv, "org.python.core.PyClass", PyClass)

class ClassEnquirer(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        from .org.python.util import (ClassEnquirer,
                                      ClassListEnquirer,
                                      ClassListEnquirer_1,
                                      ClassListEnquirer_ClassFilenameFilter,
                                      NamingConventionClassEnquirer)
        registerClass(jenv, "org.python.util.ClassEnquirer",
                      ClassEnquirer)
        registerClass(jenv, "org.python.util.ClassListEnquirer$ClassFilenameFilter",
                      ClassListEnquirer_ClassFilenameFilter)
        registerClass(jenv, "org.python.util.ClassListEnquirer$1",
                      ClassListEnquirer_1)
        registerClass(jenv, "org.python.util.ClassListEnquirer",
                      ClassListEnquirer)
        registerClass(jenv, "org.python.util.NamingConventionClassEnquirer",
                      NamingConventionClassEnquirer)

class PythonInterpreter(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        from .org.python.util import (PythonInterpreter,
                                      PythonInterpreter_1,
                                      PythonInterpreter_Options,
                                      PythonInterpreter_Config,
                                      PythonInterpreter_MemoryManager,
                                      PythonInterpreter_Python,
                                      PythonInterpreter_Python_1,
                                      PythonInterpreter_Python_Platform,
                                      PythonInterpreter_Python_Windows,
                                      PythonInterpreter_Python_Linux,
                                      PythonInterpreter_Python_Solaris,
                                      PythonInterpreter_Python_MacOS,
                                      PythonInterpreter_Python_Unix)
        registerClass(jenv, "org.python.util.PythonInterpreter$Options",
                      PythonInterpreter_Options)
        registerClass(jenv, "org.python.util.PythonInterpreter$Config",
                      PythonInterpreter_Config)
        registerClass(jenv, "org.python.util.PythonInterpreter$MemoryManager",
                      PythonInterpreter_MemoryManager)
        registerClass(jenv, "org.python.util.PythonInterpreter$Python$Platform",
                      PythonInterpreter_Python_Platform)
        registerClass(jenv, "org.python.util.PythonInterpreter$Python$Windows",
                      PythonInterpreter_Python_Windows)
        registerClass(jenv, "org.python.util.PythonInterpreter$Python$Linux",
                      PythonInterpreter_Python_Linux)
        registerClass(jenv, "org.python.util.PythonInterpreter$Python$Solaris",
                      PythonInterpreter_Python_Solaris)
        registerClass(jenv, "org.python.util.PythonInterpreter$Python$MacOS",
                      PythonInterpreter_Python_MacOS)
        registerClass(jenv, "org.python.util.PythonInterpreter$Python$Unix",
                      PythonInterpreter_Python_Unix)
        registerClass(jenv, "org.python.util.PythonInterpreter$Python$1",
                      PythonInterpreter_Python_1)
        registerClass(jenv, "org.python.util.PythonInterpreter$Python",
                      PythonInterpreter_Python)
        registerClass(jenv, "org.python.util.PythonInterpreter$1",
                      PythonInterpreter_1)
        registerClass(jenv, "org.python.util.PythonInterpreter",
                      PythonInterpreter)

class PyScriptEngineFactory(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        from .org.python.jsr223 import PyScriptEngineFactory
        registerClass(jenv, "org.python.jsr223.PyScriptEngineFactory",
                      PyScriptEngineFactory)

class PyScriptEngine(jnij):

    def initialize(self, jenv: jni.JNIEnv):
        from .org.python.jsr223 import (PyScriptEngine,
                                        PyScriptEngine_PyCompiledScript)
        registerClass(jenv, "org.python.jsr223.PyScriptEngine$PyCompiledScript",
                      PyScriptEngine_PyCompiledScript)
        registerClass(jenv, "org.python.jsr223.PyScriptEngine",
                      PyScriptEngine)
