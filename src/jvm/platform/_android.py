# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Tuple
from pathlib import Path
import os
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
        self._java: Path = Path("/usr/bin/java")

        # Library file name
        self._libfile: str = "libjvm.so"

        # Predefined locations
        self._locations: Tuple[Path] = (
            Path("/usr/lib/jvm"),
            Path("/usr/java"),
            Path("/opt/sun"),
        )

        # Search methods
        self._methods = (
            self._get_from_java_home,  # self._getFromJavaHome,
            self._get_from_bin,        # self._getFromLibPath,
            self._get_from_known_locations,
        )

    def _get_from_bin(self) -> Optional[Path]:
        java_exe = self._java.resolve()
        if java_exe.exists():
            # Get to the home directory
            java_home = java_exe.parent.parent
            return self.find_libjvm(java_home)
        else:
            return None

    def _getFromJavaHome(self) -> Optional[Path]:

        java_home = self.get_java_home()

        if java_home is not None:
            # Check JAVA_HOME directory to see if Java version is adequate
            java_exe = java_home/"bin/java"
            if java_exe.is_file():
                if (not self._java_version or
                    self.get_java_version(java_exe) == self._java_version):
                    jre_home = self.get_jre_home(java_home)
                else:
                    java_home = None

        if java_home is not None:
            for jvm_subdir in ("lib/amd64/server",
                               "lib/i386/client",
                               "lib/i386/server"):
                jvm_path = jre_home/jvm_subdir/self._libfile
                if jvm_path.is_file():
                    return jvm_path
            else:
                jvm_path = None

        return None

    def _getFromLibPath(self) -> Optional[Path]:
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

    def _getFromKnownLocations(self) -> Optional[Path]:

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
