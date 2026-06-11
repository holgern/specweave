"""Behavior-centered trace bundle extraction."""

from __future__ import annotations

import json
import re
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
from specweave.python_inspect.ast_reader import (
    collect_specweave_tests,
    is_specification_mapping,
)
from specweave.specifications.parser import (
    collect_specification_files,
    parse_specification,
)


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


def _specification_evidence_refs(
    evidence_dir: Path, requirement_id: str
) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    for path, data in _load_json_files(evidence_dir):
        if not isinstance(data, dict):
            continue
        results = data.get("results")
        if not isinstance(results, list):
            continue
        for result in results:
            if not isinstance(result, dict):
                continue
            if result.get("id") != requirement_id:
                continue
            status = result.get("status")
            refs.append(
                {
                    "path": display_path(path),
                    "status": status if isinstance(status, str) else "unknown",
                }
            )
            break
    return refs


def _looks_like_requirement_id(target: str) -> bool:
    return bool(
        re.match(
            r"^(REQ|INV|IF|DATA|NFR|NGOAL|RISK|OPEN)-[A-Z0-9][A-Z0-9-]*$",
            target,
        )
    )


def build_trace_bundle(
    target: str,
    *,
    features_dir: Path = BEHAVIOR_FEATURES_DIR,
    tests_dir: Path = PYTEST_TESTS_DIR,
    evidence_dir: Path = Path("specs/behavior/evidence"),
    taskledger_mappings: Path = Path("specs/behavior/mappings/taskledger"),
    specifications_dir: Path = Path("specs/specifications"),
    specifications_evidence_dir: Path = Path("specs/specifications/evidence"),
    specifications_taskledger_mappings: Path = Path(
        "specs/specifications/mappings/taskledger"
    ),
) -> dict[str, Any]:
    """Return a normalized trace bundle for a BDD id, requirement id, or spec path."""

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
    specification_files = (
        collect_specification_files([Path(target)])
        if Path(target).exists() and str(target).endswith(".spec.md")
        else collect_specification_files([specifications_dir])
    )
    requirement_target = target if _looks_like_requirement_id(target) else None
    specification_mappings = [
        mapping for mapping in mappings if is_specification_mapping(mapping)
    ]
    for specification_path in specification_files:
        document = parse_specification(specification_path)
        spec_ref = display_path(specification_path)
        for requirement in document.requirements:
            if Path(target).exists() and str(target).endswith(".spec.md"):
                matched = True
            else:
                matched = requirement.id == requirement_target
            if not matched:
                continue
            test_refs = [
                {
                    "test_file": mapping.test_file,
                    "nodeid": mapping.nodeid,
                    "function_name": mapping.function_name,
                    "line": mapping.line,
                    "source": mapping.source,
                }
                for mapping in specification_mappings
                if mapping.spec == spec_ref and mapping.requirement == requirement.id
            ]
            evidence_refs = _specification_evidence_refs(
                specifications_evidence_dir, requirement.id
            )
            task_refs = _taskledger_refs(
                specifications_taskledger_mappings, requirement.id
            )
            gaps: list[dict[str, str]] = []
            if not test_refs:
                gaps.append(
                    _gap(
                        "missing_pytest_mapping",
                        "No explicit pytest mapping was found for this requirement.",
                    )
                )
            if not evidence_refs:
                gaps.append(
                    _gap(
                        "missing_evidence",
                        "No imported evidence references this requirement.",
                    )
                )
            traces.append(
                {
                    "schema": "combi.trace.v1",
                    "producer": "specweave",
                    "subject": {
                        "type": "requirement",
                        "id": requirement.id,
                    },
                    "specification": {
                        "path": spec_ref,
                        "title": document.title,
                        "document_id": document.spec_id,
                    },
                    "requirement": {
                        "title": requirement.title,
                        "line": requirement.line,
                        "status": requirement.status,
                        "kind": requirement.kind,
                    },
                    "source_refs": [spec_ref],
                    "test_refs": test_refs,
                    "evidence_refs": evidence_refs,
                    "taskledger_refs": task_refs,
                    "archledger_refs": [],
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
