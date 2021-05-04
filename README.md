# functimer

A decorator/wrapper package to time a given function.

[![PyPI version](https://badge.fury.io/py/functimer.svg)](https://badge.fury.io/py/functimer)

---
### Installation
PYPI:

    pip install functimer

Manual:

    poetry build
    pip install dist/*.whl

How to install [Poetry](https://python-poetry.org/docs/#installation).

### Quick Example
Comprehensive Examples in `examples`
```py
@timed(unit=Unit.second, number=1)
def timed_sleep(seconds):
    sleep(seconds)

runtime = timed_sleep(1)
"1.00 s"
```

### Tests
Run `pytest` in the root directory of the repo.

### License
MIT
