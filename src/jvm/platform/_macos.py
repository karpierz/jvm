# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import os
from os import path

from ..lib import public
from ..lib import cli

from . import _linux


@public
class JVMFinder(_linux.JVMFinder):
    """
    Mac OS X JVM library finder class
    """

    def __init__(self, java_version=None):
        super().__init__(java_version)

        # Library file name
        self._libfile = "libjli.dylib"

        # Predefined locations
        self._locations = (
            "/Library/Java/JavaVirtualMachines",
        )

        # Search methods
        self._methods += (
            self._pre_vm7_path,
            self._javahome_binary,
        )
        # self._methods += (
        #     self.defaultPath,
        # )

    def _pre_vm7_path(self):
        # Returns the previous (older then Java7) constant JVM library path
        return "/System/Library/Frameworks/JavaVM.framework/JavaVM"

    def _javahome_binary(self):
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

    def defaultPath(self):
        # This script attempts to find an existing installation of Java that
        # meets a minimum version requirement on a Mac OS X machine.

        # on darwin, the JVM is always in the same location it seems ...
        return "/System/Library/Frameworks/JavaVM.framework/JavaVM"

        java_home = os.environ.get("JAVA_HOME")

        if java_home is not None:
            # Check JAVA_HOME directory to see if Java version is adequate
            java_exe = path.join(java_home, "bin", "java")
            # [...]

        if java_home is None:
            # If the existing JAVA_HOME directory is inadequate, use '/usr/libexec/java_home'
            # to search for other possible java candidates and check their versions.
            if path.isfile("/usr/libexec/java_home"): # -x
                # Apple JDKs
                java_home = cli.cmd("/usr/libexec/java_home",
                                    "" if not self._java_version else "-v {}".format(self._java_version)).stdout
                if not java_home.strip():
                    java_home = None
            else:
                # Look for the Apple JDKs first to preserve the existing behaviour,
                # and then look for the new JDKs provided by Oracle.
                if path.islink("/System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK"):
                    # Apple JDKs
                    java_home = "/System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK" + "/Home"
                elif path.islink("/System/Library/Java/JavaVirtualMachines/CurrentJDK"):
                    # Apple JDKs
                    java_home = "/System/Library/Java/JavaVirtualMachines/CurrentJDK" + "/Contents/Home"
                elif path.islink(self._locations[0] + "/CurrentJDK"):
                    # Oracle JDKs
                    java_home = self._locations[0] + "/CurrentJDK" + "/Contents/Home"


### return top Java version
# cout = cli.cmd("/usr/libexec/java_home").stdout
# self._locations[0] + "/1.7.0.jdk/Contents/Home"

### I want Java version 1.7
# cout = cli.cmd("/usr/libexec/java_home", "-v 1.7").stdout
# "/System/Library/Java/JavaVirtualMachines/1.7.0.jdk/Contents/Home"

    # Oracle:       "/Library/Java/Home"
    # Apple: "/System/Library/Frameworks/JavaVM.framework/Home"

            # "/System/Library/Frameworks/JavaVM.framework/Versions/Current"
            # "/System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK"

    # Oracle:                   self._locations[0] + "/<JDK_version>/Contents"
    # Apple: "/System/Library/Java/JavaVirtualMachines/<JDK_version>/Contents"
