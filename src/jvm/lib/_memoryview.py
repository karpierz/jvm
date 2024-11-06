# coding: utf-8

# Memoryview object implementation
# based on: Python-3.5.1/Include/memoryobject.h, Python-3.5.1/Objects/memoryobject.c

from __future__ import absolute_import

__all__ = ('memoryview','buffer','Py_buffer','Buffer','isbuffer')

import sys
import platform
PY3 = sys.version_info[0] >= 3
long    = int
unicode = str
import gc
import struct
import binascii
from ctypes import (c_bool, c_char, c_byte, c_ubyte, c_short, c_ushort, c_int, c_uint, c_long,
                    c_ulong, c_longlong, c_ulonglong, c_ssize_t, c_size_t, c_float, c_double,
                    c_char_p, c_void_p, POINTER, pointer, byref, sizeof, addressof, resize,
                    cast, memset, memmove, py_object, create_string_buffer, Structure)
from memorybuffer import Py_buffer, Buffer, isbuffer

is_cpython = (platform.python_implementation().lower() == "cpython")

CHAR_BIT   = 8
UCHAR_MAX  = c_ubyte(-1).value
SCHAR_MIN  = -UCHAR_MAX // 2
SCHAR_MAX  = UCHAR_MAX // 2
USHRT_MAX  = c_ushort(-1).value
SHRT_MIN   = -USHRT_MAX // 2
SHRT_MAX   = USHRT_MAX // 2
UINT_MAX   = c_uint(-1).value
INT_MIN    = -UINT_MAX // 2
INT_MAX    = UINT_MAX // 2
ULONG_MAX  = c_ulong(-1).value
LONG_MIN   = -ULONG_MAX // 2
LONG_MAX   = ULONG_MAX // 2
ULLONG_MAX = c_ulonglong(-1).value
LLONG_MIN  = -ULLONG_MAX // 2
LLONG_MAX  = ULLONG_MAX // 2

if is_cpython:
    from ctypes import pythonapi
    Py_IncRef = pythonapi.Py_IncRef
    Py_IncRef.argtypes = [py_object]
    Py_IncRef.restype  = None
    Py_DecRef = pythonapi.Py_DecRef
    Py_DecRef.argtypes = [py_object]
    Py_DecRef.restype  = None
    PyObject_GetBuffer = pythonapi.PyObject_GetBuffer
    PyObject_GetBuffer.argtypes = [py_object, POINTER(Py_buffer), c_int]
    PyObject_GetBuffer.restype  = c_int
    PyBuffer_Release = pythonapi.PyBuffer_Release
    PyBuffer_Release.argtypes = [POINTER(Py_buffer)]
    PyBuffer_Release.restype  = None
    PyBuffer_IsContiguous = pythonapi.PyBuffer_IsContiguous
    PyBuffer_IsContiguous.argtypes = [POINTER(Py_buffer), c_char]
    PyBuffer_IsContiguous.restype  = c_int
    PyBuffer_FillInfo = pythonapi.PyBuffer_FillInfo
    PyBuffer_FillInfo.argtypes = [POINTER(Py_buffer), py_object, c_void_p, c_ssize_t, c_int, c_int]
    PyBuffer_FillInfo.restype  = c_int
    PyNumber_Index = pythonapi.PyNumber_Index
    PyNumber_Index.argtypes = [py_object]
    PyNumber_Index.restype  = py_object
    PyNumber_AsSsize_t = pythonapi.PyNumber_AsSsize_t
    PyNumber_AsSsize_t.argtypes = [py_object, py_object]
    PyNumber_AsSsize_t.restype  = c_ssize_t
    PyLong_AsLong = pythonapi.PyLong_AsLong
    PyLong_AsLong.argtypes = [py_object]
    PyLong_AsLong.restype  = c_long
    PyLong_AsUnsignedLong = pythonapi.PyLong_AsUnsignedLong
    PyLong_AsUnsignedLong.argtypes = [py_object]
    PyLong_AsUnsignedLong.restype  = c_ulong
    PyLong_AsLongLong = pythonapi.PyLong_AsLongLong
    PyLong_AsLongLong.argtypes = [py_object]
    PyLong_AsLongLong.restype  = c_longlong
    PyLong_AsUnsignedLongLong = pythonapi.PyLong_AsUnsignedLongLong
    PyLong_AsUnsignedLongLong.argtypes = [py_object]
    PyLong_AsUnsignedLongLong.restype  = c_ulonglong
    PyLong_AsSsize_t = pythonapi.PyLong_AsSsize_t
    PyLong_AsSsize_t.argtypes = [py_object]
    PyLong_AsSsize_t.restype  = c_ssize_t
    PyLong_AsSize_t = pythonapi.PyLong_AsSize_t
    PyLong_AsSize_t.argtypes = [py_object]
    PyLong_AsSize_t.restype  = c_size_t
    PyFloat_AsDouble = pythonapi.PyFloat_AsDouble
    PyFloat_AsDouble.argtypes = [py_object]
    PyFloat_AsDouble.restype  = c_double
    Py_FatalError = pythonapi.Py_FatalError
    Py_FatalError.argtypes = [c_char_p]
    Py_FatalError.restype  = None
else:
    def Py_IncRef(*args, **kwargs): return None
    def Py_DecRef(*args, **kwargs): return None
    #def PyObject_GetBuffer(*args, **kwargs): return None
    #def PyBuffer_Release(*args, **kwargs): return None
    #def PyBuffer_IsContiguous(*args, **kwargs): return None
    #def PyBuffer_FillInfo(*args, **kwargs): return None
    #def PyNumber_Index(*args, **kwargs): return None
    #def PyNumber_AsSsize_t(*args, **kwargs): return None
    #def PyLong_AsLong(*args, **kwargs): return None
    #def PyLong_AsUnsignedLong(*args, **kwargs): return None
    #def PyLong_AsLongLong(*args, **kwargs): return None
    #def PyLong_AsUnsignedLongLong(*args, **kwargs): return None
    #def PyLong_AsSsize_t(*args, **kwargs): return None
    #def PyLong_AsSize_t(*args, **kwargs): return None
    #def PyFloat_AsDouble(*args, **kwargs): return None
    #def Py_FatalError(*args, **kwargs): return None

def ct_ptr_add(ptr, offset):
    vptr = cast(ptr, c_void_p)
    vptr.value += offset
    return cast(vptr, type(ptr))

def ct_copy(dst, src):
    pointer(dst)[0] = src

def ct_clone(src):
    dst = type(src)()
    pointer(dst)[0] = src
    return dst

def is_multislice(idx):
    return isinstance(idx, tuple) and idx and all(isinstance(item, slice) for item in idx)

def is_multiindex(idx):
    return isinstance(idx, tuple) and all(hasattr(item, "__index__") for item in idx)

# ManagedBuffer Object:
# ---------------------
#
#   The purpose of this object is to facilitate the handling of chained
#   memoryviews that have the same underlying exporting object. PEP-3118
#   allows the underlying object to change while a view is exported. This
#   could lead to unexpected results when constructing a new memoryview
#   from an existing memoryview.
#
#   Rather than repeatedly redirecting buffer requests to the original base
#   object, all chained memoryviews use a single buffer snapshot. This
#   snapshot is generated by the constructor managedbuffer(object).
#
# Ownership rules:
# ----------------
#
#   The managed buffer is filled in by the original base object.
#   shape, strides, suboffsets and format are read-only for all consumers.
#
#   A memoryview's buffer is a private copy of the exporter's buffer. shape,
#   strides and suboffsets belong to the memoryview and are thus writable.
#
#   If a memoryview itself exports several buffers via memoryview.__getbuffer__(),
#   all buffer copies share shape, strides and suboffsets. In this case, the
#   arrays are NOT writable.
#
# Reference count assumptions:
# ----------------------------
#
#   The 'obj' member of a buffer must either be NULL or refer to the
#   exporting base object. In the Python codebase, all getbufferprocs
#   return a new reference to view.obj (example: bytes_buffer_getbuffer()).
#
#   PyBuffer_Release() decrements view.obj (if non-NULL), so the
#   releasebufferprocs must NOT decrement view.obj.

_Py_MANAGED_BUFFER_RELEASED = 0x0001  # access to exporter blocked

class managedbuffer(Py_buffer):

    __slots__ = ('_flags','_exports')

    def __new__(cls, *args, **kwargs):

        self = super(managedbuffer, cls).__new__(cls, *args, **kwargs)
        self._flags   = _Py_MANAGED_BUFFER_RELEASED  # state flags
        self._exports = 0  # number of direct memoryview exports
        return self

    def __init__(self, obj=None, flags=Py_buffer.PyBUF_FULL_RO):

        # (self, object, flags=PyBUF_RECORDS_RO | PyBUF_C_CONTIGUOUS): # memorybuffers

        super(managedbuffer, self).__init__()

        if obj is None:
            return

        try:
            result = PyObject_GetBuffer(obj, self, flags)
        except Exception as exc:
            self.obj = py_object()
            raise exc
        if result != 0: #!!! a nie TypeError ???
            self.obj = py_object()
            raise ValueError("Unable to retrieve Buffer from {}".format(obj))
        if not self.buf: #!!! a nie TypeError ???
            self.obj = py_object()
            raise ValueError("Null pointer result from {}".format(obj))

        self._flags &= ~_Py_MANAGED_BUFFER_RELEASED

    def __del__(self, PyBuffer_Release=PyBuffer_Release):

        # NOTE: at this point self._exports can still be > 0 if this function
        # is called from Py_buffer.__clear() to break up a reference cycle.

        #!!!assert self._exports == 0, self._exports

        if self._flags & _Py_MANAGED_BUFFER_RELEASED:
            return

        self._flags |= _Py_MANAGED_BUFFER_RELEASED

        #if not self.buf: # tego nie bylo w memoryview !!!
        #    return

        PyBuffer_Release(self)
        #!!!self.buf = None # NULL
        memset(byref(self), 0, sizeof(Py_buffer))

