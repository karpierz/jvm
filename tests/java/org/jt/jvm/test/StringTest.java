
package org.jt.jvm.test;

import java.lang.String;

public class StringTest
{
    public static String fieldStaticString = new String("hello \uD83C\uDF0E!");
    public static String methodStaticString() { return new String("hello \uD83C\uDF0E!"); }
}
