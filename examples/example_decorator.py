from time import sleep

from functimer import Unit, timed


@timed(unit=Unit.second, number=1)
def timed_sleep(seconds):
    sleep(seconds)


@timed(enable_return=True)
def timed_with_return():
    return True


@timed
def suppress_stdout():
    print("Hello")


@timed(enable_stdout=True, number=1)
def enabled_stdout():
    print("Inside Timer")


@timed(unit=Unit.minute, estimate=True)
def estimate_func():
    sleep(2)


@timed(enabled=False, enable_return=True)
def disabled_with_return():
    return True


if __name__ == "__main__":
    runtime = timed_sleep(0.3)
    print("Runtime of timed_sleep:", runtime)
    print()

    runtime, ret = timed_with_return()
    print("Runtime of timed_with_return:", runtime)
    print("Returned value of timed_with_return:", ret)
    print()

    runtime = suppress_stdout()
    print("Runtime of suppress_stdout:", runtime)
    print()

    runtime = enabled_stdout()
    print("Runtime of enable_stdout:", runtime)
    print()

    runtime = estimate_func()
    print("Estimated total runtime of estimate_func:", runtime)
    print()

    ret = disabled_with_return()
    print("Returned value of disabled_with_return:", ret)
