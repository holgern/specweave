"""Narrow parser for generated/editable feature files.

Supports only the subset needed by ``bind`` and ``check``:

- ``@tags``
- ``Feature:``
- ``Scenario:``
- step lines beginning with ``Given``, ``When``, ``Then``, ``And``, ``But``
- comments and blank lines are ignored.
"""

from __future__ import annotations

from specweave.gherkin.model import Feature, Scenario, Step
from specweave.gherkin.tags import is_tag, parse_tag

_STEP_KEYWORDS = frozenset({"Given", "When", "Then", "And", "But"})


def _parse_tags(lines: list[str], start: int) -> tuple[tuple[str, ...], int]:
    """Collect consecutive tag lines from *start*.

    Returns (tags, next_line_index).
    """
    tags: list[str] = []
    i = start
    while i < len(lines) and is_tag(lines[i]):
        tag = parse_tag(lines[i])
        if tag:
            tags.append(tag)
        i += 1
    return tuple(tags), i


def parse_feature(text: str) -> Feature:
    """Parse a Gherkin feature from *text*.

    Raises ValueError on structural errors.
    """
    lines = text.splitlines()
    i = 0

    # Skip leading blanks / comments
    while i < len(lines) and (not lines[i].strip() or lines[i].strip().startswith("#")):
        i += 1

    # Feature-level tags
    feature_tags, i = _parse_tags(lines, i)

    # Feature:
    if i >= len(lines) or not lines[i].strip().startswith("Feature:"):
        raise ValueError("Expected 'Feature:' line")
    feature_title = lines[i].strip()[len("Feature:") :].strip()
    i += 1

    scenarios: list[Scenario] = []

    while i < len(lines):
        line = lines[i].strip()

        # Skip blanks and comments
        if not line or line.startswith("#"):
            i += 1
            continue

        # Scenario-level tags
        scenario_tags, i = _parse_tags(lines, i)

        # Scenario:
        if i >= len(lines) or not lines[i].strip().startswith("Scenario:"):
            raise ValueError("Expected 'Scenario:' line")
        scenario_title = lines[i].strip()[len("Scenario:") :].strip()
        i += 1

        steps: list[Step] = []
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith("#"):
                i += 1
                continue
            # Check if next line starts a new scenario (tag or Scenario:)
            if is_tag(line) or line.startswith("Scenario:"):
                break
            # Unexpected mid-feature, but handle gracefully
            if line.startswith("Feature:"):
                break

            # Parse step
            first_word = line.split(maxsplit=1)[0] if " " in line else line
            if first_word in _STEP_KEYWORDS:
                keyword = first_word
                text = line[len(keyword) :].strip()
                steps.append(Step(keyword=keyword, text=text))
                i += 1
            else:
                # Unknown line — skip (description lines, etc.)
                i += 1
                continue

        scenarios.append(
            Scenario(
                title=scenario_title,
                steps=tuple(steps),
                tags=scenario_tags,
            )
        )

    return Feature(title=feature_title, scenarios=tuple(scenarios), tags=feature_tags)
