# aarchiba_tools

Handy python tools I often use.

These should work on both python 2.7 and python 3. (The need for python 2.7 is because a number of pulsar tools have not yet been ported to python 3.) If I add bits that only work on one or the other I'll try to make sure they fail gracefully when the package is used in the wrong place. Ditto more exotic dependencies (like those pulsar tools) - the package should do what it can when they are not available.

## Development

The source distribution can be tested with `tox`; simply run it from the same directory as `setup.py` and it will install the package in a virtualenv and run the test suite.

Development work can most easily be done from an editable pip install (`pip install -e .`) in a suitable virtualenv.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

