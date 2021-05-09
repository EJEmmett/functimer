import pytest

from functimer import Unit
from functimer.classes import TimedResult


@pytest.fixture
def timed_result_micro():
    return TimedResult(1e-6, Unit.microsecond)


@pytest.fixture
def timed_result_milli():
    return TimedResult(1e-3, Unit.millisecond)
