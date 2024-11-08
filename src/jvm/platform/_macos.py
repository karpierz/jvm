# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Tuple
from pathlib import Path

from ..lib import public
from ..lib import run

from . import _linux


@public
class JVMFinder(_linux.JVMFinder):
    """
    Mac OS X JVM library finder class
    """

    def __init__(self, java_version=None):
        super().__init__(java_version)

        # Library file name
        self._libfile: str = "libjli.dylib"

        # Predefined locations
        self._locations: Tuple[Path] = (
            Path("/Library/Java/JavaVirtualMachines"),
        )

        # Search methods
        self._methods += (
            self._pre_vm7_path,
            self._javahome_binary,
        )
        # self._methods += (
        #     self.defaultPath,
        # )

    def _pre_vm7_path(self) -> Optional[Path]:
        # Returns the previous (older then Java7) constant JVM library path
        return Path("/System/Library/Frameworks/JavaVM.framework/JavaVM")

    def _javahome_binary(self) -> Optional[Path]:
        # For osx > 10.5 we have the nice util /usr/libexec/java_home available.
        # Invoke it and return its output.
        # It seems this tool has been removed in osx 10.9.
        import platform
        import subprocess
        from distutils.version import StrictVersion
        current = StrictVersion(platform.mac_ver()[0][:4])
        if not (current >= StrictVersion("10.6") and current < StrictVersion("10.9")):
            return None
        return subprocess.check_output(["/usr/libexec/java_home"]).strip()

    def defaultPath(self) -> Optional[Path]:
        # This script attempts to find an existing installation of Java that
        # meets a minimum version requirement on a Mac OS X machine.

        # on darwin, the JVM is always in the same location it seems ...
        return Path("/System/Library/Frameworks/JavaVM.framework/JavaVM")

        java_home = self.get_java_home()

        if java_home is not None:
            # Check JAVA_HOME directory to see if Java version is adequate
            java_exe = java_home/"bin/java"
            # [...]

        if java_home is None:
            # If the existing JAVA_HOME directory is inadequate, use '/usr/libexec/java_home'
            # to search for other possible java candidates and check their versions.
            if Path("/usr/libexec/java_home").isfile(): # -x
                # Apple JDKs
                java_home = run("/usr/libexec/java_home",
                                "" if not self._java_version else f"-v {self._java_version}",
                                text=True, capture_output=True).stdout.strip()
                java_home = Path(java_home) if java_home else None
            else:
                # Look for the Apple JDKs first to preserve the existing behaviour,
                # and then look for the new JDKs provided by Oracle.
                framework_jdk = Path("/System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK")
                system_jdk    = Path("/System/Library/Java/JavaVirtualMachines/CurrentJDK")
                location_jdk  = self._locations[0]/"CurrentJDK"
                if framework_jdk.is_link():
                    # Apple JDKs
                    java_home = framework_jdk/"Home"
                elif system_jdk.is_link():
                    # Apple JDKs
                    java_home = system_jdk/"Contents/Home"
                elif location_jdk.is_link():
                    # Oracle JDKs
                    java_home = location_jdk/"Contents/Home"


### return top Java version
# cout = run("/usr/libexec/java_home", text=True, capture_output=True).stdout
# self._locations[0] + "/1.7.0.jdk/Contents/Home"

### I want Java version 1.7
# cout = run("/usr/libexec/java_home", "-v 1.7", text=True, capture_output=True).stdout
# "/System/Library/Java/JavaVirtualMachines/1.7.0.jdk/Contents/Home"

    # Oracle:       "/Library/Java/Home"
    # Apple: "/System/Library/Frameworks/JavaVM.framework/Home"

            # "/System/Library/Frameworks/JavaVM.framework/Versions/Current"
            # framework_jdk

    # Oracle:                   self._locations[0] + "/<JDK_version>/Contents"
    # Apple: "/System/Library/Java/JavaVirtualMachines/<JDK_version>/Contents"
