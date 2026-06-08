"""SpecWeave-supported Markdown-with-Gherkin (MDG) adapter.

Parses and writes a subset of Cucumber Markdown-with-Gherkin (``.feature.md``).
Tags use backticked format: `` `@tag-name` ``.
"""

from __future__ import annotations

import re
from pathlib import Path

from specweave.gherkin.model import Feature, Rule, Scenario, Step

# ---------------------------------------------------------------------------
# Tag helpers
# ---------------------------------------------------------------------------

_TAG_PATTERN = re.compile(r"`@([^`]+)`")

_TAG_LINE_PATTERN = re.compile(
    r"^\s*(`@[^`]+`(?:\s+`@[^`]+`)*)\s*$"
)


def _parse_backticked_tags(line: str) -> list[str]:
    """Extract tag names (without ``@``) from backticked tags on *line*."""
    return _TAG_PATTERN.findall(line)


def _has_backticked_tags(line: str) -> bool:
    """Check if *line* contains only backticked tags (and whitespace)."""
    return bool(_TAG_LINE_PATTERN.match(line))


def _format_backticked_tags(tags: tuple[str, ...]) -> str:
    """Render *tags* as a backticked tag line."""
    if not tags:
        return ""
    return " ".join(f"`@{t}`" for t in tags)


# ---------------------------------------------------------------------------
# Heading patterns
# ---------------------------------------------------------------------------

_FEATURE_HEADING = re.compile(r"^#{1,6}\s+Feature:\s*(.*)$", re.IGNORECASE)
_RULE_HEADING = re.compile(r"^#{1,6}\s+Rule:\s*(.*)$", re.IGNORECASE)
_SCENARIO_HEADING = re.compile(
    r"^#{1,6}\s+(Scenario|Example|Scenario Outline|Scenario Template):\s*(.*)$",
    re.IGNORECASE,
)
_STEP_BULLET = re.compile(
    r"^\s*[-*]\s+(Given|When|Then|And|But)\s+(.*)$", re.IGNORECASE
)
_STEP_KEYWORDS = frozenset({"Given", "When", "Then", "And", "But"})


def _is_blank(line: str) -> bool:
    return not line.strip()


def _is_comment(line: str) -> bool:
    """True if *line* is a Gherkin/Markdown comment (not a heading)."""
    stripped = line.strip()
    if not stripped or not stripped.startswith("#"):
        return False
    # A line starting with # followed by a space and a Gherkin keyword is a
    # Markdown heading, not a comment.
    rest = stripped.lstrip("#").strip()
    for keyword in ("Feature:", "Rule:", "Scenario:", "Example:",
                    "Scenario Outline:", "Scenario Template:"):
        if rest.startswith(keyword):
            return False
    # Not a heading keyword -> treat as comment
    return True


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