buffer = managedbuffer  # alias

#----------------------------------------------------------------------------#
#                              MemoryView Object                             #
#----------------------------------------------------------------------------#

# memoryview state flags
_Py_MEMORYVIEW_RELEASED   = 0x001  # access to master buffer blocked
_Py_MEMORYVIEW_C          = 0x002  # C-contiguous layout
_Py_MEMORYVIEW_FORTRAN    = 0x004  # Fortran contiguous layout
_Py_MEMORYVIEW_SCALAR     = 0x008  # scalar: ndim = 0
_Py_MEMORYVIEW_PIL        = 0x010  # PIL-style layout
_Py_MEMORYVIEW_STRICT_PY3 = 0x020  # strict Python3 mode


class memoryview(Buffer, Structure):

    """memoryview(object)\n\n""" \
    """Create a new memoryview object which references the given object."""

    _fields_  = (("_mbuf",     py_object),      # POINTER(managedbuffer)) # managed buffer
                 ("_hash",     c_ssize_t),      # Py_hash_t,hash value for read-only views
                 ("_flags",    c_int),          # state flags
                 ("_exports",  c_ssize_t),      # number of buffer re-exports
                 ("_view",     Py_buffer),      # private copy of the exporter's view
                 ("_ob_array", c_ssize_t * 0))  # shape, strides, suboffsets

