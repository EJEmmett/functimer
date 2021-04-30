# functimer

A function decorator/wrapper package to time a given function.

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

runtime = timed_sleep(0.3)
```

### Tests
Run `pytest` in the root directory of the repo.

### License
MIT
