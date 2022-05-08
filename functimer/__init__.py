"""A decorator/wrapper package to time a given function."""

__all__ = ["get_unit", "Result", "timed", "TimingException", "Unit"]

from functimer.classes import Result, Unit
from functimer.exceptions import TimingException
from functimer.functimer import timed
from functimer.util import get_unit