#!!!def __new__(cls, object, strict_py3=False):
    def __new__(cls, object, strict_py3=True):

        # Create a memoryview from an object that implements the buffer protocol.
        # If the object is a memoryview, the new memoryview must be registered
        # with the same managed buffer. Otherwise, a new managed buffer is created.

        if isinstance(object, memoryview):

            object._check_released()
            return memoryview._new_view(object._view, object._mbuf, strict_py3=strict_py3)

        elif isbuffer(object):

            mbuf = managedbuffer(object)
            return memoryview._new_view(mbuf, mbuf, strict_py3=strict_py3)

        else:
            raise TypeError("memoryview: a bytes-like object is required, "
                            "not '{:.200}'".format(object.__class__.__name__))

    def __init__(self, object, strict_py3=False):

        super(memoryview, self).__init__()

    @classmethod
    def _new_view(cls, src, mbuf, strict_py3=False):

        # const Py_buffer* src, const Py_buffer* mbuf

        # Return a new memoryview that is registered with self.
        #
        # The new memoryview has full buffer information: shape and strides
        # are always present, suboffsets as needed. Arrays are copied to
        # the memoryview's _ob_array field.

        if src.ndim > Py_buffer.PyBUF_MAX_NDIM:
            raise ValueError("memoryview: number of dimensions "
                             "must not exceed {}".format(Py_buffer.PyBUF_MAX_NDIM))

        self = memoryview._new_incomplete_view(src, mbuf, src.ndim)
        Py_buff.init_shape_strides(self._view, src)
        Py_buff.init_suboffsets   (self._view, src)
        self._init_flags(strict_py3=strict_py3)

        return self

    @classmethod
    def _new_incomplete_view(cls, src, mbuf, ndim):

        # const Py_buffer* src, const Py_buffer* mbuf, int ndim

        # Register a new incomplete view: shape, strides, suboffsets and flags
        # still need to be initialized. Use 'ndim' instead of src.ndim to determine
        # the size of the memoryview's _ob_array.
        #
        # Assumption: ndim <= PyBUF_MAX_NDIM.

        assert ndim <= Py_buffer.PyBUF_MAX_NDIM

        # Allocate a new memoryview and perform basic initialization.
        # New memoryviews are exclusively created through the mbuf_add functions.

        self = super(memoryview, cls).__new__(cls)
        resize(self, sizeof(memoryview) + 3 * ndim * sizeof(c_ssize_t))
        memset(byref(self), 0, sizeof(memoryview) + 3 * ndim * sizeof(c_ssize_t))
        self._hash            = -1
        self._view.ndim       = ndim
        self._view.shape      = self._ob_array
        self._view.strides    = ct_ptr_add(self._view.shape,   ndim * sizeof(c_ssize_t))
        self._view.suboffsets = ct_ptr_add(self._view.strides, ndim * sizeof(c_ssize_t))
        Py_buff.init_shared_values(self._view, src)
        self._mbuf            = py_object(mbuf)

        mbuf._exports += 1

        return self

    def __del__(self):

        assert self._exports == 0

        self.release()
        self._mbuf = None

    @property
    def obj(self):

        """The underlying object of the memoryview."""

        self._check_released()
        view = self._view
        try:
            return view.obj
        except ValueError:
            return None

    @property
    def nbytes(self):

        """The amount of space in bytes that the array would use in\n""" \
        """a contiguous representation."""

        self._check_released()
        return long(self._view.len)

    @property
    def readonly(self):

        """A bool indicating whether the memory is read only."""

        self._check_released()
        return bool(self._view.readonly)

    @property
    def itemsize(self):

        """The size in bytes of each element of the memoryview."""

        self._check_released()
        return long(self._view.itemsize)

    @property
    def format(self):

        """A string containing the format (in struct module style)\n""" \
        """for each element in the view."""

        self._check_released()
        return self._view.format.decode("utf-8")

    @property
    def ndim(self):

        """An integer indicating how many dimensions of a multi-dimensional\n""" \
        """array the memory represents."""

        self._check_released()
        return long(self._view.ndim)

    @property
    def shape(self):

        """A tuple of ndim integers giving the shape of the memory\n""" \
        """as an N-dimensional array."""

        self._check_released()
        vals = self._view.shape
        return tuple(map(long, vals[:self._view.ndim])) if vals else ()

    @property
    def strides(self):

        """A tuple of ndim integers giving the size in bytes to access\n""" \
        """each element for each dimension of the array."""

        self._check_released()
        vals = self._view.strides
        return tuple(map(long, vals[:self._view.ndim])) if vals else ()

    @property
    def suboffsets(self):

        """A tuple of integers used internally for PIL-style arrays."""

        self._check_released()
        vals = self._view.suboffsets
        return tuple(map(long, vals[:self._view.ndim])) if vals else ()

    @property
    def c_contiguous(self):

        """A bool indicating whether the memory is C contiguous."""

        self._check_released()
        return bool(self._flags & (_Py_MEMORYVIEW_SCALAR | _Py_MEMORYVIEW_C))

    @property
    def f_contiguous(self):

        """A bool indicating whether the memory is Fortran contiguous."""

        self._check_released()
        return bool(self._flags & (_Py_MEMORYVIEW_SCALAR | _Py_MEMORYVIEW_FORTRAN))

    @property
    def contiguous(self):

        """A bool indicating whether the memory is contiguous."""

        self._check_released()
        return bool(self._flags & (_Py_MEMORYVIEW_SCALAR | _Py_MEMORYVIEW_C | _Py_MEMORYVIEW_FORTRAN))

    def release(self):

        """M.release() -> None\n\n""" \
        """Release the underlying buffer exposed by the memoryview object."""

        # Inform the managed buffer that this particular memoryview will not access
        # the underlying buffer again. If no other memoryviews are registered with
        # the managed buffer, the underlying buffer is released instantly and
        # marked as inaccessible for both the memoryview and the managed buffer.
        #
        # This function fails if the memoryview itself has exported buffers.

        if self._flags & _Py_MEMORYVIEW_RELEASED:
            return

        if self._exports > 0:
            raise BufferError("memoryview has {} exported buffer{}".format(self._exports,
                              "s" if self._exports > 1 else ""))

        if self._exports < 0:
            Py_FatalError("release(): negative export count")

        self._flags |= _Py_MEMORYVIEW_RELEASED

        assert self._mbuf._exports > 0

        self._mbuf._exports -= 1
        if self._mbuf._exports == 0:
            self._mbuf.__del__()
            self._mbuf = None

    def tobytes(self):

        """M.tobytes() -> bytes\n\n""" \
        """Return the data in the buffer as a byte string."""

        self._check_released()
        view = self._view

        if self._flags & (_Py_MEMORYVIEW_SCALAR | _Py_MEMORYVIEW_C):
            return cast(view.buf, POINTER(c_char))[:view.len]
        else:
            buf = create_string_buffer(view.len)
            Py_buff.buffer_to_contiguous(view, 'C', buf)
            return buf.raw

    def tolist(self):

        """M.tolist() -> list\n\n""" \
        """Return the data in the buffer as a list of elements."""

        # Return a list representation of the memoryview.
        # Currently only buffers with native format strings are supported.

        self._check_released()
        view = self._view

        fmt = Py_buff.adjust_fmt(view)
        if view.ndim == 0:
            return unpack_single(view.buf, fmt,
                                 strict_py3=bool(self._flags | _Py_MEMORYVIEW_STRICT_PY3))
        else:
            return memoryview._tolist(view.buf, view.ndim,
                                      view.shape, view.strides, view.suboffsets, fmt)

    @staticmethod
    def _tolist(ptr, ndim, shape, strides, suboffsets, fmt):

        # const char* ptr, c_ssize_t ndim,
        # const c_ssize_t* shape, const c_ssize_t* strides, const c_ssize_t* suboffsets,
        # const char* fmt

        # Unpack a multi-dimensional array into a nested list.
        # Assumption: ndim >= 1.

        assert ndim >= 1
        assert shape
        assert strides

        is_ndim_1 = (ndim == 1)

        lst = []
        stride = strides[0]
        for i in range(shape[0]):
            lst.append(unpack_single(Py_buff.adjust_ptr(ptr, suboffsets), fmt, strict_py3=True)
                       if is_ndim_1 else
                       memoryview._tolist(Py_buff.adjust_ptr(ptr, suboffsets), ndim - 1,
                                          ct_ptr_add(shape,      sizeof(c_ssize_t)),
                                          ct_ptr_add(strides,    sizeof(c_ssize_t)),
                                          ct_ptr_add(suboffsets, sizeof(c_ssize_t))
                                          if suboffsets else POINTER(c_ssize_t)(),
                                          fmt))
            ptr += stride

        return lst

    def cast(self, format, shape=None):

        """M.cast(format[, shape]) -> memoryview\n\n""" \
        """Cast a memoryview to a new format or shape."""

        # Cast a copy of 'self' to a different view. The input view must
        # be C-contiguous. The function always casts the input view to a
        # 1-D output according to 'format'. At least one of input-format,
        # output-format must have byte size.
        #
        # If 'shape' is given, the 1-D view from the previous step will
        # be cast to a C-contiguous view with new shape and strides.
        #
        # All casts must result in views that will have the exact byte
        # size of the original input. Otherwise, an error is raised.

        self._check_released()
        view = self._view

        if not isinstance(format, (str, unicode)):
            raise TypeError("memoryview: format argument must be a string")

        if not (self._flags & (_Py_MEMORYVIEW_SCALAR | _Py_MEMORYVIEW_C)):
            raise TypeError("memoryview: casts are restricted to C-contiguous views")

        is_shape = shape is not None

        if (is_shape or view.ndim != 1) and any((view.shape[i] == 0) for i in range(view.ndim)):
            raise TypeError("memoryview: cannot cast view with zeros in shape or strides")

        ndim = 1

        if is_shape:

            if not isinstance(shape, (list, tuple)):
                raise TypeError("{} must be a list or a tuple".format(shape))

            ndim = len(shape)
            if ndim > Py_buffer.PyBUF_MAX_NDIM:
                raise ValueError("memoryview: number of dimensions "
                                 "must not exceed {}".format(Py_buffer.PyBUF_MAX_NDIM))

            if view.ndim != 1 and ndim != 1:
                raise TypeError("memoryview: cast must be 1D -> ND or ND -> 1D")

        mv = memoryview._new_incomplete_view(view, self._mbuf, ndim or 1)
        mv._cast_to_1D(format)
        if is_shape:
            mv._cast_to_ND(shape, ndim)

        return mv

    def _cast_to_1D(self, format):

        # Cast a memoryview's data type to 'format'. The input array must be
        # C-contiguous. At least one of input-format, output-format must have
        # byte size. The output array is 1-D, with the same byte length as the
        # input array. Thus, view.len must be a multiple of the new itemsize.

        view = self._view

        assert view.ndim        >= 1
        #assert Py_SIZE(self)   == 3 * view.ndim
        #assert view.shape      == addressof(self._ob_array)
        #assert view.strides    == addressof(self._ob_array) + 1 * view.ndim
        #assert view.suboffsets == addressof(self._ob_array) + 2 * view.ndim

        format = format.encode("ascii")

        dest_fmtchar, itemsize = get_native_fmtchar(format)
        if dest_fmtchar is None:
            raise ValueError("memoryview: destination format must be a native single "
                             "character format prefixed with an optional '@'")

        src_fmtchar, _ = get_native_fmtchar(view.format)
        if not is_byte_format(src_fmtchar) and not is_byte_format(dest_fmtchar):
            raise TypeError("memoryview: cannot cast between two non-byte formats")

        if (view.len % itemsize) != 0:
            raise TypeError("memoryview: length is not a multiple of itemsize")

        view.format = get_native_fmtstr(format)
        if view.format is None:
            # NOT_REACHED: get_native_fmtchar() already validates the format.
            raise RuntimeError("memoryview: internal error")

        view.itemsize   = itemsize
        view.ndim       = 1
        view.shape[0]   = view.len // view.itemsize
        view.strides[0] = view.itemsize
        view.suboffsets = None

        self._init_flags(strict_py3=bool(self._flags | _Py_MEMORYVIEW_STRICT_PY3))

    def _cast_to_ND(self, shape, ndim):

        # Cast a 1-D array to a new shape. The result array will be C-contiguous.
        # If the result array does not have exactly the same byte length as the
        # input array, raise ValueError.

        view = self._view

        assert view.ndim        == 1               # ndim from _cast_to_1D()
        #assert Py_SIZE(self)   == 3 * (ndim or 1) # ndim of result array
        #assert view.shape      == addressof(self._ob_array)
        #assert view.strides    == addressof(self._ob_array) + (ndim or 1)
        assert not view.suboffsets # NULL

        view.ndim = ndim
        if view.ndim == 0:
            len = view.itemsize
            view.shape   = None
            view.strides = None
        else:
            len = Py_buff.copy_shape(view, shape)
            Py_buff.init_strides_from_shape(view)

        if len != view.len:
            raise TypeError("memoryview: product(shape) * itemsize != buffer size")

        self._init_flags(strict_py3=bool(self._flags | _Py_MEMORYVIEW_STRICT_PY3))

    def __len__(self):

        self._check_released()
        view = self._view
        return 1 if view.ndim == 0 else view.shape[0]

    def __getitem__(self, idx):

        # mv[obj] returns an object holding the data for one element if obj
        # fully indexes the memoryview or another memoryview object if it
        # does not.
        #
        # 0-d memoryview objects can be referenced using mv[...] or mv[()]
        # but not with anything else.

        self._check_released()
        view = self._view

        if view.ndim == 0:

            if idx is Ellipsis:

                return self

            elif isinstance(idx, tuple) and not idx:

                fmt = Py_buff.adjust_fmt(view)
                return unpack_single(view.buf, fmt,
                                     strict_py3=bool(self._flags | _Py_MEMORYVIEW_STRICT_PY3))

            else:
                raise TypeError("invalid indexing of 0-dim memory")

        else: # view.ndim != 0

            if hasattr(idx, "__index__"):

                idx = PyNumber_AsSsize_t(idx, IndexError)

                # Return the item at idx. In a one-dimensional view, this is an object
                # with the type specified by view.format. Otherwise, the item is a sub-view.

                fmt = Py_buff.adjust_fmt(view)

                if view.ndim != 1:
                    raise NotImplementedError("multi-dimensional sub-views are not implemented")

                return unpack_single(Py_buff.ptr_from_index(view, idx), fmt,
                                     strict_py3=bool(self._flags | _Py_MEMORYVIEW_STRICT_PY3))

            elif isinstance(idx, slice):

                sliced = memoryview._new_view(view, self._mbuf)
                Py_buff.init_slice(sliced._view, idx, 0)
                Py_buff.init_len(sliced._view)
                sliced._init_flags(strict_py3=bool(self._flags | _Py_MEMORYVIEW_STRICT_PY3))

                return sliced

            elif is_multiindex(idx):

                # Return the item at position *idx* (a tuple of indices).

                fmt = Py_buff.adjust_fmt(view)

                if len(idx) < view.ndim:
                    raise NotImplementedError("sub-views are not implemented")

                return unpack_single(Py_buff.ptr_from_tuple(view, idx), fmt,
                                     strict_py3=bool(self._flags | _Py_MEMORYVIEW_STRICT_PY3))

            elif is_multislice(idx):

                raise NotImplementedError("multi-dimensional slicing is not implemented")

            else:
                raise TypeError("memoryview: invalid slice key");

    def __setitem__(self, idx, value):

        self._check_released()
        view = self._view

        fmt = Py_buff.adjust_fmt(view)

        if view.readonly:
            raise TypeError("cannot modify read-only memory")

        if view.ndim == 0:

            if idx is Ellipsis:

                pack_single(view.buf, value, fmt)

            elif isinstance(idx, tuple) and not idx:

                pack_single(view.buf, value, fmt)

            else:
                raise TypeError("invalid indexing of 0-dim memory")

        else: # view.ndim != 0

            if hasattr(idx, "__index__"):

                if view.ndim > 1:
                    raise NotImplementedError("sub-views are not implemented")

                idx = PyNumber_AsSsize_t(idx, IndexError)

                pack_single(Py_buff.ptr_from_index(view, idx), value, fmt)

            elif isinstance(idx, slice) and view.ndim == 1:

                # one-dimensional: fast path

                if isinstance(value, memoryview):
                    value_view = value._view
                    alloc_view = None
                else:
                    # value must be Py_buffer exporter
                    value_view = alloc_view = Py_buffer()
                    PyObject_GetBuffer(value, value_view, Py_buffer.PyBUF_FULL_RO)

                try:
                    sliced_view = ct_clone(view)
                    sliced_view.shape = (c_ssize_t * 3)()
                    sliced_view.shape[0] = view.shape[0]
                    sliced_view.strides = ct_ptr_add(sliced_view.shape, 1 * sizeof(c_ssize_t))
                    sliced_view.strides[0] = view.strides[0]
                    if view.suboffsets:
                        sliced_view.suboffsets = ct_ptr_add(sliced_view.strides, 1 * sizeof(c_ssize_t))
                        sliced_view.suboffsets[0] = view.suboffsets[0]
                    Py_buff.init_slice(sliced_view, idx, 0)
                    Py_buff.init_len(sliced_view)
                    Py_buff.copy_buffer(sliced_view, value_view)
                finally:
                    if alloc_view is not None:
                        PyBuffer_Release(alloc_view); alloc_view = None

            elif is_multiindex(idx):

                if len(idx) < view.ndim:
                    raise NotImplementedError("sub-views are not implemented")

                pack_single(Py_buff.ptr_from_tuple(view, idx), value, fmt)

            elif isinstance(idx, slice) or is_multislice(idx):

                # Call __getitem__() to produce a sliced lvalue, then copy
                # rvalue into lvalue. This is already implemented in _testbuffer.c.

                raise NotImplementedError("memoryview slice assignments are currently restricted "
                                          "to ndim = 1")
            else:
                raise TypeError("memoryview: invalid slice key")

    def __delitem__(self, idx):

        self._check_released()
        raise TypeError("cannot modify read-only memory"
                        if self._view.readonly else
                        "cannot delete memory")

    def __hash__(self):

        if self._hash != -1:
            return self._hash

        self._check_released()
        view = self._view

        if not view.readonly:
            raise ValueError("cannot hash writable memoryview object")

        fmtchar, _ = get_native_fmtchar(view.format)
        if not is_byte_format(fmtchar):
            raise ValueError("memoryview: hashing is restricted to formats 'B', 'b' or 'c'")

        try:
            view.obj
        except ValueError:
            pass
        else:
            if hash(view.obj) == -1:
                # Keep the original error message
                return -1

        if self._flags & (_Py_MEMORYVIEW_SCALAR | _Py_MEMORYVIEW_C):
            buf = cast(view.buf, POINTER(c_char))[:view.len]
        else:
            buf = create_string_buffer(view.len)
            Py_buff.buffer_to_contiguous(view, 'C', buf)
            buf = buf.raw

        # Can't fail
        self._hash = hash(buf)
        return self._hash

    def __eq__ (self, other):

        if self._base_inaccessible():
            return self is other

        self_view = self._view

        if isinstance(other, memoryview):

            if other._base_inaccessible():
                return self is other

            other_view = other._view
            alloc_view = None
        else:
            other_view = alloc_view = Py_buffer()
            try:
                PyObject_GetBuffer(other, other_view, Py_buffer.PyBUF_FULL_RO)
            except Exception:
                return NotImplemented

        eq = NotImplemented

        try:
            try:
                if not Py_buff.equiv_shape(self_view, other_view):
                    return False
            except Exception:
                return False

            # Use fast unpacking for identical primitive C type formats.

            self_fmtchar,  _ = get_native_fmtchar(self_view.format)
            other_fmtchar, _ = get_native_fmtchar(other_view.format)
            if self_fmtchar  is None: self_fmtchar  = b'_'
            if other_fmtchar is None: other_fmtchar = b'_'

            if self_fmtchar == b'_' or other_fmtchar == b'_' or self_fmtchar != other_fmtchar:
                # Use struct module unpacking.
                # NOTE: Even for equal format strings, memcmp() cannot be used for item
                # comparison since it would give incorrect results in the case of NaNs
                # or uninitialized padding bytes.
                self_fmtchar = b'_'
                try:
                    self_unpack  = struct_get_unpacker(self_view.format,  self_view.itemsize)
                    other_unpack = struct_get_unpacker(other_view.format, other_view.itemsize)
                    # Translate a StructError to "not equal". Preserve other exceptions.
                    # XXX Cannot get at StructError directly?
                except (ImportError, MemoryError):
                    raise exc
                except Exception as exc:
                    # StructError: invalid or unknown format -> not equal
                    return False
            else:
                self_unpack  = None
                other_unpack = None

            if self_view.ndim == 0:
                eq = unpack_cmp(self_view.buf, other_view.buf,
                                self_fmtchar, self_unpack, other_unpack)
            else:
                eq = memoryview._cmp(self_view.buf, other_view.buf,
                                     self_view.ndim, self_view.shape,
                                     self_view.strides,  self_view.suboffsets,
                                     other_view.strides, other_view.suboffsets,
                                     self_fmtchar, self_unpack, other_unpack)
        finally:
            if alloc_view is not None:
                PyBuffer_Release(alloc_view); alloc_view = None

        if eq == NotImplemented:
            return NotImplemented
        elif eq < 0:
            # exception
            return 0 # NULL;
        else:
            return bool(eq)

    @staticmethod
    def _cmp(ptr_p, ptr_q, ndim, shape,
             strides_p, suboffsets_p,
             strides_q, suboffsets_q,
             fmtchar, unpack_p, unpack_q):

        # const char* ptr_p, const char* ptr_q,
        # c_ssize_t ndim, const c_ssize_t* shape,
        # const c_ssize_t* strides_p, const c_ssize_t* suboffsets_p,
        # const c_ssize_t* strides_q, const c_ssize_t* suboffsets_q,
        # char fmtchar, unpacker* unpack_p, unpacker* unpack_q

        # Recursively compare two multi-dimensional arrays that have the same logical structure.
        # Assumption: ndim >= 1.

        assert ndim >= 1
        assert shape
        assert strides_p
        assert strides_q

        is_ndim_1 = (ndim == 1)

        stride_p = strides_p[0]
        stride_q = strides_q[0]
        for i in range(shape[0]):
            eq = (unpack_cmp(Py_buff.adjust_ptr(ptr_p, suboffsets_p),
                            Py_buff.adjust_ptr(ptr_q, suboffsets_q),
                            fmtchar, unpack_p, unpack_q)
                  if is_ndim_1 else
                  memoryview._cmp(Py_buff.adjust_ptr(ptr_p, suboffsets_p),
                                  Py_buff.adjust_ptr(ptr_q, suboffsets_q),
                                  ndim - 1,
                                  ct_ptr_add(shape,        sizeof(c_ssize_t)),
                                  ct_ptr_add(strides_p,    sizeof(c_ssize_t)),
                                  ct_ptr_add(suboffsets_p, sizeof(c_ssize_t))
                                  if suboffsets_p else POINTER(c_ssize_t)(),
                                  ct_ptr_add(strides_q,    sizeof(c_ssize_t)),
                                  ct_ptr_add(suboffsets_q, sizeof(c_ssize_t))
                                  if suboffsets_q else POINTER(c_ssize_t)(),
                                  fmtchar, unpack_p, unpack_q))
            if eq is NotImplemented or eq <= 0:
                return eq
            ptr_p += stride_p
            ptr_q += stride_q

        return True

    def __ne__(self, other):

        eq = self.__eq__(other)
        return NotImplemented if eq is NotImplemented else not eq

    def hex(self):

        """hex($self, /)\n""" \
        """--\n\n""" \
        """Return the data in the buffer as a string of hexadecimal numbers."""

        self._check_released()
        view = self._view

        if self._flags & (_Py_MEMORYVIEW_SCALAR | _Py_MEMORYVIEW_C):
            buf = cast(view.buf, POINTER(c_char))[:view.len]
        else:
            buf = self.tobytes()
        return binascii.hexlify(buf).decode("ascii")

    def __enter__(self):

        self._check_released()
        return self

    def __exit__(self, *exc_info):

        del exc_info
        return self.release()

    def __repr__(self):

        return ("<released memory at 0x{:08X}>"
                if self._flags & _Py_MEMORYVIEW_RELEASED else
                "<memory at 0x{:08X}>").format(id(self))

    #----------------------------------------------------------------------------#
    #                          extension for ctypes                              #
    #----------------------------------------------------------------------------#

    @property
    def as_ctypes(self):

        self._check_released()
        view = self._view

        if not view.buf:
            raise ValueError("operation forbidden on released buffer object")

        if not view.buf:
            return None

        buffer = (c_char * view.len).from_address(view.buf)
        if view.readonly:
            buffer = type(buffer).from_buffer_copy(buffer)
        else:
            buffer._obj = view.obj
        return buffer

    #----------------------------------------------------------------------------#
    #                          getbuffer/releasebuffer                           #
    #----------------------------------------------------------------------------#

    def __getbuffer__(self, view, flags):

        # Py_buffer view, int flags -> int

        self._check_released()

        # start with complete information
        ct_copy(view, self._view)
        view.obj = py_object() # NULL

        if (flags & Py_buffer.PyBUF_WRITABLE) == Py_buffer.PyBUF_WRITABLE and self._view.readonly:
            raise BufferError("memoryview: underlying buffer is not writable")

        if (flags & Py_buffer.PyBUF_FORMAT) != Py_buffer.PyBUF_FORMAT:
            # NULL indicates that the buffer's data type has been cast to 'B'.
            # view.itemsize is the _previous_ itemsize. If shape is present,
            # the equality product(shape) * itemsize = len still holds at this
            # point. The equality calcsize(format) = itemsize does _not_ hold
            # from here on!
            view.format = None

        if ((flags & Py_buffer.PyBUF_C_CONTIGUOUS) == Py_buffer.PyBUF_C_CONTIGUOUS and
            not (self._flags & (_Py_MEMORYVIEW_SCALAR | _Py_MEMORYVIEW_C))):
            raise BufferError("memoryview: underlying buffer is not C-contiguous")

        if ((flags & Py_buffer.PyBUF_F_CONTIGUOUS) == Py_buffer.PyBUF_F_CONTIGUOUS and
            not (self._flags & (_Py_MEMORYVIEW_SCALAR | _Py_MEMORYVIEW_FORTRAN))):
            raise BufferError("memoryview: underlying buffer is not Fortran contiguous")

        if ((flags & Py_buffer.PyBUF_ANY_CONTIGUOUS) == Py_buffer.PyBUF_ANY_CONTIGUOUS and
            not (self._flags & (_Py_MEMORYVIEW_SCALAR | _Py_MEMORYVIEW_C | _Py_MEMORYVIEW_FORTRAN))):
            raise BufferError("memoryview: underlying buffer is not contiguous")

        if ((flags & Py_buffer.PyBUF_INDIRECT) != Py_buffer.PyBUF_INDIRECT and
            (self._flags & _Py_MEMORYVIEW_PIL)):
            raise BufferError("memoryview: underlying buffer requires suboffsets")

        if (flags & Py_buffer.PyBUF_STRIDES) != Py_buffer.PyBUF_STRIDES:
            if not (self._flags & (_Py_MEMORYVIEW_SCALAR | _Py_MEMORYVIEW_C)):
                raise BufferError("memoryview: underlying buffer is not C-contiguous")
            view.strides = None

        if (flags & Py_buffer.PyBUF_ND) != Py_buffer.PyBUF_ND:
            # PyBUF_SIMPLE or PyBUF_WRITABLE: at this point buf is C-contiguous,
            # so self._view.buf = ndbuf.data.
            if view.format is not None:
                # PyBUF_SIMPLE | PyBUF_FORMAT and PyBUF_WRITABLE | PyBUF_FORMAT do not make sense.
                raise BufferError("memoryview: cannot cast to unsigned bytes if the format flag "
                                  "is present")

            # product(shape) * itemsize = len and calcsize(format) = itemsize
            # do _not_ hold from here on!
            view.ndim  = 1
            view.shape = None

        view.obj = py_object(self)

        self._exports += 1

    def __releasebuffer__(self, view):

        # Py_buffer view

        self._exports -= 1

        # PyBuffer_Release() decrements view.obj after this function returns.

    #------------------------------------------------------------------------#

    def _check_released(self):

        if self._base_inaccessible():
            raise ValueError("operation forbidden on released memoryview object")

    def _base_inaccessible(self):

        # In the process of breaking reference cycles managedbuffer.__del__()
        # can be called before self.release().

        return ((self._flags       & _Py_MEMORYVIEW_RELEASED) or
                (self._mbuf._flags & _Py_MANAGED_BUFFER_RELEASED))

    def _init_flags(self, strict_py3=False):

        # Initialize memoryview buffer properties.

        view = self._view

        flags = 0x0
        if view.ndim == 0:
            flags |= (_Py_MEMORYVIEW_SCALAR | _Py_MEMORYVIEW_C | _Py_MEMORYVIEW_FORTRAN)
        elif view.ndim == 1:
            # Fast contiguity test. Must ensure suboffsets == NULL and ndim == 1.
            if view.shape[0] == 1 or view.strides[0] == view.itemsize:
                flags |= (_Py_MEMORYVIEW_C | _Py_MEMORYVIEW_FORTRAN)
        else:
            if PyBuffer_IsContiguous(view, b'C'): flags |= _Py_MEMORYVIEW_C
            if PyBuffer_IsContiguous(view, b'F'): flags |= _Py_MEMORYVIEW_FORTRAN

        if view.suboffsets:
            flags &= ~(_Py_MEMORYVIEW_C | _Py_MEMORYVIEW_FORTRAN)
            flags |= _Py_MEMORYVIEW_PIL

        if strict_py3:
            self._flags |= _Py_MEMORYVIEW_STRICT_PY3

        self._flags = flags

