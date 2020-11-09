# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

__all__ = ('encrypt', 'decrypt')

from itertools import starmap, cycle


def encrypt(key, data):
    if isinstance(key,  str): key  = key.encode("utf-8")
    if isinstance(data, str): data = data.encode("utf-8")
    enc = lambda db, kb: chr((db + kb) % 256).encode("latin1")
    return b"".join(starmap(enc, zip(data, cycle(key))))


def decrypt(key, data):
    if isinstance(key, str): key = key.encode("utf-8")
    dec = lambda db, kb: chr((db - kb) % 256).encode("latin1")
    return b"".join(starmap(dec, zip(data, cycle(key))))
