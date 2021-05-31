import timeit
from functools import wraps
from typing import Callable

from functimer.classes import Result, TimedResult, Unit
from functimer.util import suppress_stdout

template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        ret = {stmt}
    _t1 = _timer()
    return _t1 - _t0, ret
"""


def timed(
    func: Callable = None,
    *,
    enabled: bool = True,
    unit: Unit = Unit.microsecond,
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

    def deco_args_wrapper(f) -> Callable:
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
        def func_wrapper(*args, **kwargs) -> Result:
            if timeit.template != template:
                timeit.template = template
            with suppress_stdout(enable_stdout):
                t, ret = timeit.timeit(
                    stmt=lambda: f(*args, **kwargs),
                    globals=f.__globals__ if hasattr(f, "__globals__") else None,
                    number=number if not estimate else 1,
                )

            u_string = TimedResult(t * (number if estimate else (1 / number)), unit)

            if enable_return:
                return u_string, ret
            return u_string

        return func_wrapper

    if func is None:
        return deco_args_wrapper
    return deco_args_wrapper(func)


# Alias
create_timed_function = timed
