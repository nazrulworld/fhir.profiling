# _*_ coding: utf-8 _*_
import abc
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Deque, List, Optional, Union, cast

from .utils import EMPTY, NULL, LeftRightTuple, ensure_array, has_value, finalize_value

__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


@dataclass(init=True)
class QuantityUnit:
    unit: str = field(init=True)
    value: Union[int, float] = field(init=True)


class ReadonlyClass:
    __slots__ = ()

    def __setattr__(self, key, value):
        """ """
        raise TypeError("Readonly object!")


class EvaluationError(Exception, ReadonlyClass):
    """@todo: contact errors"""

    __slots__ = ("msg", "expression")

    def __init__(self, msg: str, expression: str):
        """ """
        object.__setattr__(self, "msg", msg)
        object.__setattr__(self, "expression", expression)
        Exception.__init__(self, msg)


class Evaluation(abc.ABC, ReadonlyClass):
    """ """

    __slots__ = ("value",)

    def __init__(self, value: Any):
        """Terms for variable error."""
        object.__setattr__(self, "value", finalize_value(ensure_array(value)))

    def get_verdict(self) -> bool:
        """ """
        if has_value(self.value) is False:
            return False
        if len(self.value) == 1 and isinstance(self.value[0], bool):
            return self.value[0]
        return True

    def __bool__(self) -> bool:
        """ """
        return self.get_verdict()

    def __len__(self):
        """ """
        return len(self.value)


class EvaluatorBase:
    """ """

    __antlr4_node_type__: str = ""
    __slots__ = ("__expression_literal__", "__storage__", "__predecessor__")

    def __init__(self, expression: Optional[str] = None):
        """ """
        self.__expression_literal__ = expression
        self.__predecessor__: Optional["EvaluatorBase"] = None
        self.__storage__: Deque[Any] = deque(maxlen=2)

    def evaluate(self, input_collection: List[Any]) -> Evaluation:
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

    @staticmethod
    def ensure_evaluation(value: Any):
        """ """
        if isinstance(value, Evaluation):
            return value
        return Evaluation(value)


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
        evaluation_left = LogicalOperator.extract_value(nodes.left, resource)
        evaluation_right = LogicalOperator.extract_value(nodes.right, resource)
        self.validate(evaluation_left, evaluation_right)
        return getattr(self, self.__operators__[self.operator])(
            evaluation_left, evaluation_right
        )

    @staticmethod
    def return_false() -> Evaluation:
        """ """
        return Evaluation([False])

    @staticmethod
    def return_true() -> Evaluation:
        """ """
        return Evaluation([True])

    @staticmethod
    def extract_value(node: Any, resource: Any = EMPTY) -> Any:
        """ """
        if node is EMPTY and resource is not EMPTY:
            return EvaluatorBase.ensure_evaluation(resource)
        if resource is EMPTY and isinstance(node, EvaluatorBase):
            raise ValueError
        if isinstance(node, EvaluatorBase):
            return node.evaluate(resource)
        return EvaluatorBase.ensure_evaluation(node)


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
    "EvaluationError",
    "QuantityUnit",
    "EMPTY",
    "NULL",
    "LeftRightTuple",
    "ParenthesizedTermEvaluator",
]
