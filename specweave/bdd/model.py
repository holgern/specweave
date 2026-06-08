"""Task-local BDD data models.

These models are a portable representation of task BDD (rules and examples).
They are deliberately independent of the Gherkin :mod:`specweave.gherkin` model
and of Taskledger task state; :mod:`specweave.bdd.convert` translates between
the two.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BddRule:
    """A behaviour rule grouping one or more BDD examples."""

    id: str
    title: str


@dataclass(frozen=True)
class BddExample:
    """A single BDD example (Given/When/Then) linked to acceptance criteria."""

    id: str
    title: str
    given: tuple[str, ...] = ()
    when: tuple[str, ...] = ()
    then: tuple[str, ...] = ()
    rule_id: str | None = None
    acceptance_criteria: tuple[str, ...] = ()
    tags: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class TaskBddSpec:
    """A task-local BDD specification: task id, feature title, rules, examples."""

    task_id: str
    feature: str
    rules: tuple[BddRule, ...] = field(default_factory=tuple)
    examples: tuple[BddExample, ...] = field(default_factory=tuple)
