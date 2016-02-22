#!/usr/bin/env python3

"""Spiro control point information."""

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

__all__ = ['CPType', 'ControlPoints']

# Standard library imports.
from collections import namedtuple
try:
    # Python 3.3+
    from collections.abc import MutableSequence, Sequence
except ImportError:
    # Python pre-3.3
    from collections import MutableSequence, Sequence
from ctypes import pointer, Structure, c_double, c_char

# Native interface definitions.
class spiro_cp(Structure):
    _fields_ = [('x', c_double),
                ('y', c_double),
                ('ty', c_char)]


CPType = namedtuple('CPType_tuple',
                    ('corner', 'g4', 'g2', 'left', 'right', 'end',
                     'open_contour', 'end_open_contour')
                    )(b'v', b'o', b'c', b'[', b']', b'z', b'{', b'}')

# Completely optional sequence type for control points.
class ControlPoints(MutableSequence):
    """A sequence of spiro control points.

    Use of this sequence type is optional; any sequence type can be
    passed in, and this type's from_param() class method will adapt it
    for the native libspiro function calls.

    """
    @classmethod
    def from_param(cls, obj):
        """Adapt sequence types for native function calls."""
        if isinstance(obj, Sequence):
            points = list(spiro_cp(*point) for point in obj)
            return (spiro_cp * len(obj))(*points)
        else:
            raise TypeError('{} can only adapt sequence types, not '
                            '{!r}'.format(cls.__name__, type(obj).__name__))

    def __init__(self, seq=None):
        self._seq = [] if seq is None else list(seq)

    def __getitem__(self, index):
        return self._seq[index]

    def __setitem__(self, index, val):
        x, y, cptype = val
        if cptype not in CPType:
            raise ValueError('unknown control point type: {!r}'.format(cptype))
        self._seq[index] = [x, y, cptype]

    def __delitem__(self, index):
        del self._seq[index]

    def __len__(self):
        return len(self._seq)

    def insert(self, index, val):
        self._seq.insert(index, val)
