// Copyright (c) 2004 Adam Karpierz
// SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
// Please refer to the accompanying LICENSE file.

package org.jt.reflect;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;

public final class ProxyHandler implements InvocationHandler
{
    public long target;

    public ProxyHandler(long target)
    {
        this.initialize(target);
        this.target = target;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable
    {
        return this.invoke(this.target, proxy, method, args);
    }

    @Override
    protected void finalize() throws Throwable
    {
        try
        {
            this.release(this.target);
            this.target = 0;
        }
        finally
        {
            super.finalize();
        }
    }

    private native Object invoke(long target, Object proxy, Method method, Object[] args);
    private native void initialize(long target);
    private native void release(long target);
}
