# _*_ coding: utf-8 _*_
from typing import Any, List, Optional

from .base import Evaluation, EvaluatorBase, LogicalOperator
from .invocation import MemberInvocationEvaluator
from .utils import ensure_array

__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


class IndexerExpressionEvaluator(EvaluatorBase):
    """ """

    __antlr4_node_type__ = "IndexerExpression"

    def init(self, member_invocation: MemberInvocationEvaluator, index: int):
        """ """
        self.add_node(member_invocation)
        self.add_node(index)

    def evaluate(self, input_collection: List[Any]) -> Evaluation:
        """ """
        collection = ensure_array(input_collection)
        nodes = self.get_nodes()
        member_invocation = nodes.left
        index = nodes.right
        evaluation = member_invocation.evaluate(collection)
        try:
            return Evaluation(evaluation.value[index])
        except IndexError:
            return Evaluation([])


class OrExpressionEvaluator(LogicalOperator):
    __operators__ = {"or": "or_", "xor": "xor"}
    __antlr4_node_type__ = "OrExpression"

    def or_(
        self,
        left_evaluation: Evaluation,
        right_evaluation: Evaluation,
    ) -> Evaluation:
        """ """
        if (
            left_evaluation.get_verdict() is True
            or right_evaluation.get_verdict() is True
        ):
            return Evaluation([True])
        return Evaluation([False])

    def xor(
        self,
        left_evaluation: Evaluation,
        right_evaluation: Evaluation,
    ) -> Evaluation:
        """ """
        if not (
            all([left_evaluation.get_verdict(), right_evaluation.get_verdict()])
            or all(
                [not left_evaluation.get_verdict(), not right_evaluation.get_verdict()]
            )
        ) and any([left_evaluation.get_verdict(), right_evaluation.get_verdict()]):
            return Evaluation([True])
        return Evaluation([False])


class AndExpressionEvaluator(LogicalOperator):
    __operators__ = {"and": "and_"}
    __antlr4_node_type__ = "AndExpression"

    def and_(
        self,
        left_evaluation: Evaluation,
        right_evaluation: Evaluation,
    ) -> Evaluation:
        """ """
        if all([left_evaluation.get_verdict(), right_evaluation.get_verdict()]):
            return Evaluation([True])

        return Evaluation([False])


class EqualityExpressionEvaluator(LogicalOperator):
    """ """

    __operators__ = {
        "=": "eq",
        "~": "undefined",
        "!=": "ne",
        "!~": "undefined",
    }
    __antlr4_node_type__ = "EqualityExpression"

    def eq(
        self,
        left_evaluation: Evaluation,
        right_evaluation: Evaluation,
    ):
        """ """
        # @todo: blind compare?
        return Evaluation([left_evaluation.value == right_evaluation.value])

    def ne(self, left_evaluation: Evaluation, right_evaluation: Evaluation):
        """ """
        # @todo: blind compare?
        return Evaluation([left_evaluation.value != right_evaluation.value])


class InequalityExpressionEvaluator(LogicalOperator):
    """ """

    __operators__ = {"<=": "le", "<": "lt", ">": "gt", ">=": "ge"}
    __antlr4_node_type__ = "InequalityExpression"

    @staticmethod
    def pre_check(
        left_evaluation: Evaluation, right_evaluation: Evaluation
    ) -> Optional[Evaluation]:
        """ """
        if (len(left_evaluation.value) != len(right_evaluation.value)) or not all(
            [left_evaluation.get_verdict(), right_evaluation.get_verdict()]
        ):
            return LogicalOperator.return_false()

    def lt(
        self, left_evaluation: Evaluation, right_evaluation: Evaluation
    ) -> Evaluation:
        """ """
        evaluation = InequalityExpressionEvaluator.pre_check(
            left_evaluation, right_evaluation
        )
        if evaluation is not None:
            return evaluation

        if len(left_evaluation.value) == 1:
            try:
                return Evaluation([left_evaluation.value < right_evaluation.value])
            except TypeError as exc:
                # @TODO: logging
                return LogicalOperator.return_false()

        result = []
        for idx, value in left_evaluation.value:
            result.append(value < right_evaluation.value[idx])
        return Evaluation(result)

    def gt(self, left_evaluation: Evaluation, right_evaluation: Evaluation):
        """ """
        evaluation = InequalityExpressionEvaluator.pre_check(
            left_evaluation, right_evaluation
        )
        if evaluation is not None:
            return evaluation

        if len(left_evaluation.value) == 1:
            try:
                return Evaluation([left_evaluation.value > right_evaluation.value])
            except TypeError as exc:
                # @TODO: logging
                return LogicalOperator.return_false()

        result = []
        for idx, value in left_evaluation.value:
            result.append(value > right_evaluation.value[idx])
        return Evaluation(result)

    def le(self, left_evaluation: Evaluation, right_evaluation: Evaluation):
        """ """
        evaluation = InequalityExpressionEvaluator.pre_check(
            left_evaluation, right_evaluation
        )
        if evaluation is not None:
            return evaluation

        if len(left_evaluation.value) == 1:
            try:
                return Evaluation([left_evaluation.value <= right_evaluation.value])
            except TypeError as exc:
                # @TODO: logging
                return LogicalOperator.return_false()

        result = []
        for idx, value in left_evaluation.value:
            result.append(value <= right_evaluation.value[idx])
        return Evaluation(result)

    def ge(self, left_evaluation: Evaluation, right_evaluation: Evaluation):
        """ """
        evaluation = InequalityExpressionEvaluator.pre_check(
            left_evaluation, right_evaluation
        )
        if evaluation is not None:
            return evaluation

        if len(left_evaluation.value) == 1:
            try:
                return Evaluation([left_evaluation.value >= right_evaluation.value])
            except TypeError as exc:
                # @TODO: logging
                return LogicalOperator.return_false()

        result = []
        for idx, value in left_evaluation.value:
            result.append(value >= right_evaluation.value[idx])
        return Evaluation(result)


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
