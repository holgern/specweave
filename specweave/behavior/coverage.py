"""Static coverage checks between behavior specs and plain pytest tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from specweave.behavior.common import (
    canonical_test_path,
    display_path,
    iter_feature_scenarios,
    scenario_identifier,
)
from specweave.config import BEHAVIOR_FEATURES_DIR, PYTEST_TESTS_DIR
from specweave.gherkin.lint import collect_feature_files
from specweave.gherkin.parser import parse_feature
from specweave.python_inspect.ast_reader import (
    SpecweaveTestMapping,
    collect_specweave_tests,
)

_DEPRECATED_SCAN_PATHS = (
    Path("specs/bdd/features"),
    Path("tests/bdd/features"),
    Path("tests/behavior/features"),
    Path("tests/bdd"),
    Path("tests/behavior"),
)


def _test_files(tests_dir: Path) -> list[Path]:
    return sorted(
        candidate for candidate in tests_dir.rglob("*.py") if candidate.is_file()
    )


def _normalize_nodeid(nodeid: str) -> str:
    if "::" not in nodeid:
        return nodeid
    file_part, remainder = nodeid.split("::", 1)
    return f"{display_path(Path(file_part))}::{remainder}"


def _mapping_lookup(
    mappings: list[SpecweaveTestMapping],
) -> tuple[
    dict[tuple[str, str], list[SpecweaveTestMapping]],
    dict[str, list[SpecweaveTestMapping]],
]:
    by_key: dict[tuple[str, str], list[SpecweaveTestMapping]] = {}
    by_name: dict[str, list[SpecweaveTestMapping]] = {}
    for mapping in mappings:
        by_key.setdefault((mapping.feature, mapping.scenario), []).append(mapping)
        by_name.setdefault(mapping.function_name, []).append(mapping)
    return by_key, by_name


def _deprecated_paths(project_root: Path) -> list[str]:
    findings: list[str] = []
    for path in _DEPRECATED_SCAN_PATHS:
        candidate = project_root / path
        if not candidate.exists():
            continue
        if candidate.is_file():
            findings.append(display_path(candidate))
            continue
        for found in sorted(candidate.rglob("*")):
            if found.is_file():
                findings.append(display_path(found))
    return findings


def _forbidden_pytest_bdd_usages(test_files: list[Path]) -> list[str]:
    findings: list[str] = []
    for path in test_files:
        text = path.read_text(encoding="utf-8")
        if "pytest_bdd" in text or "scenarios(" in text:
            findings.append(display_path(path))
    return findings


def build_behavior_coverage(
    *,
    features_dir: Path = BEHAVIOR_FEATURES_DIR,
    tests_dir: Path = PYTEST_TESTS_DIR,
) -> dict[str, Any]:
    """Build the coverage report for canonical behavior specs."""

    feature_files = collect_feature_files((features_dir,))
    test_files = _test_files(tests_dir)
    mappings = collect_specweave_tests(test_files)
    mapping_by_key, _ = _mapping_lookup(mappings)

    feature_refs = {display_path(path) for path in feature_files}
    expected_scenarios: dict[tuple[str, str], Path] = {}
    missing_bindings: list[dict[str, str]] = []
    stale_bindings: list[dict[str, str]] = []
    features_bound = 0
    scenarios_total = 0
    scenarios_bound = 0

    for feature_path in feature_files:
        feature = parse_feature(
            feature_path.read_text(encoding="utf-8"),
            source_path=feature_path,
        )
        feature_ref = display_path(feature_path)
        expected_test_file = canonical_test_path(feature_path, tests_dir=tests_dir)
        if expected_test_file.exists():
            features_bound += 1
        else:
            missing_bindings.append(
                {
                    "feature": feature_ref,
                    "test_file": display_path(expected_test_file),
                    "reason": "missing_test_file",
                }
            )
        for _, scenario in iter_feature_scenarios(feature):
            scenarios_total += 1
            scenario_ref = scenario_identifier(scenario)
            expected_scenarios[(feature_ref, scenario_ref)] = expected_test_file
            manual = {"manual", "waived"} & set(scenario.tags)
            linked = mapping_by_key.get((feature_ref, scenario_ref), [])
            if linked:
                scenarios_bound += 1
            elif not manual:
                missing_bindings.append(
                    {
                        "feature": feature_ref,
                        "scenario": scenario_ref,
                        "test_file": display_path(expected_test_file),
                        "reason": "missing_scenario_binding",
                    }
                )

    for mapping in mappings:
        key = (mapping.feature, mapping.scenario)
        if key not in expected_scenarios:
            stale_bindings.append(
                {
                    "feature": mapping.feature,
                    "scenario": mapping.scenario,
                    "test_file": mapping.test_file,
                    "nodeid": mapping.nodeid,
                    "reason": (
                        "missing_feature"
                        if mapping.feature not in feature_refs
                        else "missing_scenario"
                    ),
                }
            )

    deprecated_paths = _deprecated_paths(features_dir.resolve().parent.parent.parent)
    forbidden_pytest_bdd_usages = _forbidden_pytest_bdd_usages(test_files)

    return {
        "schema_version": 1,
        "features_total": len(feature_files),
        "scenarios_total": scenarios_total,
        "features_bound": features_bound,
        "scenarios_bound": scenarios_bound,
        "missing_bindings": missing_bindings,
        "stale_bindings": stale_bindings,
        "deprecated_paths": deprecated_paths,
        "forbidden_pytest_bdd_usages": forbidden_pytest_bdd_usages,
    }


def write_coverage_json(data: dict[str, Any], path: str | Path) -> None:
    """Write behavior coverage *data* to *path*."""

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
