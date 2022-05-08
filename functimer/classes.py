from enum import Enum
from functools import total_ordering
from typing import Any, Tuple, Union

from functimer.exceptions import TimingException


class Unit(Enum):
    NANOSECOND = "ns", 1e9
    MICROSECOND = "µs", 1e6
    MILLISECOND = "ms", 1e3
    SECOND = "s", 1
    MINUTE = "m", 1 / 60

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}.{self.name}"

    @staticmethod
    def from_str(string: str) -> "Unit":
        try:
            return _unit_map[string.lower()]
        except KeyError:
            try:
                return Unit[string.upper()]
            except KeyError:
                raise TimingException(f"'{string}' is not a valid Unit.") from None


_unit_map = {
    "ns": Unit.NANOSECOND,
    "µs": Unit.MICROSECOND,
    "ms": Unit.MILLISECOND,
    "s": Unit.SECOND,
    "m": Unit.MINUTE,
}


@total_ordering
class Result:
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


TResult = Union[Result, Tuple[Result, Any]]