#PyTypeObject PyMemoryView_Type =
#
#    PyVarObject_HEAD_INIT(&PyType_Type,  0)
#    offsetof(memoryview, _ob_array),     # tp_basicsize
#    sizeof(c_ssize_t),                   # tp_itemsize

#----------------------------------------------------------------------------#
#                                Constructors                                #
#----------------------------------------------------------------------------#

#def PyMemoryView_FromMemory(char* mem, c_ssize_t size, int flags):
def  PyMemoryView_FromMemory(mem, size, flags):

    # Expose a raw memory area as a view of contiguous bytes. flags can be
    # PyBUF_READ or PyBUF_WRITE. view.format is set to "B" (unsigned bytes).
    # The memoryview has complete buffer information.

    assert mem
    assert flags in (Py_buffer.PyBUF_READ, Py_buffer.PyBUF_WRITE)

    mbuf = managedbuffer()
    readonly = 0 if flags == Py_buffer.PyBUF_WRITE else 1
    PyBuffer_FillInfo(byref(mbuf), py_object(), c_void_p(mem), size,
                      readonly, Py_buffer.PyBUF_FULL_RO)

    return memoryview._new_view(mbuf, mbuf)

#def PyMemoryView_FromBuffer(Py_buffer* info):
def  PyMemoryView_FromBuffer(info):

    # Create a memoryview from a given buffer. For simple byte views,
    # PyMemoryView_FromMemory() should be used instead.
    # This function is the only entry point that can create a master buffer
    # without full information. Because of this fact Py_buff.init_shape_strides()
    # must be able to reconstruct missing values.

    if not info.buf:
        raise ValueError("PyMemoryView_FromBuffer(): info->buf must not be NULL")

    mbuf = managedbuffer()
    # info.obj is either NULL or a borrowed reference.
    # This reference should not be decremented in PyBuffer_Release().
    memmove(byref(mbuf), byref(info), sizeof(Py_buffer)) # copy
    mbuf.obj = py_object() # NULL

    return memoryview._new_view(mbuf, mbuf)

