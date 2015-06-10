#!/usr/bin/env python3

"""Unit tests for the PySpiro _native module."""

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
import unittest

# Module to be tested.
from spiro import _native

# Test cases.
class TestNativeFunctions(unittest.TestCase):
    """Test ctypes wrappers of native functions."""
    def is__FuncPtr(self, fn):
        """Test whether a function is an instance of ctypes._FuncPtr."""
        # Callable foreign functions are instances of the private ctypes class
        # '_FuncPtr', so we settle for checking its repr() instead.
        return repr(fn).startswith('<_FuncPtr object at ')
        
    def test_SpiroCPsToBezier_wrapper(self):
        """Test the wrapper of the SpiroCPsToBezier() function."""
        self.assertTrue(self.is__FuncPtr(_native.SpiroCPsToBezier))
        self.assertTrue(callable(_native.SpiroCPsToBezier))
        self.assertEqual(len(_native.SpiroCPsToBezier.argtypes), 4)
        self.assertIsNone(_native.SpiroCPsToBezier.restype)

    def test_TaggedSpiroCPsToBezier_wrapper(self):
        """Test the wrapper of the SpiroCPsToBezier() function."""
        self.assertTrue(self.is__FuncPtr(_native.TaggedSpiroCPsToBezier))
        self.assertTrue(callable(_native.TaggedSpiroCPsToBezier))
        self.assertEqual(len(_native.TaggedSpiroCPsToBezier.argtypes), 2)
        self.assertIsNone(_native.TaggedSpiroCPsToBezier.restype)
