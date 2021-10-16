# Copyright (c) 2012-2022 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

__all__ = ('PyTypeObject',)

from ctypes import (c_uint, c_ulong, c_ssize_t, c_char_p, c_void_p, py_object,
                    POINTER, Structure, Union)


class PyTypeObject(Structure):
    """Python level PyTypeObject struct analog."""

    # equivalent of: Python-(3.6.0+)/Include/object.h/PyTypeObject

    # `Type flags (tp_flags)
    #
    # These flags are used to extend the type structure in a backwards-compatible
    # fashion. Extensions can use the flags to indicate (and test) when a given
    # type structure contains a new feature. The Python core will use these when
    # introducing new functionality between major revisions (to avoid mid-version
    # changes in the PYTHON_API_VERSION).
    #
    # Arbitration of the flag bit positions will need to be coordinated among
    # all extension writers who publically release their extensions (this will
    # be fewer than you might expect!)..
    #
    # Most flags were removed as of Python 3.0 to make room for new flags. (Some
    # flags are not for backwards compatibility but to indicate the presence of an
    # optional feature; these flags remain of course.)
    #
    # Type definitions should use Py_TPFLAGS_DEFAULT for their tp_flags value.
    #
    # Code can use PyType_HasFeature(type_ob, flag_value) to test whether the
    # given type object has a specified feature.

    # Set if the type object is dynamically allocated
    Py_TPFLAGS_HEAPTYPE = (0x1 << 9)

    # Set if the type allows subclassing
    Py_TPFLAGS_BASETYPE = (0x1 << 10)

    # Set if the type is 'ready' -- fully initialized
    Py_TPFLAGS_READY = (0x1 << 12)

    # Set while the type is being 'readied', to prevent recursive ready calls
    Py_TPFLAGS_READYING = (0x1 << 13)

    # Objects support garbage collection (see objimp.h)
    Py_TPFLAGS_HAVE_GC = (0x1 << 14)

    # These two bits are preserved for Stackless Python, next after this is 17
    Py_TPFLAGS_HAVE_STACKLESS_EXTENSION = 0x0 #ifndef STACKLESS else (0x3 << 15)

    # Objects support type attribute cache
    Py_TPFLAGS_HAVE_VERSION_TAG  = (0x1 << 18)
    Py_TPFLAGS_VALID_VERSION_TAG = (0x1 << 19)

    # Type is abstract and cannot be instantiated
    Py_TPFLAGS_IS_ABSTRACT = (0x1 << 20)

    # These flags are used to determine if a type is a subclass.
    Py_TPFLAGS_LONG_SUBCLASS     = (0x1 << 24)
    Py_TPFLAGS_LIST_SUBCLASS     = (0x1 << 25)
    Py_TPFLAGS_TUPLE_SUBCLASS    = (0x1 << 26)
    Py_TPFLAGS_BYTES_SUBCLASS    = (0x1 << 27)
    Py_TPFLAGS_UNICODE_SUBCLASS  = (0x1 << 28)
    Py_TPFLAGS_DICT_SUBCLASS     = (0x1 << 29)
    Py_TPFLAGS_BASE_EXC_SUBCLASS = (0x1 << 30)
    Py_TPFLAGS_TYPE_SUBCLASS     = (0x1 << 31)

    Py_TPFLAGS_DEFAULT = (Py_TPFLAGS_HAVE_STACKLESS_EXTENSION |
                          Py_TPFLAGS_HAVE_VERSION_TAG |
                          0x0)

    # NOTE: The following flags reuse lower bits (removed as part of the
    # Python 3.0 transition).

    # Type structure has tp_finalize member (3.4)
    Py_TPFLAGS_HAVE_FINALIZE = (0x1 << 0)

    __slots__ = ()
    _fields_ = [# PyObject_VAR_HEAD
        ("ob_refcnt",         c_ssize_t),
        ("ob_type",           c_void_p),
        ("ob_size",           c_ssize_t),
        # PyTypeObject body
        ("tp_name",           c_char_p),  # For printing, in format "<module>.<name>"
        ("tp_basicsize",      c_ssize_t), # For allocation
        ("tp_itemsize",       c_ssize_t), # For allocation
        # Methods to implement standard operations
        ("tp_dealloc",        c_void_p),  # destructor
        ("tp_print",          c_void_p),  # printfunc
        ("tp_getattr",        c_void_p),  # getattrfunc
        ("tp_setattr",        c_void_p),  # setattrfunc
        ("tp_reserved",       c_void_p),  # void*
        ("tp_repr",           c_void_p),  # reprfunc
        # Method suites for standard classes
        ("tp_as_number",      c_void_p),  # PyNumberMethods*
        ("tp_as_sequence",    c_void_p),  # PySequenceMethods*
        ("tp_as_mapping",     c_void_p),  # PyMappingMethods*
        # More standard operations (here for binary compatibility)
        ("tp_hash",           c_void_p),  # hashfunc
        ("tp_call",           c_void_p),  # ternaryfunc
        ("tp_str",            c_void_p),  # reprfunc
        ("tp_getattro",       c_void_p),  # getattrofunc
        ("tp_setattro",       c_void_p),  # setattrofunc
        # Functions to access object as input/output buffer
        ("tp_as_buffer",      c_void_p),  # PyBufferProcs*
        # Flags to define presence of optional/expanded features
        ("tp_flags",          c_ulong),
        ("tp_doc",            c_char_p),  # Documentation string
        # Assigned meaning in release 2.0
        # call function for all accessible objects
        ("tp_traverse",       c_void_p),  # traverseproc
        # delete references to contained objects
        ("tp_clear",          c_void_p),  # inquiry
        # Assigned meaning in release 2.1
        # rich comparisons
        ("tp_richcompare",    c_void_p),  # richcmpfunc
        # weak reference enabler
        ("tp_weaklistoffset", c_ssize_t),
        # Iterators
        ("tp_iter",           c_void_p),  # getiterfunc
        ("tp_iternext",       c_void_p),  # iternextfunc
        # Attribute descriptor and subclassing stuff
        ("tp_methods",        c_void_p),  # struct PyMethodDef*
        ("tp_members",        c_void_p),  # struct PyMemberDef*
        ("tp_getset",         c_void_p),  # struct PyGetSetDef*
        ("tp_base",           c_void_p),  # struct PyTypeObject*
        ("tp_dict",           py_object),
        ("tp_descr_get",      c_void_p),  # descrgetfunc
        ("tp_descr_set",      c_void_p),  # descrsetfunc
        ("tp_dictoffset",     c_ssize_t),
        ("tp_init",           c_void_p),  # initproc
        ("tp_alloc",          c_void_p),  # allocfunc
        ("tp_new",            c_void_p),  # newfunc
        ("tp_free",           c_void_p),  # freefunc # Low-level free-memory routine
        ("tp_is_gc",          c_void_p),  # inquiry  # For PyObject_IS_GC
        ("tp_bases",          py_object),
        ("tp_mro",            py_object), # method resolution order
        ("tp_cache",          py_object),
        ("tp_subclasses",     py_object),
        ("tp_weaklist",       py_object),
        ("tp_del",            c_void_p),  # destructor
        # Type attribute cache version tag.
        ("tp_version_tag",    c_uint),
        ("tp_finalize",       c_void_p)]  # destructor
    if False: #ifdef COUNT_ALLOCS
        _fields_.extend([
        # these must be last and never explicitly initialized
        ("tp_allocs",         c_ssize_t),
        ("tp_frees",          c_ssize_t),
        ("tp_maxalloc",       c_ssize_t),
        ("tp_prev",           c_void_p),  # struct PyTypeObject*
        ("tp_next",           c_void_p)]) # struct PyTypeObject*
    _fields_ = tuple(_fields_)