#def __memory_from_contiguous_copy(Py_buffer* src, char order):
def  __memory_from_contiguous_copy(src, order):

    # Return a memoryview that is based on a contiguous copy of src.
    # Assumptions: src has PyBUF_FULL_RO information, src.ndim > 0.
    #
    # Ownership rules:
    #   1) As usual, the returned memoryview has a private copy
    #      of src.shape, src.strides and src.suboffsets.
    #   2) src.format is copied to the master buffer and released
    #      in managedbuffer.__del__(). The releasebufferproc of the bytes
    #      object is NULL, so it does not matter that managedbuffer.__del__()
    #      passes the altered format pointer to PyBuffer_Release().

    assert src.ndim > 0
    assert src.shape

    bytes = b"\0" * src.len
    mbuf = managedbuffer(bytes)
    del bytes

    # Copy the format string from a base object that might vanish.
    if src.format is not None:
        cp = PyMem_Malloc(strlen(src.format) + 1) # char*
        mbuf.format = strcpy(cp, src.format)

    mv = memoryview._new_incomplete_view(mbuf, mbuf, src.ndim)
    del mbuf
    dest = mv._view

    # shared values are initialized correctly except for itemsize
    dest.itemsize = src.itemsize
    for i in range(src.ndim):
        dest.shape[i] = src.shape[i]
    Py_buff.init_strides_from_shape(dest, order)
    dest.suboffsets = None
    mv._init_flags()
    Py_buff.copy_buffer(dest, src)

    return mv

#def PyMemoryView_GetContiguous(PyObject *obj, int buffertype, char order):
def  PyMemoryView_GetContiguous(obj, buffertype, order):

    # Return a new memoryview object based on a contiguous exporter with
    # buffertype={PyBUF_READ, PyBUF_WRITE} and order={'C', 'F'ortran, or 'A'ny}.
    # The logical structure of the input and output buffers is the same
    # (i.e. tolist(input) == tolist(output)), but the physical layout in
    # memory can be explicitly chosen.
    #
    # As usual, if buffertype=PyBUF_WRITE, the exporter's buffer must be writable,
    # otherwise it may be writable or read-only.
    #
    # If the exporter is already contiguous with the desired target order,
    # the memoryview will be directly based on the exporter.
    #
    # Otherwise, if the buffertype is PyBUF_READ, the memoryview will be
    # based on a new bytes object. If order={'C', 'A'ny}, use 'C' order,
    # 'F'ortran order otherwise.

    assert buffertype in (Py_buffer.PyBUF_READ, Py_buffer.PyBUF_WRITE)
    assert order in (b'C', b'F', b'A')

    mv = memoryview(obj)
    view = mv._view

    if buffertype == Py_buffer.PyBUF_WRITE and view.readonly:
        raise BufferError("underlying buffer is not writable")

    if PyBuffer_IsContiguous(view, order):
        return mv

    if buffertype == Py_buffer.PyBUF_WRITE:
        raise BufferError("writable contiguous buffer requested for a non-contiguous object.")

    return __memory_from_contiguous_copy(view, order)

class buffer_full:

    """ """
   # Py_buffer view;
   # c_ssize_t array[1];

#int PyBuffer_ToContiguous(void *buf, Py_buffer* src, c_ssize_t len, char order):
def  PyBuffer_ToContiguous(buf, src, len, order):

    assert order in (b'C', b'F', b'A')

    if len != src.len:
        raise ValueError("PyBuffer_ToContiguous: len != view->len")

    if PyBuffer_IsContiguous(src, order):

        memmove(buf, src.buf, len)
        return 0

    else:

        # Py_buff.buffer_to_contiguous() assumes PyBUF_FULL
        #buffer_full *fb = NULL;
        fb = PyMem_Malloc(sizeof *fb + 3 * src.ndim * (sizeof *fb.array))
        fb._view.ndim       = src.ndim
        fb._view.shape      = fb.array
        fb._view.strides    = fb.array + 1 * src.ndim
        fb._view.suboffsets = fb.array + 2 * src.ndim

        Py_buff.init_shared_values(fb._view, src)
        Py_buff.init_shape_strides(fb._view, src)
        Py_buff.init_suboffsets   (fb._view, src)

        return Py_buff.buffer_to_contiguous(fb._view, order, buf)

#----------------------------------------------------------------------------#
#            Optimized pack/unpack for all native format specifiers          #
#----------------------------------------------------------------------------#

# Timings with the ndarray from _testbuffer.c indicate that using the
# struct module is around 15x slower than the two functions below.

def unpack_single(ptr, fmt, strict_py3=False):

    # const void* ptr, const char* fmt

    # Unpack a single item.
    # 'fmt' can be any native format character in struct module syntax.
    # This function is very sensitive to small changes.
    # With this layout gcc automatically generates a fast jump table.

    global _unpack_single_funcs
    global _unpack_single_funcs_PY3
    unpack_funcs = _unpack_single_funcs_PY3 if strict_py3 else _unpack_single_funcs
    try:
        func = unpack_funcs[fmt[:1]]
    except KeyError:
        raise NotImplementedError("memoryview: format {} not supported".format(fmt)) from None
    return func(ptr)

