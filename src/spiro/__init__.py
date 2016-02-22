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

__all__ = ['BezierContext', 'ControlPoints', 'CPType', 'SVGPathContext',
           'to_bezier', 'tagged_to_bezier']

# Standard library imports.
from ctypes import POINTER

# Local imports.
from ._context import BezierContext, SVGPathContext
from ._cp import ControlPoints, CPType
from ._native import SpiroCPsToBezier, TaggedSpiroCPsToBezier

# Functions for using libspiro.
def to_bezier(points, is_closed, context):
    """Convert a sequence of Spiro points to Bézier curves."""
    SpiroCPsToBezier(points, len(points),
                     1 if is_closed else 0, context)

def tagged_to_bezier(points, context):
    """Convert a "tagged" sequence of Spiro points to Bézier curves."""
    TaggedSpiroCPsToBezier(points, context)
