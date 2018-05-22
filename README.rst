jtypes.jvm
==========

Pure Python Java package

Overview
========

  | jtypes.jvm is a bridge between Python and Java JVM, allowing these to intercommunicate.
  | It is an effort to allow python programs full access to Java class libraries.
  | 
  | jtypes.jvm is a lightweight Python package, based on the ctypes FFI library.
  | It is a fork of Steve Menard's good known JPype package by reimplementing whole it's
    functionality in a clean Python instead of C/C++.


What is jtypes.jvm:
-------------------

  jtypes.jvm is an effort to allow python programs full access to Java class libraries.
  This is achieved not through re-implementing Python, as Jython/JPython has done,
  but rather through interfacing at the native level in both virtual machines.

  Eventually, it should be possible to replace Java with python in many, though not all, situations.
  JSP, Servlets, RMI servers and IDE plugins are good candidates.

  Once this integration is achieved, a second phase will be started to separate the Java logic from
  the Python logic, eventually allowing the bridging technology to be used in other environments,
  I.E. Ruby, Perl, COM, etc ...


Known Bugs/Limitations :
    * Java classes outside of a package (in the <default>) cannot be imported.
    * Because of lack of JVM support, you cannot shutdown the JVM and then restart it.
    * Some methods rely on the "current" class/caller. Since calls coming directly from
      python code do not have a current class, these methods do not work. The User Manual
      lists all the known methods like that.

Support
-------

If you need assistance, you can ask for help on our mailing list:

* User Group : https://groups.google.com/group/kivy-users
* Email      : kivy-users@googlegroups.com

We also have an IRC channel:

* Server  : irc.freenode.net
* Port    : 6667, 6697 (SSL only)
* Channel : #kivy


Installation
============

Prerequisites:

+ Python 2.7 or higher or 3.4 or higher

  * http://www.python.org/
  * 2.7 and 3.4 are primary test environments.

+ pip and setuptools

  * http://pypi.python.org/pypi/pip
  * http://pypi.python.org/pypi/setuptools

To install run::

    python -m pip install --upgrade jtypes.jvm

To ensure everything is running correctly you can run the tests using::

    python -m jt.jvm.tests

License
=======

  | Copyright (c) 2004-2018 Adam Karpierz
  |
  | Licensed under proprietary License
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Adam Karpierz <python@python.pl>
