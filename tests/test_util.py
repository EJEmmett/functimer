import pytest

from functimer import Unit, get_unit


@pytest.mark.parametrize(
    "_input, expected",
    [
        ("0.2 ns", Unit.NANOSECOND),
        ("0.2 µs", Unit.MICROSECOND),
        ("0.2 ms", Unit.MILLISECOND),
        ("0.2 s", Unit.SECOND),
        ("0.2 m", Unit.MINUTE),
    ],
)
def test_get_unit(_input, expected):
    assert get_unit(_input) == expected


def test_get_unit_func(mock_timed):
    assert get_unit(mock_timed(lambda x: x, unit=Unit.NANOSECOND)()) == Unit.NANOSECOND
