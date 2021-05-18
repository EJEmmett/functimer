import argparse
import builtins
import sys
from contextlib import contextmanager
from importlib import import_module
from re import findall, sub
from types import FunctionType, ModuleType
from typing import Dict, Union

from functimer import TimingException, Unit, timed
from functimer.classes import TimedResult

unit_map: Dict[str, Unit] = {
    "ns": Unit.nanosecond,
    "ms": Unit.microsecond,
    "Ms": Unit.millisecond,
    "s": Unit.second,
    "m": Unit.minute,
}

RE_ARGS = r"\((.*?)\)"
RE_LAMBDA = r"\((.*)\)\s*\((.*)\)"


def parse_unit(s: str) -> Unit:
    try:
        return unit_map[s]
    except KeyError:
        try:
            return Unit[s]
        except KeyError:
            raise ValueError()


def parse_int(s: str) -> int:
    return int(s.replace(",", ""))


@contextmanager
def create_local(func_chain: str, **kwargs) -> Dict[str, Union[ModuleType, FunctionType]]:
    try:
        method = getattr(builtins, func_chain)
        local = {method.__name__: timed(method, **kwargs, enable_return=True)}
        print(type(local[method.__name__]))
        yield local
    except AttributeError:
        module, *subattrs, method = func_chain.split(".")
        module = import_module(module)
        local = {module.__name__: module}
        for submodule in subattrs:
            module = getattr(module, submodule)
        store_method = getattr(module, method)
        setattr(module, method, timed(store_method, **kwargs, enable_return=True))
        yield local
        setattr(module, method, store_method)


def exec_func(func: str, **kwargs) -> TimedResult:
    if "(" not in func and ")" not in func:
        raise TimingException("Malformed input.")

    if not func.startswith("(lambda"):
        func_chain = sub(RE_ARGS, "", func)
        with create_local(func_chain, **kwargs) as local:
            return eval(func, globals(), local)
    else:
        lamb, args = findall(RE_LAMBDA, func)[0]
        lamb = eval(lamb)
        timed_f = timed(lamb, **kwargs, enable_return=True)  # NOQA
        return eval(f"timed_f({args})")


def cli():
    parser = argparse.ArgumentParser(
        prog="functimer",
        description="A decorator/wrapper package to time a given function.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "func",
        metavar="function",
        help="Given function call to time. Inner quotes must be single. \neg. "
        '"sqrt(4)" or "functimer.util.get_unit(\'1.00 s\')" or "(lambda x: x+x)(10)"',
    )

    parser.add_argument(
        "-r",
        "--return",
        action="store_true",
        dest="ret",
        help="Output the return value of function.",
    )

    parser.add_argument(
        "-e",
        "--estimate",
        action="store_true",
        help="Roughly estimate the total time needed to time function over number of executions.",
    )

    parser.add_argument(
        "-u",
        "--unit",
        type=parse_unit,
        default=Unit.microsecond,
        help=f"Set the resulting unit, defaults to microsecond."
        f"({', '.join(list(unit_map.keys()))})",
    )

    parser.add_argument(
        "-n",
        "--number",
        metavar="int",
        type=parse_int,
        default=10_000,
        help="Set the number of times to execute.",
    )

    args = parser.parse_args()

    runtime, ret = exec_func(
        args.func, unit=args.unit, estimate=args.estimate, number=args.number
    )

    print(
        f"{'Average' if not args.estimate else 'Estimated'} runtime of {args.number:,} executions: {runtime}"
    )
    if args.ret:
        print(f"{args.func} -> {repr(ret)}")

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(cli())
