"""Tests for specification document parsing."""

from __future__ import annotations

from pathlib import Path

from specweave.specifications.parser import parse_specification


def _write_spec(tmp_path: Path, relative_path: str, text: str) -> Path:
    path = tmp_path / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


SPEC_TEXT = """\
---
id: SPEC-COV
kind: capability-spec
title: Coverage and reverse coverage
status: active
version: 1
---

# Coverage and reverse coverage

## Intent

SpecWeave verifies requirement/test traceability in both directions.

## Requirements

### REQ-COV-001 — Bidirectional coverage

SpecWeave SHALL report coverage from requirements to pytest tests
and from pytest tests back to requirements.

Rationale:
One-way coverage hides orphan tests and weakens traceability.

Verification:
- pytest: tests/test_behavior_coverage.py::test_render_coverage_text_both_directions
- cli: specweave specifications coverage --view both

### REQ-COV-002 — No title-only matching

SpecWeave SHALL NOT treat matching titles as a valid verification link.

Verification:
- pytest: tests/test_behavior_coverage.py::test_title_only_never_drives_matching
"""


def test_parses_front_matter(tmp_path: Path) -> None:
    path = _write_spec(
        tmp_path,
        "specs/specifications/capabilities/coverage.spec.md",
        SPEC_TEXT,
    )

    document = parse_specification(path)

    assert document.spec_id == "SPEC-COV"
    assert document.kind == "capability-spec"
    assert document.title == "Coverage and reverse coverage"
    assert document.status == "active"


def test_parses_product_spec(tmp_path: Path) -> None:
    path = _write_spec(
        tmp_path,
        "specs/specifications/product.spec.md",
        """\
---
id: SPEC-PRODUCT
title: Product specification
kind: product-spec
status: active
version: 1
---

# Product specification

## Requirements

### REQ-PRODUCT-001 — Support behaviour and specifications

SpecWeave SHALL support both modes.

Verification:
- manual: define project-specific verification
""",
    )

    document = parse_specification(path)

    assert document.spec_id == "SPEC-PRODUCT"
    assert document.kind == "product-spec"
    assert len(document.requirements) == 1
    assert document.requirements[0].id == "REQ-PRODUCT-001"


def test_parses_requirement_headings(tmp_path: Path) -> None:
    path = _write_spec(
        tmp_path,
        "specs/specifications/capabilities/coverage.spec.md",
        SPEC_TEXT,
    )

    document = parse_specification(path)

    assert [requirement.id for requirement in document.requirements] == [
        "REQ-COV-001",
        "REQ-COV-002",
    ]
    assert [requirement.title for requirement in document.requirements] == [
        "Bidirectional coverage",
        "No title-only matching",
    ]


def test_parses_verification_lists(tmp_path: Path) -> None:
    path = _write_spec(
        tmp_path,
        "specs/specifications/capabilities/coverage.spec.md",
        SPEC_TEXT,
    )

    document = parse_specification(path)
    first_requirement = document.requirements[0]

    assert tuple(
        (ref.kind, ref.target) for ref in first_requirement.verification_refs
    ) == (
        (
            "pytest",
            "tests/test_behavior_coverage.py::test_render_coverage_text_both_directions",
        ),
        ("cli", "specweave specifications coverage --view both"),
    )


def test_preserves_line_numbers(tmp_path: Path) -> None:
    path = _write_spec(
        tmp_path,
        "specs/specifications/capabilities/coverage.spec.md",
        SPEC_TEXT,
    )

    document = parse_specification(path)

    assert document.requirements[0].line == 17
    assert document.requirements[1].line == 29
