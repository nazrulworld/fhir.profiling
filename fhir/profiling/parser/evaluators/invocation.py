# _*_ coding: utf-8 _*_
from typing import Any, List, Optional, Union

from .base import EMPTY, Evaluation, EvaluatorBase, ValuedEvaluation

__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


class InvocationExpressionEvaluator(EvaluatorBase):
    __antlr4_node_type__ = "InvocationExpression"

    def init(self, node_left: EvaluatorBase, node_right: EvaluatorBase):
        """ """
        self.add_node(node_left)
        self.add_node(node_right)

    def evaluate(self, resource: Any) -> Evaluation:
        """ """
        nodes = self.get_nodes()
        value_evaluation = nodes.left.evaluate(resource)
        value = value_evaluation.get_verdict(True)
        if nodes.right is EMPTY:
            return value
        return nodes.right.evaluate(value)


class FunctionInvocationEvaluator(EvaluatorBase):
    """TODO: inspect function"""

    __antlr4_node_type__ = "FunctionInvocation"
    __slots__ = (
        "func_name",
        "param_list",
    ) + EvaluatorBase.__slots__

    def __init__(
        self,
        expression: str = None,
    ):
        """param_list: (param name, param value, EqualityExpression)"""
        EvaluatorBase.__init__(self, expression)
        self.func_name = None
        self.param_list = None

    def init(self, func_name: str, param_list: Optional[List[EvaluatorBase]] = None):
        try:
            getattr(self, func_name)
            self.func_name = func_name
        except AttributeError:
            raise ValueError
        self.param_list = param_list

    def evaluate(self, resource: Any) -> Evaluation:
        """ """
        return getattr(self, self.func_name)(resource, param_list=self.param_list)

    def where(self):
        """ """

    def count(self):
        """ """

    def exists(self):
        """ """


class MemberInvocationEvaluator(EvaluatorBase):
    __antlr4_node_type__ = "MemberInvocation"

    def init(self, identifier: str):
        """ """
        self.add_node(identifier)

    def add_node(self, node: str):
        """ """
        if len(self.__storage__) > 0:
            raise ValueError("identifier is already assigned.")
        self.__storage__.append(node)

    def evaluate(self, resource: Any) -> Union[Evaluation, ValuedEvaluation]:
        """ """
        nodes = self.get_nodes()
        try:
            value: Any = getattr(resource, nodes.left)
            return ValuedEvaluation(value)
        except AttributeError:
            # @todo: handle error properly
            raise


__all__ = [
    "MemberInvocationEvaluator",
    "FunctionInvocationEvaluator",
    "InvocationExpressionEvaluator",
]
