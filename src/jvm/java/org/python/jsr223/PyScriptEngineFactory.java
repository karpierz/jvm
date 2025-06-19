// Copyright (c) 2004 Adam Karpierz
// SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
// Please refer to the accompanying LICENSE file.

package org.python.jsr223;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineFactory;
import javax.script.ScriptException;

import org.python.Version;

public class PyScriptEngineFactory implements ScriptEngineFactory
{
    /*-- Implementation of javax.script.ScriptEngineFactory --*/

    @Override
    public String getEngineName()
    {
        return engineName;
    }

    @Override
    public String getEngineVersion()
    {
        return engineVersion;
    }

    @Override
    public String getLanguageName()
    {
        return languageName;
    }

    @Override
    public String getLanguageVersion()
    {
        return languageVersion;
    }

    @Override
    public Object getParameter(String key)
    {
        return parameters.get(key);
    }

    @Override
    public List<String> getNames()
    {
        return names;
    }

    @Override
    public List<String> getMimeTypes()
    {
        return mimeTypes;
    }

    @Override
    public List<String> getExtensions()
    {
        return extensions;
    }

    @Override
    public String getMethodCallSyntax(String obj, String m, String... args)
    {
        return String.format("%s.%s(%s)", obj, m, String.join(", ", args));
    }

    @Override
    public String getOutputStatement(String toDisplay)
    {
        //return String.format("print(%s)", Py.newUnicode(toDisplay).__repr__());
        //return "print " + toDisplay; // <AK> was error !!!
        return String.format("print(u'%s')", toDisplay);
    }

    @Override
    public String getProgram(String... statements)
    {
        return String.join("\n", statements);
    }

    @Override
    public ScriptEngine getScriptEngine()
    {
        try
        {
            return new PyScriptEngine(this);
        }
        catch ( ScriptException exc )
        {
            //#// throw exc; // in Jython simple re-throw
            // we can throw it in the constructor, but not here.
            throw new RuntimeException(exc);
        }
    }

    /*--------------------------------------------------------*/

    private static final String engineName      = "jtypes Python Engine";
    private static final String engineVersion   = String.format("%d.%d.%d%s", 2,0,0,"");
    private static final String languageName    = "python";
    private static final String languageVersion = String.format("%d.%d",
                                                                Version.PY_MAJOR_VERSION,
                                                                Version.PY_MINOR_VERSION);

    private static final List<String> names = Collections.unmodifiableList(Arrays.asList(
                                              "python",
                                              "cpython",
                                              "jtypes"));

    private static final List<String> mimeTypes = Collections.unmodifiableList(Arrays.asList(
                                              "text/python",
                                              "application/python",
                                              "text/x-python",
                                              "application/x-python"));

    private static final List<String> extensions = Collections.unmodifiableList(Arrays.asList(
                                              "py", "pyc", "pyo"));

    private static final Map<String, Object> parameters = new HashMap<>();
    static
    {
        parameters.put(ScriptEngine.NAME,             engineName);
        parameters.put(ScriptEngine.ENGINE,           engineName);
        parameters.put(ScriptEngine.ENGINE_VERSION,   engineVersion);
        parameters.put(ScriptEngine.LANGUAGE,         languageName);
        parameters.put(ScriptEngine.LANGUAGE_VERSION, languageVersion);
      /*parameters.put("THREADING",                   "MULTITHREADED");*/
    }
}
