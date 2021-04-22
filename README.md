# functimer

A function decorator/wrapper package to time a given function.

## Contents

- `functimer/timer.py`: contains the `timer` decorator.
- `functimer/util.py`: contains `get_unit` function, parses the unit from given string following the format of `0.0 ms`
- `functimer/classes.py`: contains general classes and enums of package.

### Installation
To install from PYPI:

    pip install functimer

To manually install:
    
    poetry build
    pip install dist/*.whl

How to install [Poetry](https://python-poetry.org/docs/#installation).

### Quick Example
Comprehensive Examples in `examples`
```py
@timed(unit=Unit.second, number=1)
def timed_sleep(seconds):
    sleep(seconds)

runtime = timed_sleep(0.3)
```

### Tests
Run `pytest` in the root directory of the repo.

### License
MIT
