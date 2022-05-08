import pytest

from functimer import Unit
from functimer.classes import Result


@pytest.fixture
def timed_result_micro():
    return Result(1e-6, Unit.MICROSECOND)


@pytest.fixture
def timed_result_milli():
    return Result(1e-3, Unit.MILLISECOND)


def test_timed_result_eq(timed_result_micro):
    t1 = timed_result_micro
    t2 = timed_result_micro
    assert t1 == t2


def test_timed_result_lt(timed_result_micro, timed_result_milli):
    t1 = timed_result_micro
    t2 = timed_result_milli
    assert t1 < t2


def test_timed_result_str(timed_result_micro, timed_result_milli):
    t1 = timed_result_micro
    t2 = timed_result_milli

    assert str(t1) == "1.00 µs"
    assert str(t2) == "1.00 ms"


def test_timed_result_repr(timed_result_micro, timed_result_milli):
    t1 = timed_result_micro
    t2 = timed_result_milli

    assert (
        repr(t1)
        == "<functimer.classes.Result(value: 1e-06, unit: Unit.MICROSECOND, precision: 2)>"
    )

    assert (
        repr(t2)
        == "<functimer.classes.Result(value: 0.001, unit: Unit.MILLISECOND, precision: 2)>"
    )
