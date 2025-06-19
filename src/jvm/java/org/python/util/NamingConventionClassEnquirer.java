//
//
//

package org.python.util;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Set;
import java.util.HashSet;
import java.util.Locale;

public class NamingConventionClassEnquirer implements ClassEnquirer
{
    // A simple ClassEnquirer to see if the package/class to be imported in
    // a Python sub-interpreter should be considered as a Java package/class.
    // This enquirer can check for import statements beginning with java,
    // com, org, gov, etc and country codes such as us, uk, fr, ch, etc.
    //
    // This class is useful for the following scenarios:
    //  - You don't want the overhead of initializing ClassListEnquirer.getInstance()
    //  - You don't want all the classes in a package automatically imported
    //  - You don't have Python modules that resemble Java package names

    // the default top level package names.
    protected static final List<String> TOP_LEVEL = Collections.unmodifiableList(
        Arrays.asList("java", "javax", "javafx",
                      "com", "org", "gov", "edu", "mil", "net"));

    protected Set<String> javaNames;

    public NamingConventionClassEnquirer()
    {
        this(true);
    }

    public NamingConventionClassEnquirer(boolean includeDefaults)
    {
        this(includeDefaults, false);
    }

    public NamingConventionClassEnquirer(boolean includeDefaults,
                                         boolean includeCountryCodes)
    {
        // Constructor
        //
        // @param includeDefaults
        //        whether or not typical package names such as java, javax,
        //        com, org, gov should be considered as a java package.
        // @param includeCountryCodes
        //        whether or not a name starting with a 2-letter country code
        //        such a uk, fr, us, ch should be considered as a Java package.

        if ( includeCountryCodes )
        {
            String[] codes = Locale.getISOCountries();

            if ( includeDefaults )
            {
                this.javaNames = new HashSet<>(TOP_LEVEL.size() + codes.length);
                this.javaNames.addAll(TOP_LEVEL);
            }
            else
                this.javaNames = new HashSet<>(codes.length);

            for ( String country : codes )
                this.javaNames.add(country.toLowerCase());

            for ( String restrictedPkg : ClassEnquirer.RESTRICTED_PKG_NAMES )
                this.javaNames.remove(restrictedPkg);
        }
        else
        {
            if ( includeDefaults )
                this.javaNames = new HashSet<>(TOP_LEVEL);
            else
                this.javaNames = new HashSet<>();
        }
    }

    public void addTopLevelPackageName(String pkgStart)
    {
        // Adds a top level package name to the list of names that should be
        // considered as Java packages
        //
        // @param pkgStart
        //        the start of a java package name to check, e.g. com, org,
        //        gov, us, it, fr

        this.javaNames.add(pkgStart);
    }

    //-- Implementation of ClassEnquirer --//

    @Override
    public boolean isJavaPackage(String name)
    {
        if ( name == null )
            throw new IllegalArgumentException("name must not be null");

        if ( this.javaNames.contains(name) )
            return true;
        else
        {
            String[] split = name.split("\\.");
            return (split.length > 0 && this.javaNames.contains(split[0]) &&
                    Character.isLowerCase(split[split.length - 1].charAt(0)));
        }
    }

    @Override
    public String[] getClassNames(String pkgName)
    {
        return null;
    }

    @Override
    public String[] getSubPackages(String pkgName)
    {
        return null;
    }
}
