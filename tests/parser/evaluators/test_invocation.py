# _*_ coding: utf-8 _*_
from fhir.profiling.parser.evaluators import api
from fhir.profiling.parser import compile_fhirpath_expression
from fhir.resources.patient import Patient
from tests.fixtures import STATIC_US_DIR

__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"

US_PATIENT_1 = Patient.parse_file(STATIC_US_DIR / "Patient-example.json")


def test_member_invocation():
    """ """
    expression_node = compile_fhirpath_expression("active")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1)
    assert val.get_verdict() is True

    expression_node = compile_fhirpath_expression("text.status")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1)
    assert val.get_verdict() == "generated"

    # Test with error handling
    expression_node = compile_fhirpath_expression("text.unknown")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1)
    assert val.has_error() is True
    assert isinstance(val.error, api.EvaluationError)
    assert val.error.expression == "text.unknown"
