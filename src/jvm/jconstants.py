# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import enum

import jni
from .lib import public

@public
class EJavaType(enum.IntEnum):
    VOID    =  0
    CHAR    =  1
    BYTE    =  2
    SHORT   =  3
    INT     =  4
    LONG    =  5
    FLOAT   =  6
    DOUBLE  =  7
    BOOLEAN =  8
    OBJECT  = 10
    ARRAY   = 20
    STRING  = 21
    CLASS   = 22

@public
class EJavaModifiers(enum.IntEnum):
    PUBLIC    = 0
    PROTECTED = 1
    STATIC    = 2
    FINAL     = 3
    ABSTRACT  = 4

@public
class EStatusCode(enum.IntEnum):
    SUCCESS   = 1000
    UNKNOWN   = 1001
    EXCEPTION = 1002
    HOST      = 1003
    ERR       = jni.JNI_ERR        # unknown error
    EDETACHED = jni.JNI_EDETACHED  # thread detached from the VM
    EVERSION  = jni.JNI_EVERSION   # JNI version error
    ENOMEM    = jni.JNI_ENOMEM     # not enough memory
    EEXIST    = jni.JNI_EEXIST     # VM already created
    EINVAL    = jni.JNI_EINVAL     # invalid arguments
