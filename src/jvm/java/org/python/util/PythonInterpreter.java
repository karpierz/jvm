//
//
//

package org.python.util;

import java.io.File;
import java.io.OutputStream;
import java.net.URL;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.Locale;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.Set;
import java.util.HashSet;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.SynchronousQueue;
/*
import java.lang.ref.ReferenceQueue;
import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Iterator;
*/

import org.python.core.PyObject;
import org.python.core.PyException;

public class PythonInterpreter implements AutoCloseable
{
    // Embeds CPython in Java.
    // Each PythonInterpreter instance provides access to a Python interpreter
    // and maintains an independent global namespace for Python variables.
    // Values can be passed from Java to Python using the various set() methods.
    // Various methods, such as execfile(String), exec(String), eval(String) and
    // invoke(String, Object...) can be used to execute Python code.
    // Python variables can be accessed using get(String).
    //
    // In general, methods called on a PythonInterpreter instance must be called from
    // the same thread that created the instance.
    // To maintain stability, avoid having two PythonInterpreter instances running on
    // the same thread at the same time. Instead provide different threads or close()
    // one before instantiating another on the same thread.
    // PythonInterpreter instances should always be closed when no longer needed to
    // prevent memory leaks.

    private static final String THREAD_WARNING = "JT THREAD WARNING: ";

    // windows requires this as unix newline...
    private static final String LINE_SEP = "\n";

    private boolean       closed      = false;
    public  long          tstate      = 0;
    private Thread        thread      = null;  // all calls must originate from same thread
    private ClassLoader   classLoader = null;  // used by default if not passed/set by caller
    private boolean       interactive = false; // eval() storage.
    private StringBuilder evalLines   = null;  // -||-
    private final boolean isSubInterpreter;

    // keep track of objects that we create.
    // do this to prevent crashes in userland if PythonInterpreter is closed.
    public final MemoryManager memoryManager;

    // Tracks if this thread has been used for an interpreter before.
    // Using different interpreter instances on the same thread is iffy at best.
    // If you make use of CPython extensions (e.g. numpy) that use the GIL,
    // then this gets even more risky and can potentially deadlock.
    //
    private static final ThreadLocal<Boolean> threadUsed = new ThreadLocal<Boolean>() {
        @Override
        protected Boolean initialValue()
        {
            return false;
        }
    };

    public static class Options
    {
        // A configuration object for setting Python pre-initialization parameters.

        protected int noSiteFlag            = -1;
        protected int noUserSiteDirectory   = -1;
        protected int ignoreEnvironmentFlag = -1;
        protected int verboseFlag           = -1;
        protected int optimizeFlag          = -1;
        protected int dontWriteBytecodeFlag = -1;
        protected int hashRandomizationFlag = -1;
        protected String pythonHome         = null;

        public Options setNoSiteFlag(int noSiteFlag)
        {
            // Set the Py_NoSiteFlag variable on the Python interpreter.
            // This corresponds to the python "-S" flag and will prevent
            // the "site" module from being automatically loaded.

            this.noSiteFlag = noSiteFlag;
            return this;
        }

        public Options setNoUserSiteDirectory(int noUserSiteDirectory)
        {
            // Set the Py_NoUserSiteDirectory variable on the Python interpreter.
            // This corresponds to the python "-s" flag and will prevent the user's
            // local python site directory from being added to sys.path.

            this.noUserSiteDirectory = noUserSiteDirectory;
            return this;
        }

        public Options setIgnoreEnvironmentFlag(int ignoreEnvironmentFlag)
        {
            // Set the Py_IgnoreEnvironmentFlag variable on the Python interpreter.
            // This corresponds to the python "-E" flag and will instruct python
            // to ignore all PYTHON* environment variables (e.g. PYTHONPATH).

            this.ignoreEnvironmentFlag = ignoreEnvironmentFlag;
            return this;
        }

        public Options setVerboseFlag(int verboseFlag)
        {
            // Set the Py_VerboseFlag variable on the Python interpreter.
            // This corresponds to the python "-v" flag and will increase
            // verbosity, in particular tracing import statements.

            this.verboseFlag = verboseFlag;
            return this;
        }

        public Options setOptimizeFlag(int optimizeFlag)
        {
            // Set the Py_OptimizeFlag variable on the Python interpreter.
            // This corresponds to the python "-O" flag and will slightly optimize
            // the generated bytecode.

            this.optimizeFlag = optimizeFlag;
            return this;
        }

        public Options setDontWriteBytecodeFlag(int dontWriteBytecodeFlag)
        {
            // Set the Py_DontWriteBytecodeFlag variable on the Python interpreter.
            // This corresponds to the python "-B" flag and will instruct python
            // to not write .py[co] files on import.

            this.dontWriteBytecodeFlag = dontWriteBytecodeFlag;
            return this;
        }

        public Options setHashRandomizationFlag(int hashRandomizationFlag)
        {
            // Set the Py_HashRandomizationFlag variable on the Python interpreter.
            // This corresponds to the environment variable PYTHONHASHSEED.

            this.hashRandomizationFlag = hashRandomizationFlag;
            return this;
        }

        public Options setPythonHome(String pythonHome)
        {
            // Set the home location on the Python interpreter.
            // This is the location of the standard python libraries.
            // This corresponds to the environment variable PYTHONHOME.

            this.pythonHome = pythonHome;
            return this;
        }
    }

    public static class Config
    {
        // A configuration object for constructing a PythonInterpreter instance,
        // corresponding to the configuration of the particular Python sub-interpreter.
        // This class is intended to make constructing PythonInterpreter instances easier
        // while maintaining compatible APIs between releases.

