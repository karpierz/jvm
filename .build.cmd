@echo off
setlocal
set JAVA8_HOME=C:\Program Files\Java\jdk1.8.0_181
if not defined JAVA_HOME (set JAVA_HOME=%JAVA8_HOME%)
set javac="%JAVA_HOME%"\bin\javac -encoding UTF-8 -g:none -deprecation -Xlint:unchecked ^
    -source 1.8 -target 1.8 -bootclasspath "%JAVA8_HOME%\jre\lib\rt.jar"
set py=C:\Windows\py.exe -3.6 -B
set vc32="%ProgramFiles(x86)%\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars32.bat"
set vc64="%ProgramFiles(x86)%\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat"
pushd "%~dp0"
rmdir /Q/S %TEMP%\jtypes.jvm 2> nul
setlocal
set ARCH=x86
set BUILD_DIR=%TEMP%\jtypes.jvm\build-%ARCH%
mkdir %BUILD_DIR%
call %vc32%
cl /TC /O2 /Ob2 /LD ^
   /wd4133 /Y- /Fd%BUILD_DIR%\ /Fo%BUILD_DIR%\ ^
   /Fe.\src\jt\jvm\java\org\python\util\PythonInterpreter-windows-%ARCH%.dll ^
   /I..\jtypes.jni\src .\src\jt\jvm\java\org\python\util\PythonInterpreter.c ^
   /link /IMPLIB:%BUILD_DIR%\PythonInterpreter.lib /INCREMENTAL:NO
endlocal
setlocal
set ARCH=x64
set BUILD_DIR=%TEMP%\jtypes.jvm\build-%ARCH%
mkdir %BUILD_DIR%
call %vc64%
cl /TC /O2 /Ob2 /LD ^
   /wd4133 /Y- /Fd%BUILD_DIR%\ /Fo%BUILD_DIR%\ ^
   /Fe.\src\jt\jvm\java\org\python\util\PythonInterpreter-windows-%ARCH%.dll ^
   /I..\jtypes.jni\src .\src\jt\jvm\java\org\python\util\PythonInterpreter.c ^
   /link /IMPLIB:%BUILD_DIR%\PythonInterpreter.lib /INCREMENTAL:NO
endlocal
popd
pushd "%~dp0"\src\jt\jvm\java
%javac% ^
    com\jt\*.java ^
    com\jt\reflect\*.java ^
    com\jt\ref\*.java ^
    org\python\*.java ^
    org\python\core\*.java ^
    org\python\util\*.java ^
    org\python\jsr223\*.java
%py% -m class2py com\jt\ProxyException.class
%py% -m class2py com\jt\reflect\ProxyHandler.class
%py% -m class2py com\jt\ref\Reference.class
%py% -m class2py com\jt\ref\ReferenceQueue.class
%py% -m class2py org\python\Version.class
%py% -m class2py org\python\core\PyObject.class
%py% -m class2py org\python\core\PyModule.class
%py% -m class2py org\python\core\PyClass.class
%py% -m class2py org\python\core\PyException.class
%py% -m class2py org\python\util\PythonInterpreter$Options.class
%py% -m class2py org\python\util\PythonInterpreter$Config.class
%py% -m class2py org\python\util\PythonInterpreter$MemoryManager.class
%py% -m class2py org\python\util\PythonInterpreter.class
%py% -m class2py org\python\util\PythonInterpreter$1.class
%py% -m class2py org\python\util\PythonInterpreter$Python.class
%py% -m class2py org\python\util\PythonInterpreter$Python$1.class
%py% -m class2py org\python\util\PythonInterpreter$Python$Platform.class
%py% -m class2py org\python\util\PythonInterpreter$Python$Windows.class
%py% -m class2py org\python\util\PythonInterpreter$Python$Linux.class
%py% -m class2py org\python\util\PythonInterpreter$Python$Solaris.class
%py% -m class2py org\python\util\PythonInterpreter$Python$MacOS.class
%py% -m class2py org\python\util\PythonInterpreter$Python$Unix.class
%py% -m class2py org\python\util\ClassEnquirer.class
%py% -m class2py org\python\util\ClassListEnquirer.class
%py% -m class2py org\python\util\ClassListEnquirer$1.class
%py% -m class2py org\python\util\ClassListEnquirer$ClassFilenameFilter.class
%py% -m class2py org\python\util\NamingConventionClassEnquirer.class
%py% -m class2py org\python\jsr223\PyScriptEngineFactory.class
%py% -m class2py org\python\jsr223\PyScriptEngine.class
%py% -m class2py org\python\jsr223\PyScriptEngine$PyCompiledScript.class
del /F/Q/S ^
    com\*.class ^
    org\*.class ^
    > nul
popd
pushd "%~dp0"\tests\c
rmdir /Q/S build 2> nul & mkdir build
%javac% -d build ^
    ..\..\src\jt\jvm\java\org\python\util\Run.java ^
    ..\..\src\jt\jvm\java\org\python\util\PythonInterpreter.java ^
    ..\..\src\jt\jvm\java\org\python\util\ClassEnquirer.java ^
    ..\..\src\jt\jvm\java\org\python\util\ClassListEnquirer.java ^
    ..\..\src\jt\jvm\java\org\python\util\NamingConventionClassEnquirer.java ^
    ..\..\src\jt\jvm\java\org\python\core\PyModule.java ^
    ..\..\src\jt\jvm\java\org\python\core\PyObject.java ^
    ..\..\src\jt\jvm\java\org\python\core\PyException.java
popd
pushd "%~dp0"\tests
rmdir /Q/S java\classes 2> nul & mkdir java\classes
dir /S/B/O:N ^
    ..\src\jt\jvm\java\org\python\*.java ^
    ..\src\jt\jvm\java\org\python\core\*.java ^
    ..\src\jt\jvm\java\org\python\util\*.java ^
    ..\src\jt\jvm\java\com\jt\ref\*.java ^
    java\*.java ^
    2> nul > build.fil
%javac% -d java/classes -classpath java/lib/* @build.fil
del /F/Q build.fil
popd
endlocal
