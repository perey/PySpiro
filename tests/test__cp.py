#!/usr/bin/env python3

"""Unit tests for the PySpiro _cp module."""

# Copyright © 2015 Timothy Pederick.
# Based on libspiro:
#     Copyright © 2007 Raph Levien
#
# This file is part of PySpiro.
#
# PySpiro is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PySpiro is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PySpiro. If not, see <http://www.gnu.org/licenses/>.

# Standard library imports.
try:
    # Python 3.3+
    from collections.abc import MutableSequence
except ImportError:
    # Python pre-3.3
    from collections import MutableSequence
import ctypes
import unittest

# Module to be tested.
from spiro import _cp

# Test cases.
class TestDataStructures(unittest.TestCase):
    """Test Python equivalents of libspiro data structures."""
    def test_CPType_enum(self):
        """Check the definition of the CPTypes enumeration."""
        self.assertEqual(len(_cp.CPType), 8)

        self.assertEqual(_cp.CPType.corner,           b'v')
        self.assertEqual(_cp.CPType.g4,               b'o')
        self.assertEqual(_cp.CPType.g2,               b'c')
        self.assertEqual(_cp.CPType.left,             b'[')
        self.assertEqual(_cp.CPType.right,            b']')
        self.assertEqual(_cp.CPType.end,              b'z')
        self.assertEqual(_cp.CPType.open_contour,     b'{')
        self.assertEqual(_cp.CPType.end_open_contour, b'}')

    def test_spiro_cp_structure(self):
        """Check the definition of the spiro_cp structure."""
        self.assertTrue(issubclass(_cp.spiro_cp, ctypes.Structure))
        self.assertEqual(len(_cp.spiro_cp._fields_), 3)

        expected_fields = {'x': ctypes.c_double,
                           'y': ctypes.c_double,
                           'ty': ctypes.c_char}
        for fieldname, fieldtype in _cp.spiro_cp._fields_:
            expected_type = expected_fields.get(fieldname)
            self.assertIsNotNone(expected_type)
            self.assertIs(fieldtype, expected_type)


class TestControlPointsInstantiation(unittest.TestCase):
    """Test instantiation of the ControlPoints sequence type."""
    def test_instantiable_alone(self):
        cps = _cp.ControlPoints()
        self.assertIsInstance(cps, MutableSequence)
        self.assertIsInstance(cps, _cp.ControlPoints)
        self.assertEqual(len(cps), 0)

    def test_instantiable_from_sequence(self):
        cps = _cp.ControlPoints([(1, 2, b'o'), (3, 4, b'c')])
        self.assertIsInstance(cps, MutableSequence)
        self.assertIsInstance(cps, _cp.ControlPoints)
        self.assertEqual(len(cps), 2)


class TestControlPointsSequence(unittest.TestCase):
    """Test whether ControlPoints implements the sequence interface.

    As ControlPoints derives from the MutableSequence ABC (tested in the
    TestControlPointsInstantiation test case), the mixin methods that
    the ABC provides are not tested. Only the five methods (__getitem__,
    __setitem__, __delitem__, __len__, and insert) that the ABC leaves
    abstract are tested.

    """
    def setUp(self):
        self.cps = _cp.ControlPoints()

    def test_getitem(self):
        # Sequence types raise IndexError, others raise TypeError.
        with self.assertRaises(IndexError):
            self.cps[0]

    def test_setitem(self):
        # Mutable sequence types raise IndexError, others raise TypeError.
        with self.assertRaises(IndexError):
            self.cps[0] = (1, 2, b'o')

    def test_delitem(self):
        # Mutable sequence types raise IndexError, others raise TypeError.
        with self.assertRaises(IndexError):
            del self.cps[0]

    def test_has_length(self):
        self.assertEqual(len(self.cps), 0)

    def test_insert(self):
        self.cps.insert(0, (1, 2, b'o'))
        self.assertEqual(len(self.cps), 1)

    def test_setitem_wrong(self):
        self.cps.insert(0, (1, 2, b'o'))
        with self.assertRaisesRegex(TypeError, 'object is not iterable'):
            self.cps[0] = 0
        with self.assertRaisesRegex(ValueError, 'not enough values to unpack'):
            self.cps[0] = (1, 2)
        with self.assertRaisesRegex(ValueError, 'unknown control point type'):
            self.cps[0] = (1, 2, 'o')
        with self.assertRaisesRegex(TypeError,
                                    'coordinates must be real numeric'):
            self.cps[0] = ('one', 2, b'o')
        with self.assertRaisesRegex(TypeError,
                                    'coordinates must be real numeric'):
            self.cps[0] = (1, 2j, b'o')

    def test_insert_wrong(self):
        self.assertRaisesRegex(TypeError, 'object is not iterable',
                               self.cps.insert, 0, 0)
        self.assertRaisesRegex(ValueError, 'not enough values to unpack',
                               self.cps.insert, 0, (1, 2))
        self.assertRaisesRegex(ValueError, 'unknown control point type',
                               self.cps.insert, 0, (1, 2, 'o'))
        self.assertRaisesRegex(TypeError, 'coordinates must be real numeric',
                               self.cps.insert, 0, ('one', 2, b'o'))
        self.assertRaisesRegex(TypeError, 'coordinates must be real numeric',
                               self.cps.insert, 0, (1, 2j, b'o'))
