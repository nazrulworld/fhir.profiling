# _*_ coding: utf-8 _*_
import logging
from typing import Any, List, Optional

from .base import EMPTY, Evaluation, EvaluatorBase
from .utils import ensure_array, has_value

__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"

LOG = logging.getLogger("evaluator.invocation")


class InvocationExpressionEvaluator(EvaluatorBase):
    __antlr4_node_type__ = "InvocationExpression"

    def init(self, node_left: EvaluatorBase, node_right: EvaluatorBase):
        """ """
        self.add_node(node_left)
        self.add_node(node_right)

    def evaluate(self, input_collection: List[Any]) -> Evaluation:
        """ """
        collection = ensure_array(input_collection)
        nodes = self.get_nodes()
        value_evaluation = nodes.left.evaluate(collection)
        if nodes.right is EMPTY:
            return value_evaluation
        return nodes.right.evaluate(value_evaluation.value)


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

    def hasValue(self):
        """Returns true if the input collection contains a single value which is a FHIR primitive,
        and it has a primitive value (e.g. as opposed to not having a value and just having extensions).
        Otherwise, the return value is empty.

        Note to implementers: The FHIR conceptual model talks about "primitives" as subclasses of the
        type Element that also have id and extensions. What this actually means is that a FHIR primitive
        is not a primitive in an implementation language. The introduction (section 2 above) describes
        the navigation tree as if the FHIR model applies - primitives are both primitives and elements
        with children.
        In FHIRPath, this means that FHIR primitives have a value child, but,
        as described above, they are automatically cast to FHIRPath primitives when
        comparisons are made, and that the primitive value will be included in the set
        returned by children() or descendants().
        """

    def children(self):
        """Returns a collection with all immediate child nodes of all items
        in the input collection. Note that the ordering of the children is
        undefined and using functions like first() on the result may return
        different results on different platforms."""


class MemberInvocationEvaluator(EvaluatorBase):
    __antlr4_node_type__ = "MemberInvocation"
    """https://hl7.github.io/fhirpath.js/"""

    def init(self, identifier: str):
        """ """
        self.add_node(identifier)

    def add_node(self, node: str):
        """ """
        if len(self.__storage__) > 0:
            raise ValueError("identifier is already assigned.")
        self.__storage__.append(node)

    def evaluate(self, input_collection: List[Any]) -> Evaluation:
        """ """
        collection = ensure_array(input_collection)
        nodes = self.get_nodes()
        result = []
        for item in collection:
            try:
                val = item.get(nodes.left, [])
                if has_value(val):
                    result.append(val)
            except (AttributeError, TypeError) as exc:
                LOG.debug(str(exc), exc_info=exc)

        return Evaluation(result)


__all__ = [
    "MemberInvocationEvaluator",
    "FunctionInvocationEvaluator",
    "InvocationExpressionEvaluator",
]
