# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

from typing import Tuple
from pathlib import Path
import os
import struct
import itertools

from ..lib import public
from ..lib import platform

from . import _jvmfinder
from ._jvmfinder import JVMNotSupportedError

RegPath = Path


@public
class JVMFinder(_jvmfinder.JVMFinder):
    """Windows JVM library finder class"""

    def __init__(self, java_version=None):
        """Initializer"""
        super().__init__(java_version)

        # Library file name
        self._libfile: str = "jvm.dll"

        # Predefined locations
        self._locations: Tuple[Path] = (
            Path(os.environ["ProgramFiles"])/"Java",
            Path(os.environ["ProgramFiles"])/"Zulu",
        )

        # Search methods
        self._winreg = self._get_winreg()
        if self._winreg is not None:
            self._methods = (
                # self._get_from_java_home,  # <AK> !!! temporary !!!
                self._get_from_registry,
            )
        else:
            self._methods = (
                self._get_from_java_home,
            )

    def check(self, jvm: Path):

        IMAGE_FILE_MACHINE_I386  = 332
        IMAGE_FILE_MACHINE_IA64  = 512
        IMAGE_FILE_MACHINE_AMD64 = 34404

        with jvm.open("rb") as f:
            if f.read(2) != b"MZ":
                raise JVMNotSupportedError("JVM not valid")
            f.seek(60)
            header_offset = struct.unpack("<L", f.read(4))[0]
            f.seek(header_offset + 4)
            machine = struct.unpack("<H", f.read(2))[0]

        if machine in (IMAGE_FILE_MACHINE_I386,):
            if not platform.is_32bit:
                raise JVMNotSupportedError("JVM mismatch, "
                                           "Python is 64 bit and JVM is 32 bit.")
        elif machine in (IMAGE_FILE_MACHINE_IA64, IMAGE_FILE_MACHINE_AMD64):
            if platform.is_32bit:
                raise JVMNotSupportedError("JVM mismatch, "
                                           "Python is 32 bit and JVM is 64 bit.")
        else:
            raise JVMNotSupportedError("Unable to deterime JVM Type")

    def _get_from_registry(self) -> Path | None:
        if self._winreg is None: return None
        return next(itertools.chain(self._get_from_registry_Oracle(),
                                    self._get_from_registry_Zulu(),
                                    self._get_from_registry_Liberica()), None)

    def _get_from_registry_Oracle(self) -> Path | None:
        for node in (RegPath("SOFTWARE"), RegPath("SOFTWARE/Wow6432Node")):
            jre_reg_keys = (node/"JavaSoft/JRE",
                            node/"JavaSoft/Java Runtime Environment")
            jdk_reg_keys = (node/"JavaSoft/JDK",
                            node/"JavaSoft/Java Development Kit")
            for hkey in (self._winreg.HKEY_LOCAL_MACHINE,):
                for key_path, is_jre in ([(key_path, True)  for key_path in jre_reg_keys]
                                       + [(key_path, False) for key_path in jdk_reg_keys]):
                    try:
                        with self._open_key(hkey, key_path) as java_key:
                            version = self._query_value(java_key, "CurrentVersion")[0]
                            version_matches = (not self._java_version
                                               or float(".".join(version.split(".")[:2]))
                                               == self._java_version)
                            version_key = version if version_matches else str(self._java_version)
                            with self._open_key(java_key, version_key) as jvm_key:
                                java_home = Path(self._query_value(jvm_key, "JavaHome")[0])
                                if is_jre:
                                    jvm_path = Path(self._query_value(jvm_key, "RuntimeLib")[0])
                                    if jvm_path.is_file():
                                        yield jvm_path
                                    jre_home = java_home
                                else:
                                    jre_home = java_home/"jre"
                                    jre_home = jre_home if jre_home.exists() else java_home
                        jvm_path_cli = jre_home/"bin/client"/self._libfile
                        jvm_path_srv = jre_home/"bin/server"/self._libfile
                        yield (jvm_path_cli
                               if jvm_path_cli.is_file() or not jvm_path_srv.exists()
                               else jvm_path_srv)
                    except OSError:
                        pass

    def _get_from_registry_Zulu(self) -> Path | None:
        for node in (RegPath("SOFTWARE"), RegPath("SOFTWARE/Wow6432Node")):
            reg_keys = (node/"Azul Systems/Zulu",
                        node/"Azul Systems/Zulu 32-bit")
            for hkey in (self._winreg.HKEY_LOCAL_MACHINE,):
                for key_path in reg_keys:
                    try:
                        with self._open_key(hkey, key_path) as java_key:
                            for subkey_name in self._sub_keys(java_key):
                                with self._open_key(hkey, key_path/subkey_name) as jvm_key:
                                    is_jre = subkey_name.endswith("-jre")
                                    version_major = self._query_value(jvm_key, "MajorVersion")[0]
                                    version_minor = self._query_value(jvm_key, "MinorVersion")[0]
                                    version = f"{version_major}.{version_minor}"
                                    version_matches = (not self._java_version
                                                       or float(".".join(version.split(".")[:2]))
                                                       == self._java_version)
                                    java_home = Path(self._query_value(jvm_key,
                                                     "InstallationPath")[0].rstrip("\\"))
                                    if version_matches:
                                        if is_jre:
                                            jre_home = java_home
                                        else:
                                            jre_home = java_home/"jre"
                                            jre_home = jre_home if jre_home.exists() else java_home
                                        jvm_path_cli = jre_home/"bin/client"/self._libfile
                                        jvm_path_srv = jre_home/"bin/server"/self._libfile
                                        yield (jvm_path_cli
                                               if jvm_path_cli.is_file()
                                                  or not jvm_path_srv.exists()
                                               else jvm_path_srv)
                    except OSError:
                        pass

    def _get_from_registry_Liberica(self) -> Path | None:
        for node in (RegPath("SOFTWARE"), RegPath("SOFTWARE/Wow6432Node")):
            reg_keys = (node/"BellSoft/Liberica",
                        node/"BellSoft/Liberica 32-bit")
            for hkey in (self._winreg.HKEY_LOCAL_MACHINE,):
                for key_path in reg_keys:
                    try:
                        with self._open_key(hkey, key_path) as java_key:
                            for subkey_name in self._sub_keys(java_key):
                                with self._open_key(hkey, key_path/subkey_name):  # as jvm_key:
                                    # is_jre = subkey_name.startswith("jre-")
                                    # version_major = self._query_value(jvm_key, "MajorVersion")[0]
                                    # version_minor = self._query_value(jvm_key, "MinorVersion")[0]
                                    # build_number  = self._query_value(jvm_key, "BuildNumber")[0]
                                    pass
                    except OSError:
                        pass

    def _get_winreg(self):
        try:
            import winreg
            return winreg
        except (ImportError, WindowsError):
            pass
        return None

    def _open_key(self, key, sub_key, **kwargs):
        return self._winreg.OpenKey(key, str(sub_key), **kwargs)

    def _query_value(self, key, value_name):
        return self._winreg.QueryValueEx(key, value_name)

    def _sub_keys(self, key):
        idx = 0
        while True:
            try:
                subkey = self._winreg.EnumKey(key, idx)
                yield subkey
                idx += 1
            except WindowsError:
                break
