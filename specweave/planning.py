"""SpecWeave planning: create plans and Taskledger drafts."""

from __future__ import annotations

import json
import re
from pathlib import Path

from specweave.config import SpecWeaveConfig
from specweave.gherkin.lint import iter_feature_scenarios
from specweave.gherkin.parser import parse_feature


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _derive_test_file(area: str, feature_slug: str) -> str:
    if area:
        return f"tests/test_{area}_{feature_slug}.py"
    return f"tests/test_{feature_slug}.py"


def _derive_area(feature_path: Path, features_dir: Path) -> str:
    try:
        relative = feature_path.relative_to(features_dir)
        if len(relative.parts) >= 2:
            return relative.parts[0]
    except ValueError:
        pass
    return ""


def create_plan(
    *,
    feature_path: Path,
    out_path: Path = Path("plan.md"),
    config: SpecWeaveConfig | None = None,
) -> None:
    """Create a deterministic implementation plan from a feature file."""
    if config is None:
        config = SpecWeaveConfig()

    text = feature_path.read_text(encoding="utf-8")
    feature = parse_feature(text)

    feature_slug = _slug(feature.title)
    area = _derive_area(feature_path, config.paths.features_dir)
    test_file = _derive_test_file(area, feature_slug)

    lines: list[str] = [
        f"# Plan: {feature.title}",
        "",
        "## Scope",
        "",
        f"Implement behavior described in `{feature_path}`.",
        "",
    ]

    lines.append("## Rules and scenarios")
    lines.append("")
    for rule in feature.rules:
        lines.append(f"### Rule: {rule.title}")
        lines.append("")
        for scenario in rule.scenarios:
            lines.append(f"- **{scenario.title}**")
        lines.append("")
    for scenario in feature.scenarios:
        lines.append(f"- **{scenario.title}**")
    lines.append("")

    lines.append("## Proposed test file")
    lines.append("")
    lines.append(f"`{test_file}`")
    lines.append("")

    lines.append("## Implementation TODOs")
    lines.append("")
    todo_num = 1
    for rule in feature.rules:
        for scenario in rule.scenarios:
            lines.append(f"{todo_num}. Implement **{scenario.title}**")
            lines.append(f"   - Write test in `{test_file}`")
            for step in scenario.steps:
                lines.append(f"   - {step.keyword} {step.text}")
            todo_num += 1
    for scenario in feature.scenarios:
        lines.append(f"{todo_num}. Implement **{scenario.title}**")
        lines.append(f"   - Write test in `{test_file}`")
        for step in scenario.steps:
            lines.append(f"   - {step.keyword} {step.text}")
        todo_num += 1
    lines.append("")

    lines.append("## Acceptance mapping")
    lines.append("")
    for rule in feature.rules:
        for scenario in rule.scenarios:
            bdd_tags = [t for t in scenario.tags if t.startswith("bdd-")]
            ac_tags = [t for t in scenario.tags if t.startswith("ac-")]
            for tag in bdd_tags:
                lines.append(f"- `@{tag}`")
                for ac in ac_tags:
                    lines.append(f"  - linked to `@{ac}`")
    for scenario in feature.scenarios:
        bdd_tags = [t for t in scenario.tags if t.startswith("bdd-")]
        for tag in bdd_tags:
            lines.append(f"- `@{tag}`")
    lines.append("")

    report_segment = f"reports/{config.spelling}"
    junit_file = f"{report_segment}/{area}-{feature_slug}-junit.xml"

    lines.append("## Validation")
    lines.append("")
    lines.append("```bash")
    lines.append("specweave doctor")
    lines.append(f"specweave behavior generate-tests {feature_path}")
    lines.append(f"pytest {test_file} --junitxml={junit_file}")
    lines.append(f"specweave behavior import-report {junit_file} --format junit-xml")
    lines.append("specweave review specs")
    lines.append("```")
    lines.append("")

    lines.append("## Evidence import")
    lines.append("")
    lines.append("```bash")
    lines.append(f"specweave behavior import-report {junit_file} \\")
    lines.append("  --format junit-xml \\")
    evidence = (
        f"specs/{config.spelling}/evidence/{area}-{feature_slug}.pytest-evidence.json"
    )
    lines.append(f"  --out {evidence}")
    lines.append("```")
    lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def create_taskledger_draft(
    *,
    feature_path: Path,
    out_path: Path = Path("specs/behavior/mappings/taskledger/draft.json"),
    config: SpecWeaveConfig | None = None,
) -> None:
    """Create a Taskledger task draft JSON from a feature file.

    This produces a file-based draft only.
    It does not import or call Taskledger.
    """
    if config is None:
        config = SpecWeaveConfig()

    text = feature_path.read_text(encoding="utf-8")
    feature = parse_feature(text)

    feature_slug = _slug(feature.title)
    report_segment = f"reports/{config.spelling}"
    area = _derive_area(feature_path, config.paths.features_dir)
    test_file = _derive_test_file(area, feature_slug)
    junit_file = f"{report_segment}/{area}-{feature_slug}-junit.xml"

    acceptance_criteria: list[dict] = []
    ac_num = 1
    for scenario in iter_feature_scenarios(feature):
        bdd_tags = [t for t in scenario.tags if t.startswith("bdd-")]
        steps_text = "; ".join(f"{s.keyword} {s.text}" for s in scenario.steps)
        criterion = {
            "id": f"ac-{ac_num:04d}",
            "text": steps_text,
        }
        if bdd_tags:
            criterion["bdd_id"] = bdd_tags[0]
        acceptance_criteria.append(criterion)
        ac_num += 1

    suggested_validation = [
        "specweave doctor",
        f"pytest {test_file} --junitxml={junit_file}",
        (f"specweave behavior import-report {junit_file} --format junit-xml"),
    ]

    draft = {
        "schema_version": 1,
        "source": "specweave",
        "feature": str(feature_path),
        "title": f"Implement {feature.title} behavior",
        "acceptance_criteria": acceptance_criteria,
        "suggested_validation": suggested_validation,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(draft, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