def parse_markdown_feature(  # noqa: C901
    text: str, *, source_path: Path | None = None
) -> Feature:
    """Parse Markdown-with-Gherkin *text* into a SpecWeave ``Feature``.

    Supported subset:
    - Backticked tags (`` `@tag` ``) before headings
    - ``Feature:``, ``Rule:``, ``Scenario:``/``Example:`` headings
    - Bullet steps (``* Given`` / ``- When`` / etc.)
    - Free Markdown prose as descriptions
    """
    lines = text.splitlines()

    feature_title = ""
    feature_tags: tuple[str, ...] = ()
    feature_description = ""
    feature_line: int | None = None

    top_scenarios: list[Scenario] = []
    rules: list[Rule] = []

    # Parse state
    i = 0
    current_tags: tuple[str, ...] = ()
    pending_tags: tuple[str, ...] = ()
    collected_desc: list[str] = []

    def _flush_description() -> str:
        nonlocal collected_desc
        result = "\n".join(collected_desc).strip()
        collected_desc = []
        return result

    while i < len(lines):
        line = lines[i]

        if _is_blank(line) or _is_comment(line):
            i += 1
            continue

        # Apply any pending tags from rule break-out
        if pending_tags:
            current_tags = pending_tags
            pending_tags = ()

        # Tag line
        if _has_backticked_tags(line):
            current_tags = tuple(_parse_backticked_tags(line))
            i += 1
            continue

        # Feature heading
        m = _FEATURE_HEADING.match(line)
        if m:
            feature_title = m.group(1).strip()
            feature_tags = current_tags
            current_tags = ()
            feature_line = i + 1
            i += 1
            # Collect description until next heading or tag line
            while i < len(lines):
                if _is_blank(lines[i]):
                    collected_desc.append("")
                    i += 1
                    continue
                if _is_comment(lines[i]):
                    i += 1
                    continue
                if _has_backticked_tags(lines[i]):
                    break
                if _RULE_HEADING.match(lines[i]):
                    break
                if _SCENARIO_HEADING.match(lines[i]):
                    break
                if _FEATURE_HEADING.match(lines[i]):
                    break
                collected_desc.append(lines[i].strip())
                i += 1
            feature_description = _flush_description()
            continue

        # Rule heading
        m = _RULE_HEADING.match(line)
        if m:
            rule_title = m.group(1).strip()
            rule_tags = current_tags
            current_tags = ()
            rule_line = i + 1
            # Determine heading depth for nesting
            raw_rule = line.rstrip()
            rule_depth = len(raw_rule) - len(raw_rule.lstrip("#"))
            i += 1
            rule_desc_lines: list[str] = []
            rule_scenarios: list[Scenario] = []

            # Collect description / scenarios until next rule or feature heading
            while i < len(lines):
                if _is_blank(lines[i]):
                    rule_desc_lines.append("")
                    i += 1
                    continue
                if _is_comment(lines[i]):
                    i += 1
                    continue
                if _has_backticked_tags(lines[i]):
                    # Tags before scenario - store temporarily
                    scenario_tags = tuple(_parse_backticked_tags(lines[i]))
                    i += 1
                    # Skip blanks
                    while i < len(lines) and _is_blank(lines[i]):
                        i += 1
                    if i >= len(lines):
                        break
                    # Check heading depth to avoid nesting same-level scenarios
                    raw_h = lines[i].rstrip()
                    h_depth = len(raw_h) - len(raw_h.lstrip("#"))
                    if h_depth <= rule_depth:
                        # Same or shallower depth -> outside this rule
                        pending_tags = scenario_tags
                        break
                    sm = _SCENARIO_HEADING.match(lines[i])
                    if sm:
                        scenario_title = sm.group(2).strip()
                        scenario_keyword = sm.group(1)
                        scenario_line = i + 1
                        scenario_desc_lines: list[str] = []
                        steps: list[Step] = []
                        i += 1
                        while i < len(lines):
                            if _is_blank(lines[i]):
                                scenario_desc_lines.append("")
                                i += 1
                                continue
                            if _is_comment(lines[i]):
                                i += 1
                                continue
                            if _has_backticked_tags(lines[i]):
                                break
                            step_m = _STEP_BULLET.match(lines[i])
                            if step_m:
                                kw = step_m.group(1)
                                txt = step_m.group(2).strip()
                                steps.append(
                                    Step(keyword=kw, text=txt)
                                )
                                i += 1
                                continue
                            if _RULE_HEADING.match(lines[i]):
                                break
                            if _FEATURE_HEADING.match(lines[i]):
                                break
                            if _SCENARIO_HEADING.match(lines[i]):
                                break
                            # Description line within scenario
                            scenario_desc_lines.append(lines[i].strip())
                            i += 1
                        scenario_desc = "\n".join(scenario_desc_lines).strip()
                        rule_scenarios.append(
                            Scenario(
                                title=scenario_title,
                                steps=tuple(steps),
                                tags=scenario_tags,
                                keyword=scenario_keyword,
                                description=scenario_desc,
                                line=scenario_line,
                            )
                        )
                    continue
                # Check heading depth to avoid nesting same-level scenarios
                raw_h = lines[i].rstrip()
                h_depth = len(raw_h) - len(raw_h.lstrip("#"))
                if h_depth <= rule_depth:
                    # Same or shallower depth -> outside this rule
                    break
                sm = _SCENARIO_HEADING.match(lines[i])
                if sm:
                    scenario_title = sm.group(2).strip()
                    scenario_keyword = sm.group(1)
                    scenario_line = i + 1
                    scenario_desc_lines = []
                    steps = []
                    i += 1
                    while i < len(lines):
                        if _is_blank(lines[i]):
                            scenario_desc_lines.append("")
                            i += 1
                            continue
                        if _is_comment(lines[i]):
                            i += 1
                            continue
                        if _has_backticked_tags(lines[i]):
                            break
                        step_m = _STEP_BULLET.match(lines[i])
                        if step_m:
                            kw = step_m.group(1)
                            txt = step_m.group(2).strip()
                            steps.append(
                                Step(keyword=kw, text=txt)
                            )
                            i += 1
                            continue
                        if _RULE_HEADING.match(lines[i]):
                            break
                        if _FEATURE_HEADING.match(lines[i]):
                            break
                        if _SCENARIO_HEADING.match(lines[i]):
                            break
                        scenario_desc_lines.append(lines[i].strip())
                        i += 1
                    scenario_desc = "\n".join(scenario_desc_lines).strip()
                    rule_scenarios.append(
                        Scenario(
                            title=scenario_title,
                            steps=tuple(steps),
                            tags=(),
                            keyword=scenario_keyword,
                            description=scenario_desc,
                            line=scenario_line,
                        )
                    )
                    continue
                if _RULE_HEADING.match(lines[i]):
                    break
                if _FEATURE_HEADING.match(lines[i]):
                    break
                # Description line for rule
                rule_desc_lines.append(lines[i].strip())
                i += 1

            rules.append(
                Rule(
                    title=rule_title,
                    scenarios=tuple(rule_scenarios),
                    tags=rule_tags,
                    description="\n".join(rule_desc_lines).strip(),
                    line=rule_line,
                )
            )
            continue

        # Top-level scenario heading
        sm = _SCENARIO_HEADING.match(line)
        if sm:
            scenario_title = sm.group(2).strip()
            scenario_keyword = sm.group(1)
            scenario_tags = current_tags
            current_tags = ()
            scenario_line = i + 1
            scenario_desc_lines = []
            steps = []
            i += 1
            while i < len(lines):
                if _is_blank(lines[i]):
                    scenario_desc_lines.append("")
                    i += 1
                    continue
                if _is_comment(lines[i]):
                    i += 1
                    continue
                if _has_backticked_tags(lines[i]):
                    break
                step_m = _STEP_BULLET.match(lines[i])
                if step_m:
                    kw = step_m.group(1)
                    txt = step_m.group(2).strip()
                    steps.append(Step(keyword=kw, text=txt))
                    i += 1
                    continue
                if _FEATURE_HEADING.match(lines[i]):
                    break
                if _RULE_HEADING.match(lines[i]):
                    break
                if _SCENARIO_HEADING.match(lines[i]):
                    break
                scenario_desc_lines.append(lines[i].strip())
                i += 1
            scenario_desc = "\n".join(scenario_desc_lines).strip()
            top_scenarios.append(
                Scenario(
                    title=scenario_title,
                    steps=tuple(steps),
                    tags=scenario_tags,
                    keyword=scenario_keyword,
                    description=scenario_desc,
                    line=scenario_line,
                )
            )
            continue

        # Unknown line - skip
        i += 1

    return Feature(
        title=feature_title,
        scenarios=tuple(top_scenarios),
        rules=tuple(rules),
        tags=feature_tags,
        description=feature_description,
        source_path=source_path,
        line=feature_line,
    )


