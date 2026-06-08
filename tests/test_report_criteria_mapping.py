"""Tests for acceptance-criteria mapping (Phase 4).

Covers the safety rules from the SpecWeave coding agent guide:

- match by ``@bdd-*`` first, ``@ac-*`` second, never by scenario title;
- a criterion passes only if a passing linked scenario exists and no linked
  scenario failed/skipped/was pending/undefined;
- unlinked scenarios (no ``ac-*``) do not count as AC validation;
- missing expected ``ac-*`` coverage fails the report.
"""

from __future__ import annotations

from specweave.reports.mapping import (
    CoverageResult,
    extract_ids_from_tags,
    require_expected_coverage,
    summarize_criteria,
)
from specweave.reports.model import ScenarioResult


def _scenario(  # type: ignore[no-untyped-def]
    name: str, status: str, tags: tuple[str, ...]
) -> ScenarioResult:
    return ScenarioResult(name=name, status=status, tags=tags)


def test_extract_ids_partitions_by_prefix() -> None:
    ids = extract_ids_from_tags(
        ("bdd-0001", "task-0123", "rule-0001", "ac-0001", "ac-0002", "custom")
    )
    assert ids.bdd_ids == ("bdd-0001",)
    assert ids.task_ids == ("task-0123",)
    assert ids.rule_ids == ("rule-0001",)
    assert ids.ac_ids == ("ac-0001", "ac-0002")


def test_summarize_passes_when_linked_scenario_passed() -> None:
    results = (_scenario("A", "passed", ("bdd-0001", "ac-0001")),)
    criteria = summarize_criteria(results)
    assert criteria[0].criterion_id == "ac-0001"
    assert criteria[0].status == "passed"
    assert criteria[0].scenario_ids == ("bdd-0001",)


def test_summarize_fails_when_linked_scenario_failed() -> None:
    results = (
        _scenario("A", "passed", ("bdd-0001", "ac-0001")),
        _scenario("B", "failed", ("bdd-0002", "ac-0001")),
    )
    criteria = summarize_criteria(results)
    assert criteria[0].status == "failed"
    # bdd ids of all linked scenarios are recorded regardless of status
    assert set(criteria[0].scenario_ids) == {"bdd-0001", "bdd-0002"}


def test_summarize_fails_on_skipped_unless_allowed() -> None:
    """Skipped is blocking by default but tolerated when allow_skipped=True.

    Even with allow_skipped=True, a criterion still needs at least one passing
    scenario; skipped alone never satisfies a criterion (fail-closed).
    """
    only_skipped = (_scenario("A", "skipped", ("bdd-0001", "ac-0001")),)
    # Default: skipped blocks.
    assert summarize_criteria(only_skipped)[0].status == "failed"
    # allow_skipped removes the block, but no passing scenario -> still failed.
    assert summarize_criteria(only_skipped, allow_skipped=True)[0].status == "failed"

    mixed = (
        _scenario("A", "skipped", ("bdd-0001", "ac-0001")),
        _scenario("B", "passed", ("bdd-0002", "ac-0001")),
    )
    # Default: the skipped sibling blocks the otherwise-passing criterion.
    assert summarize_criteria(mixed)[0].status == "failed"
    # allow_skipped: the skipped sibling is tolerated, the passing one wins.
    assert summarize_criteria(mixed, allow_skipped=True)[0].status == "passed"


def test_summarize_fails_on_undefined_and_pending() -> None:
    for status in ("undefined", "pending", "ambiguous"):
        results = (_scenario("A", status, ("bdd-0001", "ac-0001")),)
        assert summarize_criteria(results)[0].status == "failed", status


def test_unlinked_scenarios_are_ignored() -> None:
    """A scenario with no ac-* tag must not count as AC validation."""
    results = (
        _scenario("Untagged", "passed", ("bdd-0099",)),
        _scenario("No-ac", "passed", ("rule-0001",)),
    )
    assert summarize_criteria(results) == ()


def test_matching_never_uses_title() -> None:
    """Two scenarios with identical titles but different bdd/ac ids map separately."""
    results = (
        _scenario("Same title", "passed", ("bdd-0001", "ac-0001")),
        _scenario("Same title", "failed", ("bdd-0002", "ac-0002")),
    )
    criteria = {c.criterion_id: c.status for c in summarize_criteria(results)}
    assert criteria == {"ac-0001": "passed", "ac-0002": "failed"}


def test_require_expected_coverage_missing_fails() -> None:
    results = (_scenario("A", "passed", ("bdd-0001", "ac-0001")),)
    coverage = require_expected_coverage(("ac-0001", "ac-0002"), results)
    assert coverage.status == "failed"
    assert coverage.missing == ("ac-0002",)


def test_require_expected_coverage_all_present_passes() -> None:
    results = (
        _scenario("A", "passed", ("bdd-0001", "ac-0001")),
        _scenario("B", "passed", ("bdd-0002", "ac-0002")),
    )
    coverage = require_expected_coverage(("ac-0001", "ac-0002"), results)
    assert coverage.status == "passed"
    assert coverage.missing == ()


def test_require_expected_coverage_only_failing_counts_as_missing() -> None:
    """A criterion whose only scenario failed is not 'passed' coverage."""
    results = (
        _scenario("A", "failed", ("bdd-0001", "ac-0001")),
        _scenario("B", "passed", ("bdd-0002", "ac-0002")),
    )
    coverage = require_expected_coverage(("ac-0001", "ac-0002"), results)
    assert coverage.status == "failed"
    assert coverage.missing == ("ac-0001",)


def test_empty_expected_is_passing() -> None:
    coverage = require_expected_coverage((), ())
    assert isinstance(coverage, CoverageResult)
    assert coverage.status == "passed"


def test_fail_closed_no_passing_scenario() -> None:
    """A criterion with no passing scenario at all fails (fail-closed)."""
    results = (_scenario("A", "undefined", ("bdd-0001", "ac-0001")),)
    assert summarize_criteria(results)[0].status == "failed"
