import pytest

import functimer


def func():
    print("func", flush=True)
    return 10


def func_input():
    x = input("This isn't allowed!")
    return x


@pytest.fixture
def mock_timed(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(
            functimer.functimer.timeit, "timeit", lambda *args, **kwargs: (1, func())
        )
        yield functimer.timed


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({}, "1000.00 µs"),
        ({"enabled": False}, 10),
        ({"unit": functimer.Unit.NANOSECOND}, "ns"),
        ({"estimate": True, "unit": functimer.Unit.SECOND}, 1e3),
        ({"enable_return": True}, 10),
    ],
)
def test_timed(mock_timed, kwargs, expected):
    print(mock_timed(func, **kwargs)())
    assert str(expected) in str(mock_timed(func, **kwargs)())


def test_timed_stdout(capsys, mock_timed):
    mock_timed(func, number=1, enable_stdout=True)()
    out = capsys.readouterr().out
    assert "func" in out


@pytest.mark.parametrize(
    "_input, kwargs, error",
    [
        (None, {}, TypeError),
        (func, {"number": 0}, ValueError),
        (func_input, {}, functimer.TimingException),
    ],
)
def test_timed_error(monkeypatch, _input, kwargs, error):
    with monkeypatch.context() as m:
        m.setattr(
            functimer.functimer.timeit,
            "timeit",
            lambda *args, **kwargs: (1, func_input()),
        )
        with pytest.raises(error):
            functimer.timed(_input, **kwargs)()
