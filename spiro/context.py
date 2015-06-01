#!/usr/bin/env python3

"""Bézier curve generation contexts."""

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

__all__ = ['BezierContext', 'SVGPathContext']

# Local imports.
from .native import bezctx

class BezierContext:
    """A context in which Bézier curves are generated.

    In order to convert a series of Spiro points to Bézier curves, the
    native library needs to know how Bézier curves are supposed to be
    represented. This information is encapsulated in subclasses of this
    abstract class.

    Subclasses must implement these four functions:
        * moveto(self, x, y, is_open): Generate a "move to" instruction,
            beginning a new subpath at (x, y). The argument is_open
            determines whether this subpath is open or closed. (Note
            that the native library supplies an integer, not a Boolean.)
        * lineto(self, x, y): Generate a "line to" instruction, drawing
            a straight line to (x, y).
        * quadto(self, x1, y1, x2, y2): Generate a "quad to" (quadratic
            Bézier) instruction, drawing a quadratic Bézier curve to
            (x2, y2) with control point (x1, y1).
        * curveto(self, x1, y1, x2, y2, x3, y3): Generate a "curve to"
            (cubic Bézier) instruction, drawing a cubic Bézier curve to
            (x3, y3) with control points (x1, y1) and (x2, y2).

    Optionally, a fifth function may be provided:
        * mark_knot(self, knot_idx): Mark a knot on the spline with the
            given knot index.

    Nothing should be returned by these functions.

    Other operations and information needed by the context will be
    unseen by the native library, and only accessed through these five
    functions.

    """
    @property
    def _as_parameter_(self):
        return bezctx(self.moveto, self.lineto, self.quadto, self.curveto,
                      None if not hasattr(self, 'mark_knot') else
                      self.mark_knot)

    def moveto(self, x, y, is_open):
        raise NotImplementedError

    def lineto(self, x, y):
        raise NotImplementedError

    def quadto(self, x1, y1, x2, y2):
        raise NotImplementedError

    def curveto(self, x1, y1, x2, y2, x3, y3):
        raise NotImplementedError


class SVGPathContext(BezierContext):
    """Generate Bézier curves as SVG path data.

    Use this class as a context manager, passing it a file-like object
    to which the path data will be written:
        >>> with SVGPathContext(sys.stdout) as ctx:
        ...     spiro.tagged_to_bezier(points, ctx)

    """
    def __init__(self, file):
        self.file = file
        self._first_subpath = True
        self.is_open = False

    def __enter__(self):
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context manager.

        If an exception has resulted, no further output will be emitted.
        Otherwise, one final "close path" command may be produced.

        """
        if exc_type is None and not self.is_open:
            print('Z', end='', file=self.file)

    def moveto(self, x, y, is_open):
        if self._first_subpath:
            self._first_subpath = False
        elif not self.is_open:
            print('Z', end=' ', file=self.file)
        print('M{},{}'.format(x, y), end=' ', file=self.file)
        self.is_open = is_open

    def lineto(self, x, y):
        print('L{},{}'.format(x, y), end=' ', file=self.file)

    def quadto(self, x1, y1, x2, y2):
        print('Q{},{} {},{}'.format(x1, y1, x2, y2), end=' ', file=self.file)

    def curveto(self, x1, y1, x2, y2, x3, y3):
        print('C{},{} {},{} {},{}'.format(x1, y1, x2, y2, x3, y3), end=' ',
              file=self.file)
