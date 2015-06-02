#!/usr/bin/env python3

"""A simple functional test for PySpiro."""

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
import sys

# PySpiro imports.
from spiro import CPType, SVGPathContext, to_bezier

# This example is taken from the libspiro webpage.
points = [(-100, 0, CPType.g4),
          (0, 100, CPType.g4),
          (100, 0, CPType.g4),
          (0, -100, CPType.g4)]

# Convert these points to SVG path data.
with SVGPathContext(sys.stdout) as ctx:
    to_bezier(points, True, ctx)
