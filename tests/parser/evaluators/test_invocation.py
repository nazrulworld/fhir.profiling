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
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is True
    assert val.value[0] is True

    expression_node = compile_fhirpath_expression("text.status")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.value[0] == "generated"
    assert val.get_verdict() is True

    # Test with error handling
    expression_node = compile_fhirpath_expression("text.unknown")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is False
    assert len(val.value) == 0
