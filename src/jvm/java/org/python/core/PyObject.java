// Copyright (c) 2004 Adam Karpierz
// SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
// Please refer to the accompanying LICENSE file.

package org.python.core;

import org.python.util.PythonInterpreter;

public class PyObject implements AutoCloseable
{
    // A Java object that wraps a pointer to a Python object.
    //
    // This class is not thread safe and PyObjects can only be used on the thread
    // where they were created. When a PythonInterpreter instance is closed, all
    // PyObjects from that instance will be invalid and can no longer be used.

    protected final PythonInterpreter interp;
    protected long pyobj = 0;

    public PyObject(PythonInterpreter interp, long pyobj) throws PyException
    {
        // Make a new PyObject
        // 
        // @param interp
        //        the instance of PythonInterpreter that created this object
        // @param pyobj
        //        the address of the python object

        if ( pyobj == 0 )
            throw new PyException("Unable to create object, NULL.");

        this.interp = interp;
        this.pyobj  = pyobj;

        this.incref(); // !!! dodano tu (zamiast listy obiektow ?) - w orginale jep nie bylo !!!
    }

    @Override
    public void close() throws PyException
    {
        if ( this.pyobj == 0 )
            return;

        this.checkValid();
        try
        {
            this.decref();
        }
        finally
        {
            this.pyobj = 0;
        }
    }

    protected void checkValid() throws PyException
    {
        this.interp.checkValid();
        if ( this.pyobj == 0 )
            throw new PyException(this.getClass().getSimpleName() + " has been closed.");
    }

    protected void checkValidRuntime() throws IllegalStateException
    {
        try
        {
            this.checkValid();
        }
        catch ( PyException exc )
        {
            throw new IllegalStateException(exc);
        }
    }

    // ----------- get/set/delete attributes ------------ //

    public boolean hasAttr(String name) throws PyException
    {
        // Check an existence of the attribute on the wrapped Python object,
        // similar to the Python built-in function hasattr.

        this.checkValid();
        return this.has_attr(this.interp.tstate, this.pyobj, name);
    }

    public Object getAttr(String name) throws PyException
    {
        // Access an attribute of the wrapped Python Object, similar to the
        // Python built-in function getattr.
        // This is equivalent to the Python statement: this.name

        this.checkValid();
        return this.get_attr(this.interp.tstate, this.pyobj, name, Object.class);
    }

    public <T> T getAttr(String name, Class<T> jclass) throws PyException
    {
        // Access an attribute of the wrapped Python Object, similar to the
        // Python built-in function getattr.
        // This method allows you to specify Java class of the return type.
        // Supported types are the same as PythonInterpreter.getValue(String, Class).

        this.checkValid();
        return jclass.cast(this.get_attr(this.interp.tstate, this.pyobj, name, jclass));
    }

    public void setAttr(String name, Object value) throws PyException
    {
        // Sets an attribute on the wrapped Python object, similar to the
        // Python built-in function setattr.
        // This is equivalent to the Python statement: this.name = value

        this.checkValid();
        this.set_attr(this.interp.tstate, this.pyobj, name, value);
    }

    public void delAttr(String name) throws PyException
    {
        // Deletes an attribute on the wrapped Python object, similar to the
        // Python built-in function delattr.
        // This is equivalent to the Python statement: del this.name.

        this.checkValid();
        this.del_attr(this.interp.tstate, this.pyobj, name);
    }

    private native boolean has_attr(long tstate, long pyobj, String name);
    private native Object  get_attr(long tstate, long pyobj, String name, Class<?> jclass) throws PyException;
    private native void    set_attr(long tstate, long pyobj, String name, Object value) throws PyException;
    private native void    del_attr(long tstate, long pyobj, String name) throws PyException;

//  PyObject invokeAttr(String name, PyObject... args)
//
//  PyObject invokeAttr(String name, PyObject[] args, String[] keywords)
//  PyObject invokeAttr(String name, PyObject arg1, PyObject[] args, String[] keywords)

//  /**
//   * Invokes this callable with the args in order.
//   * 
//   * @param args
//   *            args to pass to the function in order
//   * @return an {@link Object} value
//   * @throws PyException
//   *             if an error occurs
//   */
//  public Object invokeAttr(String name, Object... args) throws PyException
//  {
//      this.checkValid();
//      return invoke_attr(this.interp.tstate, this.pyobj, args, null);
//  }

//  /**
//   * Invokes this callable with keyword args.
//   * 
//   * @param kwargs
//   *            a Map of keyword args
//   * @return an {@link Object} value
//   * @throws PyException
//   *             if an error occurs
//   */
//  public Object invokeAttr(String name, Map<String, Object> kwargs) throws PyException
//  {
//      this.checkValid();
//      return invoke_attr(this.interp.tstate, this.pyobj, null, kwargs);
//  }

//  /**
//   * Invokes this callable with positional args and keyword args.
//   * 
//   * @param args
//   *            args to pass to the function in order
//   * @param kwargs
//   *            a Map of keyword args
//   * @return an {@link Object} value
//   * @throws PyException
//   *             if an error occurs
//   */
//  public Object invokeAttr(String name, Object[] args, Map<String, Object> kwargs) throws PyException
//  {
//      this.checkValid();
//      return invoke_attr(this.interp.tstate, this.pyobj, args, kwargs);
//  }

//  private native Object invoke_attr(long tstate, long pyobj,
//                                    Object[] args, Map<String, Object> kwargs) throws PyException;

    @Override
    public boolean equals(Object other)
    {
        if ( other == this )
            return true;

        if ( other == null || other.getClass() != this.getClass() )
            return false;

        this.checkValidRuntime();
        return this.py_eq(this.interp.tstate, this.pyobj, other);
    }

    @Override
    public int hashCode()
    {
        this.checkValidRuntime();
        Long value = this.py_hash(this.interp.tstate, this.pyobj);
        return value.hashCode();
    }

    @Override
    public String toString()
    {
        this.checkValidRuntime();
        return this.py_str(this.interp.tstate, this.pyobj);
    }

    private native boolean py_eq(long tstate, long pyobj, Object other);
    private native long  py_hash(long tstate, long pyobj);
    private native String py_str(long tstate, long pyobj);

    // ------------- used only in PyModule. ------------- //

    protected native long import_module(long tstate, long pymodule, String name) throws PyException;
    protected native Object  get_object(long tstate, long pymodule, String name, Class<?> clazz) throws PyException;

    // --------------- internal use only. --------------- //

    public void incref() throws PyException
    {
        this.checkValid();
        this.incref(this.interp.tstate, this.pyobj);
    }

    public void decref() throws PyException
    {
        this.checkValid();
        this.decref(this.interp.tstate, this.pyobj);
    }

    private native void incref(long tstate, long pyobj) throws PyException;
    private native void decref(long tstate, long pyobj) throws PyException;
}
