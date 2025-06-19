# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

import abc

from .lib import public
from .lib import obj


@public
class JHostABC(obj, abc.ABC):
    """???"""

    __slots__ = ()

    class ThreadState(obj, abc.ABC):
        """???"""

        __slots__ = ()

        @abc.abstractmethod
        def __init__(self):
            """Initializer"""
            raise NotImplementedError()

        @abc.abstractmethod
        def __enter__(self):
            """Enter context"""
            raise NotImplementedError()

        @abc.abstractmethod
        def __exit__(self, *exc_info):
            """Exit context"""
            raise NotImplementedError()

    class CallbackState(obj, abc.ABC):
        """???"""

        __slots__ = ()

        @abc.abstractmethod
        def __init__(self, ctx=None):
            """Initializer"""
            raise NotImplementedError()

        @abc.abstractmethod
        def __enter__(self):
            """Enter context"""
            raise NotImplementedError()

        @abc.abstractmethod
        def __exit__(self, *exc_info):
            """Exit context"""
            raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def incRef(cls, obj):
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def decRef(cls, obj):
        raise NotImplementedError()
