"""Tests for the pytest-bdd step-skeleton backend."""

from __future__ import annotations

from pathlib import Path

from specweave.backends import BACKENDS, UNSUPPORTED_BACKENDS, get_backend
from specweave.backends.pytest_bdd import generate_pytest_bdd
from specweave.gherkin.parser import parse_feature
from specweave.translate.spec_to_code import bind_feature

FEATURE_TEXT = """Feature: Password login

  Scenario: Reject invalid password
    Given a registered user exists
    When the user submits an invalid password
    Then login is rejected
"""

RULE_FEATURE_TEXT = """@task-0123
Feature: Task lifecycle gates

  @rule-0001
  Rule: Implementation requires an accepted plan

    @bdd-0001 @task-0123 @rule-0001 @ac-0001
    Scenario: Agent cannot start implementation without an accepted plan
      Given a task has a proposed plan
      When the agent starts implementation
      Then taskledger rejects the transition
"""


def _feature_path(tmp_path: Path, text: str, name: str = "test.feature") -> Path:  # type: ignore[no-untyped-def]
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


# sw: f=specs/behavior/features/backends/pytest-bdd.feature
# sw: s=@bdd-backend-registry
def test_backend_registry_contents() -> None:
    assert "behave" in BACKENDS
    assert "pytest-bdd" in BACKENDS
    assert get_backend("pytest-bdd") is generate_pytest_bdd


# sw: f=specs/behavior/features/backends/pytest-bdd.feature
# sw: s=@bdd-backend-unsupported
def test_unsupported_cucumber_backends_message() -> None:
    assert "cucumber-js" in UNSUPPORTED_BACKENDS
    assert "cucumber-jvm" in UNSUPPORTED_BACKENDS
    for name in UNSUPPORTED_BACKENDS:
        try:
            get_backend(name)
        except ValueError as exc:
            assert "not yet supported" in str(exc), name
        else:  # pragma: no cover - defensive
            raise AssertionError(f"expected ValueError for {name}")


# sw: f=specs/behavior/features/backends/pytest-bdd.feature
# sw: s=@bdd-backend-pytest-bdd-skeleton
def test_pytest_bdd_skeleton_shape(tmp_path) -> None:  # type: ignore[no-untyped-def]
    feature_path = _feature_path(tmp_path, FEATURE_TEXT)
    feature = parse_feature(feature_path.read_text(encoding="utf-8"))
    skeleton = generate_pytest_bdd(feature)
    assert "from pytest_bdd import" in skeleton
    assert "parsers" in skeleton
    assert "scenarios(" in skeleton
    # source_path is None -> filename derived from feature title.
    assert 'scenarios("password_login.feature")' in skeleton
    assert (
        '@given(parsers.parse("a registered user exists"), target_fixture=' in skeleton
    )
    assert '@when(parsers.parse("the user submits an invalid password")' in skeleton
    assert '@then(parsers.parse("login is rejected")' in skeleton
    assert "raise NotImplementedError" in skeleton


# sw: f=specs/behavior/features/backends/pytest-bdd.feature
# sw: s=@bdd-backend-pytest-bdd-dedup
def test_pytest_bdd_dedups_repeated_steps(tmp_path) -> None:  # type: ignore[no-untyped-def]
    text = """Feature: Dedup
  Scenario: S
    Given a user
    And a user
    When the user acts
    Then it works
"""
    feature = parse_feature(_feature_path(tmp_path, text).read_text(encoding="utf-8"))
    skeleton = generate_pytest_bdd(feature)
    # "a user" appears once in skeleton despite And/Given duplication.
    assert skeleton.count('parsers.parse("a user")') == 1


# sw: f=specs/behavior/features/backends/pytest-bdd.feature
# sw: s=@bdd-backend-pytest-bdd-rule-scenarios
def test_pytest_bdd_collects_rule_scenarios(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Steps inside Rule: blocks are bound by the pytest-bdd backend."""
    feature = parse_feature(
        _feature_path(tmp_path, RULE_FEATURE_TEXT, name="lifecycle.feature").read_text(
            encoding="utf-8"
        )
    )
    skeleton = generate_pytest_bdd(feature)
    assert 'parsers.parse("a task has a proposed plan")' in skeleton
    assert 'parsers.parse("the agent starts implementation")' in skeleton
    assert 'parsers.parse("taskledger rejects the transition")' in skeleton


# sw: f=specs/behavior/features/translation/spec-to-code.feature
# sw: s=@bdd-spec-to-code-bind-pytest-bdd
def test_bind_feature_writes_pytest_bdd_file(tmp_path) -> None:  # type: ignore[no-untyped-def]
    feature_path = _feature_path(tmp_path, FEATURE_TEXT)
    out_dir = tmp_path / "steps"
    bind_feature(feature_path, "pytest-bdd", out_dir)
    step_file = out_dir / "test_steps.py"
    assert step_file.exists()
    content = step_file.read_text(encoding="utf-8")
    assert "from pytest_bdd import" in content
    assert "@when(parsers.parse" in content


# sw: f=specs/behavior/features/backends/pytest-bdd.feature
# sw: s=@bdd-backend-pytest-bdd-source-path
def test_pytest_bdd_uses_source_path_filename(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """When source_path is set, scenarios() references that filename."""
    feature_path = _feature_path(tmp_path, FEATURE_TEXT, name="custom-name.feature")
    feature = parse_feature(feature_path.read_text(encoding="utf-8"))
    feature = _with_source_path(feature, feature_path)
    skeleton = generate_pytest_bdd(feature)
    assert 'scenarios("custom-name.feature")' in skeleton


def _with_source_path(feature, path: Path):  # type: ignore[no-untyped-def]
    from dataclasses import replace

    return replace(feature, source_path=path)
