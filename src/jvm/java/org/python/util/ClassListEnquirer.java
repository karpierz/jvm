//
//
//

package org.python.util;

import java.io.BufferedReader;
import java.io.File;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Set;
import java.util.StringTokenizer;
import java.util.jar.Attributes;
import java.util.jar.JarFile;
import java.util.jar.JarEntry;
import java.util.jar.Manifest;

import org.python.core.PyException;

public class ClassListEnquirer implements ClassEnquirer
{
    // A singleton that searches for loaded classes from the JRE and the
    // Java classpath. This is the default ClassEnquirer that is used if
    // no ClassEnquirer is specified when constructing PythonInterpreter
    // instances. For internal use.
    // ClassListEnquirer is also used by the command line 'jep' script.

    public static synchronized ClassListEnquirer getInstance() throws PyException
    {
        if ( ClassListEnquirer.instance == null )
            ClassListEnquirer.instance = new ClassListEnquirer();
        return ClassListEnquirer.instance;
    }

    private ClassListEnquirer() throws PyException
    {
        this.loadClassPath();
        this.loadPackages();
        this.loadClassList();

        for ( String restrictedPkg : ClassEnquirer.RESTRICTED_PKG_NAMES )
        {
            this.packageToClassMap.remove(restrictedPkg);
            this.packageToSubPackageMap.remove(restrictedPkg);
        }
    }

    //-- Implementation of ClassEnquirer --//

    @Override
    public boolean isJavaPackage(String name)
    {
        return ( this.packageToClassMap.containsKey(name) ||
                 this.packageToSubPackageMap.containsKey(name) );
    }

    @Override
    public String[] getClassNames(String pkgName)
    {
        List<String> cnames = this.packageToClassMap.get(pkgName);
        if ( cnames == null )
            return new String[0];
        else
        {
            String[] names = new String[cnames.size()];
            cnames.toArray(names);
            return names;
        }
    }

    @Override
    public String[] getSubPackages(String pkgName)
    {
        List<String> pnames = this.packageToSubPackageMap.get(pkgName);
        if ( pnames == null )
            return new String[0];
        else
            return pnames.toArray(new String[0]);
    }

    //-------------------------------------//

    private void loadClassPath()
    {
        // load jar files from class path

        String classPath = System.getProperty("java.class.path");
        String pathSep   = System.getProperty("path.separator");

        Queue<String> queue = new LinkedList<>();
        Set<String>   seen  = new HashSet<>();

        StringTokenizer tok = new StringTokenizer(classPath, pathSep);
        while ( tok.hasMoreTokens() )
        {
            String elem = tok.nextToken();
            queue.add(elem);
            seen.add(elem);
        }

        while ( ! queue.isEmpty() )
        {
            String elem = queue.remove();

            // ignore filesystem classpath
            if ( ! elem.toLowerCase().endsWith(".jar") )
                continue;

            // make sure it exists
            File file = new File(elem);
            if ( ! file.exists() || ! file.canRead() )
                continue;

            String jarDir = file.getParent();

            try ( JarFile jarfile = new JarFile(elem, false) )
            {
                // add entries from manifest to check later
                Manifest manifest = jarfile.getManifest();
                if ( manifest != null )
                {
                    Attributes jarAttributes = manifest.getMainAttributes();
                    String classpath = jarAttributes.getValue(Attributes.Name.CLASS_PATH);
                    if ( classpath != null )
                    {
                        String[] relativePaths = classpath.split(" ");
                        for ( String relativePath : relativePaths )
                        {
                            String path = jarDir + File.separator + relativePath;
                            if ( ! seen.contains(path) )
                            {
                                queue.add(path);
                                seen.add(path);
                            }
                        }
                    }
                }

                Enumeration<JarEntry> entries = jarfile.entries();
                while ( entries.hasMoreElements() )
                {
                    String line = entries.nextElement().getName();

                    if ( ! line.toLowerCase().endsWith(".class") )
                        // not a class file, so we don't care
                        continue;

                    // line looks like:
                    //   pkg/subpkg/.../ClassName.class
                    //   blah.class
                    //   org/jt/util/ClassListEnquirer.class

                    int end = line.lastIndexOf('/');
                    if ( end < 0 )
                        // a class name without a package but inside a jar
                        continue;

                    String pname = line.substring(0, end).replace('/', '.');
                    String cname = line.substring(end + 1, line.length() - ".class".length());

                    if ( ! cname.contains("$") )
                        this.addClass(pname, cname);
                }
            }
            catch ( IOException exc )
            {
                // debugging only
                exc.printStackTrace();
            }
        }
    }

