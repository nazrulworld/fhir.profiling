# _*_ coding: utf-8 _*_
from collections import deque, namedtuple
from functools import reduce

from typing import Any, List
from datetime import datetime, date, time
import uuid

__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


class Empty:
    __slots__ = ()


class Null:
    __slots__ = ()


EMPTY = Empty()
NULL = Null()
LeftRightTuple = namedtuple("LeftRightTuple", ["left", "right"], rename=False)
PRIMITIVES = (str, bytes, float, int, complex, bool, date, datetime, time, uuid.UUID)


def ensure_array(value: Any) -> List:
    """ """
    if value in (None, NULL, EMPTY):
        return []
    if isinstance(value, (list, deque)):
        return value
    return [value]


def simplify(value: Any) -> Any:
    """Reverse operation of ensure_array()"""
    if isinstance(value, (list, deque)):
        if len(value) == 1:
            return simplify(value[0])
        elif len(value) == 0:
            return None
    return value


def has_value(value: Any) -> bool:
    if isinstance(value, (list, deque)):
        return len(value) > 0
    if value in (None, EMPTY, NULL):
        return False
    return True


def finalize_value(collection: Any):
    def do(container, val):
        if isinstance(val, list):
            container = container + val
        else:
            container.append(val)
        return container

    return reduce(do, collection, [])


__all__ = ["EMPTY", "NULL", "LeftRightTuple"]
