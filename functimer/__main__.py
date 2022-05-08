import builtins
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from contextlib import contextmanager
from importlib import import_module
from re import findall, sub
from types import ModuleType
from typing import Callable, Dict, Union

from functimer import TimingException, Unit, timed
from functimer.classes import Result

unit_map: Dict[str, Unit] = {
    "ns": Unit.NANOSECOND,
    "ms": Unit.MICROSECOND,
    "Ms": Unit.MILLISECOND,
    "s": Unit.SECOND,
    "m": Unit.MINUTE,
}

RE_ARGS = r"\((.*?)\)"
RE_LAMBDA = r"\((.*)\)\s*\((.*)\)"


def parse_unit(string: str) -> Unit:
    try:
        return unit_map[string]
    except KeyError:
        try:
            return Unit[string]
        except KeyError:
            raise ValueError()


@contextmanager  # type: ignore
def localized_module(  # type: ignore
    func_chain: str, **kwargs
) -> Dict[str, Union[ModuleType, Callable]]:
    try:
        method = getattr(builtins, func_chain)
        builtin_local: Dict[str, Callable] = {
            method.__name__: timed(method, **kwargs, enable_return=True)
        }
        yield builtin_local
    except AttributeError:
        module_name, *sub_attrs, method = func_chain.split(".")
        module = import_module(module_name)
        module_local: Dict[str, ModuleType] = {module.__name__: module}
        for submodule in sub_attrs:
            module = getattr(module, submodule)
        stored_method = getattr(module, method)
        setattr(module, method, timed(stored_method, **kwargs, enable_return=True))
        yield module_local
        # Prevent Mangling of Modules in memory
        setattr(module, method, stored_method)


def exec_func(func: str, **kwargs) -> Result:
    if "(" not in func and ")" not in func:
        raise TimingException("Malformed input.")

    if not func.startswith("(lambda"):
        func_chain = sub(RE_ARGS, "", func)

        local: Dict[str, Union[ModuleType, Callable]]
        with localized_module(func_chain, **kwargs) as local:
            return eval(func, globals(), local)
    else:
        lamb, args = findall(RE_LAMBDA, func)[0]
        lamb = eval(lamb)
        timed_f = timed(lamb, **kwargs, enable_return=True)  # NOQA
        return eval(f"timed_f({args})")


def cli():
    parser = ArgumentParser(
        prog="functimer",
        description="A decorator/wrapper package to time a given function.",
        formatter_class=RawTextHelpFormatter,
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
        default=Unit.MICROSECOND,
        help=f"Set the resulting unit, defaults to microsecond. "
        f"({', '.join(list(unit_map.keys()))})",
    )

    parser.add_argument(
        "-n",
        "--number",
        metavar="int",
        type=lambda s: int(s.replace(",", "")),
        default=10_000,
        help="Set the number of times to execute.",
    )

    args = parser.parse_args()

    runtime, ret = exec_func(
        args.func, unit=args.unit, estimate=args.estimate, number=args.number
    )

    print(
        f"{'Average' if not args.estimate else 'Estimated'} "
        f"runtime of {args.number:,} executions: {runtime}"
    )
    if args.ret:
        print(f"{args.func} -> {repr(ret)}")

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(cli())
