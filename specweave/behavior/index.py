"""Behavior manifest and Markdown index generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from specweave.behavior.common import (
    canonical_test_path,
    display_path,
    feature_identity,
    scenario_id_value,
    scenario_identifier,
)
from specweave.config import (
    BEHAVIOR_FEATURES_DIR,
    BEHAVIOR_INDEX_PATH,
    BEHAVIOR_MANIFEST_PATH,
    PYTEST_TESTS_DIR,
    SPECWEAVE_EVIDENCE_DIR,
)
from specweave.gherkin.lint import collect_feature_files
from specweave.gherkin.model import Scenario
from specweave.gherkin.parser import parse_feature
from specweave.python_inspect.ast_reader import (
    collect_specweave_tests,
    is_behavior_mapping,
)


def _load_evidence(evidence_dir: Path) -> dict[tuple[str, str], str]:
    statuses: dict[tuple[str, str], str] = {}
    if not evidence_dir.exists():
        return statuses
    for path in sorted(evidence_dir.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        results = payload.get("results")
        if not isinstance(results, list):
            continue
        for result in results:
            if not isinstance(result, dict):
                continue
            feature = result.get("feature")
            scenario = result.get("scenario")
            status = result.get("status")
            if (
                isinstance(feature, str)
                and isinstance(scenario, str)
                and isinstance(status, str)
            ):
                statuses[(feature, scenario)] = status
    return statuses


def _mapping_lookup(tests_dir: Path) -> dict[tuple[str, str], dict[str, str]]:
    mappings = collect_specweave_tests(
        sorted(
            candidate for candidate in tests_dir.rglob("*.py") if candidate.is_file()
        )
    )
    by_key: dict[tuple[str, str], dict[str, str]] = {}
    for mapping in mappings:
        if not is_behavior_mapping(mapping):
            continue
        by_key[(mapping.feature, mapping.scenario)] = {
            "test_file": mapping.test_file,
            "nodeid": mapping.nodeid,
        }
    return by_key


def _scenario_manifest_entry(
    *,
    feature_ref: str,
    scenario: Scenario,
    expected_test_file: Path,
    mapping_lookup: dict[tuple[str, str], dict[str, str]],
    evidence_lookup: dict[tuple[str, str], str],
) -> dict[str, Any]:
    scenario_ref = scenario_identifier(scenario)
    mapping = mapping_lookup.get((feature_ref, scenario_ref))
    entry: dict[str, Any] = {
        "id": scenario_id_value(scenario) or scenario_ref,
        "title": scenario.title,
        "tags": list(scenario.tags),
        "line": scenario.line or 0,
        "automation": {
            "backend": "pytest",
            "test_file": (
                mapping["test_file"]
                if mapping is not None
                else display_path(expected_test_file)
            ),
            "nodeid": mapping["nodeid"] if mapping is not None else "",
            "status": "bound" if mapping is not None else "missing",
        },
    }
    evidence = evidence_lookup.get((feature_ref, scenario_ref))
    if evidence is not None:
        entry["automation"]["latest_evidence_status"] = evidence
    return entry


def build_behavior_index(
    *,
    features_dir: Path = BEHAVIOR_FEATURES_DIR,
    tests_dir: Path = PYTEST_TESTS_DIR,
    evidence_dir: Path = SPECWEAVE_EVIDENCE_DIR,
) -> tuple[dict[str, Any], str]:
    """Build the manifest payload and Markdown index."""

    feature_files = collect_feature_files((features_dir,))
    mapping_lookup = _mapping_lookup(tests_dir)
    evidence_lookup = _load_evidence(evidence_dir)

    manifest_features: list[dict[str, Any]] = []
    markdown_lines = [
        "# Behavior index",
        "",
        f"Generated from `{display_path(features_dir)}`.",
        "",
    ]

    by_area: dict[str, list[dict[str, Any]]] = {}
    for feature_path in feature_files:
        parsed_feature = parse_feature(
            feature_path.read_text(encoding="utf-8"),
            source_path=feature_path,
        )
        feature_ref = display_path(feature_path)
        area, feature_slug = feature_identity(feature_path, features_root=features_dir)
        expected_test_file = canonical_test_path(feature_path, tests_dir=tests_dir)

        rules: list[dict[str, Any]] = []
        for rule in parsed_feature.rules:
            rules.append(
                {
                    "id": next(
                        (tag for tag in rule.tags if tag.startswith("rule-")),
                        rule.title,
                    ),
                    "title": rule.title,
                    "tags": list(rule.tags),
                    "scenarios": [
                        _scenario_manifest_entry(
                            feature_ref=feature_ref,
                            scenario=scenario,
                            expected_test_file=expected_test_file,
                            mapping_lookup=mapping_lookup,
                            evidence_lookup=evidence_lookup,
                        )
                        for scenario in rule.scenarios
                    ],
                }
            )

        top_level = [
            _scenario_manifest_entry(
                feature_ref=feature_ref,
                scenario=scenario,
                expected_test_file=expected_test_file,
                mapping_lookup=mapping_lookup,
                evidence_lookup=evidence_lookup,
            )
            for scenario in parsed_feature.scenarios
        ]

        feature_entry: dict[str, Any] = {
            "path": feature_ref,
            "area": area,
            "feature_slug": feature_slug,
            "title": parsed_feature.title,
            "description": parsed_feature.description,
            "tags": list(parsed_feature.tags),
            "rules": rules,
        }
        if top_level:
            feature_entry["scenarios"] = top_level
        manifest_features.append(feature_entry)
        by_area.setdefault(area, []).append(feature_entry)

    for area in sorted(by_area):
        markdown_lines.extend([f"## {area}", ""])
        for feature_item in sorted(by_area[area], key=lambda item: str(item["path"])):
            markdown_lines.append(f"### {feature_item['title']}")
            markdown_lines.append(f"- Path: `{feature_item['path']}`")
            if feature_item.get("description"):
                summary = str(feature_item["description"]).splitlines()[0]
                markdown_lines.append(f"- Summary: {summary}")
            markdown_lines.append("")
            rules = feature_item["rules"]
            if feature_item.get("scenarios"):
                markdown_lines.append("#### Top-level scenarios")
                markdown_lines.append("")
                for scenario in feature_item["scenarios"]:
                    automation = scenario["automation"]
                    target = automation["nodeid"] or automation["test_file"]
                    markdown_lines.append(
                        "- "
                        f"`{scenario['id']}` {scenario['title']} "
                        f"-> `{target}` ({automation['status']})"
                    )
                markdown_lines.append("")
            for rule_item in rules:
                markdown_lines.append(f"#### Rule: {rule_item['title']}")
                markdown_lines.append("")
                for scenario in rule_item["scenarios"]:
                    automation = scenario["automation"]
                    target = automation["nodeid"] or automation["test_file"]
                    markdown_lines.append(
                        "- "
                        f"`{scenario['id']}` {scenario['title']} "
                        f"-> `{target}` ({automation['status']})"
                    )
                markdown_lines.append("")

    manifest = {
        "schema_version": 1,
        "features": manifest_features,
    }
    markdown = "\n".join(markdown_lines).rstrip() + "\n"
    return manifest, markdown


def write_behavior_index(
    *,
    features_dir: Path = BEHAVIOR_FEATURES_DIR,
    out: Path = BEHAVIOR_INDEX_PATH,
    manifest_path: Path = BEHAVIOR_MANIFEST_PATH,
    tests_dir: Path = PYTEST_TESTS_DIR,
    evidence_dir: Path = SPECWEAVE_EVIDENCE_DIR,
) -> tuple[Path, Path]:
    """Write the behavior Markdown index and manifest JSON."""

    manifest, markdown = build_behavior_index(
        features_dir=features_dir,
        tests_dir=tests_dir,
        evidence_dir=evidence_dir,
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown, encoding="utf-8")
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return out, manifest_path
