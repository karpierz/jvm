# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import abc
import numbers

from public import public
from .lib import obj


@public
class TypeHandlerABC(obj, abc.ABC):

    __slots__ = ('_state', '_jtype', '_jclass')

    def __init__(self, state, jtype, jclass):
        self._state  = state
        self._jtype  = jtype
        self._jclass = jclass

    javaType = property(lambda self: self._jtype)

    # Handler interface

    @abc.abstractmethod
    def isSubtypeOf(self, other: 'TypeHandlerABC') -> bool:
        # in the sense of:
        # https://docs.oracle.com/javase/specs/jls/se7/html/jls-4.html#jls-4.10
        raise NotImplementedError()

    @abc.abstractmethod
    def match(self, val: object) -> 'EMatch':
        raise NotImplementedError()

    @abc.abstractmethod
    def valid(self, val: object) -> 'EMatch':
        raise NotImplementedError()

    @abc.abstractmethod
    def toJava(self, val: object) -> object:
        raise NotImplementedError()

    @abc.abstractmethod
    def toPython(self, val: object) -> object:
        raise NotImplementedError()

    @abc.abstractmethod
    def getStatic(self, fld: 'JField', cls: 'JClass') -> object:
        raise NotImplementedError()

    @abc.abstractmethod
    def setStatic(self, fld: 'JField', cls: 'JClass', val): # val: '???'):
        raise NotImplementedError()

    @abc.abstractmethod
    def getInstance(self, fld: 'JField', this: 'JObject') -> object:
        raise NotImplementedError()

    @abc.abstractmethod
    def setInstance(self, fld: 'JField', this: 'JObject', val): # val: '???'):
        raise NotImplementedError()

    @abc.abstractmethod
    def setArgument(self, pdescr, args, pos: int, val): # , val: '???'): # -> '???':
        raise NotImplementedError()

    @abc.abstractmethod
    def callStatic(self, meth: 'JMethod', cls: 'JClass', args) -> object: # args: '???')
        raise NotImplementedError()

    @abc.abstractmethod
    def callInstance(self, meth: 'JMethod', this: 'JObject', args) -> object: # args: '???')
        raise NotImplementedError()

    @abc.abstractmethod
    def newArray(self, size: int) -> 'JArray':
        raise NotImplementedError()

    @abc.abstractmethod
    def getElement(self, arr: 'JArray', idx: int) -> object:
        raise NotImplementedError()

    @abc.abstractmethod
    def setElement(self, arr: 'JArray', idx: int, val): # val: '???'):
        raise NotImplementedError()

    @abc.abstractmethod
    def getSlice(self, arr: 'JArray', start: int, stop: int, step: int): # -> '???':
        raise NotImplementedError()

    @abc.abstractmethod
    def setSlice(self, arr: 'JArray', start: int, stop: int, step: int, val): # val: '???'):
        raise NotImplementedError()

    @abc.abstractmethod
    def getArrayBuffer(self, arr: 'JArray') -> object:
        raise NotImplementedError()

    @abc.abstractmethod
    def releaseArrayBuffer(self, arr: 'JArray', buf: object) -> object:
        raise NotImplementedError()

    # TODO also optimize array.array ...
