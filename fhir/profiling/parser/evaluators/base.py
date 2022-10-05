# _*_ coding: utf-8 _*_
import abc
from collections import deque, namedtuple
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Deque, Optional, Union, cast

from pydantic.error_wrappers import ValidationError

__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


class Empty:
    __slots__ = ()


class Null:
    __slots__ = ()


EMPTY = Empty()
NULL = Null()
LeftRightTuple = namedtuple("LeftRightTuple", ["left", "right"], rename=False)


@dataclass(init=True)
class QuantityUnit:
    unit: str = field(init=True)
    value: Union[int, float] = field(init=True)


def extract_value(node: Any, resource: Any = EMPTY) -> Any:
    """ """
    if node is EMPTY:
        # no evaluator
        return resource
    if resource is EMPTY and isinstance(node, EvaluatorBase):
        raise ValueError
    if isinstance(node, EvaluatorBase):
        value_evaluate = node.evaluate(resource)
        if isinstance(value_evaluate, Evaluation):
            # @todo: need better error handling
            value = value_evaluate.get_verdict(True)
        else:
            value = value_evaluate
    else:
        value = node
    return value


def validate_both_nodes_boolean(
    value_left: Union["EvaluationError", bool],
    value_right: Union["EvaluationError", bool],
):
    if not all(
        [
            isinstance(value_left, (EvaluationError, bool)),
            isinstance(value_right, (EvaluationError, bool)),
        ]
    ):
        # @todo: proper error need to be returned
        raise ValueError


class ReadonlyClass:
    __slots__ = ()

    def __setattr__(self, key, value):
        """ """
        raise TypeError("Readonly object!")


class Evaluation(abc.ABC, ReadonlyClass):
    """ """

    __slots__ = ("error", "success")

    def __init__(self, error: "EvaluationError" = None):
        """Terms for variable error.
        case-1 error value is None:  evaluation's result True
        case-2 error value is EMPTY: evaluation's result False
        case-3 error value: exception happening
        """
        object.__setattr__(self, "error", error)
        success = None
        if error is EMPTY:
            success = False
        elif error is None:
            success = True
        object.__setattr__(self, "success", success)

    def has_error(self):
        """ """
        return self.error not in (None, EMPTY)

    def get_verdict(self, raise_on_error: bool = False):
        """ """
        if self.has_error() and raise_on_error:
            raise ValueError
        return self.success

    def __bool__(self) -> bool:
        """ """
        return self.success is None and False or self.success


class ValuedEvaluation(Evaluation):
    """ """

    __slots__ = ("value",) + Evaluation.__slots__

    def __init__(
        self,
        value: Any,
        error: Optional[ValidationError] = None,
    ):
        """ """
        Evaluation.__init__(self, error)
        if TYPE_CHECKING:
            self.value = None
        object.__setattr__(self, "value", value)

    def get_verdict(self, raise_on_error: bool = False):
        """ """
        if self.value is not EMPTY:
            return self.value
        return Evaluation.get_verdict(self, raise_on_error)

    def __bool__(self) -> bool:
        """ """
        if self.value is EMPTY:
            return False
        if isinstance(self.value, bool):
            return self.value
        if isinstance(self.value, (dict, list, set)):
            return len(self.value) > 0
        if self.value:
            return True
        return Evaluation.__bool__(self)


class EvaluationError(abc.ABC, ReadonlyClass):
    """@todo: contact errors"""

    __slots__ = ("error", "expression")

    def __init__(self, error: ValidationError, expression: str):
        """ """
        object.__setattr__(self, "error", error)
        object.__setattr__(self, "expression", expression)


class EvaluatorBase:
    """ """

    __antlr4_node_type__: str = ""
    __slots__ = ("__expression_literal__", "__storage__", "__predecessor__")

    def __init__(self, expression: Optional[str] = None):
        """ """
        self.__expression_literal__ = expression
        self.__predecessor__: Optional["EvaluatorBase"] = None
        self.__storage__: Deque[Any] = deque(maxlen=2)

    def evaluate(self, resource: Any) -> Evaluation:
        """ """
        raise NotImplementedError

    def get_type(self):
        """ """
        return self.__antlr4_node_type__

    def get_expression(self):
        """ """
        return self.__expression_literal__

    def add_node(self, node: Any):
        """ """
        if len(self.__storage__) > 2:
            raise ValueError("left & right values are already assigned")
        self.__storage__.append(node)

    def get_nodes(self) -> LeftRightTuple:
        """ """
        if len(self.__storage__) == 0:
            return LeftRightTuple(EMPTY, EMPTY)
        elif len(self.__storage__) == 1:
            return LeftRightTuple(self.__storage__[0], EMPTY)
        else:
            return LeftRightTuple(self.__storage__[0], self.__storage__[1])

    def set_predecessor(self, evaluator: "EvaluatorBase"):
        """ """
        self.__predecessor__ = evaluator

    def get_predecessor(self):
        """ """
        return self.__predecessor__


class LogicalOperator(EvaluatorBase):
    """ """

    __operators__ = {}
    __slots__ = ("operator",) + Evaluation.__slots__

    def __init__(
        self,
        operator: str,
        expression: Optional[str] = None,
    ):
        """ """
        EvaluatorBase.__init__(self, expression)

        if operator not in self.__operators__.keys():
            raise TypeError(f"Invalid operator for '{self.__antlr4_node_type__}'.")
        self.operator = operator

    def init(self, node_left: Any, node_right: Any):
        """ """
        self.add_node(node_left)
        self.add_node(node_right)

    def validate(
        self, value_left: Any, value_right: Any = EMPTY
    ) -> Optional[Evaluation]:
        """ """
        if isinstance(value_left, EvaluationError):
            raise ValueError
        if isinstance(value_right, EvaluationError):
            raise ValueError
        return

    def evaluate(self, resource: Any = EMPTY) -> Evaluation:
        """ """
        nodes = self.get_nodes()
        value_left = extract_value(nodes.left, resource)
        value_right = extract_value(nodes.right, resource)

        value = self.validate(value_left, value_right)
        if value is not None:
            return value

        if type(value_left) != type(value_right):
            raise ValueError

        return getattr(self, self.__operators__[self.operator])(value_left, value_right)


class ParenthesizedTermEvaluator(EvaluatorBase):
    """ """

    __antlr4_node_type__ = "ParenthesizedTerm"

    def evaluate(self, resource: Any) -> Evaluation:
        """ """
        if len(self.__storage__) == 0:
            raise ValueError("No successor evaluator is assigned.")
            # raise EvaluationError()
        successor = cast(EvaluatorBase, self.__storage__[0])
        return successor.evaluate(resource)

    def add_node(self, node: EvaluatorBase):
        """ """
        if len(self.__storage__) > 0:
            raise ValueError("Successor evaluator is already assigned.")
        self.__storage__.append(node)


__all__ = [
    "EvaluatorBase",
    "QuantityUnit",
    "EMPTY",
    "NULL",
    "LeftRightTuple",
    "ParenthesizedTermEvaluator",
]