_unpack_single_funcs_PY3 = {

    # boolean
    #ifdef HAVE_C99_BOOL
    b'?': lambda ptr: bool(cast(ptr, POINTER(c_bool))[0]),
    #else
    #b'?':lambda ptr: bool(cast(ptr, POINTER(c_byte))[0]),
    #endif

    # signed integers
    b'b': lambda ptr: cast(ptr, POINTER(c_byte ))[0],
    b'h': lambda ptr: cast(ptr, POINTER(c_short))[0],
    b'i': lambda ptr: cast(ptr, POINTER(c_int  ))[0],
    b'l': lambda ptr: cast(ptr, POINTER(c_long ))[0],

    # unsigned integers
    b'B': lambda ptr: cast(ptr, POINTER(c_ubyte ))[0],
    b'H': lambda ptr: cast(ptr, POINTER(c_ushort))[0],
    b'I': lambda ptr: cast(ptr, POINTER(c_uint  ))[0],
    b'L': lambda ptr: cast(ptr, POINTER(c_ulong ))[0],

    # native 64-bit
    #ifdef HAVE_LONG_LONG
    b'q': lambda ptr: cast(ptr, POINTER(c_longlong ))[0],
    b'Q': lambda ptr: cast(ptr, POINTER(c_ulonglong))[0],
    #endif

    # ssize_t and size_t
    b'n': lambda ptr: cast(ptr, POINTER(c_ssize_t))[0],
    b'N': lambda ptr: cast(ptr, POINTER(c_size_t ))[0],

    # floats
    b'f': lambda ptr: cast(ptr, POINTER(c_float ))[0],
    b'd': lambda ptr: cast(ptr, POINTER(c_double))[0],

    # bytes object
    b'c': lambda ptr: cast(ptr, POINTER(c_char))[0],

    # pointer
    b'P': lambda ptr: cast(ptr, POINTER(c_void_p))[0],
    }

_unpack_single_funcs = _unpack_single_funcs_PY3

def pack_single(ptr, value, fmt):

    # const void* ptr, PyObject* value, const char* fmt

    # Pack a single item.
    # 'fmt' can be any native format character in struct module syntax.

    global _pack_single_funcs
    try:
        func = _pack_single_funcs[fmt[:1]]
    except KeyError:
        raise NotImplementedError("memoryview: format {} not supported".format(fmt)) from None
    func(ptr, value, fmt)

def _pack_single_z(ptr, value, fmt):
    value = not not value
    # preserve original error
    #ifdef HAVE_C99_BOOL
    cast(ptr,  POINTER(c_bool))[0] = value
    #else
    #cast(ptr, POINTER(c_byte))[0] = value
    #endif

def _pack_single_b(ptr, value, fmt):
    try:
        value = PyNumber_Index(value)
        value = PyLong_AsLong(value)
    except Exception as exc:
        raise _fix_pack_error(exc, fmt)
    if not (SCHAR_MIN <= value <= SCHAR_MAX):
        raise _pack_value_error(fmt)
    cast(ptr, POINTER(c_byte))[0] = value

def _pack_single_h(ptr, value, fmt):
    try:
        value = PyNumber_Index(value)
        value = PyLong_AsLong(value)
    except Exception as exc:
        raise _fix_pack_error(exc, fmt)
    if not (SHRT_MIN <= value <= SHRT_MAX):
        raise _pack_value_error(fmt)
    cast(ptr, POINTER(c_short))[0] = value

def _pack_single_i(ptr, value, fmt):
    try:
        value = PyNumber_Index(value)
        value = PyLong_AsLong(value)
    except Exception as exc:
        raise _fix_pack_error(exc, fmt)
    if not (INT_MIN <= value <= INT_MAX):
        raise _pack_value_error(fmt)
    cast(ptr, POINTER(c_int))[0] = value

def _pack_single_l(ptr, value, fmt):
    try:
        value = PyNumber_Index(value)
        value = PyLong_AsLong(value)
    except Exception as exc:
        raise _fix_pack_error(exc, fmt)
    cast(ptr, POINTER(c_long))[0] = value

def _pack_single_B(ptr, value, fmt):
    try:
        value = PyNumber_Index(value)
        value = PyLong_AsUnsignedLong(value)
    except Exception as exc:
        raise _fix_pack_error(exc, fmt)
    if value > UCHAR_MAX:
        raise _pack_value_error(fmt)
    cast(ptr, POINTER(c_ubyte))[0] = value

def _pack_single_H(ptr, value, fmt):
    try:
        value = PyNumber_Index(value)
        value = PyLong_AsUnsignedLong(value)
    except Exception as exc:
        raise _fix_pack_error(exc, fmt)
    if value > USHRT_MAX:
        raise _pack_value_error(fmt)
    cast(ptr, POINTER(c_ushort))[0] = value

def _pack_single_I(ptr, value, fmt):
    try:
        value = PyNumber_Index(value)
        value = PyLong_AsUnsignedLong(value)
    except Exception as exc:
        raise _fix_pack_error(exc, fmt)
    if value > UINT_MAX:
        raise _pack_value_error(fmt)
    cast(ptr, POINTER(c_uint))[0] = value

def _pack_single_L(ptr, value, fmt):
    try:
        value = PyNumber_Index(value)
        value = PyLong_AsUnsignedLong(value)
    except Exception as exc:
        raise _fix_pack_error(exc, fmt)
    cast(ptr, POINTER(c_ulong))[0] = value

def _pack_single_q(ptr, value, fmt):
    try:
        value = PyNumber_Index(value)
        value = PyLong_AsLongLong(value)
    except Exception as exc:
        raise _fix_pack_error(exc, fmt)
    cast(ptr, POINTER(c_longlong))[0] = value

def _pack_single_Q(ptr, value, fmt):
    try:
        value = PyNumber_Index(value)
        value = PyLong_AsUnsignedLongLong(value)
    except Exception as exc:
        raise _fix_pack_error(exc, fmt)
    cast(ptr, POINTER(c_ulonglong))[0] = value

def _pack_single_n(ptr, value, fmt):
    try:
        value = PyNumber_Index(value)
        value = PyLong_AsSsize_t(value)
    except Exception as exc:
        raise _fix_pack_error(exc, fmt)
    cast(ptr, POINTER(c_ssize_t))[0] = value

def _pack_single_N(ptr, value, fmt):
    try:
        value = PyNumber_Index(value)
        value = PyLong_AsSize_t(value)
    except Exception as exc:
        raise _fix_pack_error(exc, fmt)
    cast(ptr, POINTER(c_size_t))[0] = value

def _pack_single_f(ptr, value, fmt):
    try:
        value = PyFloat_AsDouble(value)
        value = c_float(value)
    except Exception as exc:
        raise _fix_pack_error(exc, fmt)
    cast(ptr, POINTER(c_float))[0] = value

def _pack_single_d(ptr, value, fmt):
    try:
        value = PyFloat_AsDouble(value)
    except Exception as exc:
        raise _fix_pack_error(exc, fmt)
    cast(ptr, POINTER(c_double))[0] = value

def _pack_single_c(ptr, value, fmt):
    if not isinstance(value, bytes):
        raise _pack_type_error(fmt)
    if len(value) != 1:
        raise _pack_value_error(fmt)
    cast(ptr, POINTER(c_char))[0] = value[0]

def _pack_single_P(ptr, value, fmt):
    try:
        value = c_void_p(value)
    except Exception as exc:
        raise _fix_pack_error(exc, fmt)
    cast(ptr, POINTER(c_void_p))[0] = value

def _fix_pack_error(exc, fmt):

    # exc, const char* fmt

    # Fix exceptions:
    #   1) Include format string in the error message.
    #   2) OverflowError -> ValueError.
    #   3) The error message from PyNumber_Index() is not ideal.

    try:
        raise exc
    except TypeError:
        return _pack_type_error(fmt)
    except (OverflowError, ValueError):
        return _pack_value_error(fmt)
    else:
        return exc

def _pack_type_error(fmt):

    return TypeError("memoryview: invalid type for format '{}'".format(fmt))

def _pack_value_error(fmt):

    return ValueError("memoryview: invalid value for format '{}'".format(fmt))

_pack_single_funcs = {

    # boolean
    b'?': _pack_single_z,

    # signed integers
    b'b': _pack_single_b,
    b'h': _pack_single_h,
    b'i': _pack_single_i,
    b'l': _pack_single_l,

    # unsigned integers
    b'B': _pack_single_B,
    b'H': _pack_single_H,
    b'I': _pack_single_I,
    b'L': _pack_single_L,

    # native 64-bit
    #ifdef HAVE_LONG_LONG
    b'q': _pack_single_q,
    b'Q': _pack_single_Q,
    #endif

    # ssize_t and size_t
    b'n': _pack_single_n,
    b'N': _pack_single_N,

    # floats
    b'f': _pack_single_f,
    b'd': _pack_single_d,

    # bytes object
    b'c': _pack_single_c,

    # pointer
    b'P': _pack_single_P,
    }

#--------------------------------------------------------------#
#                 unpack using the struct module               #
#--------------------------------------------------------------#

class unpacker(object):

    # For reasonable performance it is necessary to cache all objects required
    # for unpacking. An unpacker can handle the format passed to unpack_from().
    # Invariant: All pointer fields of the struct should either be NULL or valid
    # pointers.

    def __new__(cls):

        self = super(unpacker, cls).__new__(cls)
        self.unpack_from = NULL  # PyObject* unpack_from; # Struct.unpack_from(format)
        self.mview       = NULL  # PyObject* mview;       # cached memoryview
        self.item        = NULL  # char*     item;        # buffer for mview
        self.itemsize    = 0     # c_ssize_t itemsize;    # len(item)
        return self

    def __del__(self):

        PyMem_Free(self.item)