# ---------------------------------------------------------------------------
# Writer
# ---------------------------------------------------------------------------


def write_markdown_feature(feature: Feature) -> str:
    """Render a SpecWeave ``Feature`` to Markdown-with-Gherkin text."""
    lines: list[str] = []

    # Feature tags
    tag_line = _format_backticked_tags(feature.tags)
    if tag_line:
        lines.append(tag_line)

    # Feature heading
    lines.append(f"# Feature: {feature.title}")

    # Feature description
    if feature.description:
        for para in feature.description.splitlines():
            lines.append(f"\n{para.strip()}")

    # Top-level scenarios
    for scenario in feature.scenarios:
        _write_md_scenario(scenario, lines, has_rule=False)

    # Rules
    for rule in feature.rules:
        _write_md_rule(rule, lines)

    lines.append("")
    return "\n".join(lines)


def _write_md_scenario(
    scenario: Scenario, lines: list[str], *, has_rule: bool
) -> None:
    """Append a Markdown scenario to *lines*."""
    lines.append("")
    tag_line = _format_backticked_tags(scenario.tags)
    if tag_line:
        lines.append(tag_line)
    level = "###" if has_rule else "##"
    keyword = (
        scenario.keyword
        if scenario.keyword
        in {"Scenario", "Example", "Scenario Outline", "Scenario Template"}
        else "Scenario"
    )
    lines.append(f"{level} {keyword}: {scenario.title}")
    if scenario.description:
        for desc_line in scenario.description.splitlines():
            lines.append(f"\n{desc_line.strip()}")
    for step in scenario.steps:
        lines.append(f"* {step.keyword} {step.text}")


def _write_md_rule(rule: Rule, lines: list[str]) -> None:
    """Append a Markdown rule to *lines*."""
    lines.append("")
    tag_line = _format_backticked_tags(rule.tags)
    if tag_line:
        lines.append(tag_line)
    lines.append(f"## Rule: {rule.title}")
    if rule.description:
        for desc_line in rule.description.splitlines():
            lines.append(f"\n{desc_line.strip()}")
    for scenario in rule.scenarios:
        _write_md_scenario(scenario, lines, has_rule=True)


def markdown_to_classic(text: str) -> str:
    """Convert Markdown-with-Gherkin *text* to classic Gherkin.

    Uses SpecWeave's internal model as the intermediary.
    """
    from specweave.gherkin.writer import write_classic_feature

    feature = parse_markdown_feature(text)
    return write_classic_feature(feature)
