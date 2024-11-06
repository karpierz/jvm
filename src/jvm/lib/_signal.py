# Copyright (c) 2012 Adam Karpierz
# SPDX-License-Identifier: Zlib

__all__ = ('Signal',)


class Signal:

    def __init__(self, *types):
        self._listeners = []

    def connect(self, listener):
        self._listeners.append(listener)

    def disconnect(self, listener):
        self._listeners.remove(listener)

    def emit(self, *args, **kwargs):
        for listener in self._listeners:
            listener(*args, **kwargs)

    def __iadd__(self, listener):
        self.connect(listener)
        return self
