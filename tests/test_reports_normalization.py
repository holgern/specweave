"""Tests for report normalization and evidence generation."""

from __future__ import annotations

import json
from pathlib import Path

from specweave.reports.normalize import (
    normalize_report,
    write_evidence_json,
)

FEATURE = "specs/behavior/features/reports/normalization.feature"


def _write_cucumber(tmp_path: Path, elements: list) -> Path:
    path = tmp_path / "cucumber.json"
    path.write_text(json.dumps([{"name": "F", "elements": elements}]), encoding="utf-8")
    return path


def _write_junit(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "junit.xml"
    path.write_text(text, encoding="utf-8")
    return path


# specweave: feature=specs/behavior/features/reports/normalization.feature
# specweave: scenario=@bdd-normalize-junit-xml
def test_normalize_junit_xml(tmp_path: Path) -> None:
    """Normalization parses JUnit XML reports."""
    path = _write_junit(
        tmp_path,
        '<?xml version="1.0"?>\n<testsuites><testsuite tests="1">'
        '<testcase name="@bdd-0001 @ac-0001 ok"/></testsuite></testsuites>',
    )
    report = normalize_report(path, "junit-xml")
    assert report.status == "passed"
    assert report.runner == "junit-xml"


# specweave: feature=specs/behavior/features/reports/normalization.feature
# specweave: scenario=@bdd-normalize-cucumber-json
def test_normalize_cucumber_json(tmp_path: Path) -> None:
    """Normalization parses Cucumber JSON reports."""
    path = _write_cucumber(
        tmp_path,
        [
            {
                "name": "S",
                "tags": [{"name": "@bdd-0001"}],
                "steps": [{"result": {"status": "passed"}}],
            }
        ],
    )
    report = normalize_report(path, "cucumber-json")
    assert report.status == "passed"
    assert report.runner == "cucumber-json"


# specweave: feature=specs/behavior/features/reports/normalization.feature
# specweave: scenario=@bdd-normalize-unsupported-format
def test_normalize_unsupported_format(tmp_path: Path) -> None:
    """Normalization rejects unsupported formats."""
    path = tmp_path / "x.csv"
    path.write_text("data", encoding="utf-8")
    try:
        normalize_report(path, "csv")
    except ValueError as exc:
        assert "csv" in str(exc)
    else:
        raise AssertionError("expected ValueError")


# specweave: feature=specs/behavior/features/reports/normalization.feature
# specweave: scenario=@bdd-normalize-all-passed
def test_normalize_all_passed(tmp_path: Path) -> None:
    """Report status is passed when all scenarios pass."""
    path = _write_cucumber(
        tmp_path,
        [
            {
                "name": "S",
                "tags": [{"name": "@bdd-0001"}, {"name": "@ac-0001"}],
                "steps": [{"result": {"status": "passed"}}],
            }
        ],
    )
    report = normalize_report(path, "cucumber-json")
    assert report.status == "passed"


# specweave: feature=specs/behavior/features/reports/normalization.feature
# specweave: scenario=@bdd-normalize-any-failed
def test_normalize_any_failed(tmp_path: Path) -> None:
    """Report status is failed when any scenario fails."""
    path = _write_cucumber(
        tmp_path,
        [
            {
                "name": "S",
                "tags": [{"name": "@bdd-0001"}, {"name": "@ac-0001"}],
                "steps": [{"result": {"status": "failed"}}],
            }
        ],
    )
    report = normalize_report(path, "cucumber-json")
    assert report.status == "failed"


# specweave: feature=specs/behavior/features/reports/normalization.feature
# specweave: scenario=@bdd-normalize-skipped-fails-by-default
def test_normalize_skipped_fails_by_default(tmp_path: Path) -> None:
    """Skipped scenarios fail the report by default."""
    path = _write_cucumber(
        tmp_path,
        [
            {
                "name": "S",
                "tags": [{"name": "@bdd-0001"}, {"name": "@ac-0001"}],
                "steps": [{"result": {"status": "skipped"}}],
            }
        ],
    )
    report = normalize_report(path, "cucumber-json")
    assert report.status == "failed"


# specweave: feature=specs/behavior/features/reports/normalization.feature
# specweave: scenario=@bdd-normalize-allow-skipped
def test_normalize_allow_skipped(tmp_path: Path) -> None:
    """Skipped scenarios pass with --allow-skipped."""
    path = _write_cucumber(
        tmp_path,
        [
            {
                "name": "S",
                "tags": [{"name": "@bdd-0001"}, {"name": "@ac-0001"}],
                "steps": [{"result": {"status": "skipped"}}],
            },
            {
                "name": "T",
                "tags": [{"name": "@bdd-0002"}, {"name": "@ac-0001"}],
                "steps": [{"result": {"status": "passed"}}],
            },
        ],
    )
    report = normalize_report(path, "cucumber-json", allow_skipped=True)
    assert report.status == "passed"


# specweave: feature=specs/behavior/features/reports/normalization.feature
# specweave: scenario=@bdd-normalize-missing-ac-coverage
def test_normalize_missing_ac_coverage(tmp_path: Path) -> None:
    """Report fails when expected AC has no passing scenario."""
    path = _write_cucumber(
        tmp_path,
        [
            {
                "name": "S",
                "tags": [{"name": "@bdd-0001"}, {"name": "@ac-0001"}],
                "steps": [{"result": {"status": "passed"}}],
            }
        ],
    )
    report = normalize_report(
        path, "cucumber-json", expected_ac_ids=("ac-0001", "ac-0002")
    )
    assert report.status == "failed"


# specweave: feature=specs/behavior/features/reports/normalization.feature
# specweave: scenario=@bdd-normalize-ac-covered
def test_normalize_ac_covered(tmp_path: Path) -> None:
    """Report passes when expected AC has a passing scenario."""
    path = _write_cucumber(
        tmp_path,
        [
            {
                "name": "S",
                "tags": [{"name": "@bdd-0001"}, {"name": "@ac-0001"}],
                "steps": [{"result": {"status": "passed"}}],
            }
        ],
    )
    report = normalize_report(path, "cucumber-json", expected_ac_ids=("ac-0001",))
    assert report.status == "passed"


# specweave: feature=specs/behavior/features/reports/normalization.feature
# specweave: scenario=@bdd-normalize-evidence-json
def test_normalize_evidence_json(tmp_path: Path) -> None:
    """Normalization writes Taskledger evidence JSON."""
    path = _write_cucumber(
        tmp_path,
        [
            {
                "name": "S",
                "tags": [{"name": "@bdd-0001"}, {"name": "@ac-0001"}],
                "steps": [{"result": {"status": "passed"}}],
            }
        ],
    )
    report = normalize_report(path, "cucumber-json")
    out = tmp_path / "evidence.json"
    write_evidence_json(report, "task-0123", out)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["task_id"] == "task-0123"
    assert data["schema_version"] == 2
