"""Serialize the Gherkin model to ``.feature`` text."""

from __future__ import annotations

from specweave.gherkin.model import Feature, Rule, Scenario


def _format_tag_line(tags: tuple[str, ...], indent: str) -> str | None:
    """Render *tags* as a single space-joined line, or None when empty."""
    if not tags:
        return None
    return f"{indent}{' '.join(f'@{t}' for t in tags)}"


def _write_description(description: str, indent: str) -> list[str]:
    lines: list[str] = []
    if description:
        lines.append("")
        for line in description.strip().splitlines():
            lines.append(f"{indent}{line.strip()}")
    return lines


def _write_scenario(scenario: Scenario, indent: str, step_indent: str) -> list[str]:
    lines: list[str] = [""]
    tag_line = _format_tag_line(scenario.tags, indent)
    if tag_line is not None:
        lines.append(tag_line)
    keyword = (
        scenario.keyword if scenario.keyword in {"Scenario", "Example"} else "Scenario"
    )
    lines.append(f"{indent}{keyword}: {scenario.title}")
    lines.extend(_write_description(scenario.description, step_indent))
    for step in scenario.steps:
        lines.append(f"{step_indent}{step.keyword} {step.text}")
    return lines


def _write_rule(rule: Rule) -> list[str]:
    lines: list[str] = [""]
    tag_line = _format_tag_line(rule.tags, "  ")
    if tag_line is not None:
        lines.append(tag_line)
    lines.append(f"  Rule: {rule.title}")
    lines.extend(_write_description(rule.description, "    "))
    for scenario in rule.scenarios:
        lines.extend(_write_scenario(scenario, "    ", "      "))
    return lines


def write_feature(feature: Feature) -> str:
    """Render a *feature* to a Gherkin feature string.

    Output rules:

    - Feature tags appear before ``Feature:`` as one space-joined line.
    - Scenario and rule tags appear on one space-joined line before their
      header (e.g. ``@bdd-0001 @task-0123 @rule-0001 @ac-0001``).
    - Top-level scenarios use two-space indent; scenarios inside a rule use
      four-space indent. Steps are indented two spaces deeper than their
      scenario header.
    - A final newline is always added.
    """
    lines: list[str] = []

    tag_line = _format_tag_line(feature.tags, "")
    if tag_line is not None:
        lines.append(tag_line)

    lines.append(f"Feature: {feature.title}")
    lines.extend(_write_description(feature.description, "  "))

    for scenario in feature.scenarios:
        lines.extend(_write_scenario(scenario, "  ", "    "))

    for rule in feature.rules:
        lines.extend(_write_rule(rule))

    lines.append("")
    return "\n".join(lines)
