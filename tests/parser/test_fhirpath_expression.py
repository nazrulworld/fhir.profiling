# _*_ coding: utf-8 _*_
from fhir.profiling.parser import compile_fhirpath_expression
import json
__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


def test_compile_fhirpath_expression():
    """Number of id elements (that would be 0 or 1 I guess)
    Lloyd McKenzie5:12 AM
In other words, an element must have actual 'content' - and the id for the element isn't considered to be 'content'.
     """
    # https: // docs.ehealth.sundhed.dk / latest - released / ig / StructureDefinition - ehealth - itcompetencelevel - definitions.html
    # (name.family.exists() or name.given.exists()) xor extension.where(url='http://hl7.org/fhir/StructureDefinition/data-absent-reason').exists()
    rstm = compile_fhirpath_expression(
        "(name.family.item[0] != 'KMP') xor extension.where(url='http://hl7.org/fhir/StructureDefinition/data-absent-reason').exists()"
    )
    rstm = compile_fhirpath_expression("(name.code = 'P' and name.system = 'https://../v3-MaritalStatus') or name.exits()")
    # hl7.org/fhir/us/core/StructureDefinition-us-core-patient.html
    {
        "children": [
            {
                "type": "OrExpression",
                "text": "hasValue()or(children().count()>id.count())",
                "terminalNodeText": ["or"],
                "children": [
                    {
                        "type": "TermExpression",
                        "text": "hasValue()",
                        "terminalNodeText": [],
                        "children": [
                            {
                                "type": "InvocationTerm",
                                "text": "hasValue()",
                                "terminalNodeText": [],
                                "children": [
                                    {
                                        "type": "FunctionInvocation",
                                        "text": "hasValue()",
                                        "terminalNodeText": [],
                                        "children": [
                                            {
                                                "type": "Function",
                                                "text": "hasValue()",
                                                "terminalNodeText": ["(", ")"],
                                                "children": [
                                                    {
                                                        "type": "Identifier",
                                                        "text": "hasValue",
                                                        "terminalNodeText": [
                                                            "hasValue"
                                                        ],
                                                    }
                                                ],
                                            }
                                        ],
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "type": "TermExpression",
                        "text": "(children().count()>id.count())",
                        "terminalNodeText": [],
                        "children": [
                            {
                                "type": "ParenthesizedTerm",
                                "text": "(children().count()>id.count())",
                                "terminalNodeText": ["(", ")"],
                                "children": [
                                    {
                                        "type": "InequalityExpression",
                                        "text": "children().count()>id.count()",
                                        "terminalNodeText": [">"],
                                        "children": [
                                            {
                                                "type": "InvocationExpression",
                                                "text": "children().count()",
                                                "terminalNodeText": ["."],
                                                "children": [
                                                    {
                                                        "type": "TermExpression",
                                                        "text": "children()",
                                                        "terminalNodeText": [],
                                                        "children": [
                                                            {
                                                                "type": "InvocationTerm",
                                                                "text": "children()",
                                                                "terminalNodeText": [],
                                                                "children": [
                                                                    {
                                                                        "type": "FunctionInvocation",
                                                                        "text": "children()",
                                                                        "terminalNodeText": [],
                                                                        "children": [
                                                                            {
                                                                                "type": "Function",
                                                                                "text": "children()",
                                                                                "terminalNodeText": [
                                                                                    "(",
                                                                                    ")",
                                                                                ],
                                                                                "children": [
                                                                                    {
                                                                                        "type": "Identifier",
                                                                                        "text": "children",
                                                                                        "terminalNodeText": [
                                                                                            "children"
                                                                                        ],
                                                                                    }
                                                                                ],
                                                                            }
                                                                        ],
                                                                    }
                                                                ],
                                                            }
                                                        ],
                                                    },
                                                    {
                                                        "type": "FunctionInvocation",
                                                        "text": "count()",
                                                        "terminalNodeText": [],
                                                        "children": [
                                                            {
                                                                "type": "Function",
                                                                "text": "count()",
                                                                "terminalNodeText": [
                                                                    "(",
                                                                    ")",
                                                                ],
                                                                "children": [
                                                                    {
                                                                        "type": "Identifier",
                                                                        "text": "count",
                                                                        "terminalNodeText": [
                                                                            "count"
                                                                        ],
                                                                    }
                                                                ],
                                                            }
                                                        ],
                                                    },
                                                ],
                                            },
                                            {
                                                "type": "InvocationExpression",
                                                "text": "id.count()",
                                                "terminalNodeText": ["."],
                                                "children": [
                                                    {
                                                        "type": "TermExpression",
                                                        "text": "id",
                                                        "terminalNodeText": [],
                                                        "children": [
                                                            {
                                                                "type": "InvocationTerm",
                                                                "text": "id",
                                                                "terminalNodeText": [],
                                                                "children": [
                                                                    {
                                                                        "type": "MemberInvocation",
                                                                        "text": "id",
                                                                        "terminalNodeText": [],
                                                                        "children": [
                                                                            {
                                                                                "type": "Identifier",
                                                                                "text": "id",
                                                                                "terminalNodeText": [
                                                                                    "id"
                                                                                ],
                                                                            }
                                                                        ],
                                                                    }
                                                                ],
                                                            }
                                                        ],
                                                    },
                                                    {
                                                        "type": "FunctionInvocation",
                                                        "text": "count()",
                                                        "terminalNodeText": [],
                                                        "children": [
                                                            {
                                                                "type": "Function",
                                                                "text": "count()",
                                                                "terminalNodeText": [
                                                                    "(",
                                                                    ")",
                                                                ],
                                                                "children": [
                                                                    {
                                                                        "type": "Identifier",
                                                                        "text": "count",
                                                                        "terminalNodeText": [
                                                                            "count"
                                                                        ],
                                                                    }
                                                                ],
                                                            }
                                                        ],
                                                    },
                                                ],
                                            },
                                        ],
                                    }
                                ],
                            }
                        ],
                    },
                ],
            }
        ]
    }
