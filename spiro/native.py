#!/usr/bin/env python3

"""libspiro C interface."""

# Copyright © 2015 Timothy Pederick.
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

__all__ = []

# Standard library imports
import ctypes
from ctypes import CFUNCTYPE, POINTER, Structure, c_char, c_double, c_int
try:
    # Python 3.4+
    from enum import Enum
except ImportError:
    # Python pre-3.4
    from collections import namedtuple
    def Enum(typename, names_and_vals):
        names, vals = zip(*names_and_vals)
        return namedtuple(typename, names)(*vals)
import sys

# Native library import.
libname = 'libspiro'
if sys.platform.startswith('linux'):
    libclass, libext = ctypes.CDLL, '.so'
elif sys.platform == 'darwin':
    libclass, libext = ctypes.CDLL, '.dylib'
elif sys.platform == 'win32':
    libclass, libext = ctypes.WinDLL, '.dll'
else:
    raise ImportError('Spiro does not support {!r}'.format(sys.platform))

spiro = libclass(libname + libext)

# Type definitions.
class spiro_cp(Structure):
    _fields_ = [('x', c_double),
                ('y', c_double),
                ('ty', c_char)]


class spiro_seg(Structure):
    _fields_ = [('x', c_double),
                ('y', c_double),
                ('ty', c_char),
                ('bend_th', c_double),
                ('ks', c_double * 4),
                ('seg_ch', c_double),
                ('seg_th', c_double),
                ('l', c_double)]


SpiroCPType = Enum('SpiroCPType', (('corner', b'v'),
                                   ('g4', b'o'),
                                   ('g2', b'c'),
                                   ('left', b'['),
                                   ('right', b']'),
                                   ('end', b'z'),
                                   ('open_contour', b'{'),
                                   ('end_open_contour', b'}')))


class bezctx(Structure):
    pass
bezctx._fields_ = [('moveto', CFUNCTYPE(None, POINTER(bezctx), c_double,
                                        c_double, c_int)),
                   ('lineto', CFUNCTYPE(None, POINTER(bezctx), c_double,
                                        c_double)),
                   ('quadto', CFUNCTYPE(None, POINTER(bezctx), c_double,
                                        c_double, c_double, c_double)),
                   ('curveto', CFUNCTYPE(None, POINTER(bezctx), c_double,
                                         c_double, c_double, c_double,
                                         c_double, c_double)),
                   ('mark_knot', CFUNCTYPE(None, POINTER(bezctx), c_int))]


# Argument and return types for functions.

# spiro_seg * run_spiro(const spiro_cp *src, int n);
spiro.run_spiro.argtypes = (POINTER(spiro_cp), c_int)
spiro.run_spiro.restype = POINTER(spiro_cp)

# void free_spiro(spiro_seg *s);
spiro.free_spiro.argtypes = (POINTER(spiro_seg),)
spiro.free_spiro.restype = None

# void spiro_to_bpath(const spiro_seg *s, int n, bezctx *bc);
spiro.spiro_to_bpath.argtypes = (POINTER(spiro_seg), c_int, POINTER(bezctx))
spiro.spiro_to_bpath.restype = None

# double get_knot_th(const spiro_seg *s, int i);
spiro.get_knot_th.argtypes = (POINTER(spiro_seg), c_int)
spiro.get_knot_th.restype = c_double

# void TaggedSpiroCPsToBezier(spiro_cp *spiros, bezctx *bc);
spiro.TaggedSpiroCPsToBezier.argtypes = (POINTER(spiro_cp), POINTER(bezctx))
spiro.TaggedSpiroCPsToBezier.restype = None

# void SpiroCPsToBezier(spiro_cp *spiros, int n, int isclosed, bezctx *bc);
spiro.SpiroCPsToBezier.argtypes = (POINTER(spiro_cp), c_int, c_int,
                                   POINTER(bezctx))
spiro.SpiroCPsToBezier.restype = None