        protected boolean       interactive           = false;
        protected StringBuilder includePath           = null;
        protected ClassLoader   classLoader           = null;
        protected ClassEnquirer classEnquirer         = null;
        protected boolean       redirectOutputStreams = false;
        protected OutputStream  redirectStdout        = null;
        protected OutputStream  redirectStderr        = null;
        protected Set<String>   sharedModules         = null;

        public Config setInteractive(boolean interactive)
        {
            // Sets whether PythonInterpreter.eval(String) should support the
            // slower behavior of potentially waiting for multiple statements

            this.interactive = interactive;
            return this;
        }

        public Config setIncludePath(String includePath)
        {
            // Sets a path of directories separated by File.pathSeparator that
            // will be appended to the sub-interpreter's <code>sys.path</code>

            this.includePath = (includePath != null) ? new StringBuilder(includePath) : null;
            return this;
        }

        public Config addIncludePaths(String... includePaths)
        {
            // Adds a path of directories separated by File.pathSeparator that
            // will be appended to the sub-interpreter's <code>sys.path</code>

            if ( this.includePath == null )
                this.includePath = new StringBuilder();

            for ( String path : includePaths )
            {
                if ( this.includePath.length() > 0 )
                    this.includePath.append(File.pathSeparator);
                this.includePath.append(path);
            }

            return this;
        }

        public Config setClassLoader(ClassLoader classLoader)
        {
            // Sets the ClassLoader to use when importing Java classes from Python

            this.classLoader = classLoader;
            return this;
        }

        public Config setClassEnquirer(ClassEnquirer classEnquirer)
        {
            // Sets a ClassEnquirer to determine which imports are Python vs Java,
            // or null for the default ClassListEnquirer

            this.classEnquirer = classEnquirer;
            return this;
        }

        public Config setRedirectOutputStreams(boolean redirectOutputStreams)
        {
            // Sets whether to redirect the Python sys.stdout and sys.stderr
            // streams to the Java System.out and System.err streams

            this.redirectOutputStreams = redirectOutputStreams;
            return this;
        }

        public Config redirectStdOut(OutputStream outputStream)
        {
            // Redirects the Python interpreter's sys.stdout to the provided
            // OutputStream.

            this.redirectStdout = outputStream;
            return this;
        }

        public Config redirectStdErr(OutputStream outputStream)
        {
            // Redirects the Python interpreter's sys.stderr to the provided
            // OutputStream.

            this.redirectStderr = outputStream;
            return this;
        }

        public Config setSharedModules(Set<String> sharedModules)
        {
            // Sets the names of modules which should be shared with other
            // PythonInterpreter sub-interpreters. This can make it possible to use
            // modules which are not designed for use from Python sub-interpreters.
            // This should not be necessary for any module written in Python but
            // is intended for extensions that use the c-api.
            // For a complete discussion of the types of problems that can require
            // shared modules see the documentation on shared_modules_hook.py.

            this.sharedModules = sharedModules;
            return this;
        }

        public Config addSharedModules(String... sharedModule)
        {
            // Adds module names to the set of shared modules

            if ( this.sharedModules == null )
                this.sharedModules = new HashSet<>();

            for ( String sm : sharedModule )
                this.sharedModules.add(sm);

            return this;
        }
    }

    public static final class MemoryManager
    {
        // Manages the native memory associated with PyObjects in a PythonInterpreter instance.
        //
        // @see <a href="https://www.oracle.com/technetwork/articles/java/finalization-137655.html">
        // How to Handle Java Finalization's Memory-Retention Issues</a>

        /*
        private ReferenceQueue<PyObject> refQueue = new ReferenceQueue<>();
        private Set<PyPointer> references = Collections.newSetFromMap(new IdentityHashMap<PyPointer, Boolean>());
        */
        private final List<PyObject> pythonObjects = new ArrayList<>();
        //private     List<PyObject> pythonObjects = new ArrayList<>();

        /*
        protected ReferenceQueue<PyObject> getReferenceQueue() throws PyException
        {
            this.cleanupWeakReferences();
            return this.refQueue;
        }
        */

        /*
        public void cleanupWeakReferences() throws PyException
        {
            // Cleans out weak references to PyPointers associated with this
            // PythonInterpreter instance. Attempts to free memory earlier than
            // a PythonInterpreter.close() if the developer did not explicitly
            // free the memory with PyObject.close().

            PyPointer p = (PyPointer) this.refQueue.poll();
            while ( p != null )
            {
                p.dispose();
                p = (PyPointer) this.refQueue.poll();
            }
        }
        */

        /*
        protected void addReference(PyPointer pyPtr)
        */
        public void addReference(PyObject obj)
        {
            /*
            this.references.add(pyPtr);
            */
            // Track Python objects we create so they can be smoothly shutdown
            // with no risk of crashes due to bad reference counting.
            //
            // Internal use only.

            this.pythonObjects.add(obj);
        }

        /*
        protected void removeReference(PyPointer pyPtr)
        */
        protected void removeReference(PyObject obj)
        {
            /*
            this.references.remove(pyPtr);
            */
            this.pythonObjects.remove(obj);
        }

        public void cleanupReferences() throws PyException
        {
            // Cleans out all the known references to PyPointers associated with this
            // PythonInterpreter instance.

            /*
            Iterator<PyPointer> iter = this.references.iterator();
            while ( iter.hasNext() )
            {
                PyPointer ptr = iter.next();
                // ptr.dispose() will remove from the set, so we remove it here
                // first to avoid ConcurrentModificationException
                iter.remove();
                ptr.dispose();
            }
            */
            for ( int i = 0; i < this.pythonObjects.size(); ++i )
                this.pythonObjects.get(i).close();
            this.pythonObjects.clear();
        }
    }

    // ---------------------------- constructors ---------------------------- //

