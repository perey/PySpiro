#!/usr/bin/env python3

"""A simple functional test for PySpiro."""

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