def struct_get_unpacker(fmt, itemsize):

    # const char* fmt, c_ssize_t itemsize

    # Return a new unpacker for the given format.

    format = PyBytes_FromString(fmt)
    structobj = struct.Struct(format)

    unp = unpacker()
    unp.unpack_from = structobj.unpack_from
    unp.item        = PyMem_Malloc(itemsize)
    unp.itemsize    = itemsize
    unp.mview       = PyMemoryView_FromMemory(unp.item, itemsize, Py_buffer.PyBUF_WRITE)

    return unp

#--------------------------------------------------------------#
#                        Comparisons                           #
#--------------------------------------------------------------#

def unpack_cmp(ptr_p, ptr_q, fmtchar, unpack_p, unpack_q):

    # const void* ptr_p, const void* ptr_q, char fmtchar, unpacker* unpack_p, unpacker* unpack_q):

    # Unpack and compare single items of ptr_p and ptr_q. If both ptr_p and ptr_q
    # have the same single element native format, the comparison uses a fast path
    # (gcc creates a jump table and converts memmove into simple assignments on x86/x64).
    #
    # Otherwise, the comparison is delegated to the struct module, which is 30-60x slower.

    if fmtchar == b'_':
        # use the struct module
        global _unpack_cmp_struct
        return _unpack_cmp_struct(ptr_p, ptr_q, unpack_p, unpack_q)
    else:
        global _unpack_cmp_funcs
        try:
            func = _unpack_cmp_funcs[fmtchar]
        except KeyError:
            # NOT REACHED
            raise RuntimeError("memoryview: internal error in richcompare") from None
        else:
            return func(ptr_p, ptr_q)

_unpack_cmp_funcs = {

    # boolean
    #ifdef HAVE_C99_BOOL
    b'?': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_bool))[0] == cast(ptr_q, POINTER(c_bool))[0],
    #else
    #b'?':lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_byte))[0] == cast(ptr_q, POINTER(c_byte))[0],
    #endif

    # signed integers
    b'b': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_byte ))[0] == cast(ptr_q, POINTER(c_byte ))[0],
    b'h': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_short))[0] == cast(ptr_q, POINTER(c_short))[0],
    b'i': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_int  ))[0] == cast(ptr_q, POINTER(c_int  ))[0],
    b'l': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_long ))[0] == cast(ptr_q, POINTER(c_long ))[0],

    # unsigned integers
    b'B': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_ubyte ))[0] == cast(ptr_q, POINTER(c_ubyte ))[0],
    b'H': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_ushort))[0] == cast(ptr_q, POINTER(c_ushort))[0],
    b'I': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_uint  ))[0] == cast(ptr_q, POINTER(c_uint  ))[0],
    b'L': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_ulong ))[0] == cast(ptr_q, POINTER(c_ulong ))[0],

    # native 64-bit
    #ifdef HAVE_LONG_LONG
    b'q': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_longlong ))[0] == cast(ptr_q, POINTER(c_longlong ))[0],
    b'Q': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_ulonglong))[0] == cast(ptr_q, POINTER(c_ulonglong))[0],
    #endif

    # ssize_t and size_t
    b'n': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_ssize_t))[0] == cast(ptr_q, POINTER(c_ssize_t))[0],
    b'N': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_size_t ))[0] == cast(ptr_q, POINTER(c_size_t ))[0],

    # floats
    # XXX DBL_EPSILON?
    b'f': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_float ))[0] == cast(ptr_q, POINTER(c_float ))[0],
    b'd': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_double))[0] == cast(ptr_q, POINTER(c_double))[0],

    # bytes object #!!! sprawdzic czy dobrze !!!
    b'c': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_char))[0] == cast(ptr_q, POINTER(c_char))[0],

    # pointer #!!! sprawdzic czy dobrze !!!
    b'P': lambda ptr_p, ptr_q: cast(ptr_p, POINTER(c_void_p))[0] == cast(ptr_q, POINTER(c_void_p))[0],
    }

def _unpack_cmp_struct(ptr_p, ptr_q, unpack_p, unpack_q):

    assert unpack_p
    assert unpack_q

    # At this point any exception from the struct module should not be
    # StructError, since both formats have been accepted already.

    return struct_unpack_single(ptr_p, unpack_p) == struct_unpack_single(ptr_q, unpack_q)

def struct_unpack_single(ptr, unpack):

    memmove(unpack.item, ptr, unpack.itemsize)
    v = unpack.unpack_from(unpack.mview)
    return v[0] if len(v) == 1 else v

#--------------------------------------------------------------#
#                   Casting format and shape                   #
#--------------------------------------------------------------#

def get_native_fmtchar(fmt):

    # const char* fmt

    at = 1 if fmt[:1] == b'@' else 0

    if len(fmt) != at + 1:
        return (None, -1)

    fch = fmt[at:at+1]

    global _native_fmt_sizes
    size = _native_fmt_sizes.get(fch, -1)
    return (fch, size) if size > 0 else (None, -1)

def get_native_fmtstr(fmt):

    # const char* fmt -> char*

    if not fmt:
        return None

    at = 1 if fmt[:1] == b'@' else 0

    if len(fmt) != at + 1:
        return None

    fch = fmt[at:at+1]

    global _native_fmt_chars
    return ((b"@" + fch) if at else fch) if fch in _native_fmt_chars else None

def is_byte_format(fch):

    global _native_byte_fmt_chars
    return fch in _native_byte_fmt_chars

_native_fmt_sizes = {
    b'c': sizeof(c_char),
    b'b': sizeof(c_byte),
    b'B': sizeof(c_ubyte),
    b'h': sizeof(c_short),
    b'H': sizeof(c_ushort),
    b'i': sizeof(c_int),
    b'I': sizeof(c_uint),
    b'l': sizeof(c_long),
    b'L': sizeof(c_ulong),
    #ifdef HAVE_LONG_LONG
    b'q': sizeof(c_longlong),
    b'Q': sizeof(c_ulonglong),
    #endif
    b'n': sizeof(c_ssize_t),
    b'N': sizeof(c_size_t),  #!!! bylo (blednie?): c_ssize_t !!!
    b'f': sizeof(c_float),
    b'd': sizeof(c_double),
    #ifdef HAVE_C99_BOOL
    b'?': sizeof(c_bool),
    #else
    #'?':sizeof(c_byte),
    #endif
    b'P': sizeof(c_void_p)
    }

_native_fmt_chars = (
    b'c', b'b', b'B', b'h', b'H', b'i', b'I', b'l', b'L',
    #ifdef HAVE_LONG_LONG
    b'q', b'Q',
    #endif
    b'n', b'N', b'f', b'd', b'?', b'P'
    )

_native_byte_fmt_chars = (
    b'c', b'b', b'B'
    )

#----------------------------------------------------------------------------#
#                         Copy memoryview buffers                            #
#----------------------------------------------------------------------------#

# The functions in this section take a source and a destination buffer
# with the same logical structure: format, itemsize, ndim and shape
# are identical, with ndim > 0.
#
# NOTE: All buffers are assumed to have PyBUF_FULL information,
#       which is the case for memoryviews!

