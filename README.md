# functimer

A decorator/wrapper package to time a given function.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2ca963702d174d48ae943946a2b174b7)](https://app.codacy.com/gh/EJEmmett/functimer?utm_source=github.com&utm_medium=referral&utm_content=EJEmmett/functimer&utm_campaign=Badge_Grade_Settings)
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
