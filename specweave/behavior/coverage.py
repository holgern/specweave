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
_SHOW_VALUES = frozenset({"all", "bound", "missing", "stale", "waived"})


def _test_files(tests_dir: Path) -> list[Path]:
    return sorted(
        candidate for candidate in tests_dir.rglob("*.py") if candidate.is_file()
    )


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
) -> dict[str, Any]:
    """Build the coverage report for canonical behavior specs."""

    feature_files = _feature_files(features_dir=features_dir, feature_path=feature_path)
    test_files = _test_files(tests_dir)
    mappings = sorted(collect_specweave_tests(test_files), key=_mapping_sort_key)
    mapping_by_key, _ = _mapping_lookup(mappings)

    feature_refs = {display_path(path) for path in feature_files}
    expected_scenarios: dict[tuple[str, str], dict[str, Any]] = {}
    features: list[dict[str, Any]] = []
    missing_bindings: list[dict[str, Any]] = []
    stale_bindings: list[dict[str, Any]] = []
    duplicate_bindings: list[dict[str, Any]] = []
    features_bound = 0
    scenarios_total = 0
    scenarios_bound = 0
    scenarios_waived = 0

    for current_feature_path in feature_files:
        parsed_feature = parse_feature(
            current_feature_path.read_text(encoding="utf-8"),
            source_path=current_feature_path,
        )
        feature_ref = display_path(current_feature_path)
        expected_test_file = canonical_test_path(
            current_feature_path, tests_dir=tests_dir
        )
        scenario_entries: list[dict[str, Any]] = []

        for _, scenario in iter_feature_scenarios(parsed_feature):
            scenarios_total += 1
            scenario_ref = scenario_identifier(scenario)
            expected_scenarios[(feature_ref, scenario_ref)] = {
                "feature": feature_ref,
                "title": scenario.title,
                "line": scenario.line or 0,
            }
            linked = sorted(
                mapping_by_key.get((feature_ref, scenario_ref), []),
                key=_mapping_sort_key,
            )
            mappings_data = [_mapping_item(mapping) for mapping in linked]
            manual = bool({"manual", "waived"} & set(scenario.tags))

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
                status = "missing"
                missing_bindings.append(
                    {
                        "feature": feature_ref,
                        "scenario": scenario_ref,
                        "title": scenario.title,
                        "line": scenario.line or 0,
                        "test_file": display_path(expected_test_file),
                        "reason": "missing_scenario_binding",
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
                    "mappings": mappings_data,
                }
            )

        feature_status = _feature_status(scenario_entries)
        if feature_status in {"bound", "waived"}:
            features_bound += 1
        features.append(
            {
                "feature": feature_ref,
                "title": parsed_feature.title,
                "expected_test_file": display_path(expected_test_file),
                "status": feature_status,
                "scenarios": scenario_entries,
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

    return {
        "schema_version": 1,
        "features_total": len(feature_files),
        "scenarios_total": scenarios_total,
        "features_bound": features_bound,
        "scenarios_bound": scenarios_bound,
        "scenarios_waived": scenarios_waived,
        "coverage_percent": coverage_percent,
        "features": features,
        "missing_bindings": missing_bindings,
        "stale_bindings": stale_bindings,
        "duplicate_bindings": duplicate_bindings,
        "deprecated_paths": deprecated_paths,
        "forbidden_pytest_bdd_usages": forbidden_pytest_bdd_usages,
    }


def _validate_show(show: str) -> None:
    if show not in _SHOW_VALUES:
        expected = ", ".join(sorted(_SHOW_VALUES))
        raise ValueError(
            f"Unsupported show filter: {show}; expected one of: {expected}"
        )


def _scenario_visible(status: str, show: str) -> bool:
    if show == "all":
        return True
    if show == "bound":
        return status in {"bound", "duplicate"}
    return status == show


def render_coverage_text(data: dict[str, Any], *, show: str = "all") -> str:
    """Render human-readable behavior coverage text."""

    _validate_show(show)
    lines = [
        "Behavior coverage: "
        f"{data['scenarios_bound']}/{data['scenarios_total']} scenarios bound "
        f"({data['coverage_percent']:.1f}%), {data['scenarios_waived']} waived",
        "",
    ]

    if show != "stale":
        for feature in data["features"]:
            scenarios = [
                scenario
                for scenario in feature["scenarios"]
                if _scenario_visible(str(scenario["status"]), show)
            ]
            if not scenarios:
                continue
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
                lines.append(
                    f"{prefix} {scenario['scenario']} {scenario['title']}{suffix}"
                )
                if status == "missing":
                    lines.append(f"    expected: {scenario['expected_test_file']}")
                else:
                    for mapping in scenario["mappings"]:
                        lines.append(f"    {mapping['nodeid']} [{mapping['source']}]")
            lines.append("")

    if show in {"all", "stale"} and data["stale_bindings"]:
        lines.append("Stale mappings:")
        for binding in data["stale_bindings"]:
            lines.append(
                "  "
                f"{binding['nodeid']} -> {binding['feature']} {binding['scenario']} "
                f"({binding['reason']})"
            )
        lines.append("")

    if show in {"all", "bound"} and data["duplicate_bindings"]:
        lines.append("Duplicate mappings:")
        for binding in data["duplicate_bindings"]:
            lines.append(
                "  "
                f"{binding['feature']} {binding['scenario']} "
                f"({binding['count']} mappings)"
            )
        lines.append("")

    if show == "all" and data["deprecated_paths"]:
        lines.append("Deprecated paths:")
        for path in data["deprecated_paths"]:
            lines.append(f"  {path}")
        lines.append("")

    if show == "all" and data["forbidden_pytest_bdd_usages"]:
        lines.append("Forbidden pytest-bdd usage:")
        for path in data["forbidden_pytest_bdd_usages"]:
            lines.append(f"  {path}")
        lines.append("")

    return "\n".join(lines).rstrip()


def render_coverage_markdown(data: dict[str, Any], *, show: str = "all") -> str:
    """Render behavior coverage as Markdown."""

    _validate_show(show)
    lines = [
        "# Behavior coverage",
        "",
        (
            f"**Coverage:** {data['scenarios_bound']}/{data['scenarios_total']} "
            f"scenarios bound ({data['coverage_percent']:.1f}%), "
            f"{data['scenarios_waived']} waived"
        ),
        "",
    ]

    if show != "stale":
        for feature in data["features"]:
            scenarios = [
                scenario
                for scenario in feature["scenarios"]
                if _scenario_visible(str(scenario["status"]), show)
            ]
            if not scenarios:
                continue
            lines.append(f"## `{feature['feature']}` — {feature['title']}")
            lines.append("")
            for scenario in scenarios:
                status = str(scenario["status"])
                if status == "bound":
                    label = "bound"
                elif status == "duplicate":
                    label = "duplicate"
                elif status == "waived":
                    label = "waived"
                else:
                    label = "missing"
                lines.append(
                    f"- `{scenario['scenario']}` {scenario['title']} **[{label}]**"
                )
                if status == "missing":
                    lines.append(f"  - expected: `{scenario['expected_test_file']}`")
                else:
                    for mapping in scenario["mappings"]:
                        lines.append(f"  - `{mapping['nodeid']}` [{mapping['source']}]")
            lines.append("")

    if show in {"all", "stale"} and data["stale_bindings"]:
        lines.append("## Stale mappings")
        lines.append("")
        for binding in data["stale_bindings"]:
            lines.append(
                "- "
                f"`{binding['nodeid']}` -> `{binding['feature']}` "
                f"`{binding['scenario']}` ({binding['reason']})"
            )
        lines.append("")

    if show in {"all", "bound"} and data["duplicate_bindings"]:
        lines.append("## Duplicate mappings")
        lines.append("")
        for binding in data["duplicate_bindings"]:
            lines.append(
                "- "
                f"`{binding['feature']}` `{binding['scenario']}` "
                f"({binding['count']} mappings)"
            )
        lines.append("")

    if show == "all" and data["deprecated_paths"]:
        lines.append("## Deprecated paths")
        lines.append("")
        for path in data["deprecated_paths"]:
            lines.append(f"- `{path}`")
        lines.append("")

    if show == "all" and data["forbidden_pytest_bdd_usages"]:
        lines.append("## Forbidden pytest-bdd usage")
        lines.append("")
        for path in data["forbidden_pytest_bdd_usages"]:
            lines.append(f"- `{path}`")
        lines.append("")

    return "\n".join(lines).rstrip()


def render_mapping_inventory_text(data: dict[str, Any]) -> str:
    """Render the raw mapping inventory as text."""

    lines = [f"Discovered SpecWeave pytest mappings: {data['mappings_total']}"]
    if not data["items"]:
        return "\n".join(lines)

    lines.append("")
    for item in data["items"]:
        lines.append(
            f"{item['source']:<9} {item['test_file']}:{item['line']}  {item['nodeid']}"
        )
        lines.append(f"  feature:  {item['feature']}")
        lines.append(f"  scenario: {item['scenario']}")
        lines.append("")
    return "\n".join(lines).rstrip()


def write_coverage_json(data: dict[str, Any], path: str | Path) -> None:
    """Write behavior coverage *data* to *path*."""

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
