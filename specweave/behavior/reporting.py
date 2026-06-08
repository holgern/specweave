"""Normalize pytest/JUnit behavior evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from specweave.behavior.common import display_path
from specweave.config import BEHAVIOR_MANIFEST_PATH, PYTEST_TESTS_DIR
from specweave.python_inspect.ast_reader import (
    SpecweaveTestMapping,
    collect_specweave_tests,
)
from specweave.reports.junit_xml import parse_pytest_junit_cases


def _normalize_nodeid(nodeid: str) -> str:
    if "::" not in nodeid:
        return nodeid
    file_part, remainder = nodeid.split("::", 1)
    return f"{display_path(Path(file_part))}::{remainder}"


def _manifest_mappings(manifest_path: Path) -> list[SpecweaveTestMapping]:
    if not manifest_path.exists():
        return []
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    features = payload.get("features")
    if not isinstance(features, list):
        return []
    mappings: list[SpecweaveTestMapping] = []
    for feature in features:
        if not isinstance(feature, dict):
            continue
        feature_ref = feature.get("path")
        if not isinstance(feature_ref, str):
            continue
        scenario_groups = []
        scenarios = feature.get("scenarios")
        if isinstance(scenarios, list):
            scenario_groups.append(scenarios)
        rules = feature.get("rules")
        if isinstance(rules, list):
            for rule in rules:
                if isinstance(rule, dict) and isinstance(rule.get("scenarios"), list):
                    scenario_groups.append(rule["scenarios"])
        for group in scenario_groups:
            for scenario in group:
                if not isinstance(scenario, dict):
                    continue
                automation = scenario.get("automation")
                if not isinstance(automation, dict):
                    continue
                test_file = automation.get("test_file")
                nodeid = automation.get("nodeid")
                scenario_id = scenario.get("id")
                if not (
                    isinstance(test_file, str)
                    and isinstance(nodeid, str)
                    and isinstance(scenario_id, str)
                ):
                    continue
                function_name = nodeid.split("::")[-1] if "::" in nodeid else nodeid
                mappings.append(
                    SpecweaveTestMapping(
                        function_name=function_name,
                        test_file=test_file,
                        nodeid=nodeid,
                        feature=feature_ref,
                        scenario=(
                            scenario_id
                            if scenario_id.startswith("@")
                            else f"@{scenario_id}"
                        ),
                        line=0,
                        source="manifest",
                    )
                )
    return mappings


def _mapping_indexes(
    tests_dir: Path, manifest_path: Path
) -> tuple[
    dict[str, SpecweaveTestMapping],
    dict[tuple[str, str], SpecweaveTestMapping],
    dict[str, list[SpecweaveTestMapping]],
]:
    mappings = collect_specweave_tests(
        sorted(
            candidate for candidate in tests_dir.rglob("*.py") if candidate.is_file()
        )
    )
    mappings.extend(_manifest_mappings(manifest_path))
    by_nodeid: dict[str, SpecweaveTestMapping] = {}
    by_file_and_function: dict[tuple[str, str], SpecweaveTestMapping] = {}
    by_function: dict[str, list[SpecweaveTestMapping]] = {}
    for mapping in mappings:
        normalized_nodeid = _normalize_nodeid(mapping.nodeid)
        by_nodeid.setdefault(normalized_nodeid, mapping)
        by_file_and_function.setdefault(
            (mapping.test_file, mapping.function_name),
            mapping,
        )
        by_function.setdefault(mapping.function_name, []).append(mapping)
    return by_nodeid, by_file_and_function, by_function


def import_pytest_report(
    report: Path,
    *,
    tests_dir: Path = PYTEST_TESTS_DIR,
    manifest_path: Path = BEHAVIOR_MANIFEST_PATH,
) -> dict[str, Any]:
    """Import a pytest/JUnit report into behavior evidence JSON."""

    by_nodeid, by_file_and_function, by_function = _mapping_indexes(
        tests_dir, manifest_path
    )
    results: list[dict[str, str]] = []
    unmapped: list[dict[str, str]] = []

    for case in parse_pytest_junit_cases(report):
        mapping = None
        normalized_nodeid = _normalize_nodeid(case.nodeid)
        if normalized_nodeid:
            mapping = by_nodeid.get(normalized_nodeid)
        function_name = case.name.split("[", 1)[0]
        if mapping is None and case.test_file:
            mapping = by_file_and_function.get(
                (display_path(Path(case.test_file)), function_name)
            )
        if mapping is None and len(by_function.get(function_name, ())) == 1:
            mapping = by_function[function_name][0]
        if mapping is None:
            unmapped.append(
                {
                    "test_file": (
                        display_path(Path(case.test_file)) if case.test_file else ""
                    ),
                    "nodeid": normalized_nodeid,
                    "name": case.name,
                    "status": case.status,
                }
            )
            continue
        results.append(
            {
                "feature": mapping.feature,
                "scenario": mapping.scenario,
                "test_file": mapping.test_file,
                "nodeid": mapping.nodeid,
                "status": case.status,
            }
        )

    payload: dict[str, Any] = {
        "schema_version": 1,
        "backend": "pytest",
        "report": display_path(report),
        "results": results,
    }
    if unmapped:
        payload["unmapped"] = unmapped
    return payload


def write_pytest_evidence_json(data: dict[str, Any], path: str | Path) -> None:
    """Write imported pytest evidence *data* to *path*."""

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
