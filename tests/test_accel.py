import unittest
from klongpy import KlongInterpreter
from utils import *
from klongpy.backend import np
import numpy


class Executed:
    def __init__(self, fn):
        self.fn = fn
        self.executed = False

    def __call__(self, *args, **kwargs):
        self.executed = True
        return self.fn(*args, **kwargs)


class TestAccelerate(unittest.TestCase):
    """
    Verify that we are actually running the adverb_over accelerated paths for cases that we can.
    """

    def test_over_add(self):
        klong = KlongInterpreter()
        e = Executed(np.sum)
        try:
            np.sum = e
            r = klong('+/[1 2 3 4]')
        finally:
            np.sum = e.fn
        self.assertEqual(r, 10)
        self.assertTrue(e.executed)

    def test_over_subtract(self):
        if not hasattr(np.subtract,'reduce'):
            return
        klong = KlongInterpreter()
        e = Executed(np.subtract)
        try:
            np.subtract = e
            r = klong('-/[1 2 3 4]')
        finally:
            np.subtract = e.fn
        self.assertEqual(r, numpy.subtract.reduce([1,2,3,4]))
        self.assertTrue(e.executed)

    def test_over_multipy(self):
        if not hasattr(np.multiply,'reduce'):
            return
        klong = KlongInterpreter()
        e = Executed(np.multiply)
        try:
            np.multiply = e
            r = klong('*/[1 2 3 4]')
        finally:
            np.multiply = e.fn
        self.assertEqual(r, numpy.multiply.reduce([1,2,3,4]))
        self.assertTrue(e.executed)

    def test_over_divide(self):
        if not hasattr(np.divide,'reduce'):
            return
        klong = KlongInterpreter()
        e = Executed(np.divide)
        try:
            np.divide = e
            r = klong('%/[1 2 3 4]')
        finally:
            np.divide = e.fn
        self.assertEqual(r, numpy.divide.reduce([1,2,3,4]))
        self.assertTrue(e.executed)

    def test_over_min(self):
        klong = KlongInterpreter()
        e = Executed(np.min)
        try:
            np.min = e
            r = klong('&/[1 2 3 4]')
        finally:
            np.min = e.fn
        self.assertEqual(r, 1)
        self.assertTrue(e.executed)

    def test_over_max(self):
        klong = KlongInterpreter()
        e = Executed(np.max)
        try:
            np.max = e
            r = klong('|/[1 2 3 4]')
        finally:
            np.max = e.fn
        self.assertEqual(r, 4)
        self.assertTrue(e.executed)
