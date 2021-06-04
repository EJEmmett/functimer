from time import sleep

from functimer import Unit, get_unit, timed


def sleep_func():
    sleep(1)


if __name__ == "__main__":
    print("0.2 ns:", get_unit("0.2 ns"))
    print("0.2 µs:", get_unit("0.2 µs"))
    print("0.2 ms:", get_unit("0.2 ms"))
    print("0.2 s:", get_unit("0.2 s"))
    print("0.2 m:", get_unit("0.2 m"))

    sleep_func = timed(sleep_func, unit=Unit.MINUTE, estimate=True)
    runtime = sleep_func()
    print(f"{runtime}: {get_unit(runtime)} or {runtime.unit}")
