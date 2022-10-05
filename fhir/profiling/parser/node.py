# _*_ coding: utf-8 _*_
import ast
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic.datetime_parse import parse_date, parse_datetime, parse_time

from .evaluators import api

__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


class ExpressionNode(BaseModel):
    """ """

    node_type: str = Field(..., title="Node Type")
    text: str = Field(None, title="Text")
    terminal_node_text: Optional[List[str]] = Field(None, title="Terminal Node Text")
    children: Optional[List["ExpressionNode"]] = Field(None, title="Children node")

    def construct_evaluator(self, evaluator: Optional[api.EvaluatorBase] = None):
        """ """
        if self.node_type in ("TermExpression", "InvocationTerm"):
            # nothing to do just pass to children
            assert len(self.children) == 1
            return self.children[0].construct_evaluator(evaluator)
        # Logic-1
        if self.node_type == "MemberInvocation":
            assert len(self.children) == 1
            assert self.children[0].node_type == "Identifier"
            me = api.MemberInvocationEvaluator(expression=self.text)
            me.init(self.children[0].terminal_node_text[0])
            return ExpressionNode.finalize(me, evaluator)
        # Logic-2
        if self.node_type == "ParenthesizedTerm":
            assert len(self.children) == 1
            me = api.ParenthesizedTermEvaluator(expression=self.text)
            successor = self.children[0].construct_evaluator(me)
            me.add_node(successor)
            return ExpressionNode.finalize(me, evaluator)

        if self.node_type == "InvocationExpression":
            assert len(self.children) == 2
            me = api.InvocationExpressionEvaluator(expression=self.text)
            left_node = self.children[0].construct_evaluator(me)
            right_node = self.children[1].construct_evaluator(me)
            me.init(left_node, right_node)
            return ExpressionNode.finalize(me, evaluator)

        if self.node_type == "FunctionInvocation":
            assert len(self.children) == 1
            func_name, param_list = ExpressionNode.parse_function(self.children[0])
            me = api.FunctionInvocationEvaluator(expression=self.text)
            me.init(func_name, param_list=param_list)
            return ExpressionNode.finalize(me, evaluator)

        if self.node_type in ("AndExpression", "OrExpression"):
            me = getattr(api, self.node_type + "Evaluator")(
                self.terminal_node_text[0], expression=self.text
            )
            left_node = self.children[0].construct_evaluator(me)
            right_node = self.children[1].construct_evaluator(me)
            me.init(left_node, right_node)
            return ExpressionNode.finalize(me, evaluator)

        if self.node_type in ("EqualityExpression", "InequalityExpression"):
            me = getattr(api, self.node_type + "Evaluator")(
                self.terminal_node_text[0], expression=self.text
            )
            assert self.children[0].node_type == "TermExpression"
            left_node = ExpressionNode.parse_term_expression(self.children[0])
            right_node = ExpressionNode.parse_term_expression(self.children[1])
            me.init(left_node, right_node)
            return ExpressionNode.finalize(me, evaluator)

        if self.node_type in ("EqualityExpression", "InequalityExpression"):
            me = getattr(api, self.node_type + "Evaluator")(
                self.terminal_node_text[0], expression=self.text
            )
            assert self.children[0].node_type == "TermExpression"
            left_node = ExpressionNode.parse_term_expression(self.children[0])
            right_node = ExpressionNode.parse_term_expression(self.children[1])
            me.init(left_node, right_node)
            return ExpressionNode.finalize(me, evaluator)

    @staticmethod
    def parse_term_expression(term_node: "ExpressionNode"):
        """ """
        assert len(term_node.children) == 1
        child_term = term_node.children[0]
        if child_term.node_type == "MemberInvocation":
            assert child_term.children[0].node_type == "Identifier"
            val = api.MemberInvocationEvaluator(expression=child_term.text)
            val.init(child_term.children[0].terminal_node_text[0])
            return val
        if child_term.node_type == "LiteralTerm":
            if child_term.children[0].node_type == "QuantityLiteral":
                quantity_node = child_term.children[0].children[0]
                val = int(quantity_node.terminal_node_text[0])
                unit = quantity_node.children[0].children[0].terminal_node_text[0]
                return api.QuantityUnit(unit=unit, value=val)

            val = child_term.children[0].terminal_node_text[0]
            if child_term.children[0].node_type == "NumberLiteral":
                return "." in val and float(val) or int(val)
            if child_term.children[0].node_type == "StringLiteral":
                return ast.literal_eval(child_term.children[0].terminal_node_text[0])
            if child_term.children[0].node_type == "DateTimeLiteral":
                # stripping prefix @
                return parse_datetime(val[1:])
            if child_term.children[0].node_type == "DateLiteral":
                # stripping prefix @
                return parse_date(val[1:])
            if child_term.children[0].node_type == "TimeLiteral":
                # stripping prefix @T
                return parse_time(val[2:])
            if child_term.children[0].node_type == "NullLiteral":
                return api.NULL
            if child_term.children[0].node_type == "BooleanLiteral":
                return val == "true" and True or False
            raise ValueError("Unknown " + child_term.children[0].node_type)
        return ExpressionNode.parse_term_expression(child_term)

    @staticmethod
    def parse_function(function_node: "ExpressionNode"):
        """ """
        assert function_node.node_type == "Function"
        assert len(function_node.children) >= 1
        assert function_node.children[0].node_type == "Identifier"
        func_name = function_node.children[0].terminal_node_text[0]
        if len(function_node.children) == 1:
            return func_name, []
        param_list = []
        for node in function_node.children[1].children:
            if node.node_type in (
                "AndExpression",
                "OrExpression",
                "EqualityExpression",
                "InequalityExpression",
            ):
                param_list.append(node.construct_evaluator())
                continue
            raise ValueError
        return func_name, param_list

    @staticmethod
    def finalize(node: api.EvaluatorBase, parent: Optional[api.EvaluatorBase] = None):
        """ """
        if parent is None:
            return node
        parent.set_predecessor(node)
        return node


# important
ExpressionNode.update_forward_refs()
