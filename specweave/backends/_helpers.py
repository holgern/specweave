"""Shared helpers for step-skeleton backends.

Lives outside :mod:`specweave.backends` ``__init__`` to avoid a circular import
between the backend registry and individual backends.
"""

from __future__ import annotations

from specweave.gherkin.model import Feature, Step


def collect_steps(feature: Feature) -> list[Step]:
    """Collect all steps from top-level scenarios and rule scenarios in order."""
    steps: list[Step] = []
    for scenario in feature.scenarios:
        steps.extend(scenario.steps)
    for rule in feature.rules:
        for scenario in rule.scenarios:
            steps.extend(scenario.steps)
    return steps


__all__ = ["collect_steps"]
