import sys
from contextlib import contextmanager
from typing import Union

from functimer.classes import TimedResult, Unit, _unit_map


class DummyFile:
    def write(self, x):
        pass

    def flush(self):
        pass


@contextmanager
def suppress_stdout(enable_stdout: bool):
    if not enable_stdout:
        save_stdout = sys.stdout
        sys.stdout = DummyFile()
        yield
        sys.stdout = save_stdout
    else:
        yield


def get_unit(fmt_str: Union[str, TimedResult]) -> Unit:
    """
    Parse unit from given string or returns the unit attribute from TimerResult object.

    Attributes:
        fmt_str: Given string or TimerResult Object

    Returns:
        Parsed unit enum.

    example:
        From a string\n
        >>> str(get_unit("0.2 ms"))
        Unit.microsecond

        >>> str(get_unit("2.2 µs"))
        Unit.millisecond

        From func\n
        >>> @timed
        ... def f():
        ...     return 1
        ...
        ... runtime = f()
        ... str(get_unit(runtime))
        Unit.microsecond
    """
    # Convenience feature, can just access the unit member personally
    if isinstance(fmt_str, TimedResult):
        return fmt_str.unit
    return _unit_map[fmt_str[-2:]]
