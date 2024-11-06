# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import os
from os import path
import re

from ..lib import public

from . import _linux


@public
class JVMFinder(_linux.JVMFinder):
    """
    Android JVM library finder class
    """

    def __init__(self, java_version=None):
        super().__init__(java_version)

        # Java bin file
        self._java = "/usr/bin/java"

        # Library file name
        self._libfile = "libjvm.so"

        # Predefined locations
        self._locations = (
            "/usr/lib/jvm",
            "/usr/java",
            "/opt/sun",
        )

        # Search methods
        self._methods = (
            self._get_from_java_home,
            self._get_from_bin,
            self._get_from_known_locations,
        )
        # self._methods = (
        #     self._getFromJavaHome,
        #     self._getFromLibPath,
        #     self._get_from_known_locations,
        # )

    def _get_from_bin(self):
        java_exe = path.realpath(self._java)
        if path.exists(java_exe):
            # Get to the home directory
            java_home = path.dirname(path.dirname(java_exe))
            return self.find_libjvm(java_home)
        else:
            return None

    def _getFromJavaHome(self):
        java_home = os.environ.get("JAVA_HOME")

        if java_home is not None:
            # Check JAVA_HOME directory to see if Java version is adequate
            java_exe = path.join(java_home, "bin", "java")
            if path.isfile(java_exe):
                if not self._java_version or self.get_java_version(java_exe) == self._java_version:
                    jre_home = self.get_jre_home(java_home)
                else:
                    java_home = None

        if java_home is not None:
            for jvm_subdir in ("lib/amd64/server",
                               "lib/i386/client",
                               "lib/i386/server"):
                jvm_path = path.join(jre_home, jvm_subdir, self._libfile)
                if path.isfile(jvm_path):
                    return jvm_path
            else:
                jvm_path = None

        return None

    def _getFromLibPath(self):
        # on linux, the JVM has to be in the LD_LIBRARY_PATH anyway,
        # so might as well inspect it

        ld_library_path = os.environ.get("LD_LIBRARY_PATH")

        if ld_library_path is not None:
            for lib_path in ld_library_path.split(os.pathsep):
                if lib_path.find("jre") != -1:
                    # this could be it!
                    # TODO
                    pass

        return None

    def _getFromKnownLocations(self):
        KNOWN_LOCATIONS = [
            (r"/opt/sun/",  re.compile(r"j2sdk(.+)/jre/lib/i386/client/")),
            (r"/usr/java/", re.compile(r"j2sdk(.+)/jre/lib/i386/client/")),
            (r"/usr/java/", re.compile(r"jdk(.+)/jre/lib/i386/client/")),
        ]

        for location, pattern in KNOWN_LOCATIONS:
            pattern += self._libfile
            # TODO
            pass

        return None
