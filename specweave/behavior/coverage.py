"""Static coverage checks between behavior specs and plain pytest tests."""

from __future__ import annotations

import ast
import json
import re
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
    PytestTestItem,
    SpecweaveTestMapping,
    collect_pytest_tests,
    collect_specweave_tests,
)

_DEPRECATED_SCAN_PATHS = (
    Path("specs/bdd/features"),
    Path("tests/bdd/features"),
    Path("tests/behavior/features"),
    Path("tests/bdd"),
    Path("tests/behavior"),
)
_VIEW_VALUES = frozenset({"feature", "test", "both"})
_SHOW_VALUES = frozenset(
    {"all", "gaps", "bound", "missing", "unmapped", "stale", "waived", "duplicate"}
)
_TOKEN_RE = re.compile(r"[A-Za-z0-9]+")
_IGNORED_TOKENS = frozenset(
    {"specs", "behavior", "features", "tests", "test", "feature", "python"}
)


def _test_files(tests_dir: Path) -> list[Path]:
    return sorted(
        candidate for candidate in tests_dir.rglob("*.py") if candidate.is_file()
    )


def _selected_test_files(tests_dir: Path, test_file: Path | None) -> list[Path]:
    if test_file is None:
        return _test_files(tests_dir)
    return [test_file] if test_file.is_file() else []


def _normalize_nodeid(nodeid: str) -> str:
    if "::" not in nodeid:
        return nodeid
    file_part, remainder = nodeid.split("::", 1)
    return f"{display_path(Path(file_part))}::{remainder}"


def _mapping_sort_key(mapping: SpecweaveTestMapping) -> tuple[str, str, str, int]:
    return mapping.feature, mapping.scenario, mapping.test_file, mapping.line


def _mapping_item(mapping: SpecweaveTestMapping) -> dict[str, Any]:
    return {
        "test_file": mapping.test_file,
        "nodeid": _normalize_nodeid(mapping.nodeid),
        "function_name": mapping.function_name,
        "line": mapping.line,
        "source": mapping.source,
    }


def _mapping_target(mapping: SpecweaveTestMapping) -> dict[str, Any]:
    return {
        "feature": mapping.feature,
        "scenario": mapping.scenario,
        "source": mapping.source,
    }


def _mapping_lookup(
    mappings: list[SpecweaveTestMapping],
) -> tuple[
    dict[tuple[str, str], list[SpecweaveTestMapping]],
    dict[str, list[SpecweaveTestMapping]],
]:
    by_key: dict[tuple[str, str], list[SpecweaveTestMapping]] = {}
    by_nodeid: dict[str, list[SpecweaveTestMapping]] = {}
    for mapping in mappings:
        by_key.setdefault((mapping.feature, mapping.scenario), []).append(mapping)
        by_nodeid.setdefault(_normalize_nodeid(mapping.nodeid), []).append(mapping)
    return by_key, by_nodeid


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
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        pytest_bdd_aliases: set[str] = set()
        scenarios_aliases: set[str] = set()
        forbidden = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "pytest_bdd":
                        pytest_bdd_aliases.add(alias.asname or alias.name)
                        forbidden = True
            elif isinstance(node, ast.ImportFrom) and node.module == "pytest_bdd":
                forbidden = True
                for alias in node.names:
                    if alias.name == "scenarios":
                        scenarios_aliases.add(alias.asname or alias.name)
            elif isinstance(node, ast.Call):
                if (
                    isinstance(node.func, ast.Name)
                    and node.func.id in scenarios_aliases
                ):
                    forbidden = True
                elif (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr == "scenarios"
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id in pytest_bdd_aliases
                ):
                    forbidden = True
        if forbidden:
            findings.append(display_path(path))
    return findings


def _feature_files(
    *,
    features_dir: Path,
    feature_path: Path | None,
) -> list[Path]:
    root = feature_path if feature_path is not None else features_dir
    return collect_feature_files((root,))


def _project_root(features_dir: Path) -> Path:
    return features_dir.resolve().parent.parent.parent


def _feature_status(scenarios: list[dict[str, Any]]) -> str:
    if not scenarios:
        return "missing"
    statuses = {scenario["status"] for scenario in scenarios}
    if statuses == {"waived"}:
        return "waived"
    if statuses <= {"bound", "duplicate", "waived"}:
        return "bound"
    if "bound" in statuses or "duplicate" in statuses or "waived" in statuses:
        return "partial"
    return "missing"


def _mapping_valid(
    mapping: SpecweaveTestMapping,
    expected_scenarios: dict[tuple[str, str], dict[str, Any]],
) -> bool:
    return (mapping.feature, mapping.scenario) in expected_scenarios


