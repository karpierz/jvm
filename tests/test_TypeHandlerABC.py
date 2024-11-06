# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import unittest
import enum

from jvm.jconstants      import EJavaType
from jvm.jtypehandlerabc import TypeHandlerABC


class EMatch(enum.IntEnum):
    NONE     =   0
    EXPLICIT =   1
    IMPLICIT =  10
    PERFECT  = 100


class IncompleteHandler(TypeHandlerABC):

    __slots__ = ()

    def toJava(self, val):
        return None

    def toPython(self, val):
        return None

    def getStatic(self, fld, cls):
        return None

    def setStatic(self, fld, cls, val):
        pass

    def getInstance(self, fld, this):
        return None

    def setInstance(self, fld, this, val):
        pass

    def setArgument(self, pdescr, args, pos, val):
        pass

    def callStatic(self, meth, cls, args):
        return None

    def callInstance(self, meth, this, args):
        return None

    def newArray(self, size):
        return None

    def getElement(self, arr, idx):
        return None

    def setElement(self, arr, idx, val):
        pass

    def getSlice(self, arr, start, stop, step):
        return None

    def setSlice(self, arr, start, stop, step, val):
        pass

    def getArrayBuffer(self, arr):
        return None

    def releaseArrayBuffer(self, arr, buf):
        pass


class CompleteHandler(IncompleteHandler):

    __slots__ = ()

    def isSubtypeOf(self, other):
        return False

    def match(self, val):
        return EMatch.NONE

    def valid(self, val):
        return True


class TypeHandlerABCTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from . import jvm
        cls.jvm = jvm

    def test_IncompleteHandler(self):
        with self.assertRaisesRegex(TypeError,
                                    "Can't instantiate abstract class IncompleteHandler "):
            thandler = IncompleteHandler(None, EJavaType.VOID, None)

    def test_CompleteHandler(self):
        thandler = CompleteHandler(None, EJavaType.VOID, None)
        self.assertIs(thandler.isSubtypeOf(None), False)
        self.assertIs(thandler.match(None), EMatch.NONE)
        self.assertIs(thandler.valid(None), True)
        self.assertIs(thandler.toJava(None), None)
        self.assertIs(thandler.toPython(0x00), None)
        self.assertIs(thandler.getStatic(None, None), None)
        thandler.setStatic(None, None, None)
        self.assertIs(thandler.getInstance(None, None), None)
        thandler.setInstance(None, None, None)
        thandler.setArgument(None, None, 0, None)
        self.assertIs(thandler.callStatic(None, None, None), None)
        self.assertIs(thandler.callInstance(None, None, None), None)
        self.assertIs(thandler.newArray(100), None)
        self.assertIs(thandler.getElement(None, 0), None)
        thandler.setElement(None, 0, None)
        self.assertIs(thandler.getSlice(None, 0, 10, 1), None)
        thandler.setSlice(None, 0, 10, 1, None)
        self.assertIs(thandler.getArrayBuffer(None), None)
        thandler.releaseArrayBuffer(None, None)
