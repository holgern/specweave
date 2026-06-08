"""Adapter for the official Cucumber ``gherkin-official`` parser."""

from __future__ import annotations

from pathlib import Path

from specweave.errors import ParseError
from specweave.gherkin.model import Feature, Rule, Scenario, Step


def _gherkin_imports() -> tuple[type, type]:
    try:
        from gherkin import Compiler, Parser
    except ImportError as exc:
        raise ParseError(
            "gherkin-official is required for official parser support; "
            "install specweave with its runtime dependencies."
        ) from exc
    return Parser, Compiler


def _strip_tag_name(name: str) -> str:
    """Strip leading ``@`` from a tag name."""
    return name.lstrip("@")


def _tag_list(tags: list[dict]) -> tuple[str, ...]:
    """Convert official tag dicts to a tuple of tag names (without ``@``)."""
    return tuple(_strip_tag_name(t["name"]) for t in tags)


def _location_line(location: dict[str, int] | None) -> int | None:
    """Extract line number from a location dict."""
    if location is None:
        return None
    return location.get("line")


def _build_steps(steps_data: list[dict]) -> tuple[Step, ...]:
    """Convert official step dicts to SpecWeave Step objects."""
    result: list[Step] = []
    for s in steps_data:
        keyword = s.get("keyword", "").strip()
        text = s.get("text", "")
        result.append(Step(keyword=keyword, text=text))
    return tuple(result)


def _build_scenario(scenario_data: dict, source_path: Path | None) -> Scenario:
    """Convert an official scenario dict to SpecWeave Scenario."""
    tags = _tag_list(scenario_data.get("tags", []))
    keyword = scenario_data.get("keyword", "Scenario")
    title = scenario_data.get("name", "")
    description = scenario_data.get("description", "")
    steps = _build_steps(scenario_data.get("steps", []))
    line = _location_line(scenario_data.get("location"))
    return Scenario(
        title=title,
        steps=steps,
        tags=tags,
        keyword=keyword,
        description=description.strip(),
        line=line,
    )


def _build_rule(rule_data: dict, source_path: Path | None) -> Rule:
    """Convert an official rule dict to SpecWeave Rule."""
    tags = _tag_list(rule_data.get("tags", []))
    title = rule_data.get("name", "")
    description = rule_data.get("description", "")
    line = _location_line(rule_data.get("location"))
    scenarios: list[Scenario] = []
    for child in rule_data.get("children", []):
        if "scenario" in child:
            scenarios.append(_build_scenario(child["scenario"], source_path))
    return Rule(
        title=title,
        scenarios=tuple(scenarios),
        tags=tags,
        description=description.strip(),
        line=line,
    )


def _document_to_feature(
    doc: dict, *, source_path: Path | None = None
) -> Feature:
    """Convert a gherkin-official ``feature`` AST dict to SpecWeave Feature."""
    feature_data = doc.get("feature", {})
    tags = _tag_list(feature_data.get("tags", []))
    title = feature_data.get("name", "")
    description = feature_data.get("description", "")
    line = _location_line(feature_data.get("location"))

    top_scenarios: list[Scenario] = []
    rules: list[Rule] = []

    for child in feature_data.get("children", []):
        if "scenario" in child:
            top_scenarios.append(
                _build_scenario(child["scenario"], source_path)
            )
        elif "rule" in child:
            rules.append(_build_rule(child["rule"], source_path))

    return Feature(
        title=title,
        scenarios=tuple(top_scenarios),
        rules=tuple(rules),
        tags=tags,
        description=description.strip(),
        source_path=source_path,
        line=line,
    )


def parse_classic_with_official(
    text: str,
    *,
    source_path: Path | None = None,
    compile_pickles: bool = False,
) -> Feature:
    """Parse classic Gherkin *text* using ``gherkin-official``.

    Returns a SpecWeave ``Feature``.
    """
    Parser, Compiler = _gherkin_imports()
    try:
        doc = Parser().parse(text)
    except Exception as exc:
        raise ParseError(str(exc)) from exc

    uri = source_path.as_posix() if source_path else "<string>"
    doc["uri"] = uri

    if compile_pickles:
        Compiler().compile(doc)

    return _document_to_feature(doc, source_path=source_path)


def validate_classic_with_official(
    text: str,
    *,
    source_path: Path | None = None,
) -> None:
    """Validate classic Gherkin *text* using ``gherkin-official``.

    Raises ``ParseError`` on invalid syntax.
    """
    Parser, _ = _gherkin_imports()
    try:
        Parser().parse(text)
    except Exception as exc:
        raise ParseError(str(exc)) from exc
