#!/usr/bin/env python3

"""PySpiro: A Python 3 wrapper for libspiro."""

# Copyright © 2015 Timothy Pederick.
# Based on libspiro:
#     Copyright © 2007 Raph Levien
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

__all__ = ['CPType', 'BezierContext', 'SVGPathContext',
           'to_bezier', 'tagged_to_bezier']

# Standard library imports.
from ctypes import POINTER

# Local imports.
from ._native import (SpiroCPsToBezier, TaggedSpiroCPsToBezier,
                      SpiroCPType as CPType, spiro_cp)
from ._context import BezierContext, SVGPathContext

# Public functions.
def to_bezier(points, closed, context):
    """Convert a sequence of Spiro points to Bézier curves."""
    SpiroCPsToBezier(_to_cp_array(points), len(points),
                     1 if closed else 0, context._native_handle_)

def tagged_to_bezier(points, context):
    """Convert a "tagged" sequence of Spiro points to Bézier curves."""
    TaggedSpiroCPsToBezier(_to_cp_array(points), context._native_handle_)

# Private function.
def _to_cp_array(points):
    seq = list(spiro_cp(*point) for point in points)
    return (spiro_cp * len(points))(*seq)
