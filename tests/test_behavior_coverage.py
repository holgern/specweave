"""Tests for explicit behavior coverage reporting."""

from __future__ import annotations

from pathlib import Path

from specweave.behavior.coverage import build_behavior_coverage
from specweave.gherkin.model import Feature, Scenario, Step
from specweave.gherkin.writer import write_feature

FEATURE = "specs/behavior/features/behavior/coverage.feature"


def _write_behavior_feature(
    path: Path,
    *,
    title: str,
    scenario_id: str,
    scenario_title: str,
    tags: tuple[str, ...] = (),
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    feature = Feature(
        title=title,
        scenarios=(
            Scenario(
                title=scenario_title,
                keyword="Example",
                tags=(scenario_id.removeprefix("@"),) + tags,
                steps=(
                    Step(keyword="Given", text="a registered user exists"),
                    Step(keyword="When", text="the user submits credentials"),
                    Step(keyword="Then", text="the outcome is recorded"),
                ),
            ),
        ),
    )
    path.write_text(write_feature(feature), encoding="utf-8")
    return path


def _write_test(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


# specweave: feature=specs/behavior/features/behavior/coverage.feature
# specweave: scenario=@bdd-coverage-bound-scenario
def test_behavior_coverage_feature_md_bound_by_comment(
    tmp_path: Path, monkeypatch
) -> None:
    """Coverage marks bound scenarios."""
    monkeypatch.chdir(tmp_path)
    features_dir = tmp_path / "specs" / "behavior" / "features"
    tests_dir = tmp_path / "tests"
    _write_behavior_feature(
        features_dir / "auth" / "login.feature",
        title="Login",
        scenario_id="@bdd-login-rejects-invalid-password",
        scenario_title="Reject invalid password",
    )
    _write_test(
        tests_dir / "test_auth_login.py",
        """
# specweave: feature=specs/behavior/features/auth/login.feature
# specweave: scenario=@bdd-login-rejects-invalid-password
def test_rejects_invalid_password() -> None:
    pass
""",
    )

    result = build_behavior_coverage(features_dir=features_dir, tests_dir=tests_dir)

    assert result["scenarios_bound"] == 1
    assert result["missing_bindings"] == []


# specweave: feature=specs/behavior/features/behavior/coverage.feature
# specweave: scenario=@bdd-coverage-unbound-scenario
def test_behavior_coverage_does_not_match_by_title(tmp_path: Path, monkeypatch) -> None:
    """Coverage reports missing bindings."""
    monkeypatch.chdir(tmp_path)
    features_dir = tmp_path / "specs" / "behavior" / "features"
    tests_dir = tmp_path / "tests"
    _write_behavior_feature(
        features_dir / "auth" / "login.feature",
        title="Login",
        scenario_id="@bdd-login-rejects-invalid-password",
        scenario_title="Reject invalid password",
    )
    _write_test(
        tests_dir / "test_auth_login.py",
        """
def test_reject_invalid_password() -> None:
    pass
""",
    )

    result = build_behavior_coverage(features_dir=features_dir, tests_dir=tests_dir)

    assert result["scenarios_bound"] == 0
    assert (
        result["missing_bindings"][0]["scenario"]
        == "@bdd-login-rejects-invalid-password"
    )


# specweave: feature=specs/behavior/features/behavior/coverage.feature
# specweave: scenario=@bdd-coverage-stale-scenario
def test_behavior_coverage_reports_stale_markdown_mapping(
    tmp_path: Path, monkeypatch
) -> None:
    """Coverage reports bindings to non-existent scenarios."""
    monkeypatch.chdir(tmp_path)
    features_dir = tmp_path / "specs" / "behavior" / "features"
    tests_dir = tmp_path / "tests"
    _write_behavior_feature(
        features_dir / "auth" / "login.feature",
        title="Login",
        scenario_id="@bdd-login-rejects-invalid-password",
        scenario_title="Reject invalid password",
    )
    _write_test(
        tests_dir / "test_auth_login.py",
        """
# specweave: feature=specs/behavior/features/auth/login.feature
# specweave: scenario=@bdd-login-unknown
def test_rejects_invalid_password() -> None:
    pass
""",
    )

    result = build_behavior_coverage(features_dir=features_dir, tests_dir=tests_dir)

    assert result["stale_bindings"][0]["scenario"] == "@bdd-login-unknown"
    assert result["stale_bindings"][0]["reason"] == "missing_scenario"


# specweave: feature=specs/behavior/features/behavior/coverage.feature
# specweave: scenario=@bdd-coverage-forbidden-pytest-bdd
def test_behavior_coverage_reports_forbidden_pytest_bdd_usage(
    tmp_path: Path, monkeypatch
) -> None:
    """Coverage reports pytest-bdd imports in test files."""
    monkeypatch.chdir(tmp_path)
    features_dir = tmp_path / "specs" / "behavior" / "features"
    tests_dir = tmp_path / "tests"
    _write_behavior_feature(
        features_dir / "auth" / "login.feature",
        title="Login",
        scenario_id="@bdd-login-rejects-invalid-password",
        scenario_title="Reject invalid password",
    )
    _write_test(
        tests_dir / "test_auth_login.py",
        """
from pytest_bdd import scenarios

scenarios("login.feature")
""",
    )

    result = build_behavior_coverage(features_dir=features_dir, tests_dir=tests_dir)

    assert result["forbidden_pytest_bdd_usages"] == ["tests/test_auth_login.py"]


def test_behavior_coverage_ignores_pytest_bdd_text(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    features_dir = tmp_path / "specs" / "behavior" / "features"
    tests_dir = tmp_path / "tests"
    _write_test(
        tests_dir / "test_text.py",
        '''
"""pytest_bdd and scenarios("example.feature") are documentation text."""
from specweave.backends import pytest_bdd

def test_text() -> None:
    assert "pytest_bdd.scenarios()" == "pytest_bdd.scenarios()"
''',
    )

    result = build_behavior_coverage(features_dir=features_dir, tests_dir=tests_dir)

    assert result["forbidden_pytest_bdd_usages"] == []


# specweave: feature=specs/behavior/features/behavior/coverage.feature
# specweave: scenario=@bdd-coverage-missing-test-file
def test_coverage_missing_test_file(tmp_path: Path, monkeypatch) -> None:
    """Coverage reports missing test files."""
    monkeypatch.chdir(tmp_path)
    features_dir = tmp_path / "specs" / "behavior" / "features"
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    _write_behavior_feature(
        features_dir / "auth" / "login.feature",
        title="Login",
        scenario_id="@bdd-login-valid",
        scenario_title="Valid login",
    )
    result = build_behavior_coverage(features_dir=features_dir, tests_dir=tests_dir)
    assert len(result["missing_bindings"]) > 0


# specweave: feature=specs/behavior/features/behavior/coverage.feature
# specweave: scenario=@bdd-coverage-stale-binding
def test_coverage_stale_feature_binding(tmp_path: Path, monkeypatch) -> None:
    """Coverage reports bindings to non-existent features."""
    monkeypatch.chdir(tmp_path)
    features_dir = tmp_path / "specs" / "behavior" / "features"
    tests_dir = tmp_path / "tests"
    features_dir.mkdir(parents=True)
    _write_test(
        tests_dir / "test_auth_login.py",
        """
# specweave: feature=specs/behavior/features/auth/nonexistent.feature
# specweave: scenario=@bdd-login-valid
def test_valid_login() -> None:
    pass
""",
    )
    result = build_behavior_coverage(features_dir=features_dir, tests_dir=tests_dir)
    assert any(b["reason"] == "missing_feature" for b in result["stale_bindings"])


# specweave: feature=specs/behavior/features/behavior/coverage.feature
# specweave: scenario=@bdd-coverage-deprecated-paths
def test_coverage_deprecated_paths(tmp_path: Path, monkeypatch) -> None:
    """Coverage reports deprecated feature paths."""
    monkeypatch.chdir(tmp_path)
    features_dir = tmp_path / "specs" / "bdd" / "features"
    tests_dir = tmp_path / "tests"
    _write_behavior_feature(
        features_dir / "auth" / "login.feature",
        title="Login",
        scenario_id="@bdd-login-valid",
        scenario_title="Valid login",
    )
    tests_dir.mkdir()
    _write_test(
        tests_dir / "test_auth_login.py",
        """
# specweave: feature=specs/bdd/features/auth/login.feature
# specweave: scenario=@bdd-login-valid
def test_valid_login() -> None:
    pass
""",
    )
    canonical_features = tmp_path / "specs" / "behavior" / "features"
    canonical_features.mkdir(parents=True)
    result = build_behavior_coverage(
        features_dir=canonical_features,
        tests_dir=tests_dir,
    )
    assert len(result["deprecated_paths"]) > 0


# specweave: feature=specs/behavior/features/behavior/coverage.feature
# specweave: scenario=@bdd-coverage-manual-scenario
def test_coverage_manual_scenario_skipped(tmp_path: Path, monkeypatch) -> None:
    """Coverage skips scenarios tagged @manual."""
    monkeypatch.chdir(tmp_path)
    features_dir = tmp_path / "specs" / "behavior" / "features"
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    _write_behavior_feature(
        features_dir / "auth" / "login.feature",
        title="Login",
        scenario_id="@bdd-login-valid",
        scenario_title="Valid login",
        tags=("manual",),
    )
    result = build_behavior_coverage(features_dir=features_dir, tests_dir=tests_dir)
    # Manual scenarios should not appear in missing_bindings
    manual_missing = [
        b for b in result["missing_bindings"] if b["scenario"] == "@bdd-login-valid"
    ]
    assert len(manual_missing) == 0
