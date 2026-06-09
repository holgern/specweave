"""Optional, file-based Taskledger adapter.

Taskledger owns task lifecycle, plans, acceptance criteria, and validation
state. SpecWeave exchanges data with Taskledger through JSON files only; this
module never imports Taskledger as a Python dependency.

Contracts::

    Input from Taskledger:   .taskledger/exports/task-0123.acceptance.json
    Output from SpecWeave:   specs/behavior/evidence/task-0123.bdd-evidence.json

The acceptance export may be either:

- the rich task-BDD shape (``task_id``, ``feature``, ``rules``, ``examples``),
  loaded verbatim via :func:`specweave.bdd.store.load_task_bdd_json`; or
- the legacy MVP shape (``task_id``, ``title``, ``acceptance_criteria`` list of
  ``{id, text}``), from which a minimal starter :class:`TaskBddSpec` is built
  with one empty BDD example per acceptance criterion.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from specweave.bdd.model import BddExample, TaskBddSpec
from specweave.bdd.store import task_bdd_from_dict
from specweave.behavior.common import feature_stem, slugify
from specweave.gherkin.model import Feature, Rule, Scenario, Step
from specweave.gherkin.writer import write_feature
from specweave.reports.mapping import extract_ids_from_tags
from specweave.reports.model import NormalizedBddReport
from specweave.reports.normalize import write_evidence_json


def _legacy_acceptance_to_spec(data: dict[str, Any]) -> TaskBddSpec:
    """Build a starter :class:`TaskBddSpec` from the MVP acceptance shape."""
    task_id = str(data.get("task_id", ""))
    feature = str(data.get("feature") or data.get("title") or task_id)
    criteria = data.get("acceptance_criteria") or []
    if not isinstance(criteria, list):
        raise ValueError("'acceptance_criteria' must be a list")

    examples: list[BddExample] = []
    for index, item in enumerate(criteria, start=1):
        if not isinstance(item, dict):
            continue
        ac_id = str(item.get("id") or f"ac-{index:04d}")
        text = str(item.get("text") or ac_id)
        examples.append(
            BddExample(
                id=f"bdd-{index:04d}",
                title=text,
                acceptance_criteria=(ac_id,),
            )
        )
    return TaskBddSpec(task_id=task_id, feature=feature, examples=tuple(examples))


def load_taskledger_acceptance_export(path: str | Path) -> TaskBddSpec:
    """Load a Taskledger acceptance export at *path* into a :class:`TaskBddSpec`.

    Supports both the rich task-BDD shape and the legacy MVP acceptance shape.
    """
    import json

    text = Path(path).read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("Taskledger acceptance export must be a JSON object")

    if "rules" in data or "examples" in data:
        return task_bdd_from_dict(data)
    return _legacy_acceptance_to_spec(data)


def task_id_from_report(report: NormalizedBddReport) -> str:
    """Derive the ``task-*`` id from a normalized report's scenario tags."""
    for result in report.results:
        ids = extract_ids_from_tags(result.tags)
        if ids.task_ids:
            return ids.task_ids[0]
    return ""


def write_taskledger_bdd_evidence(
    report: NormalizedBddReport,
    out: str | Path,
    task_id: str | None = None,
) -> str:
    """Write the report as Taskledger BDD evidence JSON at *out*.

    *task_id* defaults to the ``task-*`` id found in the report's scenario tags.
    Returns the task id that was recorded.
    """
    resolved = task_id or task_id_from_report(report)
    write_evidence_json(report, resolved, out)
    return resolved


def _behavior_feature_from_task_bdd(spec: TaskBddSpec, out: Path) -> Feature:
    area = slugify(out.parent.name)
    feature_slug = slugify(feature_stem(out))
    feature_tags = (f"area-{area}", f"feature-{feature_slug}")

    examples_by_rule: dict[str, list[BddExample]] = {rule.id: [] for rule in spec.rules}
    top_level: list[BddExample] = []
    for example in spec.examples:
        if example.rule_id and example.rule_id in examples_by_rule:
            examples_by_rule[example.rule_id].append(example)
        else:
            top_level.append(example)

    def to_scenario(example: BddExample) -> Scenario:
        tags: list[str] = []
        if example.id:
            tags.append(example.id)
        tags.extend(
            tag
            for tag in example.tags
            if not tag.startswith("task-") and not tag.startswith("ac-")
        )
        steps = (
            tuple(Step(keyword="Given", text=text) for text in example.given)
            + tuple(Step(keyword="When", text=text) for text in example.when)
            + tuple(Step(keyword="Then", text=text) for text in example.then)
        )
        return Scenario(
            title=example.title,
            steps=steps,
            tags=tuple(tags),
            keyword="Example",
        )

    rules = tuple(
        Rule(
            title=rule.title,
            tags=((rule.id,) if rule.id else ()),
            scenarios=tuple(
                to_scenario(example) for example in examples_by_rule[rule.id]
            ),
        )
        for rule in spec.rules
    )
    return Feature(
        title=spec.feature,
        tags=feature_tags,
        scenarios=tuple(to_scenario(example) for example in top_level),
        rules=rules,
    )


def write_behavior_feature_from_taskledger(
    path: str | Path,
    out: str | Path,
) -> Feature:
    """Write a canonical behavior feature from a Taskledger export."""

    output = Path(out)
    feature = _behavior_feature_from_task_bdd(
        load_taskledger_acceptance_export(path),
        output,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        write_feature(feature),
        encoding="utf-8",
    )
    return feature


__all__ = [
    "load_taskledger_acceptance_export",
    "task_id_from_report",
    "write_taskledger_bdd_evidence",
    "write_behavior_feature_from_taskledger",
]
