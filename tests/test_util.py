import pytest

from functimer import Unit, get_unit


@pytest.mark.parametrize(
    "_input, expected",
    [
        ("0.2 ns", Unit.nanosecond),
        ("0.2 µs", Unit.microsecond),
        ("0.2 ms", Unit.millisecond),
        ("0.2 s", Unit.second),
        ("0.2 m", Unit.minute),
    ],
)
def test_get_unit(_input, expected):
    assert get_unit(_input) == expected


def test_get_unit_func(mock_timed):
    assert get_unit(mock_timed(lambda x: x, unit=Unit.nanosecond)()) == Unit.nanosecond
