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


def test_inequality_expression_le():
    """ """
    expression_node = compile_fhirpath_expression("meta.profile.count() <= 1")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is True
    assert val.value == [True]

    expression_node = compile_fhirpath_expression("extension[1].extension.count() <= 4")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is True
    assert val.value == [True]

    expression_node = compile_fhirpath_expression("id.count() <= 2")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is True


def test_inequality_expression_lt():
    """ """
    expression_node = compile_fhirpath_expression(
        "meta.profile.where(url='not_exists').count() < 1"
    )
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is True
    assert val.value == [True]

    expression_node = compile_fhirpath_expression("extension[1].extension.count() < 5")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is True
    assert val.value == [True]

    expression_node = compile_fhirpath_expression("id.count() < 2")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is True


def test_inequality_expression_ge():
    """ """
    expression_node = compile_fhirpath_expression("meta.profile.count() >= 1")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is True
    assert val.value == [True]

    expression_node = compile_fhirpath_expression("extension[1].extension.count() >= 4")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is True
    assert val.value == [True]

    expression_node = compile_fhirpath_expression("id.count() >= 2")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is False


def test_inequality_expression_gt():
    """ """
    expression_node = compile_fhirpath_expression("meta.profile.count() > 0")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is True
    assert val.value == [True]

    expression_node = compile_fhirpath_expression("extension[1].extension.count() > 2")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is True
    assert val.value == [True]

    expression_node = compile_fhirpath_expression("id.count() > 1")
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is False


def test_equality_expression_eq():
    """ """
    expression_node = compile_fhirpath_expression(
        "meta.profile = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient'"
    )
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is True
    assert val.value == [True]

    expression_node = compile_fhirpath_expression(
        "extension.url = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-race'"
    )
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is False
    assert val.value == [False]


def test_equality_expression_ne():
    """ """
    expression_node = compile_fhirpath_expression(
        "meta.profile != 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient'"
    )
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is False
    assert val.value == [False]

    expression_node = compile_fhirpath_expression(
        "extension.url != 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-race'"
    )
    evaluator = expression_node.construct_evaluator()
    val = evaluator.evaluate(US_PATIENT_1.dict())
    assert val.get_verdict() is True
    assert val.value == [True]
