"""Tests for AST-based Python test inspection."""

from __future__ import annotations

import tempfile
from pathlib import Path

from specweave.python_inspect.assertions import describe_assert
from specweave.python_inspect.ast_reader import extract_test_scenarios


def _write_test_file(content: str) -> Path:
    """Write a temporary Python file and return its path."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    )
    tmp.write(content)
    tmp.close()
    return Path(tmp.name)


def test_extract_test_functions() -> None:
    """AST reader finds test_* functions."""
    code = """
def test_rejects_invalid_password():
    response = login("bad")
    assert response.status_code == 401
    assert response.session is None
"""
    path = _write_test_file(code)
    try:
        scenarios = extract_test_scenarios(path)
        assert len(scenarios) == 1
        scenario = scenarios[0]
        assert "Rejects Invalid Password" in scenario.title
        assert len(scenario.steps) >= 2  # at least When + Then
    finally:
        path.unlink()


def test_extract_ignores_non_test_functions() -> None:
    """Non test_* functions are ignored."""
    code = """
def helper():
    pass
"""
    path = _write_test_file(code)
    try:
        scenarios = extract_test_scenarios(path)
        assert len(scenarios) == 0
    finally:
        path.unlink()


def test_describe_assert_equals() -> None:
    """assert a == b becomes 'a equals b'."""
    import ast

    tree = ast.parse("assert x == 42")
    node = tree.body[0]
    assert isinstance(node, ast.Assert)
    result = describe_assert(node)
    assert result is not None
    assert "x" in result
    assert "equals" in result
    assert "42" in result


def test_describe_assert_is_none() -> None:
    """assert x is None becomes 'x is None'."""
    import ast

    tree = ast.parse("assert session is None")
    node = tree.body[0]
    assert isinstance(node, ast.Assert)
    result = describe_assert(node)
    assert result is not None
    assert "session" in result
    assert "is" in result
    assert "None" in result


def test_describe_assert_truthy() -> None:
    """assert x becomes 'x is truthy'."""
    import ast

    tree = ast.parse("assert user")
    node = tree.body[0]
    assert isinstance(node, ast.Assert)
    result = describe_assert(node)
    assert result == "user is truthy"


def test_describe_assert_call() -> None:
    """assert func() becomes 'func succeeds'."""
    import ast

    tree = ast.parse("assert validate_token(token)")
    node = tree.body[0]
    assert isinstance(node, ast.Assert)
    result = describe_assert(node)
    assert result is not None
    assert "succeeds" in result
