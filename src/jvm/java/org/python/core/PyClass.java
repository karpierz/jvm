// Copyright (c) 2004 Adam Karpierz
// SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
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
