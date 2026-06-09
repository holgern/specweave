"""Strict SpecWeave subset validator for Gherkin features.

Rejects constructs that SpecWeave cannot preserve in its model:
Background, Scenario Outline, Scenario Template, Examples/Scenarios tables,
data tables, doc strings, wildcard ``*`` steps, and junk lines inside scenarios.
"""

from __future__ import annotations

import re
from pathlib import Path

from specweave.errors import ParseError

# Unsupported keywords that indicate constructs outside the SpecWeave subset.
_UNSUPPORTED_KEYWORDS = (
    "Background:",
    "Scenario Outline:",
    "Scenario Template:",
    "Examples:",
    "Scenarios:",
)

# Regex for a wildcard * step: lines starting with * followed by a space.
_WILDCARD_STEP_RE = re.compile(r"^\s*\*\s+\S")


def _fail(
    message: str,
    *,
    source_path: Path | None = None,
    line: int | None = None,
) -> None:
    prefix = ""
    if source_path is not None:
        prefix = f"{source_path}"
        if line is not None:
            prefix += f":{line}"
        prefix += ": "
    raise ParseError(f"{prefix}{message}")


def validate_classic_specweave_subset(
    text: str,
    *,
    source_path: Path | None = None,
) -> None:
    """Validate classic Gherkin *text* is within the SpecWeave subset.

    Raises ``ParseError`` on unsupported or ambiguous constructs.
    """
    lines = text.splitlines()
    in_scenario = False
    steps_started = False
    feature_seen = False
    feature_count = 0

    for line_no, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()

        # Skip blanks and comments
        if not stripped or stripped.startswith("#"):
            continue

        # Track Feature:
        if stripped.startswith("Feature:"):
            feature_count += 1
            feature_seen = True
            in_scenario = False
            steps_started = False
            if feature_count > 1:
                _fail(
                    "Multiple Feature: blocks are not supported in SpecWeave subset.",
                    source_path=source_path,
                    line=line_no,
                )
            continue

        # Detect unsupported block keywords
        for kw in _UNSUPPORTED_KEYWORDS:
            if stripped.startswith(kw):
                _fail(
                    f"Unsupported construct '{kw.split(':')[0]}' is not supported "
                    f"in the SpecWeave canonical subset.",
                    source_path=source_path,
                    line=line_no,
                )

        # Detect table rows (|)
        if stripped.startswith("|"):
            _fail(
                "Data tables are not supported in the SpecWeave canonical subset.",
                source_path=source_path,
                line=line_no,
            )

        # Detect doc strings (triple quotes)
        if stripped.startswith('"""') or stripped.startswith("'''"):
            _fail(
                "Doc strings are not supported in the SpecWeave canonical subset.",
                source_path=source_path,
                line=line_no,
            )

        # Track scenario/Example context
        if stripped.startswith(("Scenario:", "Example:")):
            in_scenario = True
            steps_started = False
            continue

        # Rule resets scenario context
        if stripped.startswith("Rule:"):
            in_scenario = False
            steps_started = False
            continue

        # Tag lines
        if stripped.startswith("@"):
            continue

        # Step keywords
        token = stripped.split(maxsplit=1)[0] if stripped else ""
        if token in ("Given", "When", "Then", "And", "But"):
            if in_scenario:
                steps_started = True
            continue

        # Wildcard * step
        if _WILDCARD_STEP_RE.match(stripped):
            _fail(
                "Wildcard * steps are not supported in the SpecWeave canonical subset.",
                source_path=source_path,
                line=line_no,
            )

        # Inside a scenario after steps started, anything else is junk
        if in_scenario and steps_started:
            _fail(
                f"Unsupported or invalid scenario line: {stripped}",
                source_path=source_path,
                line=line_no,
            )

    if not feature_seen:
        _fail(
            "Missing Feature: header.",
            source_path=source_path,
        )


def validate_markdown_specweave_subset(
    text: str,
    *,
    source_path: Path | None = None,
) -> None:
    """Reject legacy Markdown-with-Gherkin input."""
    _fail(
        "Markdown .feature.md files are no longer supported; "
        "convert to classic .feature.",
        source_path=source_path,
    )
