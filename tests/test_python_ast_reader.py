"""Tests for AST-based Python test inspection."""

from __future__ import annotations

import tempfile
from pathlib import Path

from specweave.python_inspect.assertions import describe_assert
from specweave.python_inspect.ast_reader import (
    discover_specweave_tests,
    extract_test_scenarios,
)


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


def test_discover_specweave_marker_mapping() -> None:
    code = """
import pytest

SPECWEAVE_FEATURE = "specs/behavior/features/task-management/plan-gates.feature"


@pytest.mark.specweave(
    feature=SPECWEAVE_FEATURE,
    scenario="@bdd-implementation-blocked-before-plan-acceptance",
)
def test_agent_cannot_start_implementation_before_plan_approval():
    pass
"""
    path = _write_test_file(code)
    try:
        mappings = discover_specweave_tests(path)
        assert len(mappings) == 1
        mapping = mappings[0]
        assert mapping.feature.endswith("plan-gates.feature")
        assert mapping.scenario == "@bdd-implementation-blocked-before-plan-acceptance"
        assert mapping.source == "marker"
    finally:
        path.unlink()


def test_discover_specweave_comment_mapping() -> None:
    code = """
# specweave: feature=specs/behavior/features/sync/git-sync.feature
# specweave: scenario=@bdd-imports-pytest-report
def test_imports_pytest_report():
    pass
"""
    path = _write_test_file(code)
    try:
        mappings = discover_specweave_tests(path)
        assert len(mappings) == 1
        mapping = mappings[0]
        assert mapping.feature.endswith("git-sync.feature")
        assert mapping.scenario == "@bdd-imports-pytest-report"
        assert mapping.source == "comment"
    finally:
        path.unlink()


def test_docstring_mapping_accepts_feature_md(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    feature_path = (
        tmp_path / "specs" / "behavior" / "features" / "auth" / "login.feature.md"
    )
    feature_path.parent.mkdir(parents=True, exist_ok=True)
    feature_path.write_text("# Feature: Login\n", encoding="utf-8")
    code = """
def test_rejects_invalid_password():
    \"\"\"
    SpecWeave mapping:
    specs/behavior/features/auth/login.feature.md
    @bdd-login-rejects-invalid-password
    \"\"\"
    pass
"""
    path = _write_test_file(code)
    try:
        mappings = discover_specweave_tests(path)
        assert len(mappings) == 1
        mapping = mappings[0]
        assert mapping.feature == "specs/behavior/features/auth/login.feature.md"
        assert mapping.scenario == "@bdd-login-rejects-invalid-password"
        assert mapping.source == "docstring"
    finally:
        path.unlink()
