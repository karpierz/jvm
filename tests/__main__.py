# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import unittest
import sys
import os
import logging

from . import test_dir

log = logging.getLogger(__name__)

test_java = os.path.join(test_dir, "java")


def test_suite(names=None, omit=("run",)):
    from . import __name__ as pkg_name
    from . import __path__ as pkg_path
    import unittest
    import pkgutil
    if names is None:
        names = [name for _, name, _ in pkgutil.iter_modules(pkg_path)
                 if name != "__main__" and not name.startswith("tman_")
                 and name not in omit]
    names = [".".join((pkg_name, name)) for name in names]
    tests = unittest.defaultTestLoader.loadTestsFromNames(names)
    return tests


def main(argv=sys.argv):

    import jvm as _jvm
    import jvm.platform

    jvm_path = jvm.platform.JVMFinder(java_version=1.8).get_jvm_path()

    print("Running testsuite using JVM:", jvm_path, "\n", file=sys.stderr)

    package = sys.modules[__package__]
    package.jvm = jvm = _jvm.JVM(jvm_path)
    jvm.JavaException = JavaException
    jvm.ExceptionsMap = {
        _jvm.EStatusCode.ERR:       UnknownError,
        _jvm.EStatusCode.EDETACHED: ThreadNotAttachedError,
        _jvm.EStatusCode.EVERSION:  VersionNotSupportedError,
        _jvm.EStatusCode.ENOMEM:    NotEnoughMemoryError,
        _jvm.EStatusCode.EEXIST:    JVMAlreadyExistError,
        _jvm.EStatusCode.EINVAL:    InvalidArgumentError,
    }
    jvm.start("-Djava.class.path={}".format(
              os.pathsep.join([os.path.join(test_java, "classes")])),
              "-ea", "-Xms16M", "-Xmx512M")
    try:
        tests = test_suite(argv[1:] or None)
        result = unittest.TextTestRunner(verbosity=2).run(tests)
    finally:
        jvm.shutdown()

    return 0 if result.wasSuccessful() else 1


class JavaException(Exception):
    """ """

class UnknownError(Exception):
    """ """

class ThreadNotAttachedError(Exception):
    """ """

class VersionNotSupportedError(Exception):
    """ """

class NotEnoughMemoryError(Exception):
    """ """

class JVMAlreadyExistError(Exception):
    """ """

class InvalidArgumentError(Exception):
    """ """


if __name__.rpartition(".")[-1] == "__main__":
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