class Py_buff:

    @staticmethod
    def init_shared_values(dest, src):

        # dest=Py_buffer, src=Py_buffer

        # Initialize values that are shared with the managed buffer.

        dest.obj      = py_object(src.obj)
        dest.buf      = src.buf
        dest.len      = src.len
        dest.itemsize = src.itemsize
        dest.readonly = src.readonly
        dest.format   = src.format if src.format is not None else c_char_p(b"B")
        dest.internal = src.internal

    @staticmethod
    def init_shape_strides(dest, src):

        # dest=Py_buffer, src=Py_buffer

        # Copy shape and strides. Reconstruct missing values.

        if src.ndim == 0:
            dest.shape   = None
            dest.strides = None
        elif src.ndim == 1:
            dest.shape[0]   = src.shape[0]   if src.shape   else (src.len // src.itemsize)
            dest.strides[0] = src.strides[0] if src.strides else src.itemsize
        else:
            for i in range(src.ndim):
                dest.shape[i] = src.shape[i]
            if src.strides:
                for i in range(src.ndim):
                    dest.strides[i] = src.strides[i]
            else:
                Py_buff.init_strides_from_shape(dest)

    @staticmethod
    def init_suboffsets(dest, src):

        # dest=Py_buffer, src=Py_buffer

        if not src.suboffsets:
            dest.suboffsets = None
        else:
            for i in range(src.ndim):
                dest.suboffsets[i] = src.suboffsets[i]

    @staticmethod
    def init_slice(view, idx, dim):

        # view=Py_buffer, idx=slice, dim=int

        start, stop, step = idx.indices(view.shape[dim])

        if not view.suboffsets or dim == 0:
            view.buf += view.strides[dim] * start
        else:
            n = dim - 1
            while n >= 0 and view.suboffsets[n] < 0: n -= 1
            if n < 0:
                # all suboffsets are negative
                view.buf += view.strides[dim] * start
            else:
                view.suboffsets[n] += view.strides[dim] * start

        if (step > 0 and start >= stop) or (step < 0 and stop >= start):
            slicelength = 0
        else:
            slicelength = (stop - start - (1 if step >= 0 else -1)) // step + 1

        view.shape[dim]    = slicelength
        view.strides[dim] *= step

    @staticmethod
    def init_len(view):

        # view=Py_buffer

        # len = product(shape) * itemsize

        len = 1
        for i in range(view.ndim):
            len *= view.shape[i]
        len *= view.itemsize

        view.len = len

    @staticmethod
    def init_strides_from_shape(view, order='C'):

        # view=Py_buffer

        # Initialize strides for a contiguous array.

        assert view.ndim > 0
        assert order in ('C','F','A')

        if order in ('C','A'):
            # C-contiguous array and All-contiguous array
            view.strides[view.ndim - 1] = view.itemsize
            for i in range(view.ndim - 2, -1, -1):
                view.strides[i] = view.strides[i + 1] * view.shape[i + 1]
        elif order == 'F':
            # Fortran-contiguous array.
            view.strides[0] = view.itemsize
            for i in range(1, view.ndim):
                view.strides[i] = view.strides[i - 1] * view.shape[i - 1]

    @staticmethod
    def __last_dim_is_contiguous(dest, src):

        # dest=Py_buffer, src=Py_buffer, -> bool

        assert dest.ndim > 0 and src.ndim > 0

        return (not Py_buff.__have_suboffsets_in_last_dim(dest) and
                not Py_buff.__have_suboffsets_in_last_dim(src)  and
                dest.strides[dest.ndim - 1] == dest.itemsize and
                src.strides[src.ndim   - 1] == src.itemsize)

    @staticmethod
    def __have_suboffsets_in_last_dim(view):

        # view=Py_buffer, -> bool

        # The macro tests for a corner case that should perhaps be explicitly
        # forbidden in the PEP.
        # Assumptions: ndim >= 1.

        return view.suboffsets and view.suboffsets[dest.ndim - 1] >= 0

    @staticmethod
    def __equiv_structure(dest, src):

        # dest=Py_buffer, src=Py_buffer, -> bool

        # Check that the logical structure of the destination and source buffers is identical.

        return (Py_buff.equiv_format(dest, src) and
                Py_buff.equiv_shape (dest, src))

    @staticmethod
    def equiv_format(dest, src):

        # dest=Py_buffer, src=Py_buffer, -> bool

        # This is not a general function for determining format equivalence.
        # It is used in Py_buff.copy_buffer() to weed out non-matching formats.
        # Skipping the '@' character is specifically used in slice assignments,
        # where the lvalue is already known to have a single character format.
        # This is a performance hack that could be rewritten (if properly
        # benchmarked).

        assert dest.format is not None and src.format is not None

        if dest.itemsize != src.itemsize:
            return False

        dfmt = dest.format[1:] if dest.format[:1] == b'@' else dest.format
        sfmt = src.format[1:]  if src.format[:1]  == b'@' else src.format

        if dfmt != sfmt:
            return False

        return True

    @staticmethod
    def equiv_shape(dest, src):

        # dest=Py_buffer, src=Py_buffer, -> bool

        # Two shapes are equivalent if they are either equal or identical up
        # to a zero element at the same position. For example, in NumPy arrays
        # the shapes [1, 0, 5] and [1, 0, 7] are equivalent.

        if dest.ndim != src.ndim:
            return False

        for i in range(dest.ndim):
            if dest.shape[i] != src.shape[i]:
                return False
            if dest.shape[i] == 0:
                break;

        return True

    @staticmethod
    def copy_buffer(dest, src):

        # dest=Py_buffer, src=Py_buffer

        # Recursively copy src to dest.
        # Both buffers must have the same basic structure.
        # Copying is atomic, the function never fails with a partial copy.

        assert dest.ndim > 0

        if not Py_buff.__equiv_structure(dest, src):
            raise ValueError("memoryview assignment: "
                             "lvalue and rvalue have different structures")

        Py_buff.__copy(dest.shape, dest.ndim, dest.itemsize,
                       dest.buf, dest.strides, dest.suboffsets,
                       src.buf,  src.strides,  src.suboffsets,
                       None if Py_buff.__last_dim_is_contiguous(dest, src) else
                       create_string_buffer(dest.shape[dest.ndim - 1] * dest.itemsize))

    @staticmethod
    def __copy(shape, ndim, itemsize,
               dptr, dstrides, dsuboffsets,
               sptr, sstrides, ssuboffsets,
               mem):

        # const c_ssize_t* shape, c_ssize_t ndim, c_ssize_t itemsize,
        # char* dptr, const c_ssize_t* dstrides, const c_ssize_t* dsuboffsets,
        # char* sptr, const c_ssize_t* sstrides, const c_ssize_t* ssuboffsets,
        # char* mem

        # Recursively copy a source buffer to a destination buffer.
        # The two buffers have the same ndim, shape and itemsize.

        assert ndim >= 1

        if ndim == 1:

            # Base case for recursive multi-dimensional copying.
            # Contiguous arrays are copied with very little overhead.
            # Assumptions: ndim == 1, mem == NULL or sizeof(mem) == shape[0] * itemsize.

            if mem is None:
                # contiguous
                memmove(dptr, sptr, shape[0] * itemsize)
            else:
                mptr = cast(mem, c_void_p).value
                sstride = sstrides[0]
                for i in range(shape[0]):
                    memmove(mptr, Py_buff.adjust_ptr(sptr, ssuboffsets), itemsize)
                    mptr += itemsize
                    sptr += sstride
                mptr = cast(mem, c_void_p).value
                dstride = dstrides[0]
                for i in range(shape[0]):
                    memmove(Py_buff.adjust_ptr(dptr, dsuboffsets), mptr, itemsize)
                    mptr += itemsize
                    dptr += dstride

        else:

            dstride = dstrides[0]
            sstride = sstrides[0]
            for i in range(shape[0]):
                Py_buff.__copy(ct_ptr_add(shape, sizeof(c_ssize_t)),
                               ndim - 1, itemsize,
                               Py_buff.adjust_ptr(dptr, dsuboffsets),
                               ct_ptr_add(dstrides,    sizeof(c_ssize_t)),
                               ct_ptr_add(dsuboffsets, sizeof(c_ssize_t))
                               if dsuboffsets else POINTER(c_ssize_t)(),
                               Py_buff.adjust_ptr(sptr, ssuboffsets),
                               ct_ptr_add(sstrides,    sizeof(c_ssize_t)),
                               ct_ptr_add(ssuboffsets, sizeof(c_ssize_t))
                               if ssuboffsets else POINTER(c_ssize_t)(),
                               mem)
                dptr += dstride
                sptr += sstride

    @staticmethod
    def copy_shape(view, shape):

        # view=Py_buffer, shape=Sequence

        # The memoryview must have space for 3 * len(shape) elements.

        len = view.itemsize

        for i in range(view.ndim):
            item = shape[i]

            if not isinstance(item, (int, long)):
                raise TypeError("memoryview.cast(): elements of shape must be integers")

            item = PyLong_AsSsize_t(item)

            if item <= 0:
                # In general elements of shape may be 0, but not for casting.
                raise ValueError("memoryview.cast(): elements of shape must be integers > 0")
            if item > sys.maxsize // len:
                raise ValueError("memoryview.cast(): product(shape) > SSIZE_MAX")

            view.shape[i] = item
            len *= item

        return len

    @staticmethod
    def buffer_to_contiguous(view, order, mem):

        # view=Py_buffer, order=str, mem='char*'

        # Copy view to a contiguous representation.
        # order is one of 'C', 'F' (Fortran) or 'A' (Any).
        # Assumptions: view has PyBUF_FULL information, view.ndim >= 1, len(mem) == view.len.

        assert view.ndim >= 1
        assert view.shape
        assert view.strides

        # initialize dest
        dest = ct_clone(view)
        dest.buf = cast(mem, c_void_p)
        # shape is constant and shared: the logical representation of the array is unaltered.
        # The physical representation determined by strides (and possibly suboffsets) may change.
        dest.strides = (c_ssize_t * view.ndim)()
        Py_buff.init_strides_from_shape(dest, order)
        dest.suboffsets = None
        Py_buff.copy_buffer(dest, view)

    @staticmethod
    def adjust_fmt(view):

        # view=Py_buffer

        # allow explicit form of native format

        fmt = view.format[1:] if view.format[:1] == b'@' else view.format[:]
        if len(fmt) != 1:
            raise NotImplementedError("memoryview: unsupported format {}".format(view.format))
        return fmt

    # Indexing and slicing

    @staticmethod
    def ptr_from_index(view, index):

        # view=Py_buffer, index=int, -> void*

        # Get the pointer to the item at index.

        return Py_buff.lookup_dimension(view, view.buf, 0, index)

    @staticmethod
    def ptr_from_tuple(view, key):

        # view=Py_buffer, key=tuple, -> void*

        # Get the pointer to the item at tuple.

        if len(key) > view.ndim:
            raise TypeError("cannot index {}-dimension view with "
                            "{}-element tuple".format(view.ndim, len(key)))

        ptr = view.buf
        for dim, item in enumerate(key):
            idx = PyNumber_AsSsize_t(item, IndexError)
            ptr = Py_buff.lookup_dimension(view, ptr, dim, idx)

        return ptr

    @staticmethod
    def lookup_dimension(view, ptr, dim, index):

        # view=Py_buffer, ptr=c_void_p, dim=int, index=int, -> void*

        assert view.shape
        assert view.strides

        nitems = view.shape[dim]  # items in the given dimension
        if index < 0: index += nitems
        if not (0 <= index < nitems):
            raise IndexError("index out of bounds on dimension {}".format(dim + 1))

        return Py_buff.adjust_ptr(ptr + view.strides[dim] * index, view.suboffsets, dim)

    @staticmethod
    def adjust_ptr(ptr, suboffsets, dim=0):

        # Adjust ptr if suboffsets are present.

        return (ptr + suboffsets[dim]) if suboffsets and suboffsets[dim] > 0 else ptr


"""
#ifndef Py_LIMITED_API
// Get a pointer to the memoryview's private copy of the exporter's buffer.
#define PyMemoryView_GET_BUFFER(op) (&((memoryview *)(op))->view)
#endif

PyAPI_FUNC(PyObject *) PyMemoryView_FromMemory(char* mem, c_ssize_t size, int flags);
#ifndef Py_LIMITED_API
PyAPI_FUNC(PyObject *) PyMemoryView_FromBuffer(Py_buffer *info);
#endif
PyAPI_FUNC(PyObject *) PyMemoryView_GetContiguous(PyObject *base, int buffertype, char order);

"""
