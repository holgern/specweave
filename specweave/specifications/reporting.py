"""Normalize pytest/JUnit specification evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from specweave.behavior.common import display_path
from specweave.python_inspect.ast_reader import (
    SpecweaveTestMapping,
    collect_specweave_tests,
    is_specification_mapping,
)
from specweave.reports.junit_xml import parse_pytest_junit_cases


def _normalize_nodeid(nodeid: str) -> str:
    if "::" not in nodeid:
        return nodeid
    file_part, remainder = nodeid.split("::", 1)
    return f"{display_path(Path(file_part))}::{remainder}"


def _resolve_project_relative(path_text: str, reference_path: Path) -> Path:
    candidate = Path(path_text)
    if candidate.exists():
        return candidate
    if candidate.is_absolute():
        return candidate
    for ancestor in (reference_path.parent, *reference_path.parents):
        resolved = ancestor / candidate
        if resolved.exists():
            return resolved
    return candidate


def _manifest_mappings(manifest_path: Path) -> list[SpecweaveTestMapping]:
    if not manifest_path.exists():
        return []
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    requirements = payload.get("requirements")
    if not isinstance(requirements, list):
        return []
    mappings: list[SpecweaveTestMapping] = []
    for requirement in requirements:
        if not isinstance(requirement, dict):
            continue
        spec_ref = requirement.get("path")
        requirement_id = requirement.get("id")
        verification = requirement.get("verification", [])
        if not (
            isinstance(spec_ref, str)
            and isinstance(requirement_id, str)
            and isinstance(verification, list)
        ):
            continue
        for ref in verification:
            if not isinstance(ref, dict):
                continue
            if ref.get("kind") != "pytest":
                continue
            target = ref.get("target")
            if not isinstance(target, str):
                continue
            file_part, _, remainder = target.partition("::")
            resolved_file = _resolve_project_relative(file_part, manifest_path)
            normalized_nodeid = (
                f"{display_path(resolved_file)}::{remainder}"
                if remainder
                else display_path(resolved_file)
            )
            mappings.append(
                SpecweaveTestMapping(
                    function_name=remainder or target.split("::")[-1],
                    test_file=display_path(resolved_file),
                    nodeid=normalized_nodeid,
                    line=int(requirement.get("line", 0) or 0),
                    source="manifest",
                    spec=spec_ref,
                    requirement=requirement_id,
                )
            )
    return mappings


def _mapping_indexes(
    tests_dir: Path, manifest_path: Path
) -> tuple[
    dict[str, list[SpecweaveTestMapping]],
    dict[tuple[str, str], list[SpecweaveTestMapping]],
    dict[str, list[SpecweaveTestMapping]],
]:
    mappings = [
        mapping
        for mapping in collect_specweave_tests(
            sorted(
                candidate
                for candidate in tests_dir.rglob("*.py")
                if candidate.is_file()
            )
        )
        if is_specification_mapping(mapping)
    ]
    mappings.extend(_manifest_mappings(manifest_path))
    by_nodeid: dict[str, list[SpecweaveTestMapping]] = {}
    by_file_and_function: dict[tuple[str, str], list[SpecweaveTestMapping]] = {}
    by_function: dict[str, list[SpecweaveTestMapping]] = {}
    for mapping in mappings:
        normalized_nodeid = _normalize_nodeid(mapping.nodeid)
        by_nodeid.setdefault(normalized_nodeid, []).append(mapping)
        by_file_and_function.setdefault(
            (mapping.test_file, mapping.function_name),
            [],
        ).append(mapping)
        by_function.setdefault(mapping.function_name, []).append(mapping)
    return by_nodeid, by_file_and_function, by_function


def _aggregate_status(statuses: list[str]) -> str:
    if any(
        status in {"failed", "error", "undefined", "pending", "ambiguous", "skipped"}
        for status in statuses
    ):
        return "failed"
    return "passed" if any(status == "passed" for status in statuses) else "failed"


def import_pytest_report(
    report: Path,
    *,
    tests_dir: Path,
    manifest_path: Path,
) -> dict[str, Any]:
    """Import a pytest/JUnit report into specifications evidence JSON."""
    by_nodeid, by_file_and_function, by_function = _mapping_indexes(
        tests_dir, manifest_path
    )
    mapped_results: dict[tuple[str, str], dict[str, Any]] = {}
    unmapped: list[dict[str, str]] = []

    for case in parse_pytest_junit_cases(report):
        candidate_mappings: list[SpecweaveTestMapping] = []
        normalized_nodeid = _normalize_nodeid(case.nodeid)
        if normalized_nodeid:
            candidate_mappings.extend(by_nodeid.get(normalized_nodeid, []))
        function_name = case.name.split("[", 1)[0]
        if case.test_file:
            candidate_mappings.extend(
                by_file_and_function.get(
                    (display_path(Path(case.test_file)), function_name),
                    [],
                )
            )
        candidate_mappings.extend(by_function.get(function_name, []))

        unique_mappings = {
            (mapping.spec, mapping.requirement, mapping.nodeid): mapping
            for mapping in candidate_mappings
            if mapping.spec is not None and mapping.requirement is not None
        }
        if not unique_mappings:
            unmapped.append(
                {
                    "test_file": display_path(Path(case.test_file))
                    if case.test_file
                    else "",
                    "nodeid": normalized_nodeid,
                    "name": case.name,
                    "status": case.status,
                }
            )
            continue

        for mapping in unique_mappings.values():
            key = (mapping.spec or "", mapping.requirement or "")
            bucket = mapped_results.setdefault(
                key,
                {
                    "id": mapping.requirement,
                    "spec": mapping.spec,
                    "statuses": [],
                    "tests": [],
                },
            )
            bucket["statuses"].append(case.status)
            normalized_case_nodeid = _normalize_nodeid(case.nodeid)
            if normalized_case_nodeid not in bucket["tests"]:
                bucket["tests"].append(normalized_case_nodeid)

    results = []
    for key in sorted(mapped_results):
        item = mapped_results[key]
        results.append(
            {
                "id": item["id"],
                "spec": item["spec"],
                "status": _aggregate_status(item["statuses"]),
                "tests": item["tests"],
            }
        )

    payload: dict[str, Any] = {
        "schema": "specweave.evidence.v1",
        "mode": "specifications",
        "source": {
            "format": "junit-xml",
            "path": display_path(report),
        },
        "results": results,
    }
    if unmapped:
        payload["unmapped"] = unmapped
    return payload


def write_specification_evidence_json(data: dict[str, Any], path: str | Path) -> None:
    """Write imported specifications evidence *data* to *path*."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
