// Copyright (c) 2004 Adam Karpierz
// SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
// Please refer to the accompanying LICENSE file.

package org.jt.ref;

/*
 * (internal) Reference to a PyObject*.
 */
public class Reference extends java.lang.ref.PhantomReference<Object>
{
    private volatile long pyobj;

    Reference(Object referent, long pyobj,
              java.lang.ref.ReferenceQueue<Object> queue)
    {
        super(referent, queue);
        this.initialize(pyobj);
        this.pyobj = pyobj;
    }

    protected synchronized void dispose()
    {
        if ( this.pyobj == 0 )
            return;
        long pyobj = this.pyobj;
        this.pyobj = 0;
        this.release(pyobj);
    }

    private native void initialize(long pyobj);
    private native void release(long pyobj);
}
