# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

# import builtins
import ctypes as __ct

# import jni

# from ....lib.compat import *
# from ....lib import cached
# from ....lib import classproperty
from ....lib import platform

# from ....jhost   import JHost
# from ....jstring import JString
# from ....jobject import JObject
# from ....jclass  import JClass
# from ....java    import throwJavaException


def proto(restype, func, *argtypes):
    func.restype  = restype
    func.argtypes = argtypes
    return func


if platform.is_cpython:
    Py_NoSiteFlag            = __ct.c_int.in_dll(__ct.pythonapi, "Py_NoSiteFlag")
    Py_NoUserSiteDirectory   = __ct.c_int.in_dll(__ct.pythonapi, "Py_NoUserSiteDirectory")
    Py_IgnoreEnvironmentFlag = __ct.c_int.in_dll(__ct.pythonapi, "Py_IgnoreEnvironmentFlag")
    Py_VerboseFlag           = __ct.c_int.in_dll(__ct.pythonapi, "Py_VerboseFlag")
    Py_OptimizeFlag          = __ct.c_int.in_dll(__ct.pythonapi, "Py_OptimizeFlag")
    Py_DontWriteBytecodeFlag = __ct.c_int.in_dll(__ct.pythonapi, "Py_DontWriteBytecodeFlag")
    Py_HashRandomizationFlag = __ct.c_int.in_dll(__ct.pythonapi, "Py_HashRandomizationFlag")
    Py_SetPythonHome         = __ct.c_int.in_dll(__ct.pythonapi, "Py_SetPythonHome")

    PyEval_AcquireThread  = proto(None, __ct.pythonapi.PyEval_AcquireThread)
    PyEval_ReleaseThread  = proto(None, __ct.pythonapi.PyEval_ReleaseThread)
    PyThreadState_GetDict = proto(__ct.py_object, __ct.pythonapi.PyThreadState_GetDict)
    DDD = {}
    PyThreadState_GetDict = lambda: DDD
else:
    Py_NoSiteFlag            = lambda *args, **kwargs: None
    Py_NoUserSiteDirectory   = lambda *args, **kwargs: None
    Py_IgnoreEnvironmentFlag = lambda *args, **kwargs: None
    Py_VerboseFlag           = lambda *args, **kwargs: None
    Py_OptimizeFlag          = lambda *args, **kwargs: None
    Py_DontWriteBytecodeFlag = lambda *args, **kwargs: None
    Py_HashRandomizationFlag = lambda *args, **kwargs: None
    Py_SetPythonHome         = lambda *args, **kwargs: None

    PyEval_AcquireThread  = proto(None,   lambda *args, **kwargs: None)
    PyEval_ReleaseThread  = proto(None,   lambda *args, **kwargs: None)
    PyThreadState_GetDict = proto(object, lambda *args, **kwargs: None)
    DDD = {}
    PyThreadState_GetDict = lambda: DDD

del __ct
