import os
import pathlib
from os.path import dirname

TESTS_ROOT_PATH = pathlib.Path(dirname(os.path.abspath(__file__)))
IS_TRAVIS = "TRAVIS" in os.environ
STATIC_DIR = TESTS_ROOT_PATH / "static"
STATIC_DK_DIR = STATIC_DIR / "DK"
STATIC_US_DIR = STATIC_DIR / "US"
