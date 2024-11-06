# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import jni
from jni._config import make_config, get_config, set_config
from .lib import public

public(make_config = make_config)
public(get_config  = get_config)
public(set_config  = set_config)


def str2jchars(val):
    jbuf = val.encode("utf-16")[jni.sizeof(jni.jchar):]  # skip byte-order mark
    jchars = jni.cast(jni.as_cstr(jbuf), jni.POINTER(jni.jchar))
    size = len(jbuf) // jni.sizeof(jni.jchar)
    return jchars, size, jbuf
