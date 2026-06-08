"""Parse Cucumber/Behave JSON reports into :class:`ScenarioResult` lists.

Supports the classic Cucumber JSON shape and tolerates the behave ``json``
formatter variant:

- tags as ``[{"name": "@x"}]`` (Cucumber) **or** ``["@x"]`` (behave)
- step status as ``step["result"]["status"]`` (Cucumber) **or** ``step["status"]``
  (behave)
- optional ``rule`` name per element (newer Cucumber)

This module only parses native output into scenario results; it does not decide
pass/fail policy. :mod:`specweave.reports.normalize` applies fail-closed status.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from specweave.reports.model import ScenarioResult

#: Worst-first priority for combining step statuses into a scenario status.
_STATUS_PRIORITY = {
    "failed": 0,
    "ambiguous": 1,
    "undefined": 2,
    "pending": 3,
    "skipped": 4,
    "passed": 5,
}
_UNKNOWN_PRIORITY = 2  # treat unknown statuses like 'undefined' (fail-closed)


def _coerce_tags(raw: Any) -> tuple[str, ...]:
    """Normalize a Cucumber/behave tags field into a tuple of tag contents."""
    if raw is None:
        return ()
    tags: list[str] = []
    for item in raw:
        if isinstance(item, str):
            tags.append(item.lstrip("@"))
        elif isinstance(item, dict):
            name = item.get("name")
            if isinstance(name, str):
                tags.append(name.lstrip("@"))
    return tuple(tags)


def _step_status(step: dict[str, Any]) -> str:
    result = step.get("result")
    if isinstance(result, dict):
        status = result.get("status")
        if isinstance(status, str):
            return status.lower()
    status = step.get("status")
    if isinstance(status, str):
        return status.lower()
    return "undefined"


def _scenario_status(steps: list[dict[str, Any]]) -> str:
    if not steps:
        return "passed"
    return min(
        (_step_status(step) for step in steps),
        key=lambda status: _STATUS_PRIORITY.get(status, _UNKNOWN_PRIORITY),
    )


def _duration_ms_from_result(result: Any) -> int | None:
    """Best-effort duration in milliseconds from a Cucumber/behave result."""
    if not isinstance(result, dict):
        return None
    duration = result.get("duration")
    if isinstance(duration, (int, float)):
        # Cucumber reports nanoseconds; behave reports seconds (float).
        # Heuristic: values >= 1e6 are treated as nanoseconds.
        if duration >= 1_000_000:
            return int(round(duration / 1_000_000))
        return int(round(duration * 1000))
    return None


def _element_to_result(
    element: dict[str, Any],
    feature_name: str,
    evidence: tuple[str, ...],
) -> ScenarioResult:
    steps = element.get("steps") or []
    rule = element.get("rule")
    if not isinstance(rule, str):
        rule = None
    first_result = next(
        (s.get("result") for s in steps if isinstance(s, dict) and s.get("result")),
        None,
    )
    return ScenarioResult(
        name=str(element.get("name", "")),
        status=_scenario_status(steps),
        tags=_coerce_tags(element.get("tags")),
        feature=feature_name,
        rule=rule,
        duration_ms=_duration_ms_from_result(first_result),
        evidence=evidence,
    )


def parse_cucumber_json(path: str | Path) -> tuple[ScenarioResult, ...]:
    """Parse a Cucumber/Behave JSON report at *path* into scenario results."""
    text = Path(path).read_text(encoding="utf-8")
    data = json.loads(text)
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        raise ValueError("Cucumber JSON report must be a list of feature objects")

    evidence = (str(path),)
    results: list[ScenarioResult] = []
    for feature in data:
        if not isinstance(feature, dict):
            continue
        feature_name = str(feature.get("name", ""))
        elements = feature.get("elements") or feature.get("scenarios") or []
        if not isinstance(elements, list):
            continue
        for element in elements:
            if not isinstance(element, dict):
                continue
            results.append(_element_to_result(element, feature_name, evidence))
    return tuple(results)
