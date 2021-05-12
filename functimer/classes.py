from enum import Enum
from functools import total_ordering
from typing import Any, Tuple, Union

from functimer.exceptions import TimingException


class Unit(Enum):
    nanosecond = "ns", 1e9
    microsecond = "µs", 1e6
    millisecond = "ms", 1e3
    second = "s", 1
    minute = "m", 1 / 60

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__qualname__}.{self.name}"

    @staticmethod
    def from_str(s):
        s = s.lower()
        try:
            return _unit_map[s]
        except KeyError:
            try:
                return Unit[s]
            except KeyError:
                raise TimingException(f"'{s}' is not a valid Unit.") from None


_unit_map = {
    "ns": Unit.nanosecond,
    "µs": Unit.microsecond,
    "ms": Unit.millisecond,
    "s": Unit.second,
    "m": Unit.minute,
}


@total_ordering
class TimedResult:
    __slots__ = ["value", "unit", "precision"]

    def __init__(self, value: float, unit: Unit, precision: int = 2):
        self.value = value
        self.unit = unit
        self.precision = precision

    def __str__(self):
        return (
            f"{self.value * self.unit.value[1]:.{self.precision}f} {self.unit.value[0]}"
        )

    def __repr__(self):
        return (
            f"<{self.__class__.__module__}.{self.__class__.__qualname__}"
            f"({', '.join(f'{slot}: {repr(getattr(self, slot))}' for slot in self.__slots__)})>"
        )

    def __lt__(self, other):
        return self.value < other

    def __eq__(self, other):
        return self.value == other


Result = Union[TimedResult, Tuple[TimedResult, Any]]
