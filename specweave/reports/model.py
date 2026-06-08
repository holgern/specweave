"""Normalized BDD report models.

These models describe runner-native BDD output normalized to a single
SpecWeave shape (schema version 2). They are produced by the format-specific
parsers (:mod:`specweave.reports.cucumber_json`, :mod:`specweave.reports.junit_xml`)
and assembled by :mod:`specweave.reports.normalize`.

Status vocabulary (per the SpecWeave coding agent guide):

- ``passed``
- ``failed`` (includes runner errors / hook failures)
- ``skipped``
- ``undefined``
- ``pending``
- ``ambiguous``

Normalization is fail-closed: ``failed``/``undefined``/``pending``/``ambiguous``
(and ``skipped`` unless explicitly allowed) mark the whole report ``failed``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

#: Statuses that always fail a normalized report.
HARD_FAIL_STATUSES = frozenset({"failed", "undefined", "pending", "ambiguous"})
#: All recognized scenario statuses.
ALL_STATUSES = frozenset(
    {"passed", "failed", "skipped", "undefined", "pending", "ambiguous"}
)


@dataclass(frozen=True)
class ScenarioResult:
    """A single scenario result extracted from a runner-native report."""

    name: str
    status: str
    tags: tuple[str, ...] = ()
    feature: str = ""
    rule: str | None = None
    duration_ms: int | None = None
    evidence: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class CriterionResult:
    """An acceptance-criterion roll-up over linked scenario results."""

    criterion_id: str
    status: str  # passed | failed
    scenario_ids: tuple[str, ...] = ()  # linked bdd-* ids
    evidence: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class NormalizedBddReport:
    """A fully normalized BDD execution report."""

    runner: str
    source_report: str
    results: tuple[ScenarioResult, ...]
    criteria: tuple[CriterionResult, ...] = field(default_factory=tuple)
    command: tuple[str, ...] = field(default_factory=tuple)
    status: str = "failed"
    schema_version: int = 2
    generated_by: str = "specweave"
    scenarios: int = 0
    passed: int = 0
    failed: int = 0
    undefined: int = 0
    pending: int = 0
    skipped: int = 0
    ambiguous: int = 0
    evidence: tuple[str, ...] = field(default_factory=tuple)
