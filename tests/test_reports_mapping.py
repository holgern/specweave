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

FEATURE = "specs/behavior/features/reports/mapping.feature.md"


def _scenario(  # type: ignore[no-untyped-def]
    name: str, status: str, tags: tuple[str, ...]
) -> ScenarioResult:
    return ScenarioResult(name=name, status=status, tags=tags)


# specweave: feature=specs/behavior/features/reports/mapping.feature.md
# specweave: scenario=@bdd-tag-extraction-bdd
def test_extract_ids_partitions_by_prefix() -> None:
    """Extraction finds @bdd-* tags."""
    ids = extract_ids_from_tags(
        ("bdd-0001", "task-0123", "rule-0001", "ac-0001", "ac-0002", "custom")
    )
    assert ids.bdd_ids == ("bdd-0001",)
    assert ids.task_ids == ("task-0123",)
    assert ids.rule_ids == ("rule-0001",)
    assert ids.ac_ids == ("ac-0001", "ac-0002")


# specweave: feature=specs/behavior/features/reports/mapping.feature.md
# specweave: scenario=@bdd-criteria-summary
def test_summarize_passes_when_linked_scenario_passed() -> None:
    """Summarization groups scenarios by acceptance criterion."""
    results = (_scenario("A", "passed", ("bdd-0001", "ac-0001")),)
    criteria = summarize_criteria(results)
    assert criteria[0].criterion_id == "ac-0001"
    assert criteria[0].status == "passed"
    assert criteria[0].scenario_ids == ("bdd-0001",)


# specweave: feature=specs/behavior/features/reports/mapping.feature.md
# specweave: scenario=@bdd-criteria-fail-closed
def test_summarize_fails_when_linked_scenario_failed() -> None:
    """Failed scenarios fail the linked criterion."""
    results = (
        _scenario("A", "passed", ("bdd-0001", "ac-0001")),
        _scenario("B", "failed", ("bdd-0002", "ac-0001")),
    )
    criteria = summarize_criteria(results)
    assert criteria[0].status == "failed"
    # bdd ids of all linked scenarios are recorded regardless of status
    assert set(criteria[0].scenario_ids) == {"bdd-0001", "bdd-0002"}


def test_summarize_fails_on_skipped_unless_allowed() -> None:
    """Failed scenarios fail the linked criterion (skipped)."""
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
    """Failed scenarios fail the linked criterion (undefined/pending)."""
    for status in ("undefined", "pending", "ambiguous"):
        results = (_scenario("A", status, ("bdd-0001", "ac-0001")),)
        assert summarize_criteria(results)[0].status == "failed", status


# specweave: feature=specs/behavior/features/reports/mapping.feature.md
# specweave: scenario=@bdd-tag-extraction-empty
def test_unlinked_scenarios_are_ignored() -> None:
    """Extraction returns empty lists when no matching tags."""
    results = (
        _scenario("Untagged", "passed", ("bdd-0099",)),
        _scenario("No-ac", "passed", ("rule-0001",)),
    )
    assert summarize_criteria(results) == ()


def test_matching_never_uses_title() -> None:
    """Summarization groups scenarios by acceptance criterion (title matching)."""
    results = (
        _scenario("Same title", "passed", ("bdd-0001", "ac-0001")),
        _scenario("Same title", "failed", ("bdd-0002", "ac-0002")),
    )
    criteria = {c.criterion_id: c.status for c in summarize_criteria(results)}
    assert criteria == {"ac-0001": "passed", "ac-0002": "failed"}


# specweave: feature=specs/behavior/features/reports/mapping.feature.md
# specweave: scenario=@bdd-criteria-missing-coverage
def test_require_expected_coverage_missing_fails() -> None:
    """Expected AC with no scenarios fails coverage."""
    results = (_scenario("A", "passed", ("bdd-0001", "ac-0001")),)
    coverage = require_expected_coverage(("ac-0001", "ac-0002"), results)
    assert coverage.status == "failed"
    assert coverage.missing == ("ac-0002",)


def test_require_expected_coverage_all_present_passes() -> None:
    """Summarization groups scenarios by acceptance criterion (all present)."""
    results = (
        _scenario("A", "passed", ("bdd-0001", "ac-0001")),
        _scenario("B", "passed", ("bdd-0002", "ac-0002")),
    )
    coverage = require_expected_coverage(("ac-0001", "ac-0002"), results)
    assert coverage.status == "passed"
    assert coverage.missing == ()


def test_require_expected_coverage_only_failing_counts_as_missing() -> None:
    """Expected AC with no scenarios fails coverage (only failing)."""
    results = (
        _scenario("A", "failed", ("bdd-0001", "ac-0001")),
        _scenario("B", "passed", ("bdd-0002", "ac-0002")),
    )
    coverage = require_expected_coverage(("ac-0001", "ac-0002"), results)
    assert coverage.status == "failed"
    assert coverage.missing == ("ac-0001",)


def test_empty_expected_is_passing() -> None:
    """Summarization groups scenarios by acceptance criterion (empty)."""
    coverage = require_expected_coverage((), ())
    assert isinstance(coverage, CoverageResult)
    assert coverage.status == "passed"


def test_fail_closed_no_passing_scenario() -> None:
    """Failed scenarios fail the linked criterion (no passing)."""
    results = (_scenario("A", "undefined", ("bdd-0001", "ac-0001")),)
    assert summarize_criteria(results)[0].status == "failed"
