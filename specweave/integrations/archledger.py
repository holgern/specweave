"""Optional Archledger candidate generation.

Archledger owns durable architecture/spec behavior records and traceability.
SpecWeave does NOT write to Archledger's accepted record store; it only renders
candidate markdown from a feature file and a BDD example id. Archledger decides
whether to accept and persist the record.

Suggested usage::

    specweave archledger candidate \\
        --feature tests/bdd/features/task-0123-lifecycle.feature \\
        --bdd bdd-0001 \\
        --out .archledger/candidates/al_runtime_task_0123_bdd_0001.md
"""

from __future__ import annotations

from pathlib import Path

from specweave.gherkin.model import Feature, Rule, Scenario
from specweave.reports.mapping import extract_ids_from_tags


def _first_tag(tags: tuple[str, ...], prefix: str) -> str | None:
    for tag in tags:
        if tag.startswith(prefix):
            return tag
    return None


def _find_scenario(
    feature: Feature, bdd_id: str
) -> tuple[Scenario, Rule | None] | None:
    """Locate the scenario tagged with *bdd_id* and its enclosing rule, if any."""
    for rule in feature.rules:
        for scenario in rule.scenarios:
            if bdd_id in extract_ids_from_tags(scenario.tags).bdd_ids:
                return scenario, rule
    for scenario in feature.scenarios:
        if bdd_id in extract_ids_from_tags(scenario.tags).bdd_ids:
            return scenario, None
    return None


def _behavior_lines(scenario: Scenario) -> list[str]:
    """Render scenario steps as ``<Keyword> <text>`` lines."""
    return [f"{step.keyword} {step.text}".rstrip() for step in scenario.steps]


def render_archledger_candidate(feature: Feature, bdd_id: str) -> str:
    """Render candidate Archledger markdown for *bdd_id* found in *feature*.

    Raises ValueError when no scenario tagged with *bdd_id* is found.
    """
    located = _find_scenario(feature, bdd_id)
    if located is None:
        raise ValueError(
            f"No scenario tagged with bdd id {bdd_id!r} in feature {feature.title!r}"
        )
    scenario, rule = located

    task_id = _first_tag(feature.tags, "task-") or ""
    rule_id: str | None = None
    if rule is not None:
        rule_id = _first_tag(rule.tags, "rule-")
    ac_ids = extract_ids_from_tags(scenario.tags).ac_ids
    feature_path = str(feature.source_path) if feature.source_path else "(unknown)"

    source_lines: list[str] = []
    if task_id:
        source_lines.append(f"- Task: {task_id}")
    if rule_id:
        source_lines.append(f"- Rule: {rule_id}")
    source_lines.append(f"- BDD example: {bdd_id}")
    for ac_id in ac_ids:
        source_lines.append(f"- Acceptance criterion: {ac_id}")
    source_lines.append(f"- Feature file: {feature_path}")

    behavior = _behavior_lines(scenario)
    rationale = (
        "This behavior is a durable lifecycle gate and should be considered for "
        "architecture/spec tracking."
    )

    sections = [
        f"# Candidate behavior record: {scenario.title}",
        "",
        "## Source",
        "",
        *source_lines,
        "",
        "## Behavior",
        "",
        *behavior,
        "",
        "## Rationale",
        "",
        rationale,
    ]
    return "\n".join(sections) + "\n"


def write_archledger_candidate(feature: Feature, bdd_id: str, out: str | Path) -> None:
    """Render the candidate for *bdd_id* and write it to *out* as markdown."""
    text = render_archledger_candidate(feature, bdd_id)
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")


__all__ = [
    "render_archledger_candidate",
    "write_archledger_candidate",
]
