"""Deserialize a JSON feature draft into SpecWeave's Feature model."""

from __future__ import annotations

import json
from pathlib import Path

from specweave.gherkin.model import Feature, Rule, Scenario, Step


def parse_feature_draft(data: dict) -> Feature:
    """Convert a feature-draft JSON dict into a :class:`Feature` instance.

    Expected schema::

        {
          "title": "...",
          "description": "...",
          "tags": ["area-x", "feature-y"],
          "rules": [
            {
              "title": "...",
              "tags": ["rule-z"],
              "scenarios": [
                {
                  "title": "...",
                  "keyword": "Example",
                  "tags": ["bdd-id"],
                  "steps": [
                    ["Given", "..."],
                    ["When", "..."],
                    ["Then", "..."]
                  ]
                }
              ]
            }
          ]
        }
    """

    title = data.get("title", "")
    description = data.get("description", "")
    tags = tuple(data.get("tags", ()))
    rules = tuple(_parse_rule(r) for r in data.get("rules", []))
    # Support top-level scenarios too
    scenarios = tuple(_parse_scenario(s) for s in data.get("scenarios", []))
    return Feature(
        title=title,
        description=description,
        tags=tags,
        rules=rules,
        scenarios=scenarios,
    )


def _parse_rule(data: dict) -> Rule:
    return Rule(
        title=data.get("title", ""),
        tags=tuple(data.get("tags", ())),
        description=data.get("description", ""),
        scenarios=tuple(_parse_scenario(s) for s in data.get("scenarios", [])),
    )


def _parse_scenario(data: dict) -> Scenario:
    steps = tuple(
        Step(keyword=step[0], text=step[1])
        for step in data.get("steps", [])
        if isinstance(step, (list, tuple)) and len(step) >= 2
    )
    return Scenario(
        title=data.get("title", ""),
        keyword=data.get("keyword", "Example"),
        tags=tuple(data.get("tags", ())),
        steps=steps,
    )


def load_feature_draft(path: Path) -> Feature:
    """Load a feature draft from a JSON file."""
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    return parse_feature_draft(data)
