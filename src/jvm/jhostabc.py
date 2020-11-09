# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import abc

from .lib import public
from .lib import obj


@public
class JHostABC(obj, abc.ABC):

    __slots__ = ()

    class ThreadState(obj, abc.ABC):

        __slots__ = ()

        @abc.abstractmethod
        def __init__(self):
            raise NotImplementedError()

        @abc.abstractmethod
        def __enter__(self):
            raise NotImplementedError()

        @abc.abstractmethod
        def __exit__(self, *exc_info):
            raise NotImplementedError()

    class CallbackState(obj, abc.ABC):

        __slots__ = ()

        @abc.abstractmethod
        def __init__(self, ctx=None):
            raise NotImplementedError()

        @abc.abstractmethod
        def __enter__(self):
            raise NotImplementedError()

        @abc.abstractmethod
        def __exit__(self, *exc_info):
            raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def incRef(cls, obj):
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def decRef(cls, obj):
        raise NotImplementedError()
