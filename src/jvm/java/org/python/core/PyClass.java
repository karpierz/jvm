// Copyright (c) 2004 Adam Karpierz
// Licensed under CC BY-NC-ND 4.0
// Licensed under proprietary License
// Please refer to the accompanying LICENSE file.

package org.python.core;

import org.python.util.PythonInterpreter;

public class PyClass extends PyObject
{
    public PyClass(PythonInterpreter interp, long pyobj) throws PyException
    {
        super(interp, pyobj);
    }
}
