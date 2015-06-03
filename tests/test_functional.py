#!/usr/bin/env python3

"""Functional tests for PySpiro."""

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
import io
import unittest

# PySpiro imports.
from spiro import CPType, SVGPathContext, to_bezier

# Test data.
# This example is taken from the libspiro webpage.
near_circle = [(-100, 0, CPType.g4),
               (0, 100, CPType.g4),
               (100, 0, CPType.g4),
               (0, -100, CPType.g4)]
near_circle_output = ('M-100,0 '
                      'C-100.0,26.1799 -89.2227,52.1987 -70.7107,70.7107 '
                      'C-52.1987,89.2227 -26.1799,100.0 0,100 '
                      'C26.1799,100.0 52.1987,89.2227 70.7107,70.7107 '
                      'C89.2227,52.1987 100.0,26.1799 100,0 '
                      'C100.0,-26.1799 89.2227,-52.1987 70.7107,-70.7107 '
                      'C52.1987,-89.2227 26.1799,-100.0 0,-100 '
                      'C-26.1799,-100.0 -52.1987,-89.2227 -70.7107,-70.7107 '
                      'C-89.2227,-52.1987 -100.0,-26.1799 -100,0 Z')

# Test cases.
class TestFunctional(unittest.TestCase):
    """Perform functional tests on PySpiro."""
    def setUp(self):
        """Create a StringIO buffer to hold output."""
        self.buffer = io.StringIO()

    def tearDown(self):
        """Close the StringIO buffer."""
        self.buffer.close()

    def test_near_circle(self):
        """Check output of drawing the nearly-circular example."""
        with SVGPathContext(self.buffer) as ctx:
            to_bezier(near_circle, True, ctx)
        self.assertEqual(self.buffer.getvalue(), near_circle_output)
