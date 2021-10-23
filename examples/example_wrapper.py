from time import sleep

from functimer import Unit, timed


def sleep_func():
    sleep(1)


def return_func():
    return True


if __name__ == "__main__":
    sleep_func = timed(sleep_func, unit=Unit.SECOND, number=1)
    runtime = sleep_func()
    print("Runtime of sleep_func:", runtime)

    return_func = timed(return_func, enable_return=True)
    runtime, ret = return_func()
    print("Runtime of return_func:", runtime)
    print("Result of return_func:", ret)

    timed_print = timed(print)
    runtime = timed_print("hello")
    print("Runtime of print:", runtime)
