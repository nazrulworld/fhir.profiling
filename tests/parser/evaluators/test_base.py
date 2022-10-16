# _*_ coding: utf-8 _*_
import pytest
from fhir.profiling.parser.evaluators import base
from fhir.profiling.parser import compile_fhirpath_expression
__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


def test_evaluation():
    """ """
    evaluation = base.Evaluation(True)
    assert bool(evaluation) is True
    assert evaluation.get_verdict() is True
    assert evaluation.value[0] is True

    evaluation = base.Evaluation(False)
    assert bool(evaluation) is False
    assert evaluation.get_verdict() is False
    assert evaluation.value[0] is False

    evaluation = base.Evaluation(0)
    assert evaluation.get_verdict() is True
    assert evaluation.value[0] == 0

    evaluation = base.Evaluation([])
    assert evaluation.get_verdict() is False

    evaluation = base.Evaluation(["some value"])
    assert evaluation.get_verdict() is True


def test_member_invocation_evaluator():
    """ """
    expression = "contained.all($this.is(%Patient) implies age > 10)"
    expression_node = compile_fhirpath_expression(expression)

