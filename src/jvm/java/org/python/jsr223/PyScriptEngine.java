// Copyright (c) 2004-2020 Adam Karpierz
// Licensed under CC BY-NC-ND 4.0
// Licensed under proprietary License
// Please refer to the accompanying LICENSE file.

package org.python.jsr223;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Reader;

import javax.script.AbstractScriptEngine;
import javax.script.Compilable;
import javax.script.CompiledScript;
import javax.script.Invocable;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineFactory;
import javax.script.ScriptException;
import javax.script.ScriptContext;
import javax.script.Bindings;
import javax.script.SimpleBindings;

import org.python.core.PyModule;
import org.python.core.PyException;
import org.python.util.PythonInterpreter;

public class PyScriptEngine extends AbstractScriptEngine implements Compilable, Invocable, AutoCloseable
{
    private final ScriptEngineFactory factory;
    private final PythonInterpreter   interp;

    PyScriptEngine(ScriptEngineFactory factory) throws ScriptException
    {
        super();
      //this.context.setBindings(new SimpleBindings(), ScriptContext.ENGINE_SCOPE);
        this.context.setBindings(new SimpleBindings(), ScriptContext.GLOBAL_SCOPE);
        try
        {
            this.factory = (factory == null) ? new PyScriptEngineFactory() : factory;
            /* make interactive because javax.script sucks */
            this.interp = new PythonInterpreter(new PythonInterpreter.Config()
                                                .setInteractive(true));
            this.interp.setClassLoader(Thread.currentThread().getContextClassLoader());
        }
        catch ( PyException exc )
        {
            throw _scriptException(exc);
        }
    }

    /* As java.lang.AutoCloseable */

    @Override
    public void close()
    {
        try
        {
            this.interp.close();
        }
        catch ( Exception exc )
        {
            throw new RuntimeException(exc);
        }
    }

    /*------ Implementation of javax.script.ScriptEngine -----*/

    @Override
    public Bindings createBindings()
    {
        return new SimpleBindings();
    }

    @Override
    public Bindings getBindings(int scope)
    {
        return super.getBindings(scope);
    }

    @Override
    public void setBindings(Bindings bindings, int scope)
    {
        super.setBindings(bindings, scope);
    }

    @Override
    public ScriptContext getContext()
    {
        return super.getContext();
    }

    @Override
    public void setContext(ScriptContext context)
    {
        super.setContext(context);

        try
        {
            this._setContext(this.context);
        }
        catch ( ScriptException exc )
        {
            throw new RuntimeException(exc);
        }
    }

    private void _setContext(ScriptContext context) throws ScriptException
    {
        try
        {
            this.interp.set("context", context);
        }
        catch ( PyException exc )
        {
            throw _scriptException(exc);
        }
    }

    @Override
    public ScriptEngineFactory getFactory()
    {
        return this.factory;
    }

    /*
     * Run script from string.
     */

    @Override
    public Object eval(String script) throws ScriptException
    {
        return this.eval(script, this.context);
    }

    @Override
    public Object eval(String script, ScriptContext context) throws ScriptException
    {
        return this._eval(script, context, this.context.getBindings(ScriptContext.ENGINE_SCOPE));
    }

    @Override
    public Object eval(String script, Bindings bindings) throws ScriptException
    {
        return this._eval(script, this.context, bindings);
    }

    /*
     * Run script from reader.
     */

    @Override
    public Object eval(Reader reader) throws ScriptException
    {
        /* Performance of this method will suck compared to using
           PythonInterpreter.execfile().
           Use the compiled interface or something. */

        return this.eval(reader, this.context);
    }

    @Override
    public Object eval(Reader reader, ScriptContext context) throws ScriptException
    {
        return this._eval(reader, context, this.context.getBindings(ScriptContext.ENGINE_SCOPE));
    }

    @Override
    public Object eval(Reader reader, Bindings bindings) throws ScriptException
    {
        return this._eval(reader, this.context, bindings);
    }

    private Object _eval(String script,
                         ScriptContext context,
                         Bindings bindings) throws ScriptException
    {
        try
        {
            this._setContext(context);

            this.interp.setInteractive(true);
            this.interp.eval(script);
            return null; // ???
        }
        catch ( PyException exc )
        {
            throw _scriptException(exc);
        }
    }

    private Object _eval(Reader reader,
                         ScriptContext context,
                         Bindings bindings) throws ScriptException
    {
        try
        {
            this._setContext(context);

            File temp = this._writeTemp(reader);
            this.interp.setInteractive(false);
            this.interp.execfile(temp.getAbsolutePath());
            return null; // ???
        }
        catch ( IOException exc )
        {
            throw new ScriptException("Error writing to file: " + exc.getMessage());
        }
        catch ( PyException exc )
        {
            throw _scriptException(exc);
        }
    }

