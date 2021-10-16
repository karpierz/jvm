# Copyright (c) 2012-2021 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

__all__ = ('cmd', 'pipe', 'PIPE', 'STDOUT', 'DEVNULL', 'CompletedProcess',
           'SubprocessError', 'CalledProcessError', 'TimeoutExpired')

from subprocess import Popen, PIPE, STDOUT, DEVNULL, CompletedProcess
from subprocess import SubprocessError, CalledProcessError, TimeoutExpired
from functools  import partial

pipe = partial(Popen, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)

def cmd(*args, timeout=None, **kargs):
    from subprocess import run
    if "stdout" in kargs:
        raise ValueError("stdout argument not allowed, it will be overridden.")
    if "stderr" in kargs:
        raise ValueError("stderr argument not allowed, it will be overridden.")
    return run(args if len(args) > 1 else args[0], check=True,
               stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True,
               timeout=timeout, **kargs)

del Popen, partial
