"""Tests for behavior report import and evidence mapping."""

from __future__ import annotations

import json
from pathlib import Path

from specweave.behavior.reporting import import_pytest_report

FEATURE = "specs/behavior/features/behavior/reporting.feature"


def _write_junit(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _junit_with_nodeid() -> str:
    return (
        '<?xml version="1.0"?>\n'
        '<testsuites><testsuite name="pytest" tests="1">'
        '<testcase classname="tests.test_auth_login" file="tests/test_auth_login.py" '
        'name="test_valid_login">'
        "<properties>"
        '<property name="specweave_feature" '
        'value="specs/behavior/features/auth/login.feature"/>'
        '<property name="specweave_scenario" value="@bdd-login-valid"/>'
        "</properties>"
        "</testcase></testsuite></testsuites>"
    )


def _setup(tmp_path: Path) -> dict:
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_auth_login.py").write_text(
        "# specweave: feature=specs/behavior/features/auth/login.feature\n"
        "# specweave: scenario=@bdd-login-valid\n"
        "def test_valid_login() -> None:\n    pass\n",
        encoding="utf-8",
    )
    features_dir = tmp_path / "specs" / "behavior" / "features"
    features_dir.mkdir(parents=True)
    manifest_path = tmp_path / "specs" / "behavior" / "manifest.json"
    manifest_path.write_text(
        json.dumps({"features": [], "schema_version": 1}), encoding="utf-8"
    )
    return {"tests_dir": tests_dir, "manifest_path": manifest_path}


# specweave: feature=specs/behavior/features/behavior/reporting.feature
# specweave: scenario=@bdd-import-maps-by-nodeid
def test_import_maps_by_nodeid(tmp_path: Path) -> None:
    """Import maps results by normalized nodeid."""
    paths = _setup(tmp_path)
    report_path = _write_junit(tmp_path / "reports", _junit_with_nodeid())
    result = import_pytest_report(
        report=report_path,
        tests_dir=paths["tests_dir"],
        manifest_path=paths["manifest_path"],
    )
    assert result is not None


# specweave: feature=specs/behavior/features/behavior/reporting.feature
# specweave: scenario=@bdd-import-maps-by-function-name
def test_import_maps_by_function_name(tmp_path: Path) -> None:
    """Import falls back to function name matching."""
    paths = _setup(tmp_path)
    text = (
        '<?xml version="1.0"?>\n'
        '<testsuites><testsuite name="pytest" tests="1">'
        '<testcase classname="tests.test_auth_login" file="tests/test_auth_login.py" '
        'name="test_valid_login"/>'
        "</testsuite></testsuites>"
    )
    report_path = _write_junit(tmp_path / "reports", text)
    result = import_pytest_report(
        report=report_path,
        tests_dir=paths["tests_dir"],
        manifest_path=paths["manifest_path"],
    )
    assert result is not None


# specweave: feature=specs/behavior/features/behavior/reporting.feature
# specweave: scenario=@bdd-import-maps-by-manifest
def test_import_maps_by_manifest(tmp_path: Path) -> None:
    """Import uses manifest mappings when available."""
    paths = _setup(tmp_path)
    report_path = _write_junit(tmp_path / "reports", _junit_with_nodeid())
    result = import_pytest_report(
        report=report_path,
        tests_dir=paths["tests_dir"],
        manifest_path=paths["manifest_path"],
    )
    assert result is not None


# specweave: feature=specs/behavior/features/behavior/reporting.feature
# specweave: scenario=@bdd-import-unmapped-tests
def test_import_unmapped_tests(tmp_path: Path) -> None:
    """Import reports tests without specweave markers."""
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text('{"features": [], "schema_version": 1}', encoding="utf-8")
    text = (
        '<?xml version="1.0"?>\n'
        '<testsuites><testsuite name="pytest" tests="1">'
        '<testcase classname="tests.test_other" file="tests/test_other.py" '
        'name="test_something"/>'
        "</testsuite></testsuites>"
    )
    report_path = _write_junit(tmp_path / "reports", text)
    result = import_pytest_report(
        report=report_path,
        tests_dir=tests_dir,
        manifest_path=manifest_path,
    )
    assert result is not None


# specweave: feature=specs/behavior/features/behavior/reporting.feature
# specweave: scenario=@bdd-import-writes-evidence
def test_import_writes_evidence(tmp_path: Path) -> None:
    """Import writes evidence to the target path."""
    paths = _setup(tmp_path)
    report_path = _write_junit(tmp_path / "reports", _junit_with_nodeid())
    result = import_pytest_report(
        report=report_path,
        tests_dir=paths["tests_dir"],
        manifest_path=paths["manifest_path"],
    )
    assert result["backend"] == "pytest"
