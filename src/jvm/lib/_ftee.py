# Copyright (c) 2018 Adam Karpierz
# SPDX-License-Identifier: Zlib

__all__ = ('ftee',)

import sys
import io
import contextlib


class _Tee(io.TextIOBase):

    def __init__(self, *files):
        self._files = files

    def close(self):
        super().close()
        self._files[0].flush()
        for f in self._files[1:]:
            f.close()

    def writable(self):
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        return True

    def write(self, s):
        count = 0
        for f in self._files:
            count = f.write(s)
        return count

    def flush(self):
        for f in self._files:
            f.flush()


@contextlib.contextmanager
def ftee(*filenames):
    stdout = sys.stdout
    files  = [open(fname, "w") for fname in filenames]
    try:
        sys.stdout = _Tee(sys.stdout, *files)
        yield sys.stdout
    finally:
        sys.stdout.close()
        sys.stdout = stdout


del io, contextlib
