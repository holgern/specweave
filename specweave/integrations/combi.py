"""Read-only cross-ledger integration diagnostics."""

from __future__ import annotations

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
from specweave.trace import _evidence_refs, _load_json_files, _taskledger_refs


def _test_files(tests_dir: Path) -> list[Path]:
    if not tests_dir.exists():
        return []
    return sorted(path for path in tests_dir.rglob("*.py") if path.is_file())


def _gap(
    code: str, message: str, *, severity: str = "warning", ref: str = ""
) -> dict[str, str]:
    return {"code": code, "severity": severity, "ref": ref, "message": message}


def _taskledger_ac_ids(mapping_dir: Path) -> set[str]:
    ac_ids: set[str] = set()
    for _, data in _load_json_files(mapping_dir):
        stack = [data]
        while stack:
            item = stack.pop()
            if isinstance(item, dict):
                for key, value in item.items():
                    if key in {
                        "ac_id",
                        "acceptance_criterion",
                        "acceptance_criterion_id",
                    } and isinstance(value, str):
                        ac_ids.add(value.removeprefix("@"))
                    else:
                        stack.append(value)
            elif isinstance(item, list):
                stack.extend(item)
            elif isinstance(item, str) and item.startswith("ac-"):
                ac_ids.add(item)
    return ac_ids


def run_combi_check(
    *,
    features_dir: Path = BEHAVIOR_FEATURES_DIR,
    tests_dir: Path = PYTEST_TESTS_DIR,
    taskledger_mappings: Path = Path("specs/behavior/mappings/taskledger"),
    evidence_dir: Path = Path("specs/behavior/evidence"),
    archledger_dir: Path = Path(".archledger"),
) -> dict[str, Any]:
    """Audit Taskledger, SpecWeave, pytest, evidence, and Archledger links."""

    feature_files = collect_feature_files((features_dir,))
    mappings = collect_specweave_tests(_test_files(tests_dir))
    mapping_keys = {(mapping.feature, mapping.scenario) for mapping in mappings}
    gaps: list[dict[str, str]] = []
    scenarios: list[dict[str, Any]] = []
    seen_ac_ids: set[str] = set()

    for feature_path in feature_files:
        feature = parse_feature(
            feature_path.read_text(encoding="utf-8"), source_path=feature_path
        )
        feature_ref = display_path(feature_path)
        for _, scenario in iter_feature_scenarios(feature):
            bdd_ids = [tag for tag in scenario.tags if tag.startswith("bdd-")]
            ac_ids = [tag for tag in scenario.tags if tag.startswith("ac-")]
            seen_ac_ids.update(ac_ids)
            scenario_ref = scenario_identifier(scenario)
            ref = f"{feature_ref}::{scenario_ref}"
            if not bdd_ids:
                gaps.append(
                    _gap(
                        "missing_bdd_id",
                        "Scenario has no stable @bdd-* id.",
                        severity="error",
                        ref=ref,
                    )
                )
            if (feature_ref, scenario_ref) not in mapping_keys:
                gaps.append(
                    _gap(
                        "missing_pytest_mapping",
                        "Scenario has no explicit pytest mapping.",
                        ref=ref,
                    )
                )
            for bdd_id in bdd_ids:
                if not _evidence_refs(evidence_dir, bdd_id):
                    gaps.append(
                        _gap(
                            "missing_evidence",
                            "Scenario has no imported evidence artifact.",
                            ref=ref,
                        )
                    )
                _taskledger_refs(taskledger_mappings, bdd_id)
            scenarios.append(
                {
                    "feature": feature_ref,
                    "scenario": scenario.title,
                    "bdd_ids": bdd_ids,
                    "ac_ids": ac_ids,
                }
            )

    for mapping in mappings:
        if mapping.test_file and not Path(mapping.test_file).exists():
            gaps.append(
                _gap(
                    "mapped_pytest_file_missing",
                    "Mapped pytest file does not exist.",
                    severity="error",
                    ref=mapping.test_file,
                )
            )

    for ac_id in sorted(_taskledger_ac_ids(taskledger_mappings) - seen_ac_ids):
        gaps.append(
            _gap(
                "unlinked_taskledger_ac",
                "Taskledger acceptance criterion has no linked behavior "
                "scenario or waiver.",
                severity="error",
                ref=ac_id,
            )
        )

    if archledger_dir.exists():
        archledger_status = "available"
    else:
        archledger_status = "not_configured"

    return {
        "schema": "specweave.combi-check.v1",
        "producer": "specweave",
        "features_dir": display_path(features_dir),
        "tests_dir": display_path(tests_dir),
        "taskledger_mappings": display_path(taskledger_mappings),
        "evidence_dir": display_path(evidence_dir),
        "archledger": {
            "path": display_path(archledger_dir),
            "status": archledger_status,
        },
        "scenarios": scenarios,
        "gaps": gaps,
        "summary": {
            "scenario_count": len(scenarios),
            "gap_count": len(gaps),
            "error_count": sum(1 for gap in gaps if gap["severity"] == "error"),
        },
    }
