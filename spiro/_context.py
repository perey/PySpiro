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

# Standard library imports.
from ctypes import pointer, c_void_p

# Local imports.
from ._native import (bezctx, moveto_fn, lineto_fn, quadto_fn, curveto_fn,
                      mark_knot_fn)

class BezierContext:
    """A context in which Bézier curves are generated.

    In order to convert a series of Spiro points to Bézier curves, the
    native library needs to know how Bézier curves are supposed to be
    represented. This information is encapsulated in subclasses of this
    abstract class.

    Subclasses must implement these four functions:
        * moveto(self, ctx, x, y, is_open): Generate a "move to"
            instruction, beginning a new subpath at (x, y). The argument
            is_open determines whether this subpath is open or closed.
            (Note that the native library supplies an integer, not a
            Boolean.)
        * lineto(self, ctx, x, y): Generate a "line to" instruction,
            drawing a straight line to (x, y).
        * quadto(self, ctx, x1, y1, x2, y2): Generate a "quad to"
            (quadratic Bézier) instruction, drawing a quadratic Bézier
            curve to (x2, y2) with control point (x1, y1).
        * curveto(self, ctx, x1, y1, x2, y2, x3, y3): Generate a "curve
            to" (cubic Bézier) instruction, drawing a cubic Bézier curve
            to (x3, y3) with control points (x1, y1) and (x2, y2).

    Optionally, a fifth function may be provided:
        * mark_knot(self, ctx, knot_idx): Mark a knot on the spline with
            the given knot index.

    The ctx argument to all of these functions is a copy of the instance
    as seen by the native interface; it can be ignored. Nothing should
    be returned by these functions.

    Other operations and information needed by the context will be
    unseen by the native library, and only accessed through these five
    functions.

    """
    @property
    def _native_handle_(self):
        return pointer(bezctx(moveto_fn(self.moveto),
                              lineto_fn(self.lineto),
                              quadto_fn(self.quadto),
                              curveto_fn(self.curveto),
                              mark_knot_fn(self.mark_knot)))

    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    def moveto(self, ctx, x, y, is_open):
        raise NotImplementedError

    def lineto(self, ctx, x, y):
        raise NotImplementedError

    def quadto(self, ctx, x1, y1, x2, y2):
        raise NotImplementedError

    def curveto(self, ctx, x1, y1, x2, y2, x3, y3):
        raise NotImplementedError

    def mark_knot(self, ctx, knot_idx):
        return


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
        self.is_open = True

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

    @staticmethod
    def _numstr(n, precision=6):
        """Number-to-string conversion with sensible precision."""
        fmt = '{:.' + str(int(precision)) + '}'
        return str(int(n)) if int(n) == n else fmt.format(n)

    def moveto(self, ctx, x, y, is_open):
        if self._first_subpath:
            self._first_subpath = False
        elif not self.is_open:
            print('Z', end=' ', file=self.file)
        print('M{},{}'.format(*(self._numstr(n) for n in (x, y))),
              end=' ', file=self.file)
        self.is_open = is_open

    def lineto(self, ctx, x, y):
        print('L{},{}'.format(*(self._numstr(n) for n in (x, y))),
              end=' ', file=self.file)

    def quadto(self, ctx, x1, y1, x2, y2):
        print('Q{},{} {},{}'.format(*(self._numstr(n) for n in (x1, y1,
                                                                x2, y2))),
              end=' ', file=self.file)

    def curveto(self, ctx, x1, y1, x2, y2, x3, y3):
        print('C{},{} {},{} {},{}'.format(*(self._numstr(n) for n in (x1, y1,
                                                                      x2, y2,
                                                                      x3, y3)
                                            )),
              end=' ', file=self.file)
