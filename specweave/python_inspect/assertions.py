"""Convert simple Python assertions into candidate Gherkin clauses."""

from __future__ import annotations

import ast


def describe_assert(node: ast.Assert) -> str | None:
    """Convert an ``assert`` statement into a candidate ``Then`` clause.

    Returns a short human-readable string, or ``None`` if the assertion
    pattern is not recognised.
    """
    test = node.test

    # Simple comparison: assert a == b  ->  "a equals b"
    if isinstance(test, ast.Compare) and len(test.ops) == 1:
        left = _expr_to_simple(test.left)
        right = _expr_to_simple(test.comparators[0])
        op = _op_name(test.ops[0])
        if left and right:
            return f"{left} {op} {right}"

    # Simple bool: assert <name>
    if isinstance(test, ast.Name):
        return f"{test.id} is truthy"

    # assert not <name>
    if (
        isinstance(test, ast.UnaryOp)
        and isinstance(test.op, ast.Not)
        and isinstance(test.operand, ast.Name)
    ):
        return f"{test.operand.id} is falsy"

    # assert call(args)
    if isinstance(test, ast.Call):
        func = _expr_to_simple(test.func)
        if func:
            return f"{func} succeeds"

    return None


def _op_name(op: ast.cmpop) -> str:
    """Return a human-readable name for a comparison operator."""
    mapping: dict[type, str] = {
        ast.Eq: "equals",
        ast.NotEq: "does not equal",
        ast.Lt: "is less than",
        ast.LtE: "is at most",
        ast.Gt: "is greater than",
        ast.GtE: "is at least",
        ast.Is: "is",
        ast.IsNot: "is not",
        ast.In: "is in",
        ast.NotIn: "is not in",
    }
    return mapping.get(type(op), repr(op))


def _expr_to_simple(node: ast.expr) -> str | None:
    """Convert a simple expression to a short string.

    Handles ``ast.Name``, ``ast.Attribute``, and ``ast.Constant``.
    """
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        val = _expr_to_simple(node.value)
        return val + "." + node.attr if val else None
    if isinstance(node, ast.Constant):
        if node.value is None:
            return "None"
        return repr(node.value)
    return None
