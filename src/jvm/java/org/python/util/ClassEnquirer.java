//
//
//

package org.python.util;

public interface ClassEnquirer
{
    // TODO: Implement an OSGi class enquirer.

    // Interface to enquire if a name is available to be imported from Java.
    // Used by importer hook (see
    // <a href="https://www.python.org/dev/peps/pep-0302/">PEP 302</a>)
    // to determine if an attempt to import a module/package or class should be
    // directed to the Python importer or the Java <code>ClassLoader</code>.

    // Certain Java libraries (e.g. io.netty) may meet Java package naming
    // standards but will conflict with modules that Python provides (e.g.
    // import io). In general these package names should not be considered as
    // Java packages unless a ClassEnquirer explicitly chooses to include them.
    //
    public static final String[] RESTRICTED_PKG_NAMES = { "io", "re" };

    // Checks if the name is likely available in Java as a package. A return
    // value of true implies the name corresponds to a Java package, but does
    // not guarantee that an import will succeed. A return value of false
    // implies that an import from Java would fail, but does not guarantee that
    // an import will fail. Note: A fully-qualified Java class name should
    // return false since it is not a package name and the importer hook is
    // expecting that.
    //
    // @param name
    //        the name to check, such as java, java.util,
    //        java.util.ArrayList
    // @return true if it's likely a package supported by Java, false if it's
    //         likely a Python module (or a Java class name, or an invalid
    //         import)
    //
    public boolean isJavaPackage(String name);

    // Given a Java package name, gets the fully-qualified classnames available
    // for import in the package. This method is primarily used for
    // introspection using Python's dir() method. This method can return null
    // if dir() support is not necessary.
    //
    // @param pkgName
    //        the name of a package the ClassEnquirer supports, such as
    //        java.util
    // @return the list of classnames in the package, or null
    //
    public String[] getClassNames(String pkgName);

    // Given a Java package name, gets the sub-packages available. For example,
    // a sub-package of package "java" is "util", and a sub-package of package
    // "java.util" is "concurrent". This method is primarily used for
    // introspection using Python's dir() method. This method can return null
    // if dir() support is not necessary.
    //
    // @param pkgName
    //        the name of a package the ClassEnquirer supports, such as
    //        java.util
    // @return the list of sub-packages in the package, or null
    //
    public String[] getSubPackages(String pkgName);
}