    protected PythonInterpreter(PythonInterpreter interp)
    {
        this.closed           = interp.closed;
        this.tstate           = interp.tstate;
        this.thread           = interp.thread;
        this.classLoader      = interp.classLoader;
        this.interactive      = interp.interactive;
        this.evalLines        = interp.evalLines;
        this.isSubInterpreter = interp.isSubInterpreter;
        this.memoryManager    = interp.memoryManager;
    }

    public PythonInterpreter() throws PyException
    {
        this(new Config());
    }

    public PythonInterpreter(Config config) throws PyException
    {
        this(config, true);
    }

    //protected
    public PythonInterpreter(Config config, boolean useSubInterpreter) throws PyException
    {
        Python python = Python.getInstance();

        if ( threadUsed.get() )
            throw new PyException(String.format(
                "%sUnsafe reuse of thread %s for another Python sub-interpreter.%n" +
                "Please close() the previous sub-interpreter instance to ensure " +
                "stability.%n", THREAD_WARNING, Thread.currentThread().getName()));

        this.isSubInterpreter = useSubInterpreter;
        this.memoryManager    = new MemoryManager();

        boolean hasSharedModules = config.sharedModules != null && ! config.sharedModules.isEmpty();

        this.classLoader = (config.classLoader != null)
                           ? config.classLoader : this.getClass().getClassLoader();
        this.interactive = config.interactive;
        this.tstate      = this.init(this.classLoader, hasSharedModules, this.isSubInterpreter);
        this.thread      = Thread.currentThread();
        threadUsed.set(true);
        this.configureInterpreter(config);
    }

    protected void configureInterpreter(Config config) throws PyException
    {
        // why write C code if you don't have to? :-)
        this.setupIncludePath(config.includePath);
        this.setupSharedModulesHook(config.sharedModules);
        this.setupJavaImportHook(config.classEnquirer);
        this.setupRedirectOutputStreams(config.redirectOutputStreams);
    }

    protected void setupIncludePath(StringBuilder includePath) throws PyException
    {
        if ( includePath != null )
        {
            String path = includePath.toString();
            path = path.replace("\\", "\\\\"); // For compatibility with Windows
            this.exec("import sys");
            this.exec(String.format("sys.path += '%s'.split('%s')", path, File.pathSeparator));
            this.exec(null); // flush
        }
    }

    protected void setupSharedModulesHook(Set<String> sharedModules) throws PyException
    {
        boolean hasSharedModules = sharedModules != null && ! sharedModules.isEmpty();
        if ( hasSharedModules )
        {
            this.set("shared_modules",  sharedModules);
            this.set("shared_importer", Python.getInstance());
            //!!!this.exec("from jep import shared_modules_hook");
            //!!!this.exec("shared_modules_hook.setupImporter(shared_modules, shared_importer)");
            this.exec("del shared_modules");
            this.exec("del shared_importer");
            //!!!this.exec("del shared_modules_hook");
            this.exec(null); // flush
        }
    }

    protected void setupJavaImportHook(ClassEnquirer classEnquirer) throws PyException
    {
        if ( classEnquirer == null ) classEnquirer = ClassListEnquirer.getInstance();
        //!!!this.set("class_enquirer", classEnquirer);
        //!!!this.exec("from jep import java_import_hook");
        //!!!this.exec("java_import_hook.setupImporter(class_enquirer)");
        //!!!this.exec("del class_enquirer");
        //!!!this.exec("del java_import_hook");
        this.exec(null); // flush

        //!!!this.exec("import jt");
        //!!!this.exec("jt._import.setupImporter(class_enquirer)");
    }

    protected void setupRedirectOutputStreams(boolean redirectOutputStreams) throws PyException
    {
        if ( redirectOutputStreams )
        {
            //!!!this.exec("from jep import redirect_streams");
            //!!!this.exec("redirect_streams.setup()");
            //!!!this.exec("del import redirect_streams");
            this.exec(null); // flush
        }
    }

    @Override
    public synchronized void close() throws PyException
    {
        // Shuts down the Python sub-interpreter.
        // Make sure you call this to prevent memory leaks.

        if ( this.closed )
            return;

        if ( ! Thread.currentThread().equals(this.thread) )
        {
            // This is inherently unsafe, the thread state information inside Python
            // can get screwed up if a sub-interpreter is closed from a different thread.
            // Py_EndInterpreter is assuming that the interpreter is being ended from the
            // same thread. If close() is called from a different thread, at best you will
            // lose a little bit of memory, at worst you will screw up Python's internal
            // tracking of thread state, which could lead to deadlocks or crashes.

            throw new PyException(String.format(
                "%sUnsafe close() of Python sub-interpreter by thread %s.%n" +
                "Please close() from the creating thread to ensure stability.%n",
                THREAD_WARNING, Thread.currentThread().getName()));
        }

        if ( false ) //!!!this.isSubInterpreter )
        {
            this.exec("import sys");
            this.exec(null); // flush
            Boolean hasThreads = this.get("'threading' in sys.modules", Boolean.class);
            if ( hasThreads.booleanValue() )
            {
                Integer count = this.get("sys.modules['threading'].active_count()", Integer.class);
                if ( count.intValue() > 1 )
                     throw new PyException("All threads must be stopped before closing Python sub-interpreter.");
            }
        }

        // close all the PyObjects we created
        this.memoryManager.cleanupReferences();

        // don't attempt close twice if something goes wrong
        this.closed = true;

        if ( this.tstate == 0 )
        {
            System.err.printf(
                "%sSuspicious close() of Python sub-interpreter by thread %s.%n" +
                "Tnvalid thread state.%n",
                THREAD_WARNING, Thread.currentThread().getName());
        }
        else
        {
            if ( this.isSubInterpreter )
            {
                // // ??? this.execute(this.tstate, nie wywoluje checkValid()
                // this.execute(this.tstate, "import jt");
                // this.execute(this.tstate, "jt._import.teardownImporter()");
            }

            this.close(this.tstate);
        }
        this.tstate = 0;
        threadUsed.set(false);
    }

