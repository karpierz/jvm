# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import sys
from os import path
import struct

from ..lib import public
from ..lib import platform

from . import _jvmfinder
from ._jvmfinder import JVMNotSupportedException


@public
class JVMFinder(_jvmfinder.JVMFinder):
    """
    Windows JVM library finder class
    """

    def __init__(self, java_version=None):
        super().__init__(java_version)

        # Library file name
        self._libfile = "jvm.dll"

        # Search methods
        winreg = self._get_winreg()
        if winreg is not None:
            self._methods = (
                # self._get_from_java_home,  # <AK> !!! temporary !!!
                self._get_from_registry,
            )
        else:
            self._methods = (
                self._get_from_java_home,
            )

    def check(self, jvm):

        IMAGE_FILE_MACHINE_I386  = 332
        IMAGE_FILE_MACHINE_IA64  = 512
        IMAGE_FILE_MACHINE_AMD64 = 34404

        with open(jvm, "rb") as f:
            if f.read(2) != b"MZ":
                raise JVMNotSupportedException("JVM not valid")
            f.seek(60)
            header_offset = struct.unpack("<L", f.read(4))[0]
            f.seek(header_offset + 4)
            machine = struct.unpack("<H", f.read(2))[0]

        if machine in (IMAGE_FILE_MACHINE_I386,):
            if not platform.is_32bit:
                raise JVMNotSupportedException("JVM mismatch, "
                                               "Python is 64 bit and JVM is 32 bit.")
        elif machine in (IMAGE_FILE_MACHINE_IA64, IMAGE_FILE_MACHINE_AMD64):
            if platform.is_32bit:
                raise JVMNotSupportedException("JVM mismatch, "
                                               "Python is 32 bit and JVM is 64 bit.")
        else:
            raise JVMNotSupportedException("Unable to deterime JVM Type")

    def _get_from_registry(self):
        try:
            winreg = self._get_winreg()
        except WindowsError:
            return None
        if winreg is None:
            return None

        return (self._get_from_registry_Oracle() or
                self._get_from_registry_Zulu())

    def _get_from_registry_Oracle(self):
        winreg = self._get_winreg()
        for node in (r"SOFTWARE", r"SOFTWARE\Wow6432Node"):
            jre_reg_keys = (node + r"\JavaSoft\JRE",
                            node + r"\JavaSoft\Java Runtime Environment")
            jdk_reg_keys = (node + r"\JavaSoft\JDK",
                            node + r"\JavaSoft\Java Development Kit")
            for hkey in (winreg.HKEY_LOCAL_MACHINE,):
                for key_path, is_jre in ([(key_path, True)  for key_path in jre_reg_keys] +
                                         [(key_path, False) for key_path in jdk_reg_keys]):
                    try:
                        with winreg.OpenKey(hkey, key_path) as java_key:
                            version, _ = winreg.QueryValueEx(java_key, "CurrentVersion")
                            version_matches = (not self._java_version or
                                               float(".".join(version.split(".")[:2])) ==
                                               self._java_version)
                            version_key = version if version_matches else str(self._java_version)
                            with winreg.OpenKey(java_key, version_key) as jvm_key:
                                java_home, _ = winreg.QueryValueEx(jvm_key, "JavaHome")
                                if is_jre:
                                    jvm_path, _ = winreg.QueryValueEx(jvm_key, "RuntimeLib")
                                    if path.isfile(jvm_path):
                                        return jvm_path
                                    jre_home = java_home
                                else:
                                    jre_home = path.join(java_home, "jre")
                        jvm_path_cli = path.join(jre_home, "bin", "client", self._libfile)
                        jvm_path_srv = path.join(jre_home, "bin", "server", self._libfile)
                        return (jvm_path_cli
                                if path.isfile(jvm_path_cli) or not path.exists(jvm_path_srv)
                                else jvm_path_srv)
                    except WindowsError:
                        pass
        return None

    def _get_from_registry_Zulu(self):
        winreg = self._get_winreg()
        for node in (r"SOFTWARE", r"SOFTWARE\Wow6432Node"):
            reg_keys = (node + r"\Azul Systems\Zulu",
                        node + r"\Azul Systems\Zulu 32-bit")
            for hkey in (winreg.HKEY_LOCAL_MACHINE,):
                for key_path in reg_keys:
                    try:
                        with winreg.OpenKey(hkey, key_path) as java_key:
                            for subkey_name in self._sub_keys(java_key):
                                with winreg.OpenKey(hkey, rf"{key_path}\{subkey_name}") as jvm_key:
                                    is_jre = subkey_name.endswith("-jre")
                                    version = (f"{winreg.QueryValueEx(jvm_key, 'MajorVersion')[0]}."
                                               f"{winreg.QueryValueEx(jvm_key, 'MinorVersion')[0]}")
                                    java_home, _ = winreg.QueryValueEx(jvm_key, "InstallationPath")
                                    java_home = java_home.rstrip("\\")
                                    version_matches = (not self._java_version or
                                                       float(".".join(version.split(".")[:2])) ==
                                                       self._java_version)
                                    if version_matches:
                                        jvm_path_cli = path.join(java_home, "bin", "client", self._libfile)
                                        jvm_path_srv = path.join(java_home, "bin", "server", self._libfile)
                                        return (jvm_path_cli
                                                if path.isfile(jvm_path_cli) or not path.exists(jvm_path_srv)
                                                else jvm_path_srv)
                    except WindowsError:
                        pass
        return None

    def _sub_keys(self, key):
        winreg = self._get_winreg()
        idx = 0
        while True:
            try:
                subkey = winreg.EnumKey(key, idx)
                yield subkey
                idx += 1
            except WindowsError:
                break

    def _get_winreg(self):
        try:
            import winreg
            return winreg
        except ImportError:
            pass
        return None