    /*
     * Get & Set values.
     */

    @Override
    public Object get(String name)
    {
        try
        {
            PyModule module = null;
            if ( name.indexOf('.') > 0 )
            {
                /* split package name by '.' and make modules */
                String[] tokens = name.split("\\.");
                for ( int i = 0; i < tokens.length - 1; ++i )
                {
                    String mname = tokens[i];
                    if ( module == null )
                        module = this.interp.importModule(mname);
                    else
                        module = module.importModule(mname);
                }
                name = tokens[tokens.length - 1];
            }

            if ( module == null )
                return this.interp.get(name);
            else
                return module.get(name);
        }
        catch ( PyException exc )
        {
            /* probably not found. javax.script wants use to just return null */
            return null;
        }
    }

    @Override
    public void put(String name, Object value) throws IllegalArgumentException
    {
        try
        {
            PyModule module = null;
            if ( name.indexOf('.') > 0 )
            {
                /* split package name by '.' and make modules */
                String[] tokens = name.split("\\.");
                for ( int i = 0; i < tokens.length - 1; ++i )
                {
                    String mname = tokens[i];
                    if ( module == null )
                        module = this.interp.importModule(mname);
                    else
                        module = module.importModule(mname);
                }
                name = tokens[tokens.length - 1];
            }

            if ( module == null )
                this.interp.set(name, value);
            else
                module.setAttr(name, value);
        }
        catch ( PyException exc )
        {
            throw new IllegalArgumentException(exc);
        }
    }

    /*------- Implementation of javax.script.Compilable ------*/

    @Override
    public CompiledScript compile(String script) throws ScriptException
    {
        return new PyCompiledScript(this._compileScript(script, this.context));
    }

    @Override
    public CompiledScript compile(Reader reader) throws ScriptException
    {
        return new PyCompiledScript(this._compileScript(reader, this.context));
    }

    private final class PyCompiledScript extends CompiledScript
    {
        private Object code = null;

        PyCompiledScript(Object code)
        {
            this.code = code;
        }

        @Override
        public Object eval(ScriptContext context) throws ScriptException
        {
            return PyScriptEngine.this.eval((String) this.code, context);
        }

        @Override
        public ScriptEngine getEngine()
        {
            return PyScriptEngine.this;
        }
    }

    private Object _compileScript(String script, ScriptContext context) throws ScriptException
    {
        try
        {
            String filename = (String) context.getAttribute(ScriptEngine.FILENAME);
            if ( filename == null )
                return this.interp.compile(script);
            else
            {
                //!!!interp.getLocals().__setitem__(Py.newString("__file__"), Py.newString(filename));
                return this.interp.compile(script, filename);
            }
        }
        catch ( PyException exc )
        {
            throw _scriptException(exc);
        }
    }

    private Object _compileScript(Reader reader, ScriptContext context) throws ScriptException
    {
        try
        {
            String filename = (String) context.getAttribute(ScriptEngine.FILENAME);
            if ( filename == null )
                return this.interp.compile("!!! temporary !!!");
            else
            {
                //!!!interp.getLocals().__setitem__(Py.newString("__file__"), Py.newString(filename));
                return this.interp.compile("!!! temporary !!!", filename);
            }
        }
        catch ( PyException exc )
        {
            throw _scriptException(exc);
        }
    }

    /*------- Implementation of javax.script.Invocable -------*/

    public Object invokeFunction(String name, Object... args)
        throws ScriptException, NoSuchMethodException
    {
        throw new ScriptException("Not implemented yet!");
    }

    public Object invokeMethod(Object thiz, String name, Object... args)
        throws ScriptException, NoSuchMethodException
    {
        throw new ScriptException("Not implemented yet!");
    }

    public <T> T getInterface(Class<T> clazz)
    {
        return null; /* Not implemented yet! */
    }

    public <T> T getInterface(Object thiz, Class<T> clazz)
    {
        return null; /* Not implemented yet! */
    }

    /*--------------------------------------------------------*/

    private static ScriptException _scriptException(PyException pexc)
    {
        try
        {
            return (ScriptException) new ScriptException(pexc.getMessage()).initCause(pexc);
        }
        catch ( Exception exc )
        {
            return new ScriptException(pexc);
        }
    }

    private File _writeTemp(Reader reader) throws IOException
    {
        /* write temp file from Reader */

        File temp_file = File.createTempFile("jtypes", ".py");
        try ( FileWriter fout = new FileWriter(temp_file) )
        {
            int count;
            char[] buf = new char[1024];
            while ( (count = reader.read(buf)) > 0 )
                fout.write(buf, 0, count);
        }

        return temp_file;
    }
}