    private native long init(ClassLoader cloader,
                             boolean hasSharedModules,
                             boolean useSubInterpreter) throws PyException;
    private native void close(long tstate);

    // ---------------------------------------------------------------------- //

    // protected???
    public void checkValid() throws PyException
    {
        // Internal Only

        if ( this.closed )
            throw new PyException("Python interpreter instance has been closed.");

        // Checks if the current thread is valid for the method call.
        // All calls must check the thread.

        if ( ! Thread.currentThread().equals(this.thread) )
            throw new PyException("Invalid thread access.");

        if ( this.tstate == 0 )
            throw new PyException("Initialization failed.");
    }

    // ------------------------------ settings ------------------------------ //

    public boolean isInteractive()
    {
        // Gets whether or not this sub-interpreter is interactive.

        return this.interactive;
    }

    public void setInteractive(boolean interactive)
    {
        // Changes behavior of eval(String).
        // Interactive mode can wait for further Python statements to be evaled,
        // while non-interactive mode can only execute complete Python statements.

        this.interactive = interactive;
    }

    public void setClassLoader(ClassLoader classLoader) throws PyException
    {
        // Sets the default classloader.

        if ( classLoader != null && classLoader != this.classLoader )
        {
            this.classLoader = classLoader;

            if ( this.tstate == 0 )
                throw new PyException("Initialization failed.");

            this.set_classloader(this.tstate, classLoader);
        }
    }

    private native void set_classloader(long tstate, ClassLoader cloader) throws PyException;

    // ----------------------------- run things ----------------------------- //

    // Runs a Python script.
    // 
    // @param script a <code>String</code> absolute path to script file.

    public void execfile(String script) throws PyException
    {
        this.execfile(script, null);
    }

    public void execfile(String script, ClassLoader classLoader) throws PyException
    {
        this.checkValid();

        if ( script == null )
            throw new PyException("Script filename cannot be null.");

        File file = new File(script);
        if ( ! file.exists() || ! file.canRead() )
            throw new PyException("Invalid file: " + file.getAbsolutePath());

        this.setClassLoader(classLoader);
        this.execute_file(this.tstate, script);
    }

    // Execute Python statements.
    //
    // @param string a <code>String</code> value

    public void execute(String string) throws PyException
    {
        this.checkValid();
        this.execute(this.tstate, string);
    }

    public void exec(String string) throws PyException
    {
        this.execute(string);
    }

    // Evaluate Python statements.
    //
    // In interactive mode, PythonInterpreter may not immediately execute the given
    // lines of code. In that case, eval() returns false and the statement is stored
    // and is appended to the next incoming string.
    //
    // If you're running an unknown number of statements, finish with
    // <code>eval(null)</code> to flush the statement buffer.
    //
    // Interactive mode is slower than a straight eval call since it has to
    // compile the code strings to detect the end of the block.
    // Non-interactive mode is faster, but code blocks must be complete.
    // For example:
    //
    // <pre>
    // interactive mode == false
    // <code>interp.eval("if(Test):\n    print('Hello world')");</code>
    // </pre>
    //
    // <pre>
    // interactive mode == true
    // <code>interp.eval("if(Test):");
    // interp.eval("    print('Hello world')");
    // interp.eval(null);
    // </code>
    // </pre>
    //
    // Also, Python does not readily return object values from eval().
    // Use {@link #get(java.lang.String)} instead.
    //
    // @param str a <code>String</code> statement to eval
    // @return true if statement complete and was executed.

    public Object evaluate(String string) throws PyException
    {
        this.checkValid();
        return this.evaluate(this.tstate, string);
    }

    public Object eval(String string) throws PyException
    {
        return this.evaluate(string);
/*
        try
        {
            // trim windows \r\n
            if ( string != null )
                string = string.replaceAll("\r", "");

            if ( string == null || string.trim().equals("") )
            {
                if ( ! this.interactive )
                    return null;

                if ( this.evalLines == null )
                    return true; // nothing to eval

                // null means we send lines, whether or not it compiles.
                this.execute(this.tstate, this.evalLines.toString());
                this.evalLines = null;
                return true;
            }
            else
            {
                // first check if it compiles by itself
                if ( ! this.interactive ||
                     (this.evalLines == null && this.compile(this.tstate, string) != null) )
                {
                    this.execute(this.tstate, string);
                    return true;
                }

                // doesn't compile on it's own, append to eval
                if ( this.evalLines == null )
                    this.evalLines = new StringBuilder();
                else
                    this.evalLines.append(LINE_SEP);
                this.evalLines.append(string);
                return null;
            }
        }
        catch ( PyException exc )
        {
            this.evalLines = null;
            throw exc;
        }
*/
    }

    public Object compile(String string) throws PyException
    {
        return this.compile(string, null);
    }

    public Object compile(String string, String script) throws PyException
    {
        this.checkValid();
        return this.compile(this.tstate, string, script);
    }

    private native void execute_file(long tstate, String script) throws PyException;
    private native void      execute(long tstate, String string) throws PyException;
    private native Object   evaluate(long tstate, String string) throws PyException;
    private native Object    compile(long tstate, String string, String script) throws PyException;

    // Invokes a Python function.
    // 
    // name   - a Python function name in globals dict or the name
    //          of a global object and method using dot notation.
    // args   - args to pass to the function in order
    // kwargs - a Map of keyword args

    public Object invoke(String name, Object... args) throws PyException
    {
        this.checkValid();

        if ( name == null || name.trim().equals("") )
            throw new PyException("Invalid function name.");

        return this.invoke_method(this.tstate, name, args, null);
    }

