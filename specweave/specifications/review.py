"""Aggregate specification lint, coverage, and evidence findings."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from specweave.specifications.coverage import build_specification_coverage
from specweave.specifications.lint import lint_specification_tree


def run_specifications_review(
    *,
    root: Path,
    tests_dir: Path,
    mapping_dir: Path | None = None,
    require_verification: bool = True,
) -> dict[str, Any]:
    """Run a specification-focused review and return a JSON-serialisable result."""
    lint_results = lint_specification_tree(
        root,
        require_verification=require_verification,
    )
    coverage = build_specification_coverage(
        root=root,
        tests_dir=tests_dir,
        mapping_dir=mapping_dir,
    )

    findings: list[dict[str, Any]] = []
    warnings_count = 0
    errors_count = 0

    for finding in lint_results:
        entry: dict[str, Any] = {
            "code": finding.code,
            "level": finding.level,
            "path": finding.path,
            "message": finding.message,
        }
        if finding.line is not None:
            entry["line"] = finding.line
        findings.append(entry)
        if finding.level == "error":
            errors_count += 1
        else:
            warnings_count += 1

    for binding in coverage["missing_bindings"]:
        findings.append(
            {
                "code": "SWSCOV001",
                "level": "warning",
                "path": binding["spec"],
                "requirement": binding["requirement"],
                "message": "No bound pytest test found.",
            }
        )
        warnings_count += 1

    for binding in coverage["stale_bindings"]:
        findings.append(
            {
                "code": "SWSCOV002",
                "level": "warning",
                "path": binding["test_file"],
                "requirement": binding["requirement"],
                "message": (
                    "Stale pytest mapping points to a missing specification "
                    "or requirement."
                ),
            }
        )
        warnings_count += 1

    for item in coverage["unmapped_tests"]:
        findings.append(
            {
                "code": "SWSCOV003",
                "level": "warning",
                "path": item["test_file"],
                "message": (
                    "Pytest test is not mapped to any specification requirement."
                ),
            }
        )
        warnings_count += 1

    status = "passed"
    if errors_count or coverage["status"] != "passed":
        status = "failed"

    return {
        "schema_version": 1,
        "command": "review specifications",
        "status": status,
        "summary": {
            "documents": coverage["documents_total"],
            "requirements": coverage["requirements_total"],
            "verified": coverage["requirements_bound"],
            "missing": len(coverage["missing_bindings"]),
            "reverse_gaps": coverage["pytest_tests_unmapped"]
            + coverage["pytest_mappings_stale"],
            "warnings": warnings_count,
            "errors": errors_count,
        },
        "findings": findings,
    }
