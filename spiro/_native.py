#!/usr/bin/env python3

"""libspiro C interface."""

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

__all__ = ['spiro_cp', 'CPType', 'TaggedSpiroCPsToBezier', 'SpiroCPsToBezier']

# Standard library imports
from collections import namedtuple
import ctypes
from ctypes import POINTER, Structure, c_char, c_double, c_int
import sys

# Local imports.
from ._context import BezierContext

# Native library import.
libname = 'libspiro'
if sys.platform.startswith('linux'):
    libclass, libext = ctypes.CDLL, '.so'
elif sys.platform == 'darwin':
    libclass, libext = ctypes.CDLL, '.dylib'
elif sys.platform == 'win32':
    libclass, libext = ctypes.WinDLL, '.dll'
else:
    raise ImportError('spiro does not support {!r}'.format(sys.platform))

spiro = libclass(libname + libext)

# Type definitions.
class spiro_cp(Structure):
    _fields_ = [('x', c_double),
                ('y', c_double),
                ('ty', c_char)]


CPType = namedtuple('CPType_tuple',
                    ('corner', 'g4', 'g2', 'left', 'right', 'end',
                     'open_contour', 'end_open_contour')
                    )(b'v', b'o', b'c', b'[', b']', b'z', b'{', b'}')


# Argument and return types for functions.

# void TaggedSpiroCPsToBezier(spiro_cp *spiros, bezctx *bc);
spiro.TaggedSpiroCPsToBezier.argtypes = (POINTER(spiro_cp), BezierContext)
spiro.TaggedSpiroCPsToBezier.restype = None
TaggedSpiroCPsToBezier = spiro.TaggedSpiroCPsToBezier

# void SpiroCPsToBezier(spiro_cp *spiros, int n, int isclosed, bezctx *bc);
spiro.SpiroCPsToBezier.argtypes = (POINTER(spiro_cp), c_int, c_int,
                                   BezierContext)
spiro.SpiroCPsToBezier.restype = None
SpiroCPsToBezier = spiro.SpiroCPsToBezier
