import argparse
import builtins
import importlib
import re
import sys
from typing import Callable, Dict, Tuple

from functimer import TimingException, Unit, timed
from functimer.classes import TimedResult

unit_map: Dict[str, Unit] = {
    "ns": Unit.nanosecond,
    "ms": Unit.microsecond,
    "Ms": Unit.millisecond,
    "s": Unit.second,
    "m": Unit.minute,
}

RE_LAMBDA = r"\((.*)\)\s*\((.*)\)"
RE_FUNCTION = r"(.*)\s*\((.*)\)"


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


def parse_for_method(module: str) -> Callable:
    try:
        method = getattr(builtins, module)
        return method
    except AttributeError:
        module, *submodules, method = module.split(".")
        module = importlib.import_module(module)
        for submodule in submodules:
            module = getattr(module, submodule)
        return getattr(module, method)


def parse_func(func: str) -> Tuple[Callable, str]:
    if "(" not in func and ")" not in func:
        raise TimingException("Malformed input.")
    if not func.startswith("(lambda"):
        func, args = re.findall(RE_FUNCTION, func)[0]
        method = parse_for_method(func)
    else:
        lmbda, args = re.findall(RE_LAMBDA, func)[0]
        method = eval(lmbda)
    return method, args


def exec_func(func: str, **kwargs) -> TimedResult:
    f, args = parse_func(func)
    timed_f = timed(f, **kwargs, enable_return=True)  # NOQA
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
