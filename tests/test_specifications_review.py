"""Tests for specifications and combined review output."""

from __future__ import annotations

from pathlib import Path

from specweave.config import (
    SpecWeaveConfig,
    SpecWeavePaths,
    SpecWeaveSpecificationPaths,
    load_config,
)
from specweave.review import run_review


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_review_specifications_aggregates_lint_and_coverage(tmp_path: Path) -> None:
    _write(
        tmp_path / "specs/specifications/product.spec.md",
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

Verification:
- pytest: tests/test_core_login.py::test_successful_login
""",
    )
    config = SpecWeaveConfig(
        project_root=tmp_path,
        paths=SpecWeavePaths(
            specs_root=tmp_path / "specs",
            tests_dir=tmp_path / "tests",
            specifications=SpecWeaveSpecificationPaths(
                root=tmp_path / "specs/specifications",
                product_spec=tmp_path / "specs/specifications/product.spec.md",
                readme=tmp_path / "specs/specifications/README.md",
                manifest=tmp_path / "specs/specifications/manifest.json",
                capabilities_dir=tmp_path / "specs/specifications/capabilities",
                interfaces_dir=tmp_path / "specs/specifications/interfaces",
                integrations_dir=tmp_path / "specs/specifications/integrations",
                mappings_dir=tmp_path / "specs/specifications/mappings",
                evidence_dir=tmp_path / "specs/specifications/evidence",
                reports_dir=tmp_path / "specs/specifications/reports",
                reports_state_dir=tmp_path / "specs/specifications/reports/specweave",
            ),
        ),
    )

    result = run_review(config=config, mode="specifications")

    assert result["status"] == "failed"
    assert result["summary"]["documents"] == 1
    assert any(
        finding["code"] in {"SWSCOV001", "SWSDD008"} for finding in result["findings"]
    )


def test_review_specs_includes_both_modes(tmp_path: Path) -> None:
    _write(
        tmp_path / "specs/behavior/features/core/login.feature",
        "Feature: Login\n\n"
        "  @bdd-login-success @ac-0001\n"
        "  Example: Successful login\n"
        "    Given a user exists\n"
        "    When credentials are submitted\n"
        "    Then access is granted\n",
    )
    _write(
        tmp_path / "tests/test_core_login.py",
        "# specweave:\n"
        "#   feature: specs/behavior/features/core/login.feature\n"
        "#   scenario: @bdd-login-success\n"
        "#   spec: specs/specifications/product.spec.md\n"
        "#   requirement: REQ-COV-001\n"
        "def test_successful_login() -> None:\n    pass\n",
    )
    _write(
        tmp_path / "specs/specifications/product.spec.md",
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

Verification:
- pytest: tests/test_core_login.py::test_successful_login
""",
    )
    config_file = tmp_path / "specweave.toml"
    config_file.write_text(
        "schema_version = 1\n"
        "[paths]\n"
        'specs_root = "specs"\n'
        "[paths.behaviour]\n"
        'root = "specs/behavior"\n'
        "[paths.specifications]\n"
        'root = "specs/specifications"\n',
        encoding="utf-8",
    )

    result = run_review(config=load_config(config_file), mode="both")

    assert result["status"] == "passed"
    assert result["summary"]["behaviour"]["features"] == 1
    assert result["summary"]["specifications"]["documents"] == 1
