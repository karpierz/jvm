# Copyright (c) 2016 Adam Karpierz
# SPDX-License-Identifier: Zlib

__all__ = ('Path',)

from typing import Optional, Union
import sys
import os
import re
import stat
import shutil
import tempfile
import itertools
import pathlib
import hashlib
import contextlib


class Path(pathlib.Path):

    def __new__(cls, *args, **kwargs):
        cls._flavour = (pathlib.WindowsPath
                        if os.name == "nt" else
                        pathlib.PosixPath)._flavour
        return super().__new__(cls, *args, **kwargs)

    if sys.version_info[:2] < (3,8):
        def rename(self, target):
            super().rename(target)
            return self.__class__(target)

    if sys.version_info[:2] < (3,8):
        def replace(self, target):
            super().replace(target)
            return self.__class__(target)

    if sys.version_info[:2] < (3,9):
        def is_relative_to(self, other):
            try:
                self.relative_to(other)
                return True
            except ValueError:
                return False
    elif sys.version_info[:2] < (3,12):
        def is_relative_to(self, other):
            return super().is_relative_to(other)

    if sys.version_info[:2] < (3,12):
        def relative_to(self, other):
            return super().relative_to(other)

    if sys.version_info[:2] < (3,9):
        def with_stem(self, stem):
            return self.with_name(stem + self.suffix)

    if sys.version_info[:2] < (3,10):
        def hardlink_to(self, target):
            if not hasattr(os, "link"):
                raise NotImplementedError("os.link() not available on this system")
            os.link(target, self)

    def exists(self):
        return super().exists() or self._is_real_link()

    def mkdir(self, mode=0o777, parents=False, exist_ok=True):
        return super().mkdir(mode=mode, parents=parents, exist_ok=exist_ok)

    def rmdir(self, *, ignore_errors=False, onerror=None):
        if not self.exists():
            return
        shutil.rmtree(str(self), ignore_errors=ignore_errors,
                      onerror=onerror or self.__remove_readonly)

    @staticmethod
    def __remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def cleardir(self, *, ignore_errors=False, onerror=None):
        if not self.exists():
            return
        if not self.is_dir():
            raise NotADirectoryError(f"The directory name is invalid: '{self}'")
        if self._is_real_link():
            raise NotADirectoryError("Cannot call cleardir on a symbolic link")
        for entry in self.iterdir():
            entry = self.__class__(entry)
            if entry.is_dir() and not entry.is_symlink():
                entry.rmdir(ignore_errors=ignore_errors, onerror=onerror)
            else:
                entry.unlink(missing_ok=True)

    if hasattr(os.stat_result, "st_file_attributes"):
        # Special handling for directory junctions to make them behave like
        # symlinks for shutil.rmtree, since in general they do not appear as
        # regular links.
        def _is_real_link(self):
            try:
                st = os.lstat(str(self))
                return bool(stat.S_ISLNK(st.st_mode) or
                            (st.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT
                            and (not hasattr(os.stat_result, "st_reparse_tag")
                            or st.st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT)))
            except OSError:
                return False
    else:
        def _is_real_link(self):
            return os.path.islink(str(self))

    def copydir(self, dst: pathlib.Path, *, symlinks=False, ignore=None,
                copy_function=None, ignore_dangling_symlinks=False):
        return Path(shutil.copytree(str(self), str(dst), symlinks=symlinks, ignore=ignore,
                                    copy_function=copy_function or shutil.copy2,
                                    ignore_dangling_symlinks=ignore_dangling_symlinks))

    def unlink(self, missing_ok=True):
        if missing_ok and not self.exists():
            return
        try:
            return super().unlink()
        except PermissionError:
            self.chmod(stat.S_IWRITE)
            return super().unlink()

    def copy(self, dst: pathlib.Path, *, follow_symlinks=True):
        return Path(shutil.copy2(str(self), str(dst), follow_symlinks=follow_symlinks))

    def move(self, dst: pathlib.Path, *, copy_function=None):
        if not self.exists():
            return None
        return Path(shutil.move(str(self), str(dst),
                                copy_function=copy_function or shutil.copy2))

    def copystat(self, dst: pathlib.Path, *, follow_symlinks=True):
        return shutil.copystat(str(self), str(dst), follow_symlinks=follow_symlinks)

    @classmethod
    def which(cls, cmd: str, *, mode=os.F_OK | os.X_OK, path=None):
        result = shutil.which(cmd, mode=mode, path=path)
        return Path(result) if result is not None else None

    def file_hash(self, algorithm: str, *, chuck_size: int = 65536):
        constructor = self.__hash_algorithms.get(algorithm, lambda: hashlib.new(algorithm))
        hash_value = constructor()
        with self.open("rb") as f:
            while True:
                chunk = f.read(chuck_size)
                if not chunk: break
                hash_value.update(chunk)
        return hash_value

    def dir_hash(self, algorithm: str, *, chuck_size: int = 65536):
        constructor = self.__hash_algorithms.get(algorithm, lambda: hashlib.new(algorithm))
        hash_value = constructor()
        for root, dirs, files in os.walk(self):
            for name in files:
                fpath = Path(root)/name
                with fpath.open("rb") as f:
                    while True:
                        chunk = f.read(chuck_size)
                        if not chunk: break
                        hash_value.update(chunk)
        return hash_value

    __hash_algorithms = {
        "md5":     hashlib.md5,
        "sha1":    hashlib.sha1,
        "sha224":  hashlib.sha224,
        "sha256":  hashlib.sha256,
        "sha384":  hashlib.sha384,
        "sha512":  hashlib.sha512,
        "blake2b": hashlib.blake2b,
        "blake2s": hashlib.blake2s,
    }

    def unpack_archive(self, extract_dir: pathlib.Path = None, *, format: str = None):
        return shutil.unpack_archive(self, extract_dir, format)

    def sed_inplace(self, pattern: Union[str, re.Pattern], repl: str, *, flags=0):
        """
        Perform the pure-Python equivalent of in-place `sed` substitution: e.g.,
        `sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.
        """
        # For efficiency, precompile the passed regular expression.
        if not isinstance(pattern, re.Pattern): pattern = re.compile(pattern, flags)

        # For portability, NamedTemporaryFile() defaults to mode "w+b" (i.e., binary
        # writing with updating). This is usually a good thing. In this case,
        # however, binary writing imposes non-trivial encoding constraints trivially
        # resolved by switching to text writing. Let's do that.
        for encoding in (None, "utf-8", "latin-1", "cp1252", "cp1250", "cp1257", "mbcs"):
            try:
                with tempfile.NamedTemporaryFile(mode="wt", newline="", delete=False) as tmp_file:
                    with self.open(encoding=encoding) as src_file:
                        if flags & re.MULTILINE:
                            content = src_file.read()
                            tmp_file.write(pattern.sub(repl, content))
                        else:
                            for line in src_file:
                                tmp_file.write(pattern.sub(repl, line))
            except UnicodeError:
                pass
            else:
                # Overwrite the original file with the munged temporary file
                # in a manner preserving file attributes (e.g., permissions).
                shutil.copystat(str(self), tmp_file.name)
                shutil.move(tmp_file.name, str(self))
                break
        else:
            print(str(UnicodeError("can't decode a file '{}'".format(self))))

    def chdir(self):
        os.chdir(str(self))

    @contextlib.contextmanager
    def pushd(self):
        curr_dir = os.getcwd()
        os.chdir(str(self))
        try:
            yield
        finally:
            os.chdir(curr_dir)
