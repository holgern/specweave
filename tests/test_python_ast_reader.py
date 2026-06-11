"""Tests for AST-based Python test inspection."""

from __future__ import annotations

import tempfile
from pathlib import Path

from specweave.python_inspect.assertions import describe_assert
from specweave.python_inspect.ast_reader import (
    collect_pytest_tests,
    discover_pytest_tests,
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


# sw: f=specs/behavior/features/python-inspect/ast-reader.feature
# sw: s=@bdd-ast-extract-test-functions
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


# sw: f=specs/behavior/features/python-inspect/ast-reader.feature
# sw: s=@bdd-ast-ignores-non-test
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


# sw: f=specs/behavior/features/python-inspect/ast-reader.feature
# sw: s=@bdd-ast-assert-equals
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


# sw: f=specs/behavior/features/python-inspect/ast-reader.feature
# sw: s=@bdd-ast-assert-is-none
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


# sw: f=specs/behavior/features/python-inspect/ast-reader.feature
# sw: s=@bdd-ast-assert-truthy
def test_describe_assert_truthy() -> None:
    """assert x becomes 'x is truthy'."""
    import ast

    tree = ast.parse("assert user")
    node = tree.body[0]
    assert isinstance(node, ast.Assert)
    result = describe_assert(node)
    assert result == "user is truthy"


# sw: f=specs/behavior/features/python-inspect/ast-reader.feature
# sw: s=@bdd-ast-assert-call
def test_describe_assert_call() -> None:
    """assert func() becomes 'func succeeds'."""
    import ast

    tree = ast.parse("assert validate_token(token)")
    node = tree.body[0]
    assert isinstance(node, ast.Assert)
    result = describe_assert(node)
    assert result is not None
    assert "succeeds" in result


# sw: f=specs/behavior/features/python-inspect/ast-reader.feature
# sw: s=@bdd-ast-discover-marker
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


# sw: f=specs/behavior/features/python-inspect/ast-reader.feature
# sw: s=@bdd-ast-discover-comment
def test_discover_specweave_comment_mapping() -> None:
    code = """
# sw: f=specs/behavior/features/sync/git-sync.feature
# sw: s=@bdd-imports-pytest-report
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


def test_discover_specweave_short_comment_mapping() -> None:
    code = """
# sw: f=specs/behavior/features/sync/git-sync.feature
# sw: s=@bdd-imports-pytest-report
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


def test_discover_specweave_block_comment_mapping() -> None:
    code = """
# specweave:
#   feature: specs/behavior/features/sync/git-sync.feature
#   scenario: @bdd-imports-pytest-report
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


def test_discover_specweave_requirement_comment_mapping() -> None:
    code = """
# specweave:
#   spec: specs/specifications/capabilities/coverage.spec.md
#   requirement: REQ-COV-001
def test_reports_bidirectional_coverage():
    pass
"""
    path = _write_test_file(code)
    try:
        mappings = discover_specweave_tests(path)
        assert len(mappings) == 1
        mapping = mappings[0]
        assert mapping.spec == "specs/specifications/capabilities/coverage.spec.md"
        assert mapping.requirement == "REQ-COV-001"
        assert mapping.feature is None
        assert mapping.scenario is None
        assert mapping.source == "comment"
    finally:
        path.unlink()


def test_discover_specweave_marker_requirement_mapping() -> None:
    code = """
import pytest

SPEC_PATH = "specs/specifications/capabilities/coverage.spec.md"


@pytest.mark.specweave(
    spec=SPEC_PATH,
    requirement="REQ-COV-001",
)
def test_reports_bidirectional_coverage():
    pass
"""
    path = _write_test_file(code)
    try:
        mappings = discover_specweave_tests(path)
        assert len(mappings) == 1
        mapping = mappings[0]
        assert mapping.spec == "specs/specifications/capabilities/coverage.spec.md"
        assert mapping.requirement == "REQ-COV-001"
        assert mapping.source == "marker"
    finally:
        path.unlink()


def test_one_test_can_map_to_bdd_and_sdd() -> None:
    code = """
# specweave:
#   feature: specs/behavior/features/sync/git-sync.feature
#   scenario: @bdd-imports-pytest-report
#   spec: specs/specifications/capabilities/coverage.spec.md
#   requirement: REQ-COV-001
def test_imports_pytest_report():
    pass
"""
    path = _write_test_file(code)
    try:
        mappings = discover_specweave_tests(path)
        assert len(mappings) == 2
        bdd_mapping = next(
            mapping for mapping in mappings if mapping.feature is not None
        )
        sdd_mapping = next(mapping for mapping in mappings if mapping.spec is not None)
        assert bdd_mapping.scenario == "@bdd-imports-pytest-report"
        assert sdd_mapping.requirement == "REQ-COV-001"
    finally:
        path.unlink()


# sw: f=specs/behavior/features/python-inspect/ast-reader.feature
# sw: s=@bdd-ast-discover-docstring
def test_docstring_mapping_accepts_feature_md(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    feature_path = (
        tmp_path / "specs" / "behavior" / "features" / "auth" / "login.feature"
    )
    feature_path.parent.mkdir(parents=True, exist_ok=True)
    feature_path.write_text("# Feature: Login\n", encoding="utf-8")
    code = """
def test_rejects_invalid_password():
    \"\"\"
    SpecWeave mapping:
    specs/behavior/features/auth/login.feature
    @bdd-login-rejects-invalid-password
    \"\"\"
    pass
"""
    path = _write_test_file(code)
    try:
        mappings = discover_specweave_tests(path)
        assert len(mappings) == 1
        mapping = mappings[0]
        assert mapping.feature == "specs/behavior/features/auth/login.feature"
        assert mapping.scenario == "@bdd-login-rejects-invalid-password"
        assert mapping.source == "docstring"
    finally:
        path.unlink()


def test_discover_pytest_tests_lists_all_test_functions(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "tests" / "test_auth_login.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """
def helper() -> None:
    pass


def test_valid_login() -> None:
    pass


async def test_reject_invalid_password() -> None:
    pass
""",
        encoding="utf-8",
    )

    items = discover_pytest_tests(path)

    assert [item.function_name for item in items] == [
        "test_valid_login",
        "test_reject_invalid_password",
    ]
    assert [item.nodeid for item in items] == [
        "tests/test_auth_login.py::test_valid_login",
        "tests/test_auth_login.py::test_reject_invalid_password",
    ]


def test_collect_pytest_tests_keeps_unmapped_tests(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    first = tmp_path / "tests" / "test_auth_login.py"
    second = tmp_path / "tests" / "test_config.py"
    first.parent.mkdir(parents=True, exist_ok=True)
    first.write_text(
        """
# sw: f=specs/behavior/features/auth/login.feature
# sw: s=@bdd-login-valid
def test_valid_login() -> None:
    pass
""",
        encoding="utf-8",
    )
    second.write_text(
        """
def test_loads_hidden_config() -> None:
    pass
""",
        encoding="utf-8",
    )

    items = collect_pytest_tests([first, second])

    assert [item.nodeid for item in items] == [
        "tests/test_auth_login.py::test_valid_login",
        "tests/test_config.py::test_loads_hidden_config",
    ]


def test_discover_specweave_tests_qualifies_class_mapping_nodeids(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "tests" / "test_auth_login.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '''
import pytest


class TestLogin:
    # sw: f=specs/behavior/features/auth/login.feature
    # sw: s=@bdd-login-valid
    def test_valid_login(self) -> None:
        pass

    @pytest.mark.specweave(
        feature="specs/behavior/features/auth/login.feature",
        scenario="@bdd-login-marker",
    )
    async def test_marker_mapping(self) -> None:
        pass

    def test_docstring_mapping(self) -> None:
        """
        specs/behavior/features/auth/login.feature
        @bdd-login-docstring
        """
        pass


def test_top_level_mapping() -> None:
    """
    specs/behavior/features/auth/login.feature
    @bdd-login-top-level
    """
    pass
''',
        encoding="utf-8",
    )

    mappings = discover_specweave_tests(path)

    assert [mapping.nodeid for mapping in mappings] == [
        "tests/test_auth_login.py::TestLogin::test_valid_login",
        "tests/test_auth_login.py::TestLogin::test_marker_mapping",
        "tests/test_auth_login.py::TestLogin::test_docstring_mapping",
        "tests/test_auth_login.py::test_top_level_mapping",
    ]
    assert [mapping.source for mapping in mappings] == [
        "comment",
        "marker",
        "docstring",
        "docstring",
    ]


def test_pytest_discovery_ignores_non_collectible_class_nesting(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "tests" / "test_auth_login.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """
class LoginTests:
    def test_not_collectible(self) -> None:
        pass


class TestLogin:
    class TestNested:
        def test_not_collectible(self) -> None:
            pass

    def test_collectible(self) -> None:
        pass
""",
        encoding="utf-8",
    )

    assert [item.nodeid for item in discover_pytest_tests(path)] == [
        "tests/test_auth_login.py::TestLogin::test_collectible"
    ]


# sw: f=specs/behavior/features/python-inspect/ast-reader.feature
# sw: s=@bdd-ast-discover-intentional-unmapped-waiver
def test_discover_pytest_tests_preserves_intentional_unmapped_waiver() -> None:
    code = """
# sw: unmapped=parser unit edge case; no behavior scenario
@pytest.mark.parametrize("value", ["a", "b"])
def test_parser_edge_case(value):
    pass
"""
    path = _write_test_file(code)
    try:
        items = discover_pytest_tests(path)
        assert len(items) == 1
        assert items[0].unmapped_reason == "parser unit edge case; no behavior scenario"
        assert items[0].unmapped_source == "comment"
    finally:
        path.unlink()
