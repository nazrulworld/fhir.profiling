import os
import pathlib
from os.path import dirname

TESTS_ROOT_PATH = pathlib.Path(dirname(os.path.abspath(__file__)))
IS_TRAVIS = "TRAVIS" in os.environ
