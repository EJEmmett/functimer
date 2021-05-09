from pytest import raises

from functimer import Unit


def test_timed_base(timed_base):
    assert timed_base() == 1e-6


def test_timed_disabled(timed_disabled):
    assert timed_disabled() == 10


def test_timed_unit(timed_unit):
    assert timed_unit().unit == Unit.nanosecond


def test_timed_estimate(timed_estimate):
    assert timed_estimate().value == 1


def test_timed_return(timed_return):
    assert timed_return()[1] == 10


def test_timed_stdout(timed_stdout):
    assert timed_stdout()


def test_timed_exception(timed_exception):
    with raises(ValueError):
        timed_exception()
