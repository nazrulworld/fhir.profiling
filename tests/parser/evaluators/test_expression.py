from fhir.profiling.parser import compile_fhirpath_expression
from fhir.resources.patient import Patient
from tests.fixtures import STATIC_US_DIR

__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"

US_PATIENT_1 = Patient.parse_file(STATIC_US_DIR / "Patient-example.json")


def test_indexer_expression():
    """ """
    expression_node = compile_fhirpath_expression("name[1]")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.value[0]["family"] == "Baxter"
    assert val.value[0]["given"] == ["Amy", "V."]

    expression_node = compile_fhirpath_expression("name[8]")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.value == []

    expression_node = compile_fhirpath_expression("non_field[8]")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.value == []


def test_or_expression():
    """ """
    expression_node = compile_fhirpath_expression(
        "active=false or meta.profile='http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient'"
    )
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is True
    assert val.value == [True]


def test_and_expression():
    """ """
    expression_node = compile_fhirpath_expression(
        "active=false and meta.profile='http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient'"
    )
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is False
    assert val.value == [False]

    expression_node = compile_fhirpath_expression(
        "active=true and meta.profile='http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient'"
    )
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is True
    assert val.value == [True]