    public Object invoke(String name, Map<String, Object> kwargs) throws PyException
    {
        this.checkValid();

        if ( name == null || name.trim().equals("") )
            throw new PyException("Invalid function name.");

        return this.invoke_method(this.tstate, name, null, kwargs);
    }

    public Object invoke(String name, Object[] args, Map<String, Object> kwargs) throws PyException
    {
        this.checkValid();

        if ( name == null || name.trim().equals("") )
            throw new PyException("Invalid function name.");

        return this.invoke_method(this.tstate, name, args, kwargs);
    }

    private native Object invoke_method(long tstate, String name,
                                        Object[] args, Map<String, Object> kwargs) throws PyException;

    // Create a Python module on the interpreter.
    // If the given name is valid, imported module, this method will return that module.

    @Deprecated
    public org.python.core.PyModule importModule(String name) throws PyException
    {
        this.checkValid();
        long module_obj = this.import_module(this.tstate, name);
        org.python.core.PyModule module = new org.python.core.PyModule(this, module_obj);
        this.memoryManager.addReference(module);
        return module;
    }

    protected native long import_module(long tstate, String name) throws PyException;

    // ----------------------------- get values ----------------------------- //

    // Retrieves a value from this Python interpreter.
    // Supports retrieving:
    // <ul>
    // <li>Java objects</li>
    // <li>Python None (null)</li>
    // <li>Python strings</li>
    // <li>Python True and False</li>
    // <li>Python numbers</li>
    // <li>Python lists</li>
    // <li>Python tuples</li>
    // <li>Python dictionaries</li>
    // </ul>
    //
    // For Python containers, such as lists and dictionaries, 'get' will
    // recursively move through the container and convert each item.
    // If the type of the value retrieved is not supported, PythonInterpreter
    // will fall back to returning a String representation of the object.
    // This fallback behavior will probably change in the future and should not
    // be relied upon.
    //
    // The general syntax:
    // <code>
    // exec("a = 5")
    // String a = (String) get("a")
    // </code>
    // also will work.
    //
    // @param name
    //        the name of the Python variable to get from the interpreter's
    //        global scope
    // @return an <code>Object</code> value
    // @exception PyException
    //            if an error occurs

    public Object get(String name) throws PyException
    {
        this.checkValid();
        return this.get_object(this.tstate, name, Object.class);
    }

    // Like 'get(String)' but allows specifying the return type.
    // If PythonInterpreter cannot convert the variable to the specified type
    // then a PyException is thrown. This can be used to safely ensure that
    // the return value is an expected type.
    // The following table describes what conversions are currently possible.
    //
    // <table border="1">
    //  <caption>The valid classes for Python to Java conversions</caption>
    //  <tr>
    //   <th>Python Class</th>
    //   <th>Java Classes</th>
    //   <th>Notes</th>
    //  </tr>
    //  <tr>
    //   <td>str/unicode</td>
    //   <td>{@link String}, {@link Character}</td>
    //   <td>Character conversion will fail if the str is longer than 1.</td>
    //  </tr>
    //  <tr>
    //   <td>bool</td>
    //   <td>{@link Boolean}</td>
    //  </tr>
    //  <tr>
    //   <td>int/long</td>
    //   <td>{@link Long}, {@link Integer}, {@link Short}, {@link Byte}</td>
    //   <td>Conversion fails if the number is outside the valid range for the
    //       Java type</td>
    //  </tr>
    //  <tr>
    //   <td>float</td>
    //   <td>{@link Double}, {@link Float}</td>
    //  </tr>
    //  <tr>
    //   <td>list, tuple</td>
    //   <td>{@link List}, array</td>
    //   <td>When a tuple is converted to a List it is unmodifiable.</td>
    //  </tr>
    //  <tr>
    //   <td>dict</td>
    //   <td>{@link Map}</td>
    //  </tr>
    //  <tr>
    //   <td>function, method</td>
    //   <td>Any FunctionalInterface</td>
    //  </tr>
    //  <tr>
    //   <td>numpy.ndarray</td>
    //   <td>{@link NDArray}</td>
    //   <td>Only if Jep was built with numpy support</td>
    //  </tr>
    //  <tr>
    //   <td>numpy.float64</td>
    //   <td>{@link Double}, {@link Float}</td>
    //  </tr>
    //  <tr>
    //   <td>numpy.float32</td>
    //   <td>{@link Float}, {@link Double}</td>
    //  </tr>
    //  <tr>
    //   <td>numpy.int64</td>
    //   <td>{@link Long}, {@link Integer}, {@link Short}, {@link Byte}</td>
    //   <td>Conversion fails if the number is outside the valid range for the Java type</td>
    //  </tr>
    //  <tr>
    //   <td>numpy.int32</td>
    //   <td>{@link Integer}, {@link Long}, {@link Short}, {@link Byte}</td>
    //   <td>Conversion fails if the number is outside the valid range for the Java type</td>
    //  </tr>
    //  <tr>
    //   <td>numpy.int16</td>
    //   <td>{@link Short}, {@link Integer}, {@link Long}, {@link Byte}</td>
    //   <td>Conversion fails if the number is outside the valid range for the Java type</td>
    //  </tr>
    //  <tr>
    //   <td>numpy.int8</td>
    //   <td>{@link Byte}. {@link Short}, {@link Integer}, {@link Long}</td>
    //  </tr>
    //  <tr>
    //   <td>NoneType</td>
    //   <td>Any(null)</td>
    //  </tr>
    //  <tr>
    //   <td colspan="3">Jep objects such as PyJObjects and jarrays will be
    //       returned if the Java type of the wrapped object is compatible.</td>
    //  <tr>
    //  <tr>
    //   <td>Anything else</td>
    //   <td>{@link String}, {@link PyObject}</td>
    //   <td>String conversion will likely be removed in future versions of
    //       PythonInterpreter so it is unsafe to depend on this behavior.</td>
    //  </tr>
    // </table>
    //
    // @param <T>
    //        the generic type of the return type
    // @param name
    //        the name of the Python variable to get from the interpreter's
    //        global scope
    // @param clazz
    //        the Java class of the return type.
    // @return a Java version of the variable
    // @exception PyException
    //            if an error occurs

