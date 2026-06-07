"""Serialize the Gherkin model to ``.feature`` text."""

from __future__ import annotations

from specweave.gherkin.model import Feature


def write_feature(feature: Feature) -> str:
    """Render a *feature* to a Gherkin feature string.

    Output rules:

    - Feature tags appear before ``Feature:``.
    - Scenario tags appear before ``Scenario:``.
    - Steps use two-space indentation.
    - A final newline is always added.
    """
    lines: list[str] = []

    # Feature-level tags
    for tag in feature.tags:
        lines.append(f"@{tag}")

    lines.append(f"Feature: {feature.title}")
    if feature.description:
        lines.append("")
        for line in feature.description.strip().splitlines():
            lines.append(f"  {line}")

    for scenario in feature.scenarios:
        lines.append("")
        # Scenario-level tags
        for tag in scenario.tags:
            lines.append(f"  @{tag}")
        lines.append(f"  Scenario: {scenario.title}")
        for step in scenario.steps:
            lines.append(f"    {step.keyword} {step.text}")

    lines.append("")
    return "\n".join(lines)
