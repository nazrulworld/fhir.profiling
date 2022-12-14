# _*_ coding: utf-8 _*_
from fhir.profiling.parser.node import ExpressionNode
from fhir.profiling.parser import compile_fhirpath_expression
from fhir.profiling.parser.evaluators import api
from fhir.profiling.parser.evaluators.base import QuantityUnit
import datetime

__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


def test_parse_term_expression():
    """ """
    node = compile_fhirpath_expression("name")
    val = ExpressionNode.parse_term_expression(node)
    assert isinstance(val, api.MemberInvocationEvaluator)
    assert val.get_nodes().left == "name"

    node = compile_fhirpath_expression("code.where(url='https://heart.dk')")
    val = ExpressionNode.parse_term_expression(node.children[0])
    assert val.get_nodes().left == "code"

    params_list = node.children[1].children[0].children[1].children[0]
    val = ExpressionNode.parse_term_expression(params_list.children[0])
    assert val.get_nodes().left == "url"
    val = ExpressionNode.parse_term_expression(params_list.children[1])
    assert val == "https://heart.dk"


def test_parse_function():
    """contained.where((('#'+id in (%resource.descendants().reference | %resource.descendants().as(canonical) | %resource.descendants().as(uri) | %resource.descendants().as(url))) or descendants().where(reference = '#').exists() or descendants().where(as(canonical) = '#').exists() or descendants().where(as(canonical) = '#').exists()).not()).trace('unmatched', id).empty()
    maritalStatus.coding.where(code = 'P' and system = 'http://terminology.hl7.org/CodeSystem/v3-MaritalStatus').empty() or maritalStatus.coding.where(code = 'A' and system = 'http://terminology.hl7.org/CodeSystem/v3-MaritalStatus').empty()"""
    # Tests StringLiteral
    func_node = compile_fhirpath_expression(
        "code.where(url='https://heart.dk')"
    ).children[1]
    func_name, param_list = ExpressionNode.parse_function(func_node.children[0])
    assert func_name == "where"
    assert len(param_list) == 1
    func_evaluator: api.EqualityExpressionEvaluation = param_list[0]
    assert func_evaluator.get_type() == "EqualityExpression"
    nodes = func_evaluator.get_nodes()
    assert isinstance(nodes.left, api.MemberInvocationEvaluator)
    assert nodes.left.get_nodes().left == "url"
    assert nodes.right == "https://heart.dk"
    # StringLiteral tests end
    # Test NumberLiteral
    func_node = compile_fhirpath_expression("code.where(size=81)").children[1]
    func_name, param_list = ExpressionNode.parse_function(func_node.children[0])
    assert param_list[0].get_nodes().right == 81
    assert isinstance(param_list[0].get_nodes().right, int) is True
    func_node = compile_fhirpath_expression("code.where(size=81.54)").children[1]
    func_name, param_list = ExpressionNode.parse_function(func_node.children[0])
    assert param_list[0].get_nodes().right == 81.54
    assert isinstance(param_list[0].get_nodes().right, float) is True
    # NumberLiteral tests end
    # Tests BooleanLiteral
    func_node = compile_fhirpath_expression("code.where(active=false)").children[1]
    func_name, param_list = ExpressionNode.parse_function(func_node.children[0])
    assert param_list[0].get_nodes().right is False
    func_node = compile_fhirpath_expression("code.where(active=true)").children[1]
    func_name, param_list = ExpressionNode.parse_function(func_node.children[0])
    assert param_list[0].get_nodes().right is True
    # BooleanLiteral tests end
    # Tests DateTimeLiteral
    func_node = compile_fhirpath_expression(
        "code.where(created>@2010-09-11T12:21:00+01:00)"
    ).children[1]
    func_name, param_list = ExpressionNode.parse_function(func_node.children[0])
    assert param_list[0].get_type() == "InequalityExpression"
    assert isinstance(param_list[0].get_nodes().right, datetime.datetime)

    func_node = compile_fhirpath_expression(
        "code.where(created <= @2010-09-11T12:21:00)"
    ).children[1]
    func_name, param_list = ExpressionNode.parse_function(func_node.children[0])
    assert param_list[0].get_type() == "InequalityExpression"
    assert isinstance(param_list[0].get_nodes().right, datetime.datetime)
    # DateTimeLiteral tests end
    # Tests DateLiteral
    func_node = compile_fhirpath_expression("code.where(created>@2010-09-11)").children[
        1
    ]
    func_name, param_list = ExpressionNode.parse_function(func_node.children[0])
    assert param_list[0].get_type() == "InequalityExpression"
    assert isinstance(param_list[0].get_nodes().right, datetime.date)
    # DateLiteral tests end
    # Tests TimeLiteral
    func_node = compile_fhirpath_expression("code.where(created=@T13:01:05)").children[
        1
    ]
    func_name, param_list = ExpressionNode.parse_function(func_node.children[0])
    assert param_list[0].get_type() == "EqualityExpression"
    assert isinstance(param_list[0].get_nodes().right, datetime.time)
    # TimeLiteral tests end
    # Tests QuantityLiteral
    func_node = compile_fhirpath_expression("code.where(since = 4 days)").children[1]
    func_name, param_list = ExpressionNode.parse_function(func_node.children[0])
    assert param_list[0].get_type() == "EqualityExpression"
    assert isinstance(param_list[0].get_nodes().right, QuantityUnit)
    assert param_list[0].get_nodes().right.value == 4
    # TimeLiteral tests end
    # Tests QuantityLiteral
    func_node = compile_fhirpath_expression("code.where(since = 4 days)").children[1]
    func_name, param_list = ExpressionNode.parse_function(func_node.children[0])
    assert param_list[0].get_type() == "EqualityExpression"
    assert isinstance(param_list[0].get_nodes().right, api.QuantityUnit)
    assert param_list[0].get_nodes().right.value == 4
    # QuantityLiteral tests end
    # Tests NullLiteral
    func_node = compile_fhirpath_expression("code.where(name = {})").children[1]
    func_name, param_list = ExpressionNode.parse_function(func_node.children[0])
    assert param_list[0].get_type() == "EqualityExpression"
    assert isinstance(param_list[0].get_nodes().right, type(api.NULL))
    # NullLiteral tests end


