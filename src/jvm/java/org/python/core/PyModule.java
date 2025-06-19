// Copyright (c) 2004 Adam Karpierz
// SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
// Please refer to the accompanying LICENSE file.

package org.python.core;

import org.python.util.PythonInterpreter;

public class PyModule extends PyObject
{
    public PyModule(PythonInterpreter interp, long pyobj) throws PyException
    {
        super(interp, pyobj);
    }

    public PyModule importModule(String name) throws PyException
    {
        this.checkValid();
        long module_obj = this.import_module(this.interp.tstate, this.pyobj, name);
        PyModule module = new PyModule(this.interp, module_obj);
        this.interp.memoryManager.addReference(module);
        return module;
    }

    public Object get(String name) throws PyException
    {
        this.checkValid();
        return this.get_object(this.interp.tstate, this.pyobj, name, Object.class);
    }
}
