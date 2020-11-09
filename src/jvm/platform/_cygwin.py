# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from os import path

from ..lib import public
from ..lib import platform

from . import _windows


@public
class JVMFinder(_windows.JVMFinder):
    """
    Cygwin JVM library finder class
    """

    def __init__(self, java_version=None):
        super().__init__(java_version)

        # Library file name
        self._libfile = "jvm.dll"

        # Search methods
        self._methods = (
            # self._get_from_java_home,  # <AK> !!! temporary !!!
            self._get_from_registry,
        )

    def _get_from_registry(self):
        for node in ("SOFTWARE", "SOFTWARE/Wow6432Node"):
            jre_reg_keys = (node + "/JavaSoft/JRE",
                            node + "/JavaSoft/Java Runtime Environment")
            jdk_reg_keys = (node + "/JavaSoft/JDK",
                            node + "/JavaSoft/Java Development Kit")
            for hkey in ("HKEY_LOCAL_MACHINE",):
                for key_path, is_jre in ([(key_path, True)  for key_path in jre_reg_keys] +
                                         [(key_path, False) for key_path in jdk_reg_keys]):
                    try:
                        java_key = "/proc/registry/" + hkey + "/" + key_path
                        with open(java_key + "/CurrentVersion") as f:
                            version = f.read().split('\x00')[0]
                        version_key = java_key + "/" + (version if not self._java_version or
                                                        float(".".join(version.split(".")[:2])) ==
                                                        self._java_version else str(self._java_version))
                        with open(version_key + "/JavaHome") as f:
                            java_home = f.read().split('\x00')[0]
                        if is_jre:
                            jre_home = java_home
                            with open(version_key + "/RunTimeLib") as f:
                                jvm_path = f.read().split('\x00')[0]
                        else:
                            jre_home = path.join(java_home, "jre")
                        if is_jre and path.isfile(jvm_path):
                            return jvm_path
                        else:
                            jvm_path_cli = path.join(jre_home, "bin", "client", self._libfile)
                            jvm_path_srv = path.join(jre_home, "bin", "server", self._libfile)
                            return (jvm_path_cli
                                    if path.isfile(jvm_path_cli) or not path.exists(jvm_path_srv)
                                    else jvm_path_srv)
                    except OSError:
                        pass
        return None
