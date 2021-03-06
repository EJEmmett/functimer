import gc
from functools import wraps
from time import perf_counter
from typing import Any, Callable, Tuple

from functimer.classes import Result, TResult, Unit
from functimer.util import suppress_stdout

DEFAULT_TIMER = perf_counter


def timed(
    func: Callable = None,
    *,
    enabled: bool = True,
    unit: Unit = Unit.MICROSECOND,
    number: int = 1000,
    estimate: bool = False,
    enable_return: bool = False,
    enable_stdout: bool = False,
) -> Callable:
    """Times wrapped function and returns string formatted object.

    Args:
        func:            The function to be wrapped. (None if decorated)
        enabled:         Disables timing of wrapped func.
        unit:            The scientific unit to format the returned value.
        estimate:        Toggle returning a rough estimation of total timer runtime over number
                         executions based on the runtime of one execution.
        number:          Number of times to run function, higher values increase accuracy, but take
                         longer.
        enable_return:   Whether to return the value from the function.
        enable_stdout:   Whether to suppress writes to STDOUT.
                         (Suppressing STDOUT decreases runtime of function)

    Returns:
        function_wrapper: The wrapped function.

    Raises:
        ValueError:
            If number is less than one.
    """

    if number < 1:
        raise ValueError("Argument number must be greater than 0.")

    def deco_args_wrapper(f: Callable) -> Callable:
        if not enabled:
            return f

        @wraps(
            f,
            assigned=(
                "__module__",
                "__name__",
                "__qualname__",
                "__doc__",
            ),
        )
        def func_wrapper(*args, **kwargs) -> TResult:
            with suppress_stdout(enable_stdout):
                total_time, ret = runner(
                    lambda: f(*args, **kwargs), number=1 if estimate else number
                )

            timed_result = Result(
                total_time * (number if estimate else (1 / number)), unit
            )

            if enable_return:
                return timed_result, ret
            return timed_result

        return func_wrapper

    if func is None:
        return deco_args_wrapper
    return deco_args_wrapper(func)


def runner(f: Callable, *, number: int) -> Tuple[float, Any]:
    def inner():
        ret = None
        t0 = DEFAULT_TIMER()
        for _ in range(number):
            ret = f()
        t1 = DEFAULT_TIMER()
        return t1 - t0, ret

    gc_old = gc.isenabled()
    gc.disable()
    try:
        return inner()
    finally:
        if gc_old:
            gc.enable()