def test_parse_function_with_join():
    """ """
    func_node = compile_fhirpath_expression(
        "coding.where(code = 'P' and system = 'https://../v3-MaritalStatus')"
    ).children[1]
    func_name, param_list = ExpressionNode.parse_function(func_node.children[0])
    assert func_name == "where"
    assert len(param_list) == 1
    assert isinstance(param_list[0], api.AndExpressionEvaluator)
    and_expression: api.AndExpressionEvaluator = param_list[0]
    nodes = and_expression.get_nodes()
    assert isinstance(nodes.left, api.EqualityExpressionEvaluator)
    assert isinstance(nodes.right, api.EqualityExpressionEvaluator)
    assert nodes.left.get_expression() == "code='P'"
    assert nodes.right.get_expression() == "system='https://../v3-MaritalStatus'"
    nodes_left_nodes = nodes.left.get_nodes()
    nodes_right_nodes = nodes.right.get_nodes()
    isinstance(nodes_left_nodes.left, api.MemberInvocationEvaluator)
    assert nodes_left_nodes.left.get_nodes().left == "code"
    assert nodes_left_nodes.right == "P"

    isinstance(nodes_right_nodes.left, api.MemberInvocationEvaluator)
    assert nodes_right_nodes.left.get_nodes().left == "system"
    assert nodes_right_nodes.right == "https://../v3-MaritalStatus"


def test_construct_evaluator_from_invocation_expression():
    """ """
    invocation_expression_node = compile_fhirpath_expression(
        "code.coding.where(code = 'P' and system = 'https://../v3-MaritalStatus').exists()"
    )
    invocation_expression_evaluator = invocation_expression_node.construct_evaluator()
    assert (
        invocation_expression_evaluator.get_expression()
        == "code.coding.where(code='P'andsystem='https://../v3-MaritalStatus').exists()"
    )
    main_nodes = invocation_expression_evaluator.get_nodes()
    assert isinstance(main_nodes.right, api.FunctionInvocationEvaluator)
    assert main_nodes.right.get_expression() == "exists()"
    assert isinstance(main_nodes.left, api.InvocationExpressionEvaluator)

    assert (
        main_nodes.left.get_expression()
        == "code.coding.where(code='P'andsystem='https://../v3-MaritalStatus')"
    )
    nodes_1 = main_nodes.left.get_nodes()
    assert nodes_1.right.get_type() == "FunctionInvocation"
    assert (
        nodes_1.right.get_expression()
        == "where(code='P'andsystem='https://../v3-MaritalStatus')"
    )
    assert nodes_1.left.get_type() == "InvocationExpression"
    nodes_1_1 = nodes_1.left.get_nodes()
    assert isinstance(nodes_1_1.left, api.MemberInvocationEvaluator)
    assert isinstance(nodes_1_1.right, api.MemberInvocationEvaluator)
    assert nodes_1_1.left.get_nodes().left == "code"
    assert nodes_1_1.right.get_nodes().left == "coding"


def test_construct_evaluator_from_indexer_expression():
    """ """
    expression_node = compile_fhirpath_expression("name[1]")
    nodes = expression_node.construct_evaluator().get_nodes()
    assert nodes.right == 1
    assert isinstance(nodes.left, api.MemberInvocationEvaluator)
