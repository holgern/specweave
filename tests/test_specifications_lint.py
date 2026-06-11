"""Tests for specification lint rules."""

from __future__ import annotations

from pathlib import Path

from specweave.specifications.lint import lint_specification_tree


def _write_spec(tmp_path: Path, relative_path: str, text: str) -> Path:
    path = tmp_path / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_duplicate_document_ids_fail(tmp_path: Path) -> None:
    root = tmp_path / "specs" / "specifications"
    _write_spec(
        tmp_path,
        "specs/specifications/capabilities/one.spec.md",
        """\
---
id: SPEC-DUP
title: One
kind: capability-spec
status: active
---

# One
""",
    )
    _write_spec(
        tmp_path,
        "specs/specifications/interfaces/two.spec.md",
        """\
---
id: SPEC-DUP
title: Two
kind: interface-spec
status: active
---

# Two
""",
    )

    findings = lint_specification_tree(root)

    assert sum(finding.code == "SWSDD002" for finding in findings) == 2


def test_duplicate_requirement_ids_fail(tmp_path: Path) -> None:
    root = tmp_path / "specs" / "specifications"
    _write_spec(
        tmp_path,
        "specs/specifications/product.spec.md",
        """\
---
id: SPEC-PRODUCT
title: Product
kind: product-spec
status: active
---

# Product

## Requirements

### REQ-DUP-001 — First

SpecWeave SHALL support one thing.

Verification:
- manual: verify later
""",
    )
    _write_spec(
        tmp_path,
        "specs/specifications/capabilities/two.spec.md",
        """\
---
id: SPEC-TWO
title: Two
kind: capability-spec
status: active
---

# Two

## Requirements

### REQ-DUP-001 — Second

SpecWeave SHALL support another thing.

Verification:
- manual: verify later
""",
    )

    findings = lint_specification_tree(root)

    assert sum(finding.code == "SWSDD003" for finding in findings) == 2


def test_missing_verification_fails_when_required(tmp_path: Path) -> None:
    root = tmp_path / "specs" / "specifications"
    _write_spec(
        tmp_path,
        "specs/specifications/product.spec.md",
        """\
---
id: SPEC-PRODUCT
title: Product
kind: product-spec
status: active
---

# Product

## Requirements

### REQ-COV-001 — Coverage

SpecWeave SHALL report coverage in both directions.
""",
    )

    findings = lint_specification_tree(root, require_verification=True)

    assert any(finding.code == "SWSDD005" for finding in findings)


def test_weak_normative_language_warns(tmp_path: Path) -> None:
    root = tmp_path / "specs" / "specifications"
    _write_spec(
        tmp_path,
        "specs/specifications/product.spec.md",
        """\
---
id: SPEC-PRODUCT
title: Product
kind: product-spec
status: active
---

# Product

## Requirements

### REQ-COV-001 — Coverage

SpecWeave reports coverage in both directions.

Verification:
- manual: verify later
""",
    )

    findings = lint_specification_tree(root)

    assert any(finding.code == "SWSDD007" for finding in findings)


def test_unsupported_id_prefix_fails(tmp_path: Path) -> None:
    root = tmp_path / "specs" / "specifications"
    _write_spec(
        tmp_path,
        "specs/specifications/product.spec.md",
        """\
---
id: SPEC-PRODUCT
title: Product
kind: product-spec
status: active
---

# Product

## Requirements

### CAP-COV-001 — Coverage

SpecWeave SHALL report coverage in both directions.

Verification:
- manual: verify later
""",
    )

    findings = lint_specification_tree(root)

    assert any(finding.code == "SWSDD004" for finding in findings)
