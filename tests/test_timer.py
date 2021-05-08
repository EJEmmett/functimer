from functimer import Unit, timed


def test_timed_base():
    @timed
    def f():
        return 10

    assert 0 < f()


def test_timed_disabled():
    @timed(enabled=False)
    def f():
        return 10

    assert f() == 10


def test_timed_unit():
    @timed(unit=Unit.nanosecond)
    def f():
        return 10

    assert f().unit == Unit.nanosecond


def test_timed_return():
    @timed(enable_return=True)
    def f():
        return 10

    assert f()[1] == 10


def test_timed_estimate():
    t = timed(print, estimate=True)
    assert 0 < t("Test")


def test_timed_wrapper():
    def f():
        return 10

    f = timed(f)
    assert 0 < f()
