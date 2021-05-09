import pytest

import functimer
from functimer import Unit, timed


def func():
    return 10


@pytest.fixture
def mock_timed(monkeypatch):
    monkeypatch.setattr(
        functimer.timer.timeit, "timeit", lambda *args, **kwargs: (1e-3, func())
    )
    return timed


@pytest.fixture
def timed_base(mock_timed):
    return mock_timed(func)


@pytest.fixture
def timed_disabled(mock_timed):
    return mock_timed(func, enabled=False)


@pytest.fixture
def timed_unit(mock_timed):
    return mock_timed(func, unit=Unit.nanosecond)


@pytest.fixture
def timed_number(mock_timed):
    return mock_timed(func, number=1)


@pytest.fixture
def timed_estimate(mock_timed):
    return mock_timed(func, estimate=True)


@pytest.fixture
def timed_return(mock_timed):
    return mock_timed(func, enable_return=True)


@pytest.fixture
def timed_stdout(mock_timed):
    return mock_timed(func, enable_stdout=True)


@pytest.fixture
def timed_exception(mock_timed):
    # Delay Execution of fixture
    return lambda: mock_timed(func, number=0)
