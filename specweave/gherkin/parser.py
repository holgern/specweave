"""Parser for editable Gherkin feature files."""

from __future__ import annotations

from pathlib import Path

from specweave.gherkin.model import Feature, Rule, Scenario, Step
from specweave.gherkin.tags import is_tag_line, parse_tag_line

_STEP_KEYWORDS = frozenset({"Given", "When", "Then", "And", "But"})
_SCENARIO_PREFIXES = ("Scenario:", "Example:")
_BLOCK_STARTS = ("Rule:", "Feature:", *_SCENARIO_PREFIXES)


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


def _parse_description(
    lines: list[str], start: int, *, stop_on_steps: bool = False
) -> tuple[str, int]:
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
        if stop_on_steps and _first_token(stripped) in _STEP_KEYWORDS:
            break
        if stripped and _is_block_boundary(stripped):
            break
        desc.append(stripped)
        i += 1
    return "\n".join(desc).strip(), i


def _first_token(stripped: str) -> str:
    return stripped.split(maxsplit=1)[0] if stripped else ""


def _parse_steps(
    lines: list[str], start: int, *, strict: bool = False
) -> tuple[tuple[Step, ...], int]:
    """Collect steps for the current scenario starting at *start*.

    Stops at the next tag line, ``Rule:``/``Scenario:``/``Feature:``.
    Blank and comment lines are skipped. When *strict* is True,
    unrecognized non-block lines raise ``ValueError`` instead of being
    silently skipped.
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
            i += 1
            continue
        if strict:
            raise ValueError(
                f"Unsupported or invalid scenario line at {i + 1}: {stripped}"
            )
        # Unknown line within a scenario: skip gracefully.
        i += 1
    return tuple(steps), i


def _is_scenario_header(stripped: str) -> bool:
    return stripped.startswith(_SCENARIO_PREFIXES)


def _scenario_keyword_and_title(stripped: str) -> tuple[str, str]:
    for prefix in _SCENARIO_PREFIXES:
        if stripped.startswith(prefix):
            return prefix[:-1], stripped[len(prefix) :].strip()
    raise ValueError(f"Unsupported scenario header: {stripped}")


def _parse_scenario(
    lines: list[str], start: int, tags: tuple[str, ...]
) -> tuple[Scenario, int]:
    stripped = lines[start].strip()
    keyword, title = _scenario_keyword_and_title(stripped)
    description, after_description = _parse_description(
        lines, start + 1, stop_on_steps=True
    )
    steps, end = _parse_steps(lines, after_description)
    return (
        Scenario(
            title=title,
            steps=steps,
            tags=tags,
            keyword=keyword,
            description=description,
            line=start + 1,
        ),
        end,
    )


def _parse_classic_specweave(text: str, *, source_path: Path | None = None) -> Feature:
    """Parse classic Gherkin using SpecWeave's built-in parser."""
    lines = text.splitlines()

    i = _skip_blanks_comments(lines, 0)

    # Feature-level tags
    feature_tags, i = _parse_tag_lines(lines, i)

    if i >= len(lines) or not lines[i].strip().startswith("Feature:"):
        raise ValueError("Expected 'Feature:' line")
    feature_line = i + 1
    feature_title = lines[i].strip()[len("Feature:") :].strip()
    i += 1

    description, i = _parse_description(lines, i)

    top_scenarios: list[Scenario] = []
    rules: list[Rule] = []

    while i < len(lines):
        i = _skip_blanks_comments(lines, i)
        if i >= len(lines):
            break

        tags, i = _parse_tag_lines(lines, i)
        if i >= len(lines):
            break

        stripped = lines[i].strip()

        if stripped.startswith("Rule:"):
            rule_title = stripped[len("Rule:") :].strip()
            rule_line = i + 1
            rule_description, i = _parse_description(lines, i + 1)
            rule_scenarios: list[Scenario] = []
            while i < len(lines):
                i = _skip_blanks_comments(lines, i)
                if i >= len(lines):
                    break
                scenario_tags, after_tags = _parse_tag_lines(lines, i)
                if after_tags >= len(lines):
                    i = after_tags
                    break
                nested = lines[after_tags].strip()
                if nested.startswith(("Rule:", "Feature:")):
                    break
                if _is_scenario_header(nested):
                    scenario, i = _parse_scenario(lines, after_tags, scenario_tags)
                    rule_scenarios.append(scenario)
                    continue
                i = after_tags + 1
            rules.append(
                Rule(
                    title=rule_title,
                    scenarios=tuple(rule_scenarios),
                    tags=tags,
                    description=rule_description,
                    line=rule_line,
                )
            )
            continue

        if _is_scenario_header(stripped):
            scenario, i = _parse_scenario(lines, i, tags)
            top_scenarios.append(scenario)
            continue

        if stripped.startswith("Feature:"):
            # A second feature ends parsing.
            break

        # Unknown line at block boundary: skip defensively.
        i += 1

    return Feature(
        title=feature_title,
        scenarios=tuple(top_scenarios),
        rules=tuple(rules),
        tags=feature_tags,
        description=description,
        source_path=source_path,
        line=feature_line,
    )


def parse_feature(
    text: str,
    *,
    source_path: Path | None = None,
    document_format: str | None = None,
    use_official: bool = False,
    compile_pickles: bool = False,
) -> Feature:
    """Parse a Gherkin feature from *text*.

    Dispatches based on *document_format* or *source_path* suffix:
    - ``.feature.md`` -> markdown parser
    - ``.feature`` -> classic parser (official or built-in)
    """
    if document_format is None and source_path is not None:
        if source_path.suffixes == [".feature", ".md"] or str(source_path).endswith(
            ".feature.md"
        ):
            document_format = "markdown"
        elif source_path.suffix == ".feature":
            document_format = "classic"
        else:
            document_format = "classic"
    elif document_format is None:
        document_format = "classic"

    if document_format == "markdown":
        from specweave.gherkin.markdown import parse_markdown_feature

        return parse_markdown_feature(text, source_path=source_path)

    if use_official:
        from specweave.gherkin.official import parse_classic_with_official

        return parse_classic_with_official(
            text, source_path=source_path, compile_pickles=compile_pickles
        )

    return _parse_classic_specweave(text, source_path=source_path)
