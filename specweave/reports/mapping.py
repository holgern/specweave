"""Map normalized scenario results back to acceptance criteria by stable tags.

Matching rules (per the SpecWeave coding agent guide):

- match by ``@bdd-*`` first;
- map to ``@ac-*`` second;
- use scenario title only as fallback/debug text;
- never rely on scenario title as the primary identifier.

A criterion is reported ``passed`` only when at least one linked scenario passed
**and** no linked scenario failed/errored/skipped/was pending/undefined.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from specweave.reports.model import (
    HARD_FAIL_STATUSES,
    CriterionResult,
    ScenarioResult,
)


@dataclass(frozen=True)
class TraceIds:
    """The stable ids extracted from a scenario's tags."""

    bdd_ids: tuple[str, ...] = ()
    ac_ids: tuple[str, ...] = ()
    task_ids: tuple[str, ...] = ()
    rule_ids: tuple[str, ...] = ()


def extract_ids_from_tags(tags: Iterable[str]) -> TraceIds:
    """Partition *tags* into bdd/ac/task/rule id groups by canonical prefix."""
    bdd: list[str] = []
    ac: list[str] = []
    task: list[str] = []
    rule: list[str] = []
    for tag in tags:
        if tag.startswith("bdd-"):
            bdd.append(tag)
        elif tag.startswith("ac-"):
            ac.append(tag)
        elif tag.startswith("rule-"):
            rule.append(tag)
        elif tag.startswith("task-"):
            task.append(tag)
    return TraceIds(
        bdd_ids=tuple(bdd),
        ac_ids=tuple(ac),
        task_ids=tuple(task),
        rule_ids=tuple(rule),
    )


def _is_blocking(status: str, *, allow_skipped: bool = False) -> bool:
    """True when *status* should block a criterion from passing.

    ``skipped`` is blocking unless ``allow_skipped`` is set.
    """
    if status in HARD_FAIL_STATUSES:
        return True
    return status == "skipped" and not allow_skipped


def summarize_criteria(
    results: Iterable[ScenarioResult], *, allow_skipped: bool = False
) -> tuple[CriterionResult, ...]:
    """Roll scenario results up into per-acceptance-criterion results.

    A criterion passes only if at least one linked scenario passed and no linked
    scenario is in a blocking status (failed/skipped/pending/undefined/ambiguous).
    ``skipped`` is treated as blocking unless ``allow_skipped`` is set. Scenarios
    without any ``ac-*`` tag are ignored here (they do not count as AC
    validation).
    """
    by_criterion: dict[str, list[ScenarioResult]] = {}
    evidence_by_criterion: dict[str, list[str]] = {}
    for result in results:
        ids = extract_ids_from_tags(result.tags)
        if not ids.ac_ids:
            continue
        for ac_id in ids.ac_ids:
            by_criterion.setdefault(ac_id, []).append(result)
            evidence_by_criterion.setdefault(ac_id, [])
            for evidence in result.evidence:
                if evidence not in evidence_by_criterion[ac_id]:
                    evidence_by_criterion[ac_id].append(evidence)

    criteria: list[CriterionResult] = []
    for ac_id, linked in sorted(by_criterion.items()):
        has_pass = any(r.status == "passed" for r in linked)
        any_blocking = any(
            _is_blocking(r.status, allow_skipped=allow_skipped) for r in linked
        )
        status = "passed" if has_pass and not any_blocking else "failed"
        bdd_ids: list[str] = []
        for r in linked:
            ids = extract_ids_from_tags(r.tags)
            for bdd_id in ids.bdd_ids:
                if bdd_id not in bdd_ids:
                    bdd_ids.append(bdd_id)
        criteria.append(
            CriterionResult(
                criterion_id=ac_id,
                status=status,
                scenario_ids=tuple(bdd_ids),
                evidence=tuple(evidence_by_criterion[ac_id]),
            )
        )
    return tuple(criteria)


@dataclass(frozen=True)
class CoverageResult:
    """Result of checking that all expected acceptance criteria were covered."""

    status: str  # passed | failed
    missing: tuple[str, ...]


def require_expected_coverage(
    expected_ac_ids: Iterable[str],
    results: Iterable[ScenarioResult],
    *,
    allow_skipped: bool = False,
) -> CoverageResult:
    """Verify every expected ``ac-*`` has at least one passing linked scenario.

    Missing or only-failing coverage marks the result ``failed`` (fail-closed).
    """
    expected = tuple(expected_ac_ids)
    if not expected:
        return CoverageResult(status="passed", missing=())

    passed_criteria = {
        criterion.criterion_id
        for criterion in summarize_criteria(results, allow_skipped=allow_skipped)
        if criterion.status == "passed"
    }
    missing = tuple(ac_id for ac_id in expected if ac_id not in passed_criteria)
    return CoverageResult(
        status="failed" if missing else "passed",
        missing=missing,
    )
