# _*_ coding: utf-8 _*_
from collections import deque, namedtuple
from typing import Any, List

__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


class Empty:
    __slots__ = ()


class Null:
    __slots__ = ()


EMPTY = Empty()
NULL = Null()
LeftRightTuple = namedtuple("LeftRightTuple", ["left", "right"], rename=False)


def ensure_array(value: Any) -> List:
    """ """
    if value in (None, NULL, EMPTY):
        return []
    if isinstance(value, (list, deque)):
        return value
    return [value]


def has_value(value: Any) -> bool:
    if isinstance(value, (list, deque)):
        return len(value) > 0
    if value in (None, EMPTY, NULL):
        return False
    return True


__all__ = ["EMPTY", "NULL", "LeftRightTuple"]
