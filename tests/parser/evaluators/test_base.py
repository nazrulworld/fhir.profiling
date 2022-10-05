# _*_ coding: utf-8 _*_
import pytest
from fhir.profiling.parser.evaluators import base
from fhir.profiling.parser import compile_fhirpath_expression
__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


def test_evaluation():
    """ """
    evaluation = base.Evaluation()
    assert bool(evaluation) is True
    assert evaluation.has_error() is False
    with pytest.raises(TypeError) as excinfo:
        evaluation.error = "some value"
    assert str(excinfo.value) == "Readonly object!"

    evaluation = base.Evaluation(error=base.EMPTY)
    assert evaluation.get_verdict() is False
    assert evaluation.has_error() is False


def test_valued_evaluation():
    """ """
    evaluation = base.ValuedEvaluation("Hello")
    assert evaluation.has_error() is False
    assert evaluation.get_verdict() == "Hello"

    evaluation = base.ValuedEvaluation(
        value=base.EMPTY, error=base.EvaluationError(None, "fake.id")
    )
    assert evaluation.has_error() is True
    with pytest.raises(ValueError) as exc:
        evaluation.get_verdict(raise_on_error=True)


def test_member_invocation_evaluator():
    """ """
    expression = "gender.exist()"
    expression_node = compile_fhirpath_expression(expression)

