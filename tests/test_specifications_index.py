"""Tests for specifications index generation."""

from __future__ import annotations

import json
from pathlib import Path

from specweave.specifications.index import write_specification_index


def _write_spec(tmp_path: Path, relative_path: str, text: str) -> Path:
    path = tmp_path / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_writes_manifest(tmp_path: Path) -> None:
    root = tmp_path / "specs" / "specifications"
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

### REQ-PRODUCT-001 — Support both modes

SpecWeave SHALL support behaviour and specifications.

Verification:
- manual: define project-specific verification
""",
    )
    _write_spec(
        tmp_path,
        "specs/specifications/capabilities/coverage.spec.md",
        """\
---
id: SPEC-COV
title: Coverage and reverse coverage
kind: capability-spec
status: active
---

# Coverage and reverse coverage

## Requirements

### REQ-COV-001 — Bidirectional coverage

SpecWeave SHALL report coverage in both directions.

Verification:
- pytest: tests/test_behavior_coverage.py::test_render_coverage_text_both_directions
""",
    )
    out = root / "README.md"
    manifest_path = root / "manifest.json"

    write_specification_index(root=root, out=out, manifest_path=manifest_path)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["schema"] == "specweave.specifications-manifest.v1"
    assert manifest["mode"] == "specifications"
    assert manifest["product_spec"] == "specs/specifications/product.spec.md"
    assert {document["id"] for document in manifest["documents"]} == {
        "SPEC-PRODUCT",
        "SPEC-COV",
    }


def test_includes_product_spec_capabilities_interfaces_and_integrations(
    tmp_path: Path,
) -> None:
    root = tmp_path / "specs" / "specifications"
    for relative_path, spec_id, kind in (
        ("specs/specifications/product.spec.md", "SPEC-PRODUCT", "product-spec"),
        (
            "specs/specifications/capabilities/coverage.spec.md",
            "SPEC-COV",
            "capability-spec",
        ),
        (
            "specs/specifications/interfaces/cli.spec.md",
            "SPEC-CLI",
            "interface-spec",
        ),
        (
            "specs/specifications/integrations/taskledger.spec.md",
            "SPEC-TL",
            "integration-spec",
        ),
    ):
        _write_spec(
            tmp_path,
            relative_path,
            f"""\
---
id: {spec_id}
title: {spec_id}
kind: {kind}
status: active
---

# {spec_id}
""",
        )

    out = root / "README.md"
    manifest_path = root / "manifest.json"
    write_specification_index(root=root, out=out, manifest_path=manifest_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert {document["id"] for document in manifest["documents"]} == {
        "SPEC-PRODUCT",
        "SPEC-COV",
        "SPEC-CLI",
        "SPEC-TL",
    }


def test_includes_verification_refs(tmp_path: Path) -> None:
    root = tmp_path / "specs" / "specifications"
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

### REQ-PRODUCT-001 — Support both modes

SpecWeave SHALL support behaviour and specifications.

Verification:
- pytest: tests/test_behavior_coverage.py::test_render_coverage_text_both_directions
- cli: specweave specifications coverage --view both
""",
    )

    out = root / "README.md"
    manifest_path = root / "manifest.json"
    write_specification_index(root=root, out=out, manifest_path=manifest_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    requirement = manifest["requirements"][0]
    assert requirement["verification"] == [
        {
            "kind": "pytest",
            "target": (
                "tests/test_behavior_coverage.py::"
                "test_render_coverage_text_both_directions"
            ),
        },
        {
            "kind": "cli",
            "target": "specweave specifications coverage --view both",
        },
    ]
