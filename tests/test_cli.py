import sys

import pytest

import functimer
import functimer.__main__ as main
from functimer import TimingException, Unit


@pytest.mark.parametrize(
    "_input, expected",
    [
        ("sum", "sum"),
        ("math.sqrt", "math"),
        ("functimer.util.get_unit", "functimer"),
    ],
)
def test_create_local(_input, expected):
    with main.create_local(_input, **{}) as local:
        assert list(local.keys())[0] == expected


@pytest.mark.parametrize(
    "_input, error",
    [
        ("func(1, 2, 3)", ValueError),
        ("malformed input", TimingException),
        ("package.subpackage.method('testing')", ModuleNotFoundError),
        ("package.subpackage", TimingException),
    ],
)
def test_exec_func_exception(_input, error):
    with pytest.raises(error):
        main.exec_func(_input, **{})


@pytest.mark.parametrize(
    "_input, expected",
    [
        ("sum([1, 2, 3])", 6),
        ("math.sqrt(4)", 2.0),
        ("functimer.util.get_unit('1.00 s')", Unit.SECOND),
        ("(lambda x: x+x)(10)", 20),
        ("(lambda x, y: x+y)(10, 22)", 32),
        ("(lambda x: sorted(x))([3,2,1])", [1, 2, 3]),
        ("(lambda x: x+x)(x=1)", 2),
        ("functimer.classes.Unit.from_str('s')", Unit.SECOND),
        ("tests.Test(1, 2).mult()", 2),
    ],
)
def test_exec_func(monkeypatch, _input, expected):
    with monkeypatch.context() as m:
        m.setattr(
            functimer.functimer.timeit, "timeit", lambda *args, **kwargs: (1, expected)
        )
        runtime, ret = main.exec_func(_input)
        assert ret == expected


@pytest.mark.parametrize(
    "_input, error",
    [
        ("sum(1)", TypeError),
        ("functimer.util.get_unit('invalid')", TimingException),
    ],
)
def test_exec_func_inner_exception(_input, error):
    with pytest.raises(error):
        main.exec_func(_input)


@pytest.mark.parametrize(
    "_input, expected",
    [
        (["sum([1, 2, 3])"], "Average runtime of 10,000"),
        (["sum([1, 2, 3])", "-r"], "sum([1, 2, 3]) -> 6"),
        (["sum([1, 2, 3])", "-e"], "Estimated"),
        (["sum([1, 2, 3])", "-u", "ns"], "ns"),
        (["sum([1, 2, 3])", "-n", "1,000"], "1,000"),
    ],
)
def test_cli(monkeypatch, capsys, _input, expected):
    sys.argv[1:] = _input
    with monkeypatch.context() as m:
        m.setattr(functimer.functimer.timeit, "timeit", lambda *args, **kwargs: (1, 6))
        main.cli()
        out = capsys.readouterr().out
        assert expected in out


@pytest.mark.parametrize(
    "_input, error, match",
    [
        ([], SystemExit, "2"),
        (["-u", "malformed", "sum([1, 2, 3]"], SystemExit, "2"),
        (["1"], TimingException, "Malformed"),
    ],
)
def test_cli_error(_input, error, match):
    with pytest.raises(error, match=match):
        sys.argv[1:] = _input
        main.cli()
