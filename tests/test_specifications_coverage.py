"""Tests for specifications coverage reporting."""

from __future__ import annotations

import json
from pathlib import Path

from specweave.specifications.coverage import build_specification_coverage


def _write_spec(tmp_path: Path, relative_path: str, text: str) -> Path:
    path = tmp_path / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _write_test(tmp_path: Path, relative_path: str, text: str) -> Path:
    path = tmp_path / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_requirement_bound_by_pytest_mapping_passes_coverage(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    root = tmp_path / "specs" / "specifications"
    tests_dir = tmp_path / "tests"
    _write_spec(
        tmp_path,
        "specs/specifications/product.spec.md",
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
    _write_test(
        tmp_path,
        "tests/test_behavior_coverage.py",
        """\
# specweave: spec=specs/specifications/product.spec.md requirement=REQ-COV-001
def test_reports_bidirectional_coverage() -> None:
    pass
""",
    )

    result = build_specification_coverage(root=root, tests_dir=tests_dir)

    assert result["requirements_bound"] == 1
    assert result["missing_bindings"] == []
    assert result["status"] == "passed"


def test_missing_pytest_mapping_fails_coverage(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    root = tmp_path / "specs" / "specifications"
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    _write_spec(
        tmp_path,
        "specs/specifications/product.spec.md",
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

    result = build_specification_coverage(root=root, tests_dir=tests_dir)

    assert result["status"] == "failed"
    assert result["missing_bindings"][0]["requirement"] == "REQ-COV-001"


def test_stale_pytest_nodeid_fails_coverage(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    root = tmp_path / "specs" / "specifications"
    tests_dir = tmp_path / "tests"
    _write_spec(
        tmp_path,
        "specs/specifications/product.spec.md",
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
    _write_test(
        tmp_path,
        "tests/test_behavior_coverage.py",
        """\
# specweave: spec=specs/specifications/product.spec.md requirement=REQ-MISSING-001
def test_reports_bidirectional_coverage() -> None:
    pass
""",
    )

    result = build_specification_coverage(root=root, tests_dir=tests_dir)

    assert result["status"] == "failed"
    assert result["stale_bindings"][0]["reason"] == "missing_requirement"


def test_reverse_coverage_lists_unmapped_pytest_tests(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    root = tmp_path / "specs" / "specifications"
    tests_dir = tmp_path / "tests"
    _write_spec(
        tmp_path,
        "specs/specifications/product.spec.md",
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
    _write_test(
        tmp_path,
        "tests/test_behavior_coverage.py",
        """\
def test_reports_bidirectional_coverage() -> None:
    pass
""",
    )

    result = build_specification_coverage(root=root, tests_dir=tests_dir)

    assert result["pytest_tests_total"] == 1
    assert result["pytest_tests_unmapped"] == 1
    assert result["unmapped_tests"][0]["nodeid"] == (
        "tests/test_behavior_coverage.py::test_reports_bidirectional_coverage"
    )


def test_intentional_unmapped_policy_waives_reverse_gap(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    root = tmp_path / "specs" / "specifications"
    tests_dir = tmp_path / "tests"
    mappings_dir = root / "mappings"
    mappings_dir.mkdir(parents=True, exist_ok=True)
    _write_spec(
        tmp_path,
        "specs/specifications/product.spec.md",
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
    _write_test(
        tmp_path,
        "tests/test_behavior_coverage.py",
        """\
def test_reports_bidirectional_coverage() -> None:
    pass
""",
    )
    (mappings_dir / "intentional-unmapped.json").write_text(
        json.dumps(
            {
                "schema": "specweave.intentional-unmapped.v1",
                "mode": "specifications",
                "tests": [
                    {
                        "nodeid": (
                            "tests/test_behavior_coverage.py::"
                            "test_reports_bidirectional_coverage"
                        ),
                        "reason": "Internal helper verification only.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    result = build_specification_coverage(root=root, tests_dir=tests_dir)

    assert result["pytest_tests_unmapped"] == 0
    assert result["pytest_tests_waived"] == 1
