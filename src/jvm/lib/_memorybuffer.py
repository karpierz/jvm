# Copyright (c) 2012-2022 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

__all__ = ('Py_buffer','Buffer','isbuffer')

from ctypes import (c_bool, c_ubyte, c_int, c_ulong, c_ssize_t, c_void_p,
                    c_char_p, py_object, POINTER, pointer, byref, sizeof,
                    cast, memset, Structure)
from ctypes import CFUNCTYPE as CFUNC
from ctypes import pythonapi
from ._typeobject import PyTypeObject

#----------------------------------------------------------------------------#
#                               Buffer Object                                #
#----------------------------------------------------------------------------#

class Py_buffer(Structure):
    """Python level Py_buffer struct analog."""

    # equivalent of: Python-(3.6.0+)/Include/object.h/Py_buffer

    # Maximum number of dimensions
    PyBUF_MAX_NDIM = 64

    # Flags for getting buffers
    PyBUF_SIMPLE         = 0x0000
    PyBUF_WRITABLE       = 0x0001
    PyBUF_WRITEABLE      = PyBUF_WRITABLE  # backwards compatible alias
    PyBUF_FORMAT         = 0x0004
    PyBUF_ND             = 0x0008
    PyBUF_STRIDES        = 0x0010 | PyBUF_ND
    PyBUF_C_CONTIGUOUS   = 0x0020 | PyBUF_STRIDES
    PyBUF_F_CONTIGUOUS   = 0x0040 | PyBUF_STRIDES
    PyBUF_ANY_CONTIGUOUS = 0x0080 | PyBUF_STRIDES
    PyBUF_INDIRECT       = 0x0100 | PyBUF_STRIDES

    PyBUF_CONTIG     = PyBUF_ND | PyBUF_WRITABLE
    PyBUF_CONTIG_RO  = PyBUF_ND

    PyBUF_STRIDED    = PyBUF_STRIDES | PyBUF_WRITABLE
    PyBUF_STRIDED_RO = PyBUF_STRIDES

    PyBUF_RECORDS    = PyBUF_STRIDES | PyBUF_WRITABLE | PyBUF_FORMAT
    PyBUF_RECORDS_RO = PyBUF_STRIDES | PyBUF_FORMAT

    PyBUF_FULL       = PyBUF_INDIRECT | PyBUF_WRITABLE | PyBUF_FORMAT
    PyBUF_FULL_RO    = PyBUF_INDIRECT | PyBUF_FORMAT

    PyBUF_READ  = 0x0100
    PyBUF_WRITE = 0x0200

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
        ("suboffsets", POINTER(c_ssize_t)),
        ("internal",   c_void_p)]
    _fields_ = tuple(_fields_)

#----------------------------------------------------------------------------#
#                               Buffer Mixin                                 #
#----------------------------------------------------------------------------#

class Buffer:
    """Python level buffer protocol exporter."""

    __slots__ = ()

    @classmethod
    def __from_buffer__(cls, obj, length):
        return cast((c_ubyte * length).from_buffer(obj), c_void_p)

class _PyBufferProcs(Structure):

    # equivalent of: Python-(3.6.0+)/Include/object.h/PyBufferProcs

    getbufferproc     = CFUNC(c_int, py_object, POINTER(Py_buffer), c_int)
    releasebufferproc = CFUNC(None,  py_object, POINTER(Py_buffer))

    __slots__ = ()
    _fields_  = [
        ("bf_getbuffer",     getbufferproc),
        ("bf_releasebuffer", releasebufferproc)]
    _fields_ = tuple(_fields_)

@_PyBufferProcs.getbufferproc
def _bf_getbuffer(self, view_p, flags):

    try:
        getbuffer = self.__getbuffer__
    except AttributeError:
        raise NotImplementedError("abstract method") from None

    try:
        rval = getbuffer(view_p[0] if view_p else None, flags)
    except Exception as exc:
        try:
            raise exc
        except Exception:
            return -1

    if rval is not None:
        raise BufferError("__getbuffer__ method return value was not None")

    return 0

@_PyBufferProcs.releasebufferproc
def _bf_releasebuffer(self, view_p):

    releasebuffer = getattr(self, "__releasebuffer__", None)

    try:
        if releasebuffer is not None:
            releasebuffer(view_p[0] if view_p else None)
    except Exception:
        pass

_buffer_procs = _PyBufferProcs(bf_getbuffer=_bf_getbuffer,
                               bf_releasebuffer=_bf_releasebuffer)
BufferTypeObject = PyTypeObject.from_address(id(Buffer))
BufferTypeObject.tp_as_buffer = cast(pointer(_buffer_procs), c_void_p)
BufferTypeObject.tp_flags |= (PyTypeObject.Py_TPFLAGS_DEFAULT |
                              PyTypeObject.Py_TPFLAGS_BASETYPE)
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
        # from 3.5.1
        TypeObj = PyTypeObject.from_address(id(type(obj)))
        tp_as_buffer = cast(TypeObj.tp_as_buffer, POINTER(_PyBufferProcs))
        return bool(tp_as_buffer) and bool(tp_as_buffer.contents.bf_getbuffer)
