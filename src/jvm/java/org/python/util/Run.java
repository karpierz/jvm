// Copyright (c) 2004 Adam Karpierz
// Licensed under proprietary License
// Please refer to the accompanying LICENSE file.

package org.python.util;

import java.io.File;

public class Run
{
    protected Run() { }

    protected static Class current_class = Run.class;

    protected static String USAGE =
        "  Usage: %s [OPTIONS]... [FILE [SCRIPT ARGS]]\n" +
        "  Options:\n" +
        "    -i  Run script interactively.\n" +
        "    -s  Run script in event dispatching thread (for use with Swing)\n\n";

    protected static String console_file = "jep" + File.separator + "console.py";

    private static boolean interactive   = false;
    private static boolean swing_app     = false;
    private static String  file          = null;
    private static boolean is_real_file  = false;
    private static int     argc          = 0;
    private static String  script_args[] = null;

    public static void main(String args[]) throws Throwable
    {
        String class_name = current_class.getCanonicalName();

        argc = 0;
        script_args = new String[args.length];
        for ( int i = 0; i < args.length; ++i )
        {
            if ( file != null )
                script_args[argc++] = args[i];
            else if ( args[i].equals("-h") )
            {
                System.out.printf(USAGE, class_name);
                System.exit(1);
            }
            else if ( args[i].equals("-i") )
                interactive = true;
            else if ( args[i].equals("-s") )
                swing_app = true;
            else if ( args[i].startsWith("-") )
            {
                System.out.println("Run: Unknown option: " + args[i]);
                System.out.printf(USAGE, class_name);
                System.exit(1);
            }
            else
                file = args[i];
        }

        is_real_file = file != null && ! file.endsWith(console_file);
        if ( ! is_real_file )
            interactive = true;

        if ( file == null && ! interactive )
        {
            System.out.println("Run: Invalid file, null");
            System.out.printf(USAGE, class_name);
            System.exit(1);
        }

        if ( ! swing_app )
            // in case we're run with -Xrs
            System.exit(Run.run(false));
        else
            // run in the event-dispatching thread
            javax.swing.SwingUtilities.invokeAndWait(
                new Runnable() {
                    @Override
                    public void run()
                    {
                        Run.run(true);
                    }
                });
    }

    public static int run(boolean eventDispatch)
    {
        PythonInterpreter interp = null;
        try
        {
            interp = new PythonInterpreter(new PythonInterpreter.Config()
                                           .setIncludePath("."));
        }
        catch ( Throwable exc )
        {
            exc.printStackTrace();
            return 1;
        }

        return run(eventDispatch, interp);
    }

    protected static int run(boolean eventDispatch, PythonInterpreter interp)
    {
        try
        {
            interp.setInteractive(false);
            interp.exec("import sys; sys.argv = argv = " + Run.argv());
            if ( is_real_file )
                interp.execfile(file);
            if ( interactive )
            {
                interp.set("python", interp);
                interp.exec("from jvm.java.org.python.util import console");
                interp.setInteractive(true);
                interp.exec("console.prompt(python)");
            }
        }
        catch ( Throwable exc )
        {
            exc.printStackTrace();
            if ( interp != null )
                try
                {
                    interp.close();
                }
                catch ( Throwable e )
                {
                    e.printStackTrace();
                    return 1;
                }
            return 1;
        }

        if ( ! eventDispatch )
            try
            {
                interp.close();
            }
            catch ( Throwable e )
            {
                e.printStackTrace();
                return 1;
            }

        return 0;
    }

    private static String argv()
    {
        String ret = "[";
        if ( file != null )
            ret += "'" + file + "'";
        for ( int i = 0; i < argc; ++i )
            ret += ",'" + script_args[i] + "'";
        ret += "]";
        // Windows file system compatibility
        ret = ret.replace("\\", "\\\\");
        ret = ret.replace(":",  "\\:");

        return ret;
    }
}
