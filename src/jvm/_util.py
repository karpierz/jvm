# Copyright (c) 2004-2022 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import jni
from jni._util import get_config, make_config
from .lib import public

public(get_config  = get_config)
public(make_config = make_config)


def str2jchars(val):
    jbuf = val.encode("utf-16")[jni.sizeof(jni.jchar):]  # skip byte-order mark
    jchars = jni.cast(jni.as_cstr(jbuf), jni.POINTER(jni.jchar))
    size = len(jbuf) // jni.sizeof(jni.jchar)
    return jchars, size, jbuf
