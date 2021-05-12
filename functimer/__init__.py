"""A decorator/wrapper package to time a given function."""

__all__ = ["create_timed_function", "get_unit", "timed", "TimingException", "Unit"]

from functimer.classes import Unit
from functimer.exceptions import TimingException
from functimer.timer import create_timed_function, timed
from functimer.util import get_unit
