# Copyright (c) 2012-2018 Adam Karpierz
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib

from __future__ import absolute_import

__all__ = ('Py_buffer','Buffer','isbuffer')

import sys
import ctypes
py_version = sys.version_info[:2]
if py_version < (2,6):
    # Only if the new buffer protocol is available
    raise ImportError("Buffer interface only usable on Python 2.6+")
from ctypes import (c_bool, c_int, c_ulong, c_void_p, c_char_p, py_object,
                    POINTER, pointer, byref, sizeof, cast, memset, Structure)
from ctypes import pythonapi
c_ssize_t = getattr(ctypes, "c_ssize_t", c_ulong)  # Python 2.6 doesn't define this
from ctypes import CFUNCTYPE as CFUNC
from .typeobject import PyTypeObject

#----------------------------------------------------------------------------#
#                               Buffer Object                                #
#----------------------------------------------------------------------------#

class Py_buffer(Structure):

    """Python level Py_buffer struct analog"""

    # equivalent of: Python-(2.6.0 | 2.7.0 | 3.4.3 | 3.5.1)/Include/object.h/Py_buffer

    # Maximum number of dimensions
    PyBUF_MAX_NDIM = 64

    # Flags for getting buffers
    PyBUF_SIMPLE    = 0x0000
    PyBUF_WRITABLE  = 0x0001
    PyBUF_WRITEABLE = PyBUF_WRITABLE  # backwards compatible alias
    PyBUF_FORMAT    = 0x0004
    PyBUF_ND        = 0x0008
    PyBUF_STRIDES   = 0x0010 | PyBUF_ND

    PyBUF_C_CONTIGUOUS   = 0x0020 | PyBUF_STRIDES
    PyBUF_F_CONTIGUOUS   = 0x0040 | PyBUF_STRIDES
    PyBUF_ANY_CONTIGUOUS = 0x0080 | PyBUF_STRIDES
    PyBUF_INDIRECT       = 0x0100 | PyBUF_STRIDES

    PyBUF_CONTIG_RO  = PyBUF_ND
    PyBUF_CONTIG     = PyBUF_ND | PyBUF_WRITABLE

    PyBUF_STRIDED_RO = PyBUF_STRIDES
    PyBUF_STRIDED    = PyBUF_STRIDES | PyBUF_WRITABLE

    PyBUF_RECORDS_RO = PyBUF_STRIDES | PyBUF_FORMAT
    PyBUF_RECORDS    = PyBUF_STRIDES | PyBUF_FORMAT | PyBUF_WRITABLE

    PyBUF_FULL_RO    = PyBUF_INDIRECT | PyBUF_FORMAT
    PyBUF_FULL       = PyBUF_INDIRECT | PyBUF_FORMAT | PyBUF_WRITABLE

    PyBUF_READ   = 0x0100
    PyBUF_WRITE  = 0x0200
  # PyBUF_SHADOW = 0x0400  # coment because available only for PY2

    __slots__ = ()
    _fields_  = [
        ("buf",        c_void_p),
        ("obj",        py_object),  # owned reference
        ("len",        c_ssize_t),
        ("itemsize",   c_ssize_t),
        ("readonly",   c_int),
        ("ndim",       c_int),
        ("format",     c_char_p),
        ("shape",      POINTER(c_ssize_t)),
        ("strides",    POINTER(c_ssize_t)),
        ("suboffsets", POINTER(c_ssize_t))]
    if py_version >= (2,7) and py_version <= (3,2):
        _fields_.extend([
        ("smalltable", c_ssize_t * 2)])
    _fields_.extend([
        ("internal",   c_void_p)])
    _fields_ = tuple(_fields_)

    def __new__(cls, *args, **kargs):

        self = super(Py_buffer, cls).__new__(cls)
        memset(byref(self), 0, sizeof(Py_buffer))
        return self

#----------------------------------------------------------------------------#
#                               Buffer Mixin                                 #
#----------------------------------------------------------------------------#

class Buffer(object):

    """Python level buffer protocol exporter"""

    __slots__ = ()

class _PyBufferProcs(Structure):

    # equivalent of: Python-(3.4.3 | 2.7.10)/Include/object.h/PyBufferProcs

    getbufferproc     = CFUNC(c_int, py_object, POINTER(Py_buffer), c_int)
    releasebufferproc = CFUNC(None,  py_object, POINTER(Py_buffer))

    __slots__ = ()
    _fields_  = []
    if py_version < (3,0):
        _fields_.extend([
        ("bf_getreadbuffer",  c_void_p),
        ("bf_getwritebuffer", c_void_p),
        ("bf_getsegcount",    c_void_p),
        ("bf_getcharbuffer",  c_void_p)])
    _fields_.extend([
        ("bf_getbuffer",     getbufferproc),
        ("bf_releasebuffer", releasebufferproc)])
    _fields_ = tuple(_fields_)

@_PyBufferProcs.getbufferproc
def _bf_getbuffer(self, view_p, flags):

    try:
        getbuffer = self.__getbuffer__
    except AttributeError:
        raise NotImplementedError("abstract method")

    try:
        rval = getbuffer(view_p[0] if view_p else None, flags)
    except Exception as exc:
        try:
            raise exc
        except:
            return -1

    if rval is not None:
        raise ValueError("__getbuffer__ method return value was not None")

    return 0

@_PyBufferProcs.releasebufferproc
def _bf_releasebuffer(self, view_p):

    try:
        releasebuffer = self.__releasebuffer__
    except AttributeError:
        return

    try:
        releasebuffer(view_p[0] if view_p else None)
    except:
        pass

_buffer_procs = _PyBufferProcs(bf_getbuffer=_bf_getbuffer,
                               bf_releasebuffer=_bf_releasebuffer)
BufferTypeObject = PyTypeObject.from_address(id(Buffer))
BufferTypeObject.tp_as_buffer = cast(pointer(_buffer_procs), c_void_p)
BufferTypeObject.tp_flags |= (PyTypeObject.Py_TPFLAGS_DEFAULT  |
                              PyTypeObject.Py_TPFLAGS_BASETYPE |
                              PyTypeObject.Py_TPFLAGS_HAVE_NEWBUFFER)
del BufferTypeObject

#----------------------------------------------------------------------------#
#                                Check Buffer                                #
#----------------------------------------------------------------------------#

try:
    isbuffer = pythonapi.PyObject_CheckBuffer
    isbuffer.argtypes = [py_object]
    isbuffer.restype  = c_bool
except AttributeError:
    CFUNC(c_bool, py_object)
    def isbuffer(obj):
        # 2.6.6, 2.7.10, 3.4.3, 3.5.1
        TypeObj = PyTypeObject.from_address(id(type(obj)))
        tp_as_buffer = cast(TypeObj.tp_as_buffer, POINTER(_PyBufferProcs))
        return ((py_version >= (3,0) or
                 (TypeObj.tp_flags & PyTypeObject.Py_TPFLAGS_HAVE_NEWBUFFER)) and
                bool(tp_as_buffer) and bool(tp_as_buffer.contents.bf_getbuffer))
