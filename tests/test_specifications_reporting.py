"""Tests for specifications report import and evidence mapping."""

from __future__ import annotations

from pathlib import Path

from specweave.specifications.index import write_specification_index
from specweave.specifications.reporting import import_pytest_report


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _setup(tmp_path: Path) -> dict[str, Path]:
    root = tmp_path / "specs" / "specifications"
    tests_dir = tmp_path / "tests"
    _write(
        tmp_path / "specs" / "specifications" / "product.spec.md",
        """\
---
id: SPEC-PRODUCT
title: Product specification
kind: product-spec
status: active
---

# Product specification

## Requirements

### REQ-COV-001 — Bidirectional coverage

SpecWeave SHALL report coverage in both directions.
""",
    )
    manifest_path = root / "manifest.json"
    write_specification_index(
        root=root, out=root / "README.md", manifest_path=manifest_path
    )
    _write(
        tests_dir / "test_behavior_coverage.py",
        """\
# specweave: spec=specs/specifications/product.spec.md requirement=REQ-COV-001
def test_reports_bidirectional_coverage() -> None:
    pass
""",
    )
    return {"root": root, "tests_dir": tests_dir, "manifest_path": manifest_path}


def test_imports_junit_xml_to_requirement_evidence(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    paths = _setup(tmp_path)
    report = _write(
        tmp_path / "reports" / "junit.xml",
        (
            '<?xml version="1.0"?>\n'
            '<testsuites><testsuite name="pytest" tests="1">\n'
            '  <testcase classname="tests.test_behavior_coverage" '
            'file="tests/test_behavior_coverage.py" '
            'name="test_reports_bidirectional_coverage"/>\n'
            "</testsuite></testsuites>\n"
        ),
    )

    payload = import_pytest_report(
        report=report,
        tests_dir=paths["tests_dir"],
        manifest_path=paths["manifest_path"],
    )

    assert payload["mode"] == "specifications"
    assert payload["results"][0]["id"] == "REQ-COV-001"
    assert payload["results"][0]["tests"] == [
        "tests/test_behavior_coverage.py::test_reports_bidirectional_coverage"
    ]


def test_fail_closed_status_blocks_requirement(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    paths = _setup(tmp_path)
    report = _write(
        tmp_path / "reports" / "junit.xml",
        (
            '<?xml version="1.0"?>\n'
            '<testsuites><testsuite name="pytest" tests="1">\n'
            '  <testcase classname="tests.test_behavior_coverage" '
            'file="tests/test_behavior_coverage.py" '
            'name="test_reports_bidirectional_coverage">\n'
            '    <failure message="boom">boom</failure>\n'
            "  </testcase>\n"
            "</testsuite></testsuites>\n"
        ),
    )

    payload = import_pytest_report(
        report=report,
        tests_dir=paths["tests_dir"],
        manifest_path=paths["manifest_path"],
    )

    assert payload["results"][0]["status"] == "failed"


def test_passing_mapped_pytest_test_verifies_requirement(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    paths = _setup(tmp_path)
    report = _write(
        tmp_path / "reports" / "junit.xml",
        (
            '<?xml version="1.0"?>\n'
            '<testsuites><testsuite name="pytest" tests="1">\n'
            '  <testcase classname="tests.test_behavior_coverage" '
            'file="tests/test_behavior_coverage.py" '
            'name="test_reports_bidirectional_coverage"/>\n'
            "</testsuite></testsuites>\n"
        ),
    )

    payload = import_pytest_report(
        report=report,
        tests_dir=paths["tests_dir"],
        manifest_path=paths["manifest_path"],
    )

    assert payload["results"][0]["status"] == "passed"