    private void loadPackages() throws PyException
    {
        // the jre will tell us about what jar files it has open.
        // use that facility to get a list of packages.
        // then read the files ourselves since java won't share.

        ClassLoader classLoader = this.getClass().getClassLoader();

        Package[] pkgs = Package.getPackages();
        for ( Package pkg : pkgs )
        {
            String pname = pkg.getName();
            URL url = classLoader.getResource(pname.replace('.', '/'));

            if ( url == null || ! url.getProtocol().equals("file") )
                continue;

            File dir = null;
            try
            {
                dir = new File(url.toURI());
            }
            catch ( java.net.URISyntaxException exc )
            {
                throw new PyException(exc);
            }

            for ( File classfile : dir.listFiles(new ClassFilenameFilter()) )
            {
                String fname = classfile.getName();
                String cname = fname.substring(0, fname.length() - ".class".length());

                this.addClass(pname, cname);
            }
        }
    }

    private void loadClassList() throws PyException
    {
        // The jre keeps a list of classes in the lib folder.
        // We don't have a better way to figure out what's in the java package,
        // so this is my little hack.

        // The thread's context ClassLoader is useful if resources have a different
        // ClassLoader than classes (e.g. tomcat), while the PythonInterpreter.class
        // ClassLoader is useful if running inside an OSGi container as a Bundle
        // (e.g. eclipse).
        ClassLoader[] classLoaders = new ClassLoader[] {
                                         Thread.currentThread().getContextClassLoader(),
                                         PythonInterpreter.class.getClassLoader() };

        String rname = String.format("org/jt/util/classlist_%d.txt", getJavaVersion());

        BufferedReader reader = null;
        try
        {
            InputStream input = null;
            int i = 0;
            while ( input == null && i < classLoaders.length )
            {
                ClassLoader classLoader = classLoaders[i];
                input = classLoader.getResourceAsStream(rname);
                i++;
            }

            if ( input == null )
                throw new PyException("ClassListEnquirer couldn't find resource " + rname);

            reader = new BufferedReader(new InputStreamReader(input));

            String line = null;
            while ( (line = reader.readLine()) != null )
            {
                // ignore any class with $
                if ( line.indexOf('$') > -1 )
                    continue;

                // lines in the file look like:
                //   java/lang/String

                int end = line.lastIndexOf('/');
                //String[] parts = line.split("\\/");
                String pname = line.substring(0, end).replace('/', '.');
                String cname = line.substring(end + 1);

                this.addClass(pname, cname);
            }
        }
        catch ( IOException exc )
        {
            throw new PyException(exc);
        }
        finally
        {
            try { if ( reader != null ) reader.close(); } catch ( IOException exc ) { }
        }
    }

    private void addClass(String pname, String cname)
    {
        // add a class with given package name

        // convert to style we need in C code
        String fqname = pname + "." + cname;

        List<String> cnames = this.packageToClassMap.get(pname);
        if ( cnames == null )
        {
            cnames = new ArrayList<>();
            this.packageToClassMap.put(pname, cnames);
        }

        if ( ! cnames.contains(fqname) )
            cnames.add(fqname);

        // now figure out any sub-packages based on the package name
        int dotIdx = pname.indexOf(".");
        while ( dotIdx > -1 )
        {
            String pkgStart = pname.substring(0, dotIdx);
            int nextDotIdx  = pname.indexOf(".", dotIdx + 1);
            String subPkg   = (nextDotIdx > -1) ? pname.substring(dotIdx + 1, nextDotIdx)
                                                : pname.substring(dotIdx + 1);

            List<String> pnames = this.packageToSubPackageMap.get(pkgStart);
            if ( pnames == null )
            {
                pnames = new ArrayList<>();
                this.packageToSubPackageMap.put(pkgStart, pnames);
            }

            if ( ! pnames.contains(subPkg) )
                pnames.add(subPkg);

            dotIdx = nextDotIdx;
        }
    }

    private static int getJavaVersion()
    {
        String version = System.getProperty("java.version");
        if ( version.startsWith("1.") )
            version = version.substring(2);
        int dotIdx  = version.indexOf('.');
        int dashIdx = version.indexOf('-');
        return Integer.parseInt(version.substring(0, dotIdx  > -1 ? dotIdx :
                                                     dashIdx > -1 ? dashIdx :
                                                     version.length()));
    }

    private static class ClassFilenameFilter implements FilenameFilter
    {
        @Override
        public boolean accept(File dir, String name)
        {
            return ( name != null && name.toLowerCase().endsWith(".class") );
        }
    }

    public static void main(String argv[]) throws Throwable
    {
        // for testing only

        String[] pnames = {"java.lang",
                           "org.jt" /* test loadPackages */ };
        if ( argv.length > 0 ) pnames = argv;

        for ( String pname : pnames )
            for ( String cname : ClassListEnquirer.getInstance().getClassNames(pname) )
                System.out.println(cname);
    }

    // storage for package, member classes
    private Map<String, List<String>> packageToClassMap = new HashMap<>();
    // storage for package, sub-packages based on classes found
    private Map<String, List<String>> packageToSubPackageMap = new HashMap<>();
    private static ClassListEnquirer instance = null;
}
