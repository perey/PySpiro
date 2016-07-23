#!/usr/bin/env python3

"""libspiro C interface."""

# Copyright © 2015, 2016 Timothy Pederick.
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

__all__ = ['TaggedSpiroCPsToBezier', 'SpiroCPsToBezier']

# Standard library imports
import ctypes
import sys

# Local imports.
from ._context import BezierContext
from ._cp import ControlPoints

# Native library import.
libname = 'libspiro'
libver = '0'
if sys.platform.startswith('linux'):
    libclass, libext = ctypes.CDLL, '.so.{}'.format(libver)
elif sys.platform == 'darwin':
    libclass, libext = ctypes.CDLL, '.dylib'
elif sys.platform == 'win32':
    libclass, libext = ctypes.CDLL, '-{}.dll'.format(libver)
else:
    raise ImportError('spiro does not support {!r}'.format(sys.platform))

spiro = libclass(libname + libext)

# Argument and return types for functions.

# void TaggedSpiroCPsToBezier(spiro_cp *spiros, bezctx *bc);
spiro.TaggedSpiroCPsToBezier.argtypes = (ControlPoints, BezierContext)
spiro.TaggedSpiroCPsToBezier.restype = None
TaggedSpiroCPsToBezier = spiro.TaggedSpiroCPsToBezier

# void SpiroCPsToBezier(spiro_cp *spiros, int n, int isclosed, bezctx *bc);
spiro.SpiroCPsToBezier.argtypes = (ControlPoints, ctypes.c_int,
                                   ctypes.c_int, BezierContext)
spiro.SpiroCPsToBezier.restype = None
SpiroCPsToBezier = spiro.SpiroCPsToBezier
