# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional, Tuple
from pathlib import Path

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
        self._libfile: str = "jvm.dll"

        # Search methods
        self._methods = (
            # self._get_from_java_home,  # <AK> !!! temporary !!!
            self._get_from_registry,
        )

    def _get_from_registry(self):
        return (self._get_from_registry_Oracle() or
                self._get_from_registry_Zulu())

    def _get_from_registry_Oracle(self):
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
                        version_matches = (not self._java_version or
                                           float(".".join(version.split(".")[:2])) ==
                                           self._java_version)
                        version_key = java_key + "/" + (version if version_matches
                                                        else str(self._java_version))
                        with open(version_key + "/JavaHome") as f:
                            java_home = Path(f.read().split('\x00')[0])
                        if is_jre:
                            with open(version_key + "/RunTimeLib") as f:
                                jvm_path = Path(f.read().split('\x00')[0])
                            if jvm_path.is_file():
                                return jvm_path
                            jre_home = java_home
                        else:
                            jre_home = java_home/"jre"
                        jvm_path_cli = jre_home/"bin/client"/self._libfile
                        jvm_path_srv = jre_home/"bin/server"/self._libfile
                        return (jvm_path_cli
                                if jvm_path_cli.is_file() or not jvm_path_srv.exists()
                                else jvm_path_srv)
                    except OSError:
                        pass
        return None

    def _get_from_registry_Zulu(self):
        for node in ("SOFTWARE", "SOFTWARE/Wow6432Node"):
            reg_keys = (node + "/Azul Systems/Zulu",
                        node + "/Azul Systems/Zulu 32-bit")
            for hkey in ("HKEY_LOCAL_MACHINE",):
                for key_path in reg_keys:
                    try:
                        java_key = "/proc/registry/" + hkey + "/" + key_path
                        #with winreg.OpenKey(hkey, key_path) as java_key:
                        #    for subkey_name in self._sub_keys(java_key):
                        #        with winreg.OpenKey(hkey, rf"{key_path}\{subkey_name}") as jvm_key:
                        #            is_jre = subkey_name.endswith("-jre")
                        #            version = (f"{winreg.QueryValueEx(jvm_key, 'MajorVersion')[0]}."
                        #                       f"{winreg.QueryValueEx(jvm_key, 'MinorVersion')[0]}")
                        #            java_home = Path(winreg.QueryValueEx(jvm_key,
                        #                                                 "InstallationPath")[0].rstrip("\\"))
                        #            version_matches = (not self._java_version or
                        #                               float(".".join(version.split(".")[:2])) ==
                        #                               self._java_version)
                        #            if version_matches:
                        #                jvm_path_cli = java_home/"bin/client"/self._libfile
                        #                jvm_path_srv = java_home/"bin/server"/self._libfile
                        #                return (jvm_path_cli
                        #                        if jvm_path_cli.is_file() or not jvm_path_srv.exists()
                        #                        else jvm_path_srv)
                    except WindowsError:
                        pass
        return None
