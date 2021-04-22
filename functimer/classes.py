from enum import Enum
from typing import Any, Union


class Unit(Enum):
    nanosecond = "ns", 1e9
    microsecond = "µs", 1e6
    millisecond = "ms", 1e3
    second = "s", 1
    minute = "m", 1 / 60


_unit_map = {
    "ns": Unit.nanosecond,
    "µs": Unit.microsecond,
    "ms": Unit.millisecond,
    " s": Unit.second,
    " m": Unit.minute,
}


class TimerResult:
    def __init__(self, value: float, unit: Unit, precision: int = 2):
        # Time in seconds
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
            f"({', '.join(f'{k}: {v}' for k, v in self.__dict__.items())})"
        )


Result = Union[TimerResult, tuple[TimerResult, Any]]
