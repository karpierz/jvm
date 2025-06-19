# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

from typing import Tuple, Sequence
from pathlib import Path
import os
import re

from ..lib import public
from ..lib import run


@public
class JVMFinder:

    # JVM library finder base class

    def __init__(self, java_version=None):
        """Initializer"""

        # To specify the required version, set the 'java_version' to the
        # major version required, e.g. 1.3 or "1.3", but not e.g. "1.3.1".

        self._java_version = float(java_version) if java_version is not None else 0.0

        # Library file name
        self._libfile: str = "libjvm.so"

        # Predefined locations
        self._locations: Tuple[Path] = (
            Path("/usr/lib/jvm"),
            Path("/usr/java"),
        )

        # Search methods
        self._methods = (
            self._get_from_java_home,
            self._get_from_known_locations,
        )

    def check(self, jvm: Path):
        """
        Check if the jvm is valid for this architecture.

        This method should be overriden for each architecture.

        Raises:
            JVMNotSupportedError: If the jvm is not supported.
        """

    def get_jvm_path(self) -> Path:
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
            except (NotImplementedError, JVMNotFoundError, JVMNotSupportedError):
                pass
            else:
                if jvm is not None:
                    return jvm
        else:
            raise JVMNotFoundError("No JVM shared library file ({}) found. "
                                   "Try setting up the JAVA_HOME environment "
                                   "variable properly.".format(self._libfile))

    def find_libjvm(self, java_home: Path) -> Path:
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
            root = Path(root)
            if self._libfile in names:
                # Found it, but check for non supported jvms
                candidate = root.parts[1]
                if candidate in non_supported_jvm:
                    found_non_supported_jvm = True
                else:
                    return root/self._libfile
        else:
            if found_non_supported_jvm:
                raise JVMNotSupportedError("Sorry '{}' is known to be broken. "
                                           "Please ensure your JAVA_HOME contains "
                                           "at least another JVM implementation "
                                           "(eg. server)".format(candidate))
            else:
                raise JVMNotFoundError("Sorry no JVM could be found. "
                                       "Please ensure your JAVA_HOME environment "
                                       "variable is pointing to correct installation.")

    def find_possible_homes(self, parents: Sequence[Path],
                            java_names = ("jre", "jdk", "java")):
        """
        Generator that looks for the first-level children folders that could be \
        Java installations, according to their name.

        Parameters:
            parents: A list of parent directories

        Returns:
            The possible JVM installation folders
        """
        homes = set()
        for parent in parents:
            for home in sorted(parent.resolve().iterdir()):
                # Already known home, or not a directory -> ignore
                if home not in homes and home.is_dir():
                    # Check if the home seems OK
                    real_name = home.name.lower()
                    for java_name in java_names:
                        if java_name in real_name:
                            # Correct JVM folder name
                            homes.add(home)
                            yield home
                            break

    def get_java_home(self) -> Path | None:
        java_home = os.environ.get("JAVA_HOME")
        return Path(java_home) if java_home else None

    def get_jdk_home(self) -> Path | None:
        jdk_home = os.environ.get("JDK_HOME")
        return Path(jdk_home) if jdk_home else None

    def get_java_version(self, java_exe) -> float:
        cout = run(java_exe, "-version", text=True, capture_output=True).stderr
        match = re.search(r'^\s*java version\s+"(.+)"', cout, re.MULTILINE)
        return float(".".join(match.group(1).split(".")[:2]))

    def get_jre_home(self, java_home: Path) -> Path | None:
        if (java_home/"bin/javac").is_file():
            # this is a JDK
            java_home = java_home/"jre"
            return java_home if java_home.is_dir() else None
        elif (java_home/"bin/java").is_file():
            # this is a JRE
            return java_home
        else:
            return None

    def _get_from_java_home(self) -> Path | None:
        java_home = self.get_java_home()

        if not java_home or not java_home.exists():
            return None

        # Cygwin has a bug in realpath/resolve
        if java_home.resolve().exists():
            java_home = java_home.resolve()

        return self.find_libjvm(java_home)

    def _get_from_known_locations(self) -> Path | None:
        for home in self.find_possible_homes(self._locations):
            jvm = self.find_libjvm(home)
            if jvm is not None:
                return jvm
        else:
            return None


class JVMNotFoundError(RuntimeError):
    """???"""

class JVMNotSupportedError(RuntimeError):
    """???"""
