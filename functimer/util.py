import sys
from contextlib import contextmanager
from typing import Union

from functimer.classes import TimedResult, Unit
from functimer.exceptions import TimingException


class TrapIO:
    def write(self, *args):
        pass

    def flush(self):
        pass

    def read(self, *args):
        raise TimingException("Can't read from stdin while timing!")

    readline = read
    readlines = read
    __next__ = read


@contextmanager
def suppress_stdout(enable_stdout: bool):
    if not enable_stdout:
        save_stdout = sys.stdout
        save_stdin = sys.stdin
        sys.stdout = TrapIO()
        sys.stdin = TrapIO()
        yield
        sys.stdout = save_stdout
        sys.stdin = save_stdin
    else:
        yield


def get_unit(fmt_str: Union[str, TimedResult]) -> Unit:
    """Parse unit from given string or returns the unit attribute from TimerResult object.

    Args:
        fmt_str: Given string or TimerResult Object

    Returns:
        Parsed unit enum.
    """
    # Convenience feature, can just access the unit member personally
    if isinstance(fmt_str, TimedResult):
        return fmt_str.unit
    return Unit.from_str(fmt_str[-2:].strip())
