"""Assemble a :class:`NormalizedBddReport` from format-specific parsers.

This is the fail-closed entry point for report normalization. It:

1. Parses a runner-native report with the format-specific parser.
2. Applies the skipped policy (``skipped`` fails unless ``allow_skipped``).
3. Rolls results up into acceptance-criterion results
   (see :mod:`specweave.reports.mapping`).
4. Optionally enforces expected ``ac-*`` coverage.
5. Computes the overall report status (fail-closed).

The overall status is ``passed`` **only** when every scenario passed (and every
expected criterion was covered). Any ``failed``/``undefined``/``pending``/
``ambiguous`` scenario (or a ``skipped`` one when ``allow_skipped`` is False) or
any missing expected ``ac-*`` marks the whole report ``failed``.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from specweave.reports.cucumber_json import parse_cucumber_json
from specweave.reports.junit_xml import parse_junit_xml
from specweave.reports.mapping import (
    extract_ids_from_tags,
    require_expected_coverage,
    summarize_criteria,
)
from specweave.reports.model import (
    HARD_FAIL_STATUSES,
    NormalizedBddReport,
    ScenarioResult,
)

#: Formats supported by :func:`normalize_report`.
SUPPORTED_FORMATS = ("cucumber-json", "junit-xml")


def _parse(path: str | Path, fmt: str) -> tuple[ScenarioResult, ...]:
    if fmt == "cucumber-json":
        return parse_cucumber_json(path)
    if fmt == "junit-xml":
        return parse_junit_xml(path)
    raise ValueError(f"Unsupported format: {fmt!r}. Use one of {SUPPORTED_FORMATS}.")


def _is_blocking_for_report(status: str, allow_skipped: bool) -> bool:
    if status in HARD_FAIL_STATUSES:
        return True
    return status == "skipped" and not allow_skipped


def _count_by_status(results: Iterable[ScenarioResult]) -> dict[str, int]:
    counts = {
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "undefined": 0,
        "pending": 0,
        "ambiguous": 0,
    }
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    return counts


def _overall_status(
    results: Iterable[ScenarioResult],
    coverage_status: str,
    allow_skipped: bool,
) -> str:
    if coverage_status != "passed":
        return "failed"
    for result in results:
        if _is_blocking_for_report(result.status, allow_skipped):
            return "failed"
    return "passed"


def normalize_report(
    path: str | Path,
    fmt: str,
    *,
    allow_skipped: bool = False,
    expected_ac_ids: Iterable[str] = (),
    command: Iterable[str] = (),
) -> NormalizedBddReport:
    """Normalize the report at *path* of format *fmt* into a report.

    Parameters
    ----------
    path:
        Path to the runner-native report.
    fmt:
        One of :data:`SUPPORTED_FORMATS`.
    allow_skipped:
        When False (default), ``skipped`` scenarios are treated as ``failed``
        (fail-closed). When True, ``skipped`` scenarios do not fail the report.
    expected_ac_ids:
        Acceptance criteria that must each have at least one passing linked
        scenario. Missing coverage fails the report.
    command:
        The original command that produced the native report (preserved verbatim).
    """
    results = _parse(path, fmt)
    criteria = summarize_criteria(results, allow_skipped=allow_skipped)
    coverage = require_expected_coverage(
        expected_ac_ids, results, allow_skipped=allow_skipped
    )
    status = _overall_status(results, coverage.status, allow_skipped)
    counts = _count_by_status(results)

    return NormalizedBddReport(
        runner=fmt,
        source_report=str(path),
        results=results,
        criteria=criteria,
        command=tuple(command),
        status=status,
        scenarios=len(results),
        passed=counts["passed"],
        failed=counts["failed"],
        undefined=counts["undefined"],
        pending=counts["pending"],
        skipped=counts["skipped"],
        ambiguous=counts["ambiguous"],
        evidence=(str(path),),
    )


def _scenario_to_normalized_dict(result: ScenarioResult) -> dict[str, Any]:
    ids = extract_ids_from_tags(result.tags)
    payload: dict[str, Any] = {
        "feature": result.feature,
        "scenario": result.name,
        "status": result.status,
        "tags": list(result.tags),
        "bdd_ids": list(ids.bdd_ids),
        "acceptance_criteria": list(ids.ac_ids),
        "evidence": list(result.evidence),
    }
    if result.rule is not None:
        payload["rule"] = result.rule
    if result.duration_ms is not None:
        payload["duration_ms"] = result.duration_ms
    return payload


def to_normalized_dict(report: NormalizedBddReport) -> dict[str, Any]:
    """Serialize *report* to the full normalized JSON shape (schema version 2)."""
    return {
        "schema_version": report.schema_version,
        "generated_by": report.generated_by,
        "runner": report.runner,
        "command": list(report.command),
        "status": report.status,
        "scenarios": report.scenarios,
        "passed": report.passed,
        "failed": report.failed,
        "undefined": report.undefined,
        "pending": report.pending,
        "skipped": report.skipped,
        "ambiguous": report.ambiguous,
        "source_report": report.source_report,
        "evidence": list(report.evidence),
        "results": [_scenario_to_normalized_dict(r) for r in report.results],
        "criteria": [
            {
                "criterion_id": c.criterion_id,
                "status": c.status,
                "scenario_ids": list(c.scenario_ids),
                "evidence": list(c.evidence),
            }
            for c in report.criteria
        ],
    }


def to_evidence_dict(report: NormalizedBddReport, task_id: str) -> dict[str, Any]:
    """Serialize *report* to the Taskledger BDD evidence JSON shape."""
    scenarios: list[dict[str, Any]] = []
    for result in report.results:
        ids = extract_ids_from_tags(result.tags)
        scenarios.append(
            {
                "bdd_id": (ids.bdd_ids[0] if ids.bdd_ids else ""),
                "status": result.status,
                "tags": list(result.tags),
                "name": result.name,
            }
        )
    return {
        "schema_version": report.schema_version,
        "generated_by": report.generated_by,
        "task_id": task_id,
        "source_report": report.source_report,
        "status": report.status,
        "criteria": [
            {
                "criterion_id": c.criterion_id,
                "status": c.status,
                "bdd_ids": list(c.scenario_ids),
                "evidence": list(c.evidence),
            }
            for c in report.criteria
        ],
        "scenarios": scenarios,
    }


def write_normalized_json(report: NormalizedBddReport, path: str | Path) -> None:
    """Write *report* as the full normalized JSON to *path*."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        to_normalized_dict(report), indent=2, sort_keys=True, ensure_ascii=False
    )
    out.write_text(payload + "\n", encoding="utf-8")


def write_evidence_json(
    report: NormalizedBddReport, task_id: str, path: str | Path
) -> None:
    """Write *report* as the Taskledger BDD evidence JSON to *path*."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        to_evidence_dict(report, task_id), indent=2, sort_keys=True, ensure_ascii=False
    )
    out.write_text(payload + "\n", encoding="utf-8")
