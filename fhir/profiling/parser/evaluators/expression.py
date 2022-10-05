# _*_ coding: utf-8 _*_
from typing import Any, Optional, Union

from .base import (
    EMPTY,
    Evaluation,
    EvaluationError,
    EvaluatorBase,
    LogicalOperator,
    ValuedEvaluation,
    validate_both_nodes_boolean,
)
from .invocation import MemberInvocationEvaluator

__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


class IndexerExpressionEvaluator(EvaluatorBase):
    """ """

    __antlr4_node_type__ = "IndexerExpression"

    def init(self, member_invocation: MemberInvocationEvaluator, index: int):
        """ """
        self.add_node(member_invocation)
        self.add_node(index)

    def evaluate(self, resource: Any) -> Evaluation:
        """ """
        nodes = self.get_nodes()
        member_invocation = nodes.left
        index = nodes.right
        res = member_invocation.evaluate(resource)
        value = res.get_verdict()
        if isinstance(value, list):
            return ValuedEvaluation(value[index])
        raise ValueError


class OrExpressionEvaluator(LogicalOperator):
    __operators__ = {"or": "or_", "xor": "xor"}
    __antlr4_node_type__ = "OrExpression"

    def validate(
        self, value_left: Any, value_right: Any = EMPTY
    ) -> Optional[Evaluation]:
        """ """
        err = LogicalOperator.validate(self, value_left, value_right)
        if err:
            return err
        return validate_both_nodes_boolean(value_left, value_right)

    def or_(
        self,
        left_value: Union[bool, EvaluationError],
        right_value: Union[bool, EvaluationError],
    ) -> Evaluation:
        """ """
        if isinstance(left_value, EvaluationError):
            # @todo: better error handle
            raise EvaluationError
        if left_value is True:
            return Evaluation()
        if isinstance(right_value, EvaluationError):
            # @todo: concat error?
            raise EvaluationError
        return right_value is True and Evaluation() or Evaluation(error=EMPTY)

    def xor(
        self,
        left_value: Union[bool, EvaluationError],
        right_value: Union[bool, EvaluationError],
    ) -> Evaluation:
        """ """
        if isinstance(left_value, EvaluationError):
            # @todo: better error handle
            raise EvaluationError
        if isinstance(right_value, EvaluationError):
            # @todo: concat error?
            raise EvaluationError
        if not (
            all([left_value, right_value]) or all([not left_value, not right_value])
        ) and any([left_value, right_value]):
            return Evaluation()
        return Evaluation(error=EMPTY)


class AndExpressionEvaluator(LogicalOperator):
    __operators__ = {"and": "and_"}
    __antlr4_node_type__ = "AndExpression"

    def validate(
        self, value_left: Any, value_right: Any = EMPTY
    ) -> Optional[Evaluation]:
        """ """
        err = LogicalOperator.validate(self, value_left, value_right)
        if err:
            return err
        return validate_both_nodes_boolean(value_left, value_right)

    def and_(
        self,
        left_value: Union[bool, EvaluationError],
        right_value: Union[bool, EvaluationError],
    ) -> Evaluation:
        """ """
        if isinstance(left_value, EvaluationError):
            # @todo: better error handle
            raise EvaluationError
        if isinstance(right_value, EvaluationError):
            # @todo: concat error?
            raise EvaluationError
        if all([left_value, right_value]):
            return Evaluation()

        return Evaluation(error=EMPTY)


class EqualityExpressionEvaluator(LogicalOperator):
    """ """

    __operators__ = {
        "=": "eq",
        "~": "undefined",
        "!=": "ne",
        "!~": "undefined",
    }
    __antlr4_node_type__ = "EqualityExpression"

    def eq(self, value_left: Any, value_right: Any):
        """ """
        # @todo: blind compare?
        return value_left == value_right and Evaluation() or Evaluation(error=EMPTY)

    def ne(self, value_left: Any, value_right: Any):
        """ """
        # @todo: blind compare?
        return value_left != value_right and Evaluation() or Evaluation(error=EMPTY)


class InequalityExpressionEvaluator(LogicalOperator):
    """ """

    __operators__ = {"<=": "le", "<": "lt", ">": "gt", ">=": "ge"}
    __antlr4_node_type__ = "InequalityExpression"

    def validate(
        self, value_left: Any, value_right: Any = EMPTY
    ) -> Optional[Evaluation]:
        err = LogicalOperator.validate(self, value_left, value_right)
        if err:
            return err

        # todo: check types; int, float, datetime, object has __ge__,__le__,__gt__ or __ne__
        # __le__,__lt__,__ne__, __eq__
        def is_applicable(val):
            """ """
            return all(
                [
                    getattr(type(val), x, False)
                    for x in ("__ge__", "__le__", "__gt__", "__lt__")
                ]
            )

        if not all([is_applicable(value_left), is_applicable(value_right)]):
            raise

    def lt(self, value_left: Any, value_right: Any):
        """ """
        # @todo: blind compare?
        return value_left < value_right and Evaluation() or Evaluation(error=EMPTY)

    def gt(self, value_left: Any, value_right: Any):
        """ """
        # @todo: blind compare?
        return value_left > value_right and Evaluation() or Evaluation(error=EMPTY)

    def le(self, value_left: Any, value_right: Any):
        """ """
        # @todo: blind compare?
        return value_left <= value_right and Evaluation() or Evaluation(error=EMPTY)

    def ge(self, value_left: Any, value_right: Any):
        """ """
        # @todo: blind compare?
        return value_left >= value_right and Evaluation() or Evaluation(error=EMPTY)


class MembershipExpressionEvaluator(LogicalOperator):
    """ """

    __equality_operators__ = (
        "in",
        "contains",
    )
    __antlr4_node_type__ = "MembershipExpression"


__all__ = [
    "MembershipExpressionEvaluator",
    "InequalityExpressionEvaluator",
    "EqualityExpressionEvaluator",
    "AndExpressionEvaluator",
    "OrExpressionEvaluator",
    "IndexerExpressionEvaluator",
]
