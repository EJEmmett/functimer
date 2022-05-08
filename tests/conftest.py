import pytest

import functimer


def func():
    print("func", flush=True)
    return 10


@pytest.fixture
def mock_timed(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(functimer.functimer, "runner", lambda *args, **kwargs: (1, func()))
        yield functimer.timed
