@echo off
setlocal enableDelayedExpansion
set JAVA_HOME=C:\Program Files\Zulu\zulu-11
set javac="%JAVA_HOME%\bin\javac" -encoding UTF-8 -g:none ^
          -deprecation -Xlint:unchecked --release 8

::set py=C:\Windows\py.exe -3.9  -B
::set py=C:\Windows\py.exe -3.10 -B
::set py=C:\Windows\py.exe -3.11 -B
set py=C:\Windows\py.exe -3.12 -B
::set py=C:\Windows\py.exe -3.13 -B
set vcdir=%ProgramFiles%\Microsoft Visual Studio\2022
set vc32="%vcdir%\Community\VC\Auxiliary\Build\vcvars32.bat"
set vc64="%vcdir%\Community\VC\Auxiliary\Build\vcvars64.bat"
if exist %vc32% goto :start
set vc32="%vcdir%\BuildTools\VC\Auxiliary\Build\vcvars32.bat"
set vc64="%vcdir%\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
if exist %vc32% goto :start
echo VC compiler (2022) should be installed!
goto :exit
:start
pushd "%~dp0"
rmdir /Q/S %TEMP%\jvm 2> nul
setlocal
set ARCH=x86
set BUILD_DIR=%TEMP%\jvm\build-%ARCH%
mkdir %BUILD_DIR%
call %vc32%
cl /TC /O2 /Ob2 /LD ^
   /wd4133 /Y- /Fd%BUILD_DIR%\ /Fo%BUILD_DIR%\ ^
   /Fe.\src\jvm\java\org\python\util\PythonInterpreter-windows-%ARCH%.dll ^
   /I..\jni\src .\src\jvm\java\org\python\util\PythonInterpreter.c ^
   /link /IMPLIB:%BUILD_DIR%\PythonInterpreter.lib /INCREMENTAL:NO
endlocal
setlocal
set ARCH=x64
set BUILD_DIR=%TEMP%\jvm\build-%ARCH%
mkdir %BUILD_DIR%
call %vc64%
cl /TC /O2 /Ob2 /LD ^
   /wd4133 /Y- /Fd%BUILD_DIR%\ /Fo%BUILD_DIR%\ ^
   /Fe.\src\jvm\java\org\python\util\PythonInterpreter-windows-%ARCH%.dll ^
   /I..\jni\src .\src\jvm\java\org\python\util\PythonInterpreter.c ^
   /link /IMPLIB:%BUILD_DIR%\PythonInterpreter.lib /INCREMENTAL:NO
endlocal
popd
pushd "%~dp0"\src\jvm\java
%py% org\python\Version.py
%javac% ^
    org\jt\reflect\*.java ^
    org\jt\ref\*.java ^
    org\python\*.java ^
    org\python\core\*.java ^
    org\python\util\*.java ^
    org\python\jsr223\*.java
%py% -m class2py org\jt\reflect\ProxyHandler.class
%py% -m class2py org\jt\ref\Reference.class
%py% -m class2py org\jt\ref\ReferenceQueue.class
%py% -m class2py org\jt\ref\ReferenceQueue$Worker.class
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
    org\*.class ^
    > nul
popd
pushd "%~dp0"\tests\c
rmdir /Q/S build 2> nul & mkdir build
%javac% -d build ^
    ..\..\src\jvm\java\org\python\util\Run.java ^
    ..\..\src\jvm\java\org\python\util\PythonInterpreter.java ^
    ..\..\src\jvm\java\org\python\util\ClassEnquirer.java ^
    ..\..\src\jvm\java\org\python\util\ClassListEnquirer.java ^
    ..\..\src\jvm\java\org\python\util\NamingConventionClassEnquirer.java ^
    ..\..\src\jvm\java\org\python\core\PyModule.java ^
    ..\..\src\jvm\java\org\python\core\PyObject.java ^
    ..\..\src\jvm\java\org\python\core\PyException.java
popd
pushd "%~dp0"\tests
rmdir /Q/S java\classes 2> nul & mkdir java\classes
dir /S/B/O:N ^
    ..\src\jvm\java\org\jt\ref\*.java ^
    ..\src\jvm\java\org\python\*.java ^
    ..\src\jvm\java\org\python\core\*.java ^
    ..\src\jvm\java\org\python\util\*.java ^
    java\*.java ^
    2> nul > build.fil
%javac% -d java/classes -classpath java/lib/* @build.fil
del /F/Q build.fil
popd
:exit
endlocal