def _tokens(value: str) -> set[str]:
    return {
        token.lower()
        for token in _TOKEN_RE.findall(value.replace("-", " ").replace("_", " "))
        if token and token.lower() not in _IGNORED_TOKENS
    }


def _candidate_test_item(item: dict[str, Any], *, reason: str) -> dict[str, Any]:
    return {
        "test_file": item["test_file"],
        "nodeid": item["nodeid"],
        "function_name": item["function_name"],
        "line": item["line"],
        "reason": reason,
    }


def _intentional_unmapped_path(features_dir: Path, mapping_dir: Path | None) -> Path:
    if mapping_dir is not None:
        return mapping_dir / "intentional-unmapped.json"
    return features_dir.parent / "mappings" / "intentional-unmapped.json"


def _load_intentional_unmapped(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        items = raw
    elif isinstance(raw, dict):
        items = raw.get("items", [])
    else:
        return {}

    waivers: dict[str, dict[str, str]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        nodeid = str(item.get("nodeid") or "").strip()
        if not nodeid:
            continue
        reason = str(item.get("reason") or "intentional-unmapped").strip()
        waivers[_normalize_nodeid(nodeid)] = {
            "reason": reason or "intentional-unmapped",
            "source": display_path(path),
        }
    return waivers


def _candidate_tests_for_missing_scenario(
    *,
    feature_ref: str,
    feature_title: str,
    expected_test_file: Path,
    unmapped_tests_by_file: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    expected_test_ref = display_path(expected_test_file)
    exact_matches = unmapped_tests_by_file.get(expected_test_ref, [])
    if exact_matches:
        return [
            _candidate_test_item(item, reason="same_expected_test_file")
            for item in exact_matches
        ]
    if expected_test_file.exists():
        return []

    feature_tokens = _tokens(feature_ref) | _tokens(feature_title)
    ranked_files: list[tuple[int, str, list[dict[str, Any]]]] = []
    for test_file, items in unmapped_tests_by_file.items():
        stem_tokens = _tokens(Path(test_file).stem)
        best_item_score = max(
            (
                len(
                    feature_tokens & (stem_tokens | _tokens(str(item["function_name"])))
                )
                for item in items
            ),
            default=0,
        )
        file_score = len(feature_tokens & stem_tokens) + best_item_score
        if file_score <= 0:
            continue
        ranked_files.append((file_score, test_file, items))
    ranked_files.sort(key=lambda item: (-item[0], item[1]))

    candidates: list[dict[str, Any]] = []
    for _, _, items in ranked_files:
        for item in items:
            candidates.append(_candidate_test_item(item, reason="token_overlap"))
            if len(candidates) >= 5:
                return candidates
    return candidates


def _test_inventory(
    test_items: list[PytestTestItem],
    mappings: list[SpecweaveTestMapping],
    expected_scenarios: dict[tuple[str, str], dict[str, Any]],
    intentional_unmapped: dict[str, dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    _, mappings_by_nodeid = _mapping_lookup(mappings)
    grouped: dict[str, list[dict[str, Any]]] = {}
    unmapped_tests: list[dict[str, Any]] = []

    for test_item in test_items:
        nodeid = _normalize_nodeid(test_item.nodeid)
        linked = sorted(
            mappings_by_nodeid.get(nodeid, []),
            key=_mapping_sort_key,
        )
        valid = [
            mapping for mapping in linked if _mapping_valid(mapping, expected_scenarios)
        ]
        primary_mapping = valid[0] if valid else (linked[0] if linked else None)
        waiver = (
            {
                "reason": test_item.unmapped_reason,
                "source": test_item.unmapped_source or "comment",
            }
            if test_item.unmapped_reason
            else intentional_unmapped.get(nodeid)
        )
        if not linked and waiver:
            status = "waived"
        elif not linked:
            status = "unmapped"
        elif valid:
            status = "mapped"
        else:
            status = "stale"

        entry = {
            "nodeid": nodeid,
            "function_name": test_item.function_name,
            "line": test_item.line,
            "status": status,
            "mapping": (
                None if primary_mapping is None else _mapping_target(primary_mapping)
            ),
            "waiver": waiver,
            "test_file": test_item.test_file,
        }
        grouped.setdefault(test_item.test_file, []).append(entry)
        if status == "unmapped":
            unmapped_tests.append(entry.copy())

    tests: list[dict[str, Any]] = []
    for test_file, items in sorted(grouped.items()):
        mapped = sum(1 for item in items if item["status"] == "mapped")
        unmapped = sum(1 for item in items if item["status"] == "unmapped")
        stale = sum(1 for item in items if item["status"] == "stale")
        waived = sum(1 for item in items if item["status"] == "waived")
        if mapped == len(items):
            status = "mapped"
        elif unmapped == len(items):
            status = "unmapped"
        elif stale == len(items):
            status = "stale"
        elif waived == len(items):
            status = "waived"
        else:
            status = "mixed"
        tests.append(
            {
                "test_file": test_file,
                "status": status,
                "tests_total": len(items),
                "mapped": mapped,
                "unmapped": unmapped,
                "stale": stale,
                "waived": waived,
                "items": items,
            }
        )
    return tests, sorted(
        unmapped_tests, key=lambda item: (item["test_file"], item["line"])
    )


def _summary_lines(data: dict[str, Any]) -> list[str]:
    scenario_summary = (
        f"features: {data['features_total']}, "
        f"scenarios: {data['scenarios_total']}, "
        f"bound: {data['scenarios_bound']}, "
        f"missing bindings: {len(data['missing_bindings'])}"
    )
    pytest_summary = (
        f"pytest tests: {data['pytest_tests_total']}, "
        f"mapped: {data['pytest_tests_mapped']}, "
        f"unmapped: {data['pytest_tests_unmapped']}, "
        f"waived: {data['pytest_tests_waived']}, "
        f"stale mappings: {data['pytest_mappings_stale']}"
    )
    return [
        f"Behavior coverage: {data['status']}",
        scenario_summary,
        pytest_summary,
        "",
    ]


def _feature_visible(status: str, show: str) -> bool:
    if show == "all":
        return True
    if show == "gaps":
        return status in {"missing", "duplicate"}
    if show == "bound":
        return status == "bound"
    return status == show


def _test_visible(status: str, show: str) -> bool:
    if show == "all":
        return True
    if show == "gaps":
        return status in {"unmapped", "stale"}
    if show == "bound":
        return status == "mapped"
    return status == show


def build_behavior_mapping_inventory(
    *,
    tests_dir: Path = PYTEST_TESTS_DIR,
) -> dict[str, Any]:
    """Return the raw explicit pytest mapping inventory."""

    mappings = sorted(
        collect_specweave_tests(_test_files(tests_dir)), key=_mapping_sort_key
    )
    items = [
        {
            "feature": mapping.feature,
            "scenario": mapping.scenario,
            "test_file": mapping.test_file,
            "nodeid": _normalize_nodeid(mapping.nodeid),
            "function_name": mapping.function_name,
            "line": mapping.line,
            "source": mapping.source,
        }
        for mapping in mappings
    ]
    return {
        "schema_version": 1,
        "command": "behavior mappings",
        "tests_dir": display_path(tests_dir),
        "mappings_total": len(items),
        "items": items,
    }


def build_behavior_coverage(
    *,
    features_dir: Path = BEHAVIOR_FEATURES_DIR,
    tests_dir: Path = PYTEST_TESTS_DIR,
    feature_path: Path | None = None,
    test_file: Path | None = None,
    mapping_dir: Path | None = None,
) -> dict[str, Any]:
    """Build the coverage report for canonical behavior specs."""

    feature_files = _feature_files(features_dir=features_dir, feature_path=feature_path)
    test_files = _selected_test_files(tests_dir, test_file)
    mappings = sorted(collect_specweave_tests(test_files), key=_mapping_sort_key)

    feature_specs: list[tuple[Path, Any, str, Path]] = []
    expected_scenarios: dict[tuple[str, str], dict[str, Any]] = {}
    for current_feature_path in feature_files:
        parsed_feature = parse_feature(
            current_feature_path.read_text(encoding="utf-8"),
            source_path=current_feature_path,
        )
        feature_ref = display_path(current_feature_path)
        expected_test_file = canonical_test_path(
            current_feature_path, tests_dir=tests_dir
        )
        feature_specs.append(
            (current_feature_path, parsed_feature, feature_ref, expected_test_file)
        )
        for _, scenario in iter_feature_scenarios(parsed_feature):
            expected_scenarios[(feature_ref, scenario_identifier(scenario))] = {
                "feature": feature_ref,
                "feature_title": parsed_feature.title,
                "title": scenario.title,
                "line": scenario.line or 0,
            }

    feature_refs = {feature_ref for _, _, feature_ref, _ in feature_specs}
    mapping_by_key, _ = _mapping_lookup(mappings)
    test_items = collect_pytest_tests(test_files)
    intentional_unmapped_path = _intentional_unmapped_path(features_dir, mapping_dir)
    intentional_unmapped = _load_intentional_unmapped(intentional_unmapped_path)
    tests, unmapped_tests = _test_inventory(
        test_items, mappings, expected_scenarios, intentional_unmapped
    )
    unmapped_tests_by_file: dict[str, list[dict[str, Any]]] = {}
    for item in unmapped_tests:
        unmapped_tests_by_file.setdefault(str(item["test_file"]), []).append(item)

    features: list[dict[str, Any]] = []
    missing_bindings: list[dict[str, Any]] = []
    stale_bindings: list[dict[str, Any]] = []
    duplicate_bindings: list[dict[str, Any]] = []
    features_bound = 0
    features_partial = 0
    features_missing = 0
    scenarios_total = 0
    scenarios_bound = 0
    scenarios_waived = 0

    for _, parsed_feature, feature_ref, expected_test_file in feature_specs:
        scenario_entries: list[dict[str, Any]] = []
        for _, scenario in iter_feature_scenarios(parsed_feature):
            scenarios_total += 1
            scenario_ref = scenario_identifier(scenario)
            linked = sorted(
                mapping_by_key.get((feature_ref, scenario_ref), []),
                key=_mapping_sort_key,
            )
            mappings_data = [_mapping_item(mapping) for mapping in linked]
            manual = bool({"manual", "waived"} & set(scenario.tags))
            expected_exists = expected_test_file.exists()
            candidate_tests: list[dict[str, Any]] = []

            if linked:
                status = "duplicate" if len(linked) > 1 else "bound"
                scenarios_bound += 1
                if status == "duplicate":
                    duplicate_bindings.append(
                        {
                            "feature": feature_ref,
                            "scenario": scenario_ref,
                            "title": scenario.title,
                            "count": len(linked),
                            "mappings": mappings_data,
                        }
                    )
            elif manual:
                status = "waived"
                scenarios_waived += 1
            else:
                candidate_tests = _candidate_tests_for_missing_scenario(
                    feature_ref=feature_ref,
                    feature_title=parsed_feature.title,
                    expected_test_file=expected_test_file,
                    unmapped_tests_by_file=unmapped_tests_by_file,
                )
                if not expected_exists:
                    reason = "missing_test_file"
                elif candidate_tests:
                    reason = "unmapped_candidate_tests"
                else:
                    reason = "missing_scenario_binding"
                status = "missing"
                missing_bindings.append(
                    {
                        "feature": feature_ref,
                        "scenario": scenario_ref,
                        "title": scenario.title,
                        "line": scenario.line or 0,
                        "test_file": display_path(expected_test_file),
                        "expected_test_file": display_path(expected_test_file),
                        "expected_test_file_exists": expected_exists,
                        "reason": reason,
                        "candidate_tests": candidate_tests,
                    }
                )

            scenario_entries.append(
                {
                    "scenario": scenario_ref,
                    "title": scenario.title,
                    "line": scenario.line or 0,
                    "status": status,
                    "tags": list(scenario.tags),
                    "expected_test_file": display_path(expected_test_file),
                    "expected_test_file_exists": expected_exists,
                    "reason": reason if status == "missing" else None,
                    "mappings": mappings_data,
                    "candidate_tests": candidate_tests,
                }
            )

        feature_status = _feature_status(scenario_entries)
        if feature_status in {"bound", "waived"}:
            features_bound += 1
        elif feature_status == "partial":
            features_partial += 1
        else:
            features_missing += 1
        features.append(
            {
                "feature": feature_ref,
                "title": parsed_feature.title,
                "expected_test_file": display_path(expected_test_file),
                "status": feature_status,
                "scenarios_total": len(scenario_entries),
                "scenarios_bound": sum(
                    1
                    for entry in scenario_entries
                    if entry["status"] in {"bound", "duplicate"}
                ),
                "scenarios_missing": sum(
                    1 for entry in scenario_entries if entry["status"] == "missing"
                ),
                "scenarios": scenario_entries,
            }
        )

    for mapping in mappings:
        if _mapping_valid(mapping, expected_scenarios):
            continue
        stale_bindings.append(
            {
                "feature": mapping.feature,
                "scenario": mapping.scenario,
                "test_file": mapping.test_file,
                "nodeid": _normalize_nodeid(mapping.nodeid),
                "function_name": mapping.function_name,
                "line": mapping.line,
                "source": mapping.source,
                "reason": (
                    "missing_feature"
                    if mapping.feature not in feature_refs
                    else "missing_scenario"
                ),
            }
        )

    deprecated_paths = _deprecated_paths(_project_root(features_dir))
    forbidden_pytest_bdd_usages = _forbidden_pytest_bdd_usages(test_files)
    coverage_percent = (
        round((scenarios_bound / scenarios_total) * 100.0, 1)
        if scenarios_total
        else 0.0
    )
    pytest_tests_total = len(test_items)
    pytest_tests_mapped = sum(
        1 for group in tests for item in group["items"] if item["status"] == "mapped"
    )
    pytest_tests_unmapped = len(unmapped_tests)
    pytest_tests_waived = sum(
        1 for group in tests for item in group["items"] if item["status"] == "waived"
    )
    pytest_mappings_stale = sum(
        1 for group in tests for item in group["items"] if item["status"] == "stale"
    )
    pytest_coverage_percent = (
        round(
            ((pytest_tests_mapped + pytest_tests_waived) / pytest_tests_total) * 100.0,
            1,
        )
        if pytest_tests_total
        else 0.0
    )
    status = (
        "failed"
        if any(
            (
                missing_bindings,
                stale_bindings,
                duplicate_bindings,
                deprecated_paths,
                forbidden_pytest_bdd_usages,
                unmapped_tests,
            )
        )
        else "passed"
    )

    return {
        "schema_version": 2,
        "status": status,
        "summary": {
            "features": {
                "total": len(feature_files),
                "bound": features_bound,
                "partial": features_partial,
                "missing": features_missing,
            },
            "scenarios": {
                "total": scenarios_total,
                "bound": scenarios_bound,
                "missing": len(missing_bindings),
                "waived": scenarios_waived,
                "duplicate": len(duplicate_bindings),
                "coverage_percent": coverage_percent,
            },
            "pytest": {
                "files_total": len(tests),
                "tests_total": pytest_tests_total,
                "mapped": pytest_tests_mapped,
                "unmapped": pytest_tests_unmapped,
                "waived": pytest_tests_waived,
                "stale": pytest_mappings_stale,
                "coverage_percent": pytest_coverage_percent,
            },
            "findings": {
                "missing_bindings": len(missing_bindings),
                "stale_bindings": len(stale_bindings),
                "duplicate_bindings": len(duplicate_bindings),
                "deprecated_paths": len(deprecated_paths),
                "forbidden_pytest_bdd_usages": len(forbidden_pytest_bdd_usages),
            },
        },
        "features_total": len(feature_files),
        "scenarios_total": scenarios_total,
        "features_bound": features_bound,
        "scenarios_bound": scenarios_bound,
        "scenarios_waived": scenarios_waived,
        "coverage_percent": coverage_percent,
        "pytest_files_total": len(tests),
        "pytest_tests_total": pytest_tests_total,
        "pytest_tests_mapped": pytest_tests_mapped,
        "pytest_tests_unmapped": pytest_tests_unmapped,
        "pytest_tests_waived": pytest_tests_waived,
        "pytest_mappings_stale": pytest_mappings_stale,
        "pytest_coverage_percent": pytest_coverage_percent,
        "intentional_unmapped_path": display_path(intentional_unmapped_path),
        "features": features,
        "tests": tests,
        "missing_bindings": missing_bindings,
        "stale_bindings": stale_bindings,
        "duplicate_bindings": duplicate_bindings,
        "unmapped_tests": unmapped_tests,
        "deprecated_paths": deprecated_paths,
        "forbidden_pytest_bdd_usages": forbidden_pytest_bdd_usages,
    }


def _validate_view(view: str) -> None:
    if view not in _VIEW_VALUES:
        expected = ", ".join(sorted(_VIEW_VALUES))
        raise ValueError(
            f"Unsupported view filter: {view}; expected one of: {expected}"
        )


def _validate_show(show: str) -> None:
    if show not in _SHOW_VALUES:
        expected = ", ".join(sorted(_SHOW_VALUES))
        raise ValueError(
            f"Unsupported show filter: {show}; expected one of: {expected}"
        )


def _feature_entries(data: dict[str, Any], *, show: str) -> list[str]:
    lines: list[str] = []
    visible_any = False
    for feature in data["features"]:
        scenarios = [
            scenario
            for scenario in feature["scenarios"]
            if _feature_visible(str(scenario["status"]), show)
        ]
        if not scenarios:
            continue
        visible_any = True
        lines.append(f"{feature['feature']} — {feature['title']}")
        for scenario in scenarios:
            status = str(scenario["status"])
            if status == "bound":
                prefix = "  ✓"
                suffix = ""
            elif status == "duplicate":
                prefix = "  !"
                suffix = " [duplicate]"
            elif status == "waived":
                prefix = "  ◌"
                suffix = " [waived]"
            else:
                prefix = "  ✗"
                suffix = ""
            lines.append(f"{prefix} {scenario['scenario']} {scenario['title']}{suffix}")
            if status == "missing":
                lines.append(f"    expected: {scenario['expected_test_file']}")
                lines.append(f"    reason: {scenario['reason']}")
            else:
                for mapping in scenario["mappings"]:
                    lines.append(f"    {mapping['nodeid']} [{mapping['source']}]")
        lines.append("")
    if not visible_any:
        lines.append("No feature-side items for current filters.")
        lines.append("")
    return lines


def _feature_gaps(data: dict[str, Any], *, suggestions: bool) -> list[str]:
    lines: list[str] = []
    if data["missing_bindings"]:
        lines.append("Missing scenario bindings:")
        for binding in data["missing_bindings"]:
            lines.append(
                f"  {binding['feature']} {binding['scenario']} — {binding['title']}"
            )
            lines.append(f"    expected: {binding['expected_test_file']}")
            lines.append(f"    reason: {binding['reason']}")
            if suggestions and binding["candidate_tests"]:
                lines.append("    candidate tests:")
                for candidate in binding["candidate_tests"]:
                    lines.append(f"      {candidate['nodeid']} ({candidate['reason']})")
        lines.append("")
    if data["duplicate_bindings"]:
        lines.append("Duplicate scenario bindings:")
        for binding in data["duplicate_bindings"]:
            lines.append(
                "  "
                f"{binding['feature']} {binding['scenario']} "
                f"({binding['count']} mappings)"
            )
        lines.append("")
    if data["stale_bindings"]:
        lines.append("Stale pytest mappings:")
        for binding in data["stale_bindings"]:
            lines.append(
                "  "
                f"{binding['nodeid']} -> {binding['feature']} {binding['scenario']} "
                f"({binding['reason']})"
            )
        lines.append("")
    if data["deprecated_paths"]:
        lines.append("Deprecated paths:")
        for path in data["deprecated_paths"]:
            lines.append(f"  {path}")
        lines.append("")
    if data["forbidden_pytest_bdd_usages"]:
        lines.append("Forbidden pytest-bdd usage:")
        for path in data["forbidden_pytest_bdd_usages"]:
            lines.append(f"  {path}")
        lines.append("")
    if not lines:
        lines.extend(["No feature-side gap findings.", ""])
    return lines


def _render_test_groups(groups: list[dict[str, Any]], *, show: str) -> list[str]:
    lines: list[str] = []
    visible_any = False
    for group in groups:
        items = [
            item for item in group["items"] if _test_visible(str(item["status"]), show)
        ]
        if not items:
            continue
        visible_any = True
        lines.append(f"{group['test_file']}")
        for item in items:
            if item["status"] == "mapped":
                mapping = item["mapping"] or {}
                lines.append(
                    f"  ✓ {item['nodeid']} -> {mapping.get('feature', '')} "
                    f"{mapping.get('scenario', '')}"
                )
            elif item["status"] == "stale":
                mapping = item["mapping"] or {}
                lines.append(
                    f"  ! {item['nodeid']} -> {mapping.get('feature', '')} "
                    f"{mapping.get('scenario', '')} [stale]"
                )
            elif item["status"] == "waived":
                waiver = item["waiver"] or {}
                lines.append(
                    f"  ◌ {item['nodeid']} [waived: {waiver.get('reason', '')}]"
                )
            else:
                lines.append(f"  ✗ {item['nodeid']} [unmapped]")
        lines.append("")
    if not visible_any:
        lines.append("No pytest-side items for current filters.")
        lines.append("")
    return lines


def _test_gaps(data: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    if data["unmapped_tests"]:
        lines.append("Unmapped pytest tests:")
        current_file = None
        for item in data["unmapped_tests"]:
            test_file = item["test_file"]
            if test_file != current_file:
                current_file = test_file
                lines.append(f"  {test_file}")
            lines.append(f"    {item['nodeid']}")
        lines.append("")
    if data["stale_bindings"]:
        lines.append("Stale pytest mappings:")
        current_file = None
        for binding in data["stale_bindings"]:
            test_file = binding["test_file"]
            if test_file != current_file:
                current_file = test_file
                lines.append(f"  {test_file}")
            lines.append(
                f"    {binding['nodeid']} -> "
                f"{binding['feature']} {binding['scenario']} "
                f"({binding['reason']})"
            )
        lines.append("")
    if not lines:
        lines.extend(["No pytest-side gap findings.", ""])
    return lines


def render_coverage_text(
    data: dict[str, Any],
    *,
    view: str = "feature",
    show: str = "all",
    suggestions: bool = True,
) -> str:
    """Render human-readable behavior coverage text."""

    _validate_view(view)
    _validate_show(show)
    lines = _summary_lines(data)

    if view in {"feature", "both"}:
        lines.append("Features -> pytest")
        lines.append("")
        if show == "gaps":
            lines.extend(_feature_gaps(data, suggestions=suggestions))
        else:
            lines.extend(_feature_entries(data, show=show))

    if view in {"test", "both"}:
        lines.append("Pytest -> features")
        lines.append("")
        if show == "gaps":
            lines.extend(_test_gaps(data))
        else:
            lines.extend(_render_test_groups(data["tests"], show=show))

    return "\n".join(lines).rstrip()


def _feature_entries_markdown(
    data: dict[str, Any],
    *,
    show: str,
    suggestions: bool,
) -> list[str]:
    lines: list[str] = []
    visible_any = False
    for feature in data["features"]:
        scenarios = [
            scenario
            for scenario in feature["scenarios"]
            if _feature_visible(str(scenario["status"]), show)
        ]
        if not scenarios:
            continue
        visible_any = True
        lines.append(f"### `{feature['feature']}` — {feature['title']}")
        lines.append("")
        for scenario in scenarios:
            status = str(scenario["status"])
            lines.append(
                f"- `{scenario['scenario']}` {scenario['title']} **[{status}]**"
            )
            if status == "missing":
                lines.append(f"  - expected: `{scenario['expected_test_file']}`")
                lines.append(f"  - reason: `{scenario['reason']}`")
                if suggestions and scenario["candidate_tests"]:
                    lines.append("  - candidate tests:")
                    for candidate in scenario["candidate_tests"]:
                        lines.append(
                            f"    - `{candidate['nodeid']}` ({candidate['reason']})"
                        )
            else:
                for mapping in scenario["mappings"]:
                    lines.append(f"  - `{mapping['nodeid']}` [{mapping['source']}]")
        lines.append("")
    if not visible_any:
        lines.append("No feature-side items for current filters.")
        lines.append("")
    return lines


def _feature_gaps_markdown(data: dict[str, Any], *, suggestions: bool) -> list[str]:
    lines: list[str] = []
    if data["missing_bindings"]:
        lines.extend(["### Missing scenario bindings", ""])
        for binding in data["missing_bindings"]:
            lines.append(
                f"- `{binding['feature']}` `{binding['scenario']}` — {binding['title']}"
            )
            lines.append(f"  - expected: `{binding['expected_test_file']}`")
            lines.append(f"  - reason: `{binding['reason']}`")
            if suggestions and binding["candidate_tests"]:
                lines.append("  - candidate tests:")
                for candidate in binding["candidate_tests"]:
                    lines.append(
                        f"    - `{candidate['nodeid']}` ({candidate['reason']})"
                    )
        lines.append("")
    if data["duplicate_bindings"]:
        lines.extend(["### Duplicate scenario bindings", ""])
        for binding in data["duplicate_bindings"]:
            lines.append(
                f"- `{binding['feature']}` `{binding['scenario']}` "
                f"({binding['count']} mappings)"
            )
        lines.append("")
    if data["stale_bindings"]:
        lines.extend(["### Stale pytest mappings", ""])
        for binding in data["stale_bindings"]:
            lines.append(
                "- "
                f"`{binding['nodeid']}` -> `{binding['feature']}` "
                f"`{binding['scenario']}` ({binding['reason']})"
            )
        lines.append("")
    if data["deprecated_paths"]:
        lines.extend(["### Deprecated paths", ""])
        for path in data["deprecated_paths"]:
            lines.append(f"- `{path}`")
        lines.append("")
    if data["forbidden_pytest_bdd_usages"]:
        lines.extend(["### Forbidden pytest-bdd usage", ""])
        for path in data["forbidden_pytest_bdd_usages"]:
            lines.append(f"- `{path}`")
        lines.append("")
    if not lines:
        lines.extend(["No feature-side gap findings.", ""])
    return lines


def _render_test_groups_markdown(
    groups: list[dict[str, Any]], *, show: str
) -> list[str]:
    lines: list[str] = []
    visible_any = False
    for group in groups:
        items = [
            item for item in group["items"] if _test_visible(str(item["status"]), show)
        ]
        if not items:
            continue
        visible_any = True
        lines.append(f"### `{group['test_file']}`")
        lines.append("")
        for item in items:
            if item["status"] == "mapped":
                mapping = item["mapping"] or {}
                lines.append(
                    f"- `{item['nodeid']}` -> "
                    f"`{mapping.get('feature', '')}` "
                    f"`{mapping.get('scenario', '')}`"
                )
            elif item["status"] == "stale":
                mapping = item["mapping"] or {}
                lines.append(
                    f"- `{item['nodeid']}` -> `{mapping.get('feature', '')}` "
                    f"`{mapping.get('scenario', '')}` **[stale]**"
                )
            elif item["status"] == "waived":
                waiver = item["waiver"] or {}
                lines.append(
                    f"- `{item['nodeid']}` **[waived]** — {waiver.get('reason', '')}"
                )
            else:
                lines.append(f"- `{item['nodeid']}` **[unmapped]**")
        lines.append("")
    if not visible_any:
        lines.append("No pytest-side items for current filters.")
        lines.append("")
    return lines


def _test_gaps_markdown(data: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    if data["unmapped_tests"]:
        lines.extend(["### Unmapped pytest tests", ""])
        current_file = None
        for item in data["unmapped_tests"]:
            test_file = item["test_file"]
            if test_file != current_file:
                current_file = test_file
                lines.append(f"- `{test_file}`")
            lines.append(f"  - `{item['nodeid']}`")
        lines.append("")
    if data["stale_bindings"]:
        lines.extend(["### Stale pytest mappings", ""])
        current_file = None
        for binding in data["stale_bindings"]:
            test_file = binding["test_file"]
            if test_file != current_file:
                current_file = test_file
                lines.append(f"- `{test_file}`")
            lines.append(
                f"  - `{binding['nodeid']}` -> `{binding['feature']}` "
                f"`{binding['scenario']}` ({binding['reason']})"
            )
        lines.append("")
    if not lines:
        lines.extend(["No pytest-side gap findings.", ""])
    return lines


def render_coverage_markdown(
    data: dict[str, Any],
    *,
    view: str = "feature",
    show: str = "all",
    suggestions: bool = True,
) -> str:
    """Render behavior coverage as Markdown."""

    _validate_view(view)
    _validate_show(show)
    scenario_summary = (
        f"**Scenario coverage:** {data['scenarios_bound']}/{data['scenarios_total']} "
        f"bound ({data['coverage_percent']:.1f}%), "
        f"{len(data['missing_bindings'])} missing, "
        f"{data['scenarios_waived']} waived"
    )
    pytest_summary = (
        "**Pytest coverage:** "
        f"{data['pytest_tests_mapped'] + data['pytest_tests_waived']}/"
        f"{data['pytest_tests_total']} accepted "
        f"({data['pytest_coverage_percent']:.1f}%), "
        f"{data['pytest_tests_unmapped']} unmapped, "
        f"{data['pytest_tests_waived']} waived, "
        f"{data['pytest_mappings_stale']} stale"
    )
    lines = [
        "# Behavior coverage",
        "",
        f"**Status:** {data['status']}",
        "",
        scenario_summary,
        pytest_summary,
        "",
    ]

    if view in {"feature", "both"}:
        lines.extend(["## Features -> pytest", ""])
        if show == "gaps":
            lines.extend(_feature_gaps_markdown(data, suggestions=suggestions))
        else:
            lines.extend(
                _feature_entries_markdown(data, show=show, suggestions=suggestions)
            )

    if view in {"test", "both"}:
        lines.extend(["## Pytest -> features", ""])
        if show == "gaps":
            lines.extend(_test_gaps_markdown(data))
        else:
            lines.extend(_render_test_groups_markdown(data["tests"], show=show))

    return "\n".join(lines).rstrip()


def render_mapping_inventory_text(data: dict[str, Any]) -> str:
    """Render the raw mapping inventory as text."""

    lines = [f"Discovered SpecWeave pytest mappings: {data['mappings_total']}"]
    if data["items"]:
        lines.append("")
        for item in data["items"]:
            lines.append(
                f"{item['source']:<9} {item['test_file']}:{item['line']}  "
                f"{item['nodeid']}"
            )
            lines.append(f"  feature:  {item['feature']}")
            lines.append(f"  scenario: {item['scenario']}")
            lines.append("")
    lines.extend(
        [
            "For mapped/unmapped/stale pytest coverage, run:",
            "  specweave review coverage --view test --show gaps",
        ]
    )
    return "\n".join(lines).rstrip()


def write_coverage_json(data: dict[str, Any], path: str | Path) -> None:
    """Write behavior coverage *data* to *path*."""

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
