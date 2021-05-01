from functimer.classes import TimedResult, Unit


def test_timed_result_eq():
    t1 = TimedResult(1e-7, Unit.second)
    t2 = TimedResult(1e-7, Unit.millisecond)
    assert t1 == t2


def test_timed_result_lt():
    t1 = TimedResult(1e-8, Unit.second)
    t2 = TimedResult(1e-7, Unit.millisecond)
    assert t1 < t2
