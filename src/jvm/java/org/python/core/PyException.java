// Copyright (c) 2004-2020 Adam Karpierz
// Licensed under CC BY-NC-ND 4.0
// Licensed under proprietary License
// Please refer to the accompanying LICENSE file.

package org.python.core;

public class PyException extends Exception
{
    private static final long serialVersionUID = 1L;

    /*
     * The address of the Python type which caused this exception.
     * This is used if the PyException is thrown back into Python
     * so that a new Python exception can be thrown with the same
     * type as the original exception.
     */
    private final long python_type;

    public PyException()
    {
        super();
        this.python_type = 0;
    }

    public PyException(String message)
    {
        super(message);
        this.python_type = 0;
    }

    public PyException(String message, Throwable cause)
    {
        super(message, cause);
        this.python_type = (cause instanceof PyException)
                           ? ((PyException) cause).python_type : 0;
    }

    public PyException(Throwable cause)
    {
        super(cause);
        this.python_type = (cause instanceof PyException)
                           ? ((PyException) cause).python_type : 0;
    }

    /*---------------- internal use only. ----------------*/

    protected PyException(String message, long python_type)
    {
        super(message);
        this.python_type = python_type;
    }

    protected long getPythonType()
    {
        return this.python_type;
    }
}
