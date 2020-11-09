# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import List
import os
from os import path
import re

from ..lib import public
from ..lib import cli


@public
class JVMFinder:

    # JVM library finder base class

    def __init__(self, java_version=None):
        # To specify the required version, set the 'java_version' to the
        # major version required, e.g. 1.3 or "1.3", but not e.g. "1.3.1".

        self._java_version = float(java_version) if java_version is not None else 0.0

        # Library file name
        self._libfile = "libjvm.so"

        # Predefined locations
        self._locations = (
            "/usr/lib/jvm",
            "/usr/java",
        )

        # Search methods
        self._methods = (
            self._get_from_java_home,
            self._get_from_known_locations,
        )

    def check(self, jvm):
        """
        Check if the jvm is valid for this architecture.

        This method should be overriden for each architecture.

        Raises:
            JVMNotSupportedException: If the jvm is not supported.
        """

    def get_jvm_path(self):
        """
        Retrieves the path to the default or first found JVM library

        Returns:
            The path to the JVM shared library file

        Raises:
            RuntimeError: No JVM library found or No Support JVM found
        """
        for method in self._methods:
            try:
                jvm = method()
                # If found check the architecture
                if jvm:
                    self.check(jvm)
            except (NotImplementedError, JVMNotFoundException, JVMNotSupportedException):
                pass
            else:
                if jvm is not None:
                    return jvm
        else:
            raise JVMNotFoundException("No JVM shared library file ({}) found. "
                                       "Try setting up the JAVA_HOME environment "
                                       "variable properly.".format(self._libfile))

    def find_libjvm(self, java_home: str):
        """
        Recursively looks for the given file

        Parameters:
            java_home: A Java home folder

        Returns:
            The first found file path

        Raises:
            ValueError: No JVM library found or No Support JVM found
        """
        non_supported_jvm = ("cacao", "jamvm")
        # Look for the file
        found_non_supported_jvm = False
        for root, _, names in os.walk(java_home):
            if self._libfile in names:
                # Found it, but check for non supported jvms
                candidate = path.split(root)[1]
                if candidate in non_supported_jvm:
                    found_non_supported_jvm = True
                else:
                    return path.join(root, self._libfile)
        else:
            if found_non_supported_jvm:
                raise JVMNotSupportedException("Sorry '{}' is known to be broken. "
                                               "Please ensure your JAVA_HOME contains "
                                               "at least another JVM implementation "
                                               "(eg. server)".format(candidate))
            else:
                raise JVMNotFoundException("Sorry no JVM could be found. "
                                           "Please ensure your JAVA_HOME environment "
                                           "variable is pointing to correct installation.")

    def find_possible_homes(self, parents: List[str]):
        """
        Generator that looks for the first-level children folders that could be
        Java installations, according to their name

        Parameters:
            parents: A list of parent directories

        Returns:
            The possible JVM installation folders
        """
        java_names = ("jre", "jdk", "java")
        homes = set()
        for parent in parents:
            for childname in sorted(os.listdir(parent)):
                home = path.realpath(path.join(parent, childname))
                # Already known home, or not a directory -> ignore
                if home not in homes and path.isdir(home):
                    # Check if the home seems OK
                    real_name = path.basename(home).lower()
                    for java_name in java_names:
                        if java_name in real_name:
                            # Correct JVM folder name
                            homes.add(home)
                            yield home
                            break

    def get_java_version(self, java_exe):
        cout = cli.cmd(java_exe, "-version").stderr
        match = re.search('^\s*java version\s+"(.+)"', cout, re.MULTILINE)
        return float(".".join(match.group(1).split(".")[:2]))

    def get_jre_home(self, java_home):
        if path.isfile(path.join(java_home, "bin", "javac")):
            # this is a JDK
            java_home = path.join(java_home, "jre")
            return java_home if path.isdir(java_home) else None
        elif path.isfile(path.join(java_home, "bin", "java")):
            # this is a JRE
            return java_home
        else:
            return None

    def _get_from_java_home(self):
        java_home = os.environ.get("JAVA_HOME")

        if not java_home or not path.exists(java_home):
            return None

        java_home = path.realpath(java_home)
        # Cygwin has a bug in realpath
        if not path.exists(java_home):
            java_home = os.environ.get("JAVA_HOME")

        return self.find_libjvm(java_home)

    def _get_from_known_locations(self):
        for home in self.find_possible_homes(self._locations):
            jvm = self.find_libjvm(home)
            if jvm is not None:
                return jvm
        else:
            return None


class JVMNotFoundException(RuntimeError):
    """ """

class JVMNotSupportedException(RuntimeError):
    """ """
