jvm
===

Python bridge for the Java Virtual Machine.

Overview
========

| |package_bold| is a bridge between Python and JVM, allowing these to intercommunicate.
| It is an effort to allow Python programs full access to Java class libraries.

`PyPI record`_.

`Documentation`_.

| |package_bold| package is closely based on the `jni`_ Python package.

What is |package|:
------------------

| |package_bold| is an effort to allow Python programs full access to Java class libraries.
| This is achieved not through re-implementing Python, as Jython has done, but rather
  through interfacing at the native level in both virtual machines.

Eventually, it should be possible to replace Java with python in many, though not all,
situations. JSP, Servlets, RMI servers and IDE plugins are good candidates.

Once this integration is achieved, a second phase will be started to separate the Java
logic from the Python logic, eventually allowing the bridging technology to be used
in other environments, I.E. Ruby, Perl, COM, etc ...

Known Bugs/Limitations :
  * Java classes outside of a package (in the <default>) cannot be imported.
  * Because of lack of JVM support, you cannot shutdown the JVM and then restart it.
  * Some methods rely on the "current" class/caller. Since calls coming directly from
    python code do not have a current class, these methods do not work. The User Manual
    lists all the known methods like that.

Installation
============

Prerequisites:

+ Python 3.6 or higher

  * https://www.python.org/
  * 3.7 with Java 8 is a primary test environment.

+ pip and setuptools

  * https://pypi.org/project/pip/
  * https://pypi.org/project/setuptools/

To install run:

  .. parsed-literal::

    python -m pip install --upgrade |package|

Development
===========

Prerequisites:

+ Development is strictly based on *tox*. To install it run::

    python -m pip install --upgrade tox

Visit `development page`_.

Installation from sources:

clone the sources:

  .. parsed-literal::

    git clone |respository| |package|

and run:

  .. parsed-literal::

    python -m pip install ./|package|

or on development mode:

  .. parsed-literal::

    python -m pip install --editable ./|package|

License
=======

  | Copyright (c) 2004-2022 Adam Karpierz
  | Licensed under CC BY-NC-ND 4.0
  | Licensed under proprietary License
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Adam Karpierz <adam@karpierz.net>

.. |package| replace:: jvm
.. |package_bold| replace:: **jvm**
.. |respository| replace:: https://github.com/karpierz/jvm.git
.. _development page: https://github.com/karpierz/jvm
.. _PyPI record: https://pypi.org/project/jvm/
.. _Documentation: https://jvm.readthedocs.io/
.. _jni: https://pypi.org/project/jni/
