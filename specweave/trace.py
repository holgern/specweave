"""Behavior-centered trace bundle extraction."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from specweave.behavior.common import (
    display_path,
    iter_feature_scenarios,
    scenario_identifier,
)
from specweave.config import BEHAVIOR_FEATURES_DIR, PYTEST_TESTS_DIR
from specweave.gherkin.lint import collect_feature_files
from specweave.gherkin.parser import parse_feature
from specweave.python_inspect.ast_reader import collect_specweave_tests


def _test_files(tests_dir: Path) -> list[Path]:
    if not tests_dir.exists():
        return []
    return sorted(path for path in tests_dir.rglob("*.py") if path.is_file())


def _normalize_bdd_ref(ref: str) -> str:
    return ref[1:] if ref.startswith("@") else ref


def _gap(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def _load_json_files(root: Path) -> list[tuple[Path, Any]]:
    if not root.exists():
        return []
    files = [root] if root.is_file() else sorted(root.rglob("*.json"))
    loaded: list[tuple[Path, Any]] = []
    for path in files:
        try:
            loaded.append((path, json.loads(path.read_text(encoding="utf-8"))))
        except json.JSONDecodeError:
            continue
    return loaded


def _contains_token(value: Any, token: str) -> bool:
    if isinstance(value, str):
        return value == token or value == f"@{token}"
    if isinstance(value, list):
        return any(_contains_token(item, token) for item in value)
    if isinstance(value, dict):
        return any(_contains_token(item, token) for item in value.values())
    return False


def _evidence_refs(evidence_dir: Path, bdd_id: str) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    for path, data in _load_json_files(evidence_dir):
        if not _contains_token(data, bdd_id):
            continue
        status = "unknown"
        if isinstance(data, dict):
            raw_status = data.get("overall_status") or data.get("status")
            if isinstance(raw_status, str):
                status = raw_status
        refs.append({"path": display_path(path), "status": status})
    return refs


def _taskledger_refs(mapping_dir: Path, bdd_id: str) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    for path, data in _load_json_files(mapping_dir):
        if _contains_token(data, bdd_id):
            refs.append({"path": display_path(path)})
    return refs


def build_trace_bundle(
    target: str,
    *,
    features_dir: Path = BEHAVIOR_FEATURES_DIR,
    tests_dir: Path = PYTEST_TESTS_DIR,
    evidence_dir: Path = Path("specs/behavior/evidence"),
    taskledger_mappings: Path = Path("specs/behavior/mappings/taskledger"),
) -> dict[str, Any]:
    """Return a normalized trace bundle for a BDD id or feature path."""

    feature_files = (
        collect_feature_files((Path(target),))
        if Path(target).exists()
        else collect_feature_files((features_dir,))
    )
    mappings = collect_specweave_tests(_test_files(tests_dir))
    normalized_target = _normalize_bdd_ref(target)
    traces: list[dict[str, Any]] = []

    for feature_path in feature_files:
        feature = parse_feature(
            feature_path.read_text(encoding="utf-8"), source_path=feature_path
        )
        feature_ref = display_path(feature_path)
        for rule, scenario in iter_feature_scenarios(feature):
            bdd_ids = [tag for tag in scenario.tags if tag.startswith("bdd-")]
            if Path(target).exists():
                matched = True
            else:
                matched = normalized_target in bdd_ids
            if not matched:
                continue
            scenario_ref = scenario_identifier(scenario)
            test_refs = [
                {
                    "test_file": mapping.test_file,
                    "nodeid": mapping.nodeid,
                    "function_name": mapping.function_name,
                    "line": mapping.line,
                    "source": mapping.source,
                }
                for mapping in mappings
                if mapping.feature == feature_ref and mapping.scenario == scenario_ref
            ]
            evidence_refs = []
            task_refs = []
            for bdd_id in bdd_ids:
                evidence_refs.extend(_evidence_refs(evidence_dir, bdd_id))
                task_refs.extend(_taskledger_refs(taskledger_mappings, bdd_id))
            gaps: list[dict[str, str]] = []
            if not test_refs:
                gaps.append(
                    _gap(
                        "missing_pytest_mapping",
                        "No explicit pytest mapping was found for this scenario.",
                    )
                )
            if not evidence_refs:
                gaps.append(
                    _gap(
                        "missing_evidence",
                        "No imported evidence references this scenario.",
                    )
                )
            traces.append(
                {
                    "schema": "combi.trace.v1",
                    "producer": "specweave",
                    "subject": {
                        "type": "bdd_scenario",
                        "id": bdd_ids[0] if bdd_ids else scenario.title,
                    },
                    "feature": {"path": feature_ref, "title": feature.title},
                    "rule": {"title": rule.title, "tags": list(rule.tags)}
                    if rule
                    else None,
                    "scenario": {
                        "title": scenario.title,
                        "line": scenario.line,
                        "tags": list(scenario.tags),
                    },
                    "task_ids": sorted(
                        {tag for tag in scenario.tags if tag.startswith("task-")}
                    ),
                    "ac_ids": sorted(
                        {tag for tag in scenario.tags if tag.startswith("ac-")}
                    ),
                    "bdd_ids": bdd_ids,
                    "archledger_refs": [],
                    "source_refs": [feature_ref],
                    "test_refs": test_refs,
                    "evidence_refs": evidence_refs,
                    "taskledger_refs": task_refs,
                    "status": {
                        "evidence": evidence_refs[0]["status"]
                        if evidence_refs
                        else "missing"
                    },
                    "gaps": gaps,
                }
            )
    if not traces:
        return {
            "schema": "combi.trace.v1",
            "producer": "specweave",
            "target": target,
            "traces": [],
            "gaps": [
                _gap(
                    "trace_target_not_found", "No matching behavior scenario was found."
                )
            ],
        }
    return {
        "schema": "combi.trace.v1",
        "producer": "specweave",
        "target": target,
        "traces": traces,
        "gaps": [],
    }
