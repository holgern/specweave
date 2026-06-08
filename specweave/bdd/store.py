"""JSON load/save for the task-local BDD :class:`TaskBddSpec`.

Acceptance criteria input shape (per the SpecWeave coding agent guide)::

    {
      "task_id": "task-0123",
      "feature": "Task lifecycle gates",
      "rules": [{"id": "rule-0001", "title": "..."}],
      "examples": [
        {
          "id": "bdd-0001",
          "title": "...",
          "rule_id": "rule-0001",
          "given": ["..."],
          "when": ["..."],
          "then": ["..."],
          "acceptance_criteria": ["ac-0001"],
          "tags": ["@custom"]
        }
      ]
    }
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from specweave.bdd.model import BddExample, BddRule, TaskBddSpec


def _as_str_list(value: Any, key: str, source: str) -> list[str]:
    raw = value.get(key)
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError(f"{source} '{key}' must be a list, got {type(raw).__name__}")
    return [str(item) for item in raw]


def _example_from_dict(data: dict[str, Any]) -> BddExample:
    rule_id = data.get("rule_id")
    return BddExample(
        id=str(data.get("id", "")),
        title=str(data.get("title", "")),
        given=tuple(_as_str_list(data, "given", "example")),
        when=tuple(_as_str_list(data, "when", "example")),
        then=tuple(_as_str_list(data, "then", "example")),
        rule_id=str(rule_id) if rule_id is not None else None,
        acceptance_criteria=tuple(_as_str_list(data, "acceptance_criteria", "example")),
        tags=tuple(_as_str_list(data, "tags", "example")),
    )


def _rule_from_dict(data: dict[str, Any]) -> BddRule:
    return BddRule(
        id=str(data.get("id", "")),
        title=str(data.get("title", "")),
    )


def task_bdd_from_dict(data: dict[str, Any]) -> TaskBddSpec:
    """Build a :class:`TaskBddSpec` from a parsed JSON dict."""
    return _spec_from_dict(data)


def _spec_from_dict(data: dict[str, Any]) -> TaskBddSpec:
    if not isinstance(data, dict):
        raise ValueError("Task BDD JSON must be a JSON object")
    rules_raw = data.get("rules", [])
    if not isinstance(rules_raw, list):
        raise ValueError("'rules' must be a list")
    examples_raw = data.get("examples", [])
    if not isinstance(examples_raw, list):
        raise ValueError("'examples' must be a list")
    return TaskBddSpec(
        task_id=str(data.get("task_id", "")),
        feature=str(data.get("feature", "")),
        rules=tuple(_rule_from_dict(r) for r in rules_raw),
        examples=tuple(_example_from_dict(e) for e in examples_raw),
    )


def load_task_bdd_json(path: str | Path) -> TaskBddSpec:
    """Load a :class:`TaskBddSpec` from a JSON file at *path*."""
    text = Path(path).read_text(encoding="utf-8")
    data = json.loads(text)
    return _spec_from_dict(data)


def _spec_to_dict(spec: TaskBddSpec) -> dict[str, Any]:
    return {
        "task_id": spec.task_id,
        "feature": spec.feature,
        "rules": [{"id": rule.id, "title": rule.title} for rule in spec.rules],
        "examples": [
            {
                "id": ex.id,
                "title": ex.title,
                "rule_id": ex.rule_id,
                "given": list(ex.given),
                "when": list(ex.when),
                "then": list(ex.then),
                "acceptance_criteria": list(ex.acceptance_criteria),
                "tags": list(ex.tags),
            }
            for ex in spec.examples
        ],
    }


def save_task_bdd_json(spec: TaskBddSpec, path: str | Path) -> None:
    """Write *spec* to *path* as JSON with stable, sorted keys and indentation."""
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        _spec_to_dict(spec), indent=2, sort_keys=True, ensure_ascii=False
    )
    out_path.write_text(payload + "\n", encoding="utf-8")