    public <T> T get(String name, Class<T> clazz) throws PyException
    {
        this.checkValid();
        return clazz.cast(this.get_object(this.tstate, name, clazz));
    }

    public byte[] getByteArray(String name) throws PyException
    {
        this.checkValid();
        return this.get_bytes(this.tstate, name);
    }

    private native Object get_object(long tstate, String name, Class<?> clazz) throws PyException;
    private native byte[] get_bytes (long tstate, String name) throws PyException;

    // ----------------------------- set values ----------------------------- //

    public void set(String name, boolean value) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, value);
    }

    public void set(String name, char value) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, new String(new char[] { value }));
    }

    public void set(String name, byte value) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, value);
    }

    public void set(String name, short value) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, value);
    }

    public void set(String name, int value) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, value);
    }

    public void set(String name, long value) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, value);
    }

    public void set(String name, float value) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, value);
    }

    public void set(String name, double value) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, value);
    }

    public void set(String name, String value) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, value);
    }

    public void set(String name, Object value) throws PyException
    {
        this.checkValid();
        if ( value instanceof Class )
            this.set_var(this.tstate, name, (Class<?>) value);
        else if ( value instanceof String )
            this.set_var(this.tstate, name, (String) value);
        else if ( value instanceof Float )
            this.set_var(this.tstate, name, ((Float) value).floatValue());
        else if ( value instanceof Integer )
            this.set_var(this.tstate, name, ((Integer) value).intValue());
        else if ( value instanceof Double )
            this.set_var(this.tstate, name, ((Double) value).doubleValue());
        else if ( value instanceof Long )
            this.set_var(this.tstate, name, ((Long) value).longValue());
        else if ( value instanceof Byte )
            this.set_var(this.tstate, name, ((Byte) value).byteValue());
        else if ( value instanceof Short )
            this.set_var(this.tstate, name, ((Short) value).shortValue());
        else if ( value instanceof Boolean )
            this.set_var(this.tstate, name, ((Boolean) value).booleanValue());
        else
            this.set_var(this.tstate, name, value);
    }

    private native void set_var(long tstate, String name, boolean  value) throws PyException;
    private native void set_var(long tstate, String name, char     value) throws PyException;
    private native void set_var(long tstate, String name, byte     value) throws PyException;
    private native void set_var(long tstate, String name, short    value) throws PyException;
    private native void set_var(long tstate, String name, int      value) throws PyException;
    private native void set_var(long tstate, String name, long     value) throws PyException;
    private native void set_var(long tstate, String name, float    value) throws PyException;
    private native void set_var(long tstate, String name, double   value) throws PyException;
    private native void set_var(long tstate, String name, String   value) throws PyException;
    private native void set_var(long tstate, String name, Object   value) throws PyException;
    private native void set_var(long tstate, String name, Class<?> value) throws PyException;

    // ----------------------------- set arrays ----------------------------- //

    public void set(String name, boolean[] array) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, array);
    }

    public void set(String name, char[] array) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, new String(array));
    }

    public void set(String name, byte[] array) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, array);
    }

    public void set(String name, short[] array) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, array);
    }

    public void set(String name, int[] array) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, array);
    }

    public void set(String name, long[] array) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, array);
    }

    public void set(String name, float[] array) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, array);
    }

    public void set(String name, double[] array) throws PyException
    {
        this.checkValid();
        this.set_var(this.tstate, name, array);
    }

    private native void set_var(long tstate, String name, boolean[] array) throws PyException;
    private native void set_var(long tstate, String name, char[]    array) throws PyException;
    private native void set_var(long tstate, String name, byte[]    array) throws PyException;
    private native void set_var(long tstate, String name, short[]   array) throws PyException;
    private native void set_var(long tstate, String name, int[]     array) throws PyException;
    private native void set_var(long tstate, String name, long[]    array) throws PyException;
    private native void set_var(long tstate, String name, float[]   array) throws PyException;
    private native void set_var(long tstate, String name, double[]  array) throws PyException;

    // ----------------------- Python main interpreter ---------------------- //

    public static class Python implements AutoCloseable
    {
        // The main Python interpreter that all sub-interpreters will be created from.
        // In a simpler embedded Python project, a single Python interpreter would be
        // used and all would be good. However, since jvm supports multithreading
        // with multiple sub-interpreters (PythonInterpreter instances), we need the
        // PythonInterpreter to work around some issues.
        // 
        // The PythonInterpreter is used to avoid potential deadlocks. Python can
        // deadlock when trying to acquire the GIL through methods such as
        // <a href="https://docs.python.org/3/c-api/init.html#c.PyGILState_Ensure">
        // PyGILState_*</a>.
        // While PythonInterpreter does not use those methods, CPython extensions
        // such as numpy do. The deadlock can occur if there is more than one
        // PyThreadState per thread. To get around this, the PythonInterpreter creates
        // a unique thread that initializes Python and keeps this thread around forever.
        // This ensures that any new sub-interpreters cannot be created on the same
        // thread as the main Python interpreter.
        // 
        // The PythonInterpreter is also used to support shared modules. While each
        // sub-interpreter is fairly sandboxed, in practice this does not always work
        // well with CPython extensions. In particular, disposing of a sub-interpreter
        // that has imported a CPython extension may cause some of the CPython
        // extension's objects to be garbage collected. To get around this, shared
        // modules import on the main interpreter's thread so they can be shared
        // amongst sub-interpreters and will never be garbage collected.
        // 
        // For more information about why the PythonInterpreter class exists, see
        // <a href="https://docs.python.org/3/c-api/init.html#bugs-and-caveats">
        // Sub-interpreter bugs and caveats</a>.

        private static Options  initOptions       = null;
        private static String[] sharedModulesArgv = null;
        private static Python   python            = null;

        private Thread    thread = null;
        private Throwable error  = null;
        private BlockingQueue<String> sharedImportQueue   = new SynchronousQueue<>();
        private BlockingQueue<Object> sharedImportResults = new SynchronousQueue<>();

        public static void setInitOptions(Options options) throws PyException
        {
            // Sets interpreter settings for the main Python interpreter.
            // This method must be called before the first PythonInterpreter
            // instance is created in the process.

            if ( python.thread != null )
                throw new PyException("PythonInterpreter.setInitOptions(PythonInterpreter.Options) " +
                                      "called after initializing Python interpreter.");
            initOptions = options;
        }

        public static void setSharedModulesArgv(String... argv) throws PyException
        {
            // Sets the sys.argv values on the main Python interpreter.
            // This method must be called before the first PythonInterpreter
            // instance is created in the process.

            if ( python.thread != null )
                throw new PyException("PythonInterpreter.setSharedModulesArgv(...) " +
                                      "called after initializing Python interpreter.");
            sharedModulesArgv = argv;
        }

        protected static synchronized Python getInstance() throws Error
        {
            // Creates the PythonInterpreter.Python instance that will be used by
            // PythonInterpreter. This should be called from all PythonInterpreter
            // constructors to ensure the native module has been loaded and
            // initialized before a valid PythonInterpreter instance is produced.

            if ( python == null )
            {
                try
                {
                    python = new Python();
                    python.initialize();
                }
                catch ( Error exc )
                {
                    python.close();
                    throw exc;
                }
            }
            else if ( python.error != null )
                throw new Error("The main Python interpreter previously failed to initialize.",
                                python.error);
            return python;
        }

        private Python()
        {
            // only this class can instantiate it
        }

        protected Python(Python interp)
        {
            this.thread              = interp.thread;
            this.error               = interp.error;
            this.sharedImportQueue   = interp.sharedImportQueue;
            this.sharedImportResults = interp.sharedImportResults;
        }

        private void initialize() throws Error
        {
            // Initializes CPython, by calling a native function in this module,
            // and ultimately Py_Initialize(). We load on a separate thread
            // to try and avoid GIL issues that come about from a sub-interpreter
            // being on the same thread as the main interpreter.

            // import java.io.File;
            // import java.io.IOException;
            // import java.net.URLClassLoader;
            // import java.net.URL;
            // import java.lang.reflect.Method;
            //
            // String path;
            //
            // URL url = (new File(path)).toURI().toURL();
            //
            // public static void addURLToSystemClassLoader(URL url) throws IntrospectionException
            // { 
            //     URLClassLoader systemClassLoader = (URLClassLoader) ClassLoader.getSystemClassLoader(); 
            //     Class<URLClassLoader> classLoaderClass = URLClassLoader.class; 
            //
            //     try
            //     { 
            //         Method method = classLoaderClass.getDeclaredMethod("addURL", new Class[]{URL.class});
            //         method.setAccessible(true); 
            //         method.invoke(systemClassLoader, new Object[]{url});
            //     }
            //     catch ( Throwable exc )
            //     { 
            //         ext.printStackTrace();
            //         throw new IntrospectionException("Error when adding url to system ClassLoader "); 
            //     } 
            // }

            this.loadLibrary();

            if ( initOptions != null )
                set_init_options(initOptions.noSiteFlag,
                                 initOptions.noUserSiteDirectory,
                                 initOptions.ignoreEnvironmentFlag,
                                 initOptions.verboseFlag,
                                 initOptions.optimizeFlag,
                                 initOptions.dontWriteBytecodeFlag,
                                 initOptions.hashRandomizationFlag,
                                 initOptions.pythonHome);

            this.thread = new Thread("PythonMainInterpreter") {
                @Override
                public void run()
                {
                    try
                    {
                        initialize_python(sharedModulesArgv);
                    }
                    catch ( Throwable exc )
                    {
                        error = exc;
                    }
                    finally
                    {
                        synchronized ( Python.this )
                        {
                            Python.this.notify();
                        }
                    }

                    // We need to keep this main interpreter thread around.
                    // It might be used for importing shared modules.
                    // Even if it is not used it must remain running because
                    // if its thread shuts down while another thread is in
                    // Python, then the thread state can get messed up leading
                    // to stability/GIL issues.

                    try
                    {
                        Object initLock = new Object();
                        synchronized ( initLock )
                        {
                            try
                            {
                                initLock.wait();
                            }
                            catch ( InterruptedException exc )
                            {
                                throw exc;
                            }
                        }
                    }
                    catch ( InterruptedException exc )
                    {
                        // ignore
                    }
                }
            };

            this.thread.setDaemon(true);

            synchronized ( this )
            {
                this.thread.start();
                try
                {
                    this.wait();
                }
                catch ( InterruptedException exc )
                {
                    if ( this.error != null )
                        this.error = exc;
                }
            }

            if ( this.error != null )
                throw new Error(this.error);
        }

        private void loadLibrary() throws Error
        {
            Platform platform = newPlatform();
            String libName = "PythonInterpreter" + "-" + platform.librarySuffix();

            URL dll_url = this.getClass().getResource(libName);
            if ( dll_url == null )
                throw new ExceptionInInitializerError("Couldn't find library: " + libName);
            URI dll_uri;
            try
            {
                dll_uri = dll_url.toURI();
            }
            catch ( URISyntaxException exc )
            {
                throw new ExceptionInInitializerError("Invalid library name: " + libName);
            }

            System.load(new File(dll_uri).getAbsolutePath());  // UnsatisfiedLinkError
        }

        private static Platform newPlatform()
        {
            if ( Windows.isA() )
                return new Windows();
            else if ( Linux.isA() )
                return new Linux();
            else if ( Solaris.isA() )
                return new Solaris();
            else if ( MacOS.isA() )
                return new MacOS();
            else if ( Unix.isA() )
                return new Unix();
            else
                throw new ExceptionInInitializerError("Unsupported platform.");
                //!!!return new Unix();            
        }

        private static abstract class Platform
        {
            protected final String osArch = System.getProperty("os.arch");

            public abstract String system();
            public abstract String machine();
            public abstract String libraryExt();

            public String librarySuffix()
            {
                return this.system().toLowerCase(Locale.ENGLISH) +
                       "-" + this.machine() + this.libraryExt();
            }
        }

        private static class Windows extends Platform
        {
            public static boolean isA()
            {
                final String osName = System.getProperty("os.name");
                return osName.contains("Windows");
            }

            @Override
            public String system()
            {
                return "Windows";
            }

            @Override
            public String machine()
            {
                return isJVM64Bit() ? (this.osArch.equals("ia64") ? "ia64" : "x64") : "x86";
            }

            @Override
            public String libraryExt()
            {
                return ".dll";
            }
        }

        private static class Linux extends Platform
        {
            public static boolean isA()
            {
                final String osName = System.getProperty("os.name");
                return osName.contains("Linux");
            }

            @Override
            public String system()
            {
                return "Linux";
            }

            @Override
            public String machine()
            {
                return this.osArch.contains("ppc")
                       ? (isJVM64Bit() ? "ppc64" : "ppc")
                       : this.osArch.contains("sparc") ? "sparc"
                       : this.osArch.equals("ia64")    ? "ia64"
                       : this.osArch.equals("amd64")   ? "amd64"
                       : this.osArch.equals("i386") ||
                         this.osArch.equals("x86")     ? "i386"
                       : (isJVM64Bit() ? "amd64" : "i386");
            }

            @Override
            public String libraryExt()
            {
                return ".so";
            }
        }

        private static class Solaris extends Platform
        {
            private static boolean isA()
            {
                final String osName = System.getProperty("os.name");
                return osName.contains("SunOS") || osName.contains("Solaris");
            }

            @Override
            public String system()
            {
                return "Solaris";
            }

            @Override
            public String machine()
            {
                return this.osArch.contains("sparc")
                       ? (isJVM64Bit() ? "sparcv9" : "sparc")
                       : (isJVM64Bit() ? "amd64"   : "x86");
            }

            @Override
            public String libraryExt()
            {
                return ".so";
            }
        }

        private static class MacOS extends Platform
        {
            public static boolean isA()
            {
                final String osName = System.getProperty("os.name");
                return osName.contains("Mac OS X") || osName.contains("Darwin");
            }

            @Override
            public String system()
            {
                return "MacOSX";
            }

            @Override
            public String machine()
            {
                return this.osArch.contains("ppc")
                       ? (isJVM64Bit() ? "ppc64" : "ppc")
                       : (isJVM64Bit() ? "amd64" : "i386");
            }

            @Override
            public String libraryExt()
            {
                return ".dylib";
            }
        }

        private static class Unix extends Platform
        {
            public static boolean isA()
            {
                final String osName = System.getProperty("os.name");
                //return getCurrentPlatform().isCompatibleWith(Platform.UNIX);
                return false;
            }

            @Override
            public String system()
            {
                return null;
            }

            @Override
            public String machine()
            {
                return null;
            }

            @Override
            public String libraryExt()
            {
                return null;
            }
        }

        private static boolean isJVM64Bit()
        {
            final String sunBitness = System.getProperty("sun.arch.data.model");
            final String ibmBitness = System.getProperty("com.ibm.vm.bitmode");
            final String osArch     = System.getProperty("os.arch");
            return "64".equals(sunBitness)      // Sun-Oracle's/IBM`s/? JDK
                || "64".equals(ibmBitness)      // IBM`s JDK
                || "ia64".equals(osArch)        // Windows/Linux/? on Intel Itanium
                || "ia64w".equals(              // HP-UX on Intel Itanium
                        osArch.toLowerCase(Locale.ENGLISH))
                || "PA_RISC2.0W".equals(osArch) // HP-UX on PA-RISC 2.0
                || "amd64".equals(osArch)       // others...
                || "sparcv9".equals(osArch)     //  -||-
                || "x86_64".equals(osArch)      //  -||-
                || "ppc64".equals(osArch);      //  -||-
        }

        @Override
        public void close()
        {
            // Stop the interpreter thread.

            if ( this.thread == null )
                return;
            this.thread.interrupt();
            this.thread = null;
        }

        public void sharedImport(String module) throws PyException
        {
            // Import a module into the main Python interpreter on the correct
            // thread for that interpreter. This is called from the Python shared
            // modules import hook to create a module needed by a PythonInterpreter
            // interpreter.

            try
            {
                this.sharedImportQueue.put(module);
                Object result = this.sharedImportResults.take();
                if ( result instanceof PyException )
                    throw new PyException("Error importing shared module " + module,
                                          ((PyException) result));
            }
            catch ( InterruptedException exc )
            {
                throw new PyException(exc);
            }
        }

        private static native void set_init_options(int noSiteFlag,
                                                    int noUserSiteDiretory,
                                                    int ignoreEnvironmentFlag,
                                                    int verboseFlag,
                                                    int optimizeFlag,
                                                    int dontWriteBytecodeFlag,
                                                    int hashRandomizationFlag,
                                                    String pythonHome);
        private static native void initialize_python(String[] argv);
        private static native void shared_import(String module) throws PyException;
    }
}
