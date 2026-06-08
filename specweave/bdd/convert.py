"""Convert between :class:`TaskBddSpec` and the Gherkin :class:`Feature` model.

Conversion rules (per the SpecWeave coding agent guide):

- ``TaskBddSpec.task_id``  -> feature tag ``task-NNNN``
- ``BddRule.id``           -> rule tag ``rule-NNNN``
- ``BddExample.id``        -> scenario tag ``bdd-NNNN``
- ``BddExample.acceptance_criteria`` -> scenario tags ``ac-NNNN``
- ``given`` / ``when`` / ``then`` arrays -> Gherkin steps

The canonical scenario tag order is ``@bdd-* @task-* @rule-* @ac-*``, matching
the guide's target Gherkin. The conversion round-trips: exporting a spec to a
feature and importing it back preserves task/rule/bdd/ac ids.
"""

from __future__ import annotations

from collections.abc import Iterable

from specweave.bdd.model import BddExample, BddRule, TaskBddSpec
from specweave.gherkin.model import Feature, Rule, Scenario, Step

#: Order in which canonical id prefixes are emitted as scenario tags.
_CANONICAL_PREFIX_ORDER = ("bdd-", "task-", "rule-", "ac-")


def _find_by_prefix(tags: Iterable[str], prefix: str) -> str | None:
    """Return the first tag starting with *prefix*, or None."""
    for tag in tags:
        if tag.startswith(prefix):
            return tag
    return None


def _scenario_tags_for_example(example: BddExample, task_id: str) -> tuple[str, ...]:
    """Build the canonical ordered, de-duplicated scenario tag list."""
    ordered: list[str] = []
    seen: set[str] = set()

    def add(value: str | None) -> None:
        if value and value not in seen:
            ordered.append(value)
            seen.add(value)

    add(example.id)
    add(task_id)
    add(example.rule_id)
    for ac in example.acceptance_criteria:
        add(ac)
    for extra in example.tags:
        # Preserve extra tags but keep canonical ones first.
        if not any(extra.startswith(p) for p in _CANONICAL_PREFIX_ORDER):
            add(extra)

    return tuple(ordered)


def _example_steps(example: BddExample) -> tuple[Step, ...]:
    steps: list[Step] = []
    steps.extend(Step(keyword="Given", text=g) for g in example.given)
    steps.extend(Step(keyword="When", text=w) for w in example.when)
    steps.extend(Step(keyword="Then", text=t) for t in example.then)
    return tuple(steps)


def _example_to_scenario(example: BddExample, task_id: str) -> Scenario:
    return Scenario(
        title=example.title,
        steps=_example_steps(example),
        tags=_scenario_tags_for_example(example, task_id),
    )


def task_bdd_to_feature(spec: TaskBddSpec) -> Feature:
    """Render a :class:`TaskBddSpec` to a target-format Gherkin :class:`Feature`."""
    feature_tag = spec.task_id if spec.task_id else None
    feature_tags: tuple[str, ...] = (feature_tag,) if feature_tag else ()

    rule_ids = {rule.id for rule in spec.rules}

    top_examples = [
        ex for ex in spec.examples if not ex.rule_id or ex.rule_id not in rule_ids
    ]
    examples_by_rule: dict[str, list[BddExample]] = {rule.id: [] for rule in spec.rules}
    for ex in spec.examples:
        if ex.rule_id in rule_ids:
            examples_by_rule[ex.rule_id].append(ex)

    rules = tuple(
        Rule(
            title=rule.title,
            tags=(rule.id,) if rule.id else (),
            scenarios=tuple(
                _example_to_scenario(ex, spec.task_id)
                for ex in examples_by_rule[rule.id]
            ),
        )
        for rule in spec.rules
    )

    top_scenarios = tuple(_example_to_scenario(ex, spec.task_id) for ex in top_examples)

    return Feature(
        title=spec.feature,
        scenarios=top_scenarios,
        rules=rules,
        tags=feature_tags,
    )


def _split_steps(
    steps: Iterable[Step],
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """Group Gherkin steps into (given, when, then) text tuples.

    ``And``/``But`` continue the most recent section. A leading ``And``/``But``
    with no preceding keyword is treated as a ``Given`` (defensive fallback).
    """
    given: list[str] = []
    when: list[str] = []
    then: list[str] = []
    current: list[str] | None = None
    for step in steps:
        keyword = step.keyword
        if keyword == "Given":
            current = given
        elif keyword == "When":
            current = when
        elif keyword == "Then":
            current = then
        elif current is None:
            current = given
        if current is not None:
            current.append(step.text)
    return tuple(given), tuple(when), tuple(then)


def _scenario_to_example(
    scenario: Scenario, task_id: str, rule_id: str | None
) -> BddExample:
    bdd_id = _find_by_prefix(scenario.tags, "bdd-")
    ac_ids = tuple(t for t in scenario.tags if t.startswith("ac-"))
    reserved = {
        bdd_id,
        task_id,
        rule_id,
    }
    reserved.discard(None)
    extra_tags = tuple(
        t for t in scenario.tags if t not in reserved and not t.startswith("ac-")
    )
    given, when, then = _split_steps(scenario.steps)
    return BddExample(
        id=bdd_id or "",
        title=scenario.title,
        given=given,
        when=when,
        then=then,
        rule_id=rule_id,
        acceptance_criteria=ac_ids,
        tags=extra_tags,
    )


def feature_to_task_bdd(feature: Feature) -> TaskBddSpec:
    """Convert a Gherkin :class:`Feature` back into a :class:`TaskBddSpec`.

    Task id is taken from the feature tag matching ``task-``. Rule ids come from
    rule tags matching ``rule-``. Example ids come from scenario ``bdd-*`` tags.
    """
    task_id = _find_by_prefix(feature.tags, "task-") or ""

    rules = tuple(
        BddRule(
            id=_find_by_prefix(rule.tags, "rule-") or "",
            title=rule.title,
        )
        for rule in feature.rules
    )
    examples: list[BddExample] = []
    for rule in feature.rules:
        rule_id = _find_by_prefix(rule.tags, "rule-")
        for scenario in rule.scenarios:
            examples.append(_scenario_to_example(scenario, task_id, rule_id))
    for scenario in feature.scenarios:
        examples.append(_scenario_to_example(scenario, task_id, None))

    return TaskBddSpec(
        task_id=task_id,
        feature=feature.title,
        rules=rules,
        examples=tuple(examples),
    )
