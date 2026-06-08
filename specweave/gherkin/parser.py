"""Narrow parser for generated/editable feature files.

Supports the subset needed by ``bind`` and ``check``:

- ``@tags`` (one or more per line, and/or one tag per line)
- ``Feature:``
- ``Rule:`` (optional; groups scenarios)
- ``Scenario:``
- step lines beginning with ``Given``, ``When``, ``Then``, ``And``, ``But``
- feature/rule free-text descriptions
- comments and blank lines are ignored.

The MVP originally only allowed top-level scenarios. Rules are the preferred
grouping unit for Taskledger-linked BDD; both may coexist in one feature.
"""

from __future__ import annotations

from specweave.gherkin.model import Feature, Rule, Scenario, Step
from specweave.gherkin.tags import is_tag_line, parse_tag_line

_STEP_KEYWORDS = frozenset({"Given", "When", "Then", "And", "But"})
_BLOCK_STARTS = ("Rule:", "Scenario:", "Feature:")


def _is_blank_or_comment(line: str) -> bool:
    stripped = line.strip()
    return not stripped or stripped.startswith("#")


def _skip_blanks_comments(lines: list[str], start: int) -> int:
    """Return the index of the next meaningful line at or after *start*."""
    i = start
    while i < len(lines) and _is_blank_or_comment(lines[i]):
        i += 1
    return i


def _parse_tag_lines(lines: list[str], start: int) -> tuple[tuple[str, ...], int]:
    """Collect consecutive tag lines from *start*.

    Each line may carry one or more tags (``@a @b``). Returns
    ``(tags, next_line_index)``.
    """
    tags: list[str] = []
    i = start
    while i < len(lines) and is_tag_line(lines[i]):
        tags.extend(parse_tag_line(lines[i]))
        i += 1
    return tuple(tags), i


def _is_block_boundary(stripped: str) -> bool:
    return is_tag_line(stripped) or stripped.startswith(_BLOCK_STARTS)


def _parse_description(lines: list[str], start: int) -> tuple[str, int]:
    """Collect free-text description lines until a block boundary.

    Stops at a tag line, ``Rule:``/``Scenario:``/``Feature:``, or EOF. Comments
    are skipped without ending the description; blank lines are preserved as
    paragraph separators.
    """
    desc: list[str] = []
    i = start
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith("#"):
            i += 1
            continue
        if stripped and _is_block_boundary(stripped):
            break
        desc.append(stripped)
        i += 1
    return "\n".join(desc).strip(), i


def _first_token(stripped: str) -> str:
    return stripped.split(maxsplit=1)[0] if stripped else ""


def _parse_steps(lines: list[str], start: int) -> tuple[tuple[Step, ...], int]:
    """Collect steps for the current scenario starting at *start*.

    Stops at the next tag line, ``Rule:``/``Scenario:``/``Feature:``. Blank and
    comment lines are skipped. Unrecognized non-block lines are skipped (doc
    strings, data tables, and other unsupported constructs are not modeled).
    """
    steps: list[Step] = []
    i = start
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if _is_block_boundary(stripped):
            break
        token = _first_token(stripped)
        if token in _STEP_KEYWORDS:
            text = stripped[len(token) :].strip()
            steps.append(Step(keyword=token, text=text))
        # Unknown line within a scenario: skip gracefully.
        i += 1
    return tuple(steps), i


def parse_feature(text: str) -> Feature:
    """Parse a Gherkin feature from *text*.

    Raises ValueError on structural errors.
    """
    lines = text.splitlines()

    i = _skip_blanks_comments(lines, 0)

    # Feature-level tags
    feature_tags, i = _parse_tag_lines(lines, i)

    if i >= len(lines) or not lines[i].strip().startswith("Feature:"):
        raise ValueError("Expected 'Feature:' line")
    feature_title = lines[i].strip()[len("Feature:") :].strip()
    i += 1

    description, i = _parse_description(lines, i)

    top_scenarios: list[Scenario] = []
    rules: list[Rule] = []

    # Current rule accumulation state.
    in_rule = False
    rule_title = ""
    rule_tags: tuple[str, ...] = ()
    rule_description = ""
    rule_scenarios: list[Scenario] = []

    def flush_rule() -> None:
        nonlocal in_rule, rule_title, rule_tags, rule_description, rule_scenarios
        if in_rule:
            rules.append(
                Rule(
                    title=rule_title,
                    scenarios=tuple(rule_scenarios),
                    tags=rule_tags,
                    description=rule_description,
                )
            )
            in_rule = False
            rule_title = ""
            rule_tags = ()
            rule_description = ""
            rule_scenarios = []

    while i < len(lines):
        i = _skip_blanks_comments(lines, i)
        if i >= len(lines):
            break

        tags, i = _parse_tag_lines(lines, i)
        if i >= len(lines):
            break

        stripped = lines[i].strip()

        if stripped.startswith("Rule:"):
            flush_rule()
            in_rule = True
            rule_title = stripped[len("Rule:") :].strip()
            rule_tags = tags
            i += 1
            rule_description, i = _parse_description(lines, i)
            continue

        if stripped.startswith("Scenario:"):
            scenario_title = stripped[len("Scenario:") :].strip()
            i += 1
            steps, i = _parse_steps(lines, i)
            scenario = Scenario(title=scenario_title, steps=steps, tags=tags)
            if in_rule:
                rule_scenarios.append(scenario)
            else:
                top_scenarios.append(scenario)
            continue

        if stripped.startswith("Feature:"):
            # A second feature ends parsing.
            break

        # Unknown line at block boundary: skip defensively.
        i += 1

    flush_rule()

    return Feature(
        title=feature_title,
        scenarios=tuple(top_scenarios),
        rules=tuple(rules),
        tags=feature_tags,
        description=description,
    )
