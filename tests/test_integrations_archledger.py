"""Tests for Archledger candidate generation."""

from __future__ import annotations

from pathlib import Path

from specweave.bdd.convert import task_bdd_to_feature
from specweave.bdd.model import BddExample, BddRule, TaskBddSpec
from specweave.gherkin.parser import parse_feature
from specweave.integrations.archledger import (
    render_archledger_candidate,
    write_archledger_candidate,
)

FEATURE = "specs/behavior/features/integrations/archledger.feature"


def _feature_spec() -> TaskBddSpec:
    return TaskBddSpec(
        task_id="task-0123",
        feature="Task lifecycle gates",
        rules=(
            BddRule(id="rule-0001", title="Implementation requires an accepted plan"),
        ),
        examples=(
            BddExample(
                id="bdd-0001",
                title="Agent cannot start implementation without an accepted plan",
                rule_id="rule-0001",
                given=("a task has a proposed plan",),
                when=("the agent starts implementation",),
                then=("taskledger rejects the transition",),
                acceptance_criteria=("ac-0001",),
            ),
        ),
    )


# specweave: feature=specs/behavior/features/integrations/archledger.feature
# specweave: scenario=@bdd-archledger-candidate
def test_render_candidate_markdown() -> None:
    """archledger command renders candidate markdown."""
    feature = task_bdd_to_feature(_feature_spec())
    markdown = render_archledger_candidate(feature, "bdd-0001")
    assert "# Candidate behavior record: Agent cannot start implementation" in markdown
    assert "- Task: task-0123" in markdown
    assert "- Rule: rule-0001" in markdown
    assert "- BDD example: bdd-0001" in markdown
    assert "- Acceptance criterion: ac-0001" in markdown
    assert "- Feature file:" in markdown  # source_path is None here
    assert "Given a task has a proposed plan" in markdown
    assert "When the agent starts implementation" in markdown
    assert "Then taskledger rejects the transition" in markdown
    assert "## Rationale" in markdown
    assert markdown.endswith("\n")


def test_render_candidate_from_parsed_feature(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """archledger command renders candidate markdown from parsed feature."""
    feature_path = tmp_path / "tests/bdd/features/task-0123-lifecycle.feature"
    feature = task_bdd_to_feature(_feature_spec())
    feature_path.parent.mkdir(parents=True, exist_ok=True)
    feature_path.write_text(parse_feature_export(feature), encoding="utf-8")
    # Re-parse so source_path can be attached.
    parsed = parse_feature(feature_path.read_text(encoding="utf-8"))
    parsed = _with_source_path(parsed, feature_path)
    markdown = render_archledger_candidate(parsed, "bdd-0001")
    assert f"- Feature file: {feature_path}" in markdown


# specweave: feature=specs/behavior/features/integrations/archledger.feature
# specweave: scenario=@bdd-archledger-unknown-bdd
def test_unknown_bdd_id_raises() -> None:
    """archledger errors on unknown @bdd-* id."""
    feature = task_bdd_to_feature(_feature_spec())
    try:
        render_archledger_candidate(feature, "bdd-9999")
    except ValueError as exc:
        assert "bdd-9999" in str(exc)
    else:  # pragma: no cover - defensive
        raise AssertionError("expected ValueError for unknown bdd id")


# specweave: feature=specs/behavior/features/integrations/archledger.feature
# specweave: scenario=@bdd-archledger-candidate-only
def test_write_candidate_file(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """archledger produces candidates, not accepted records."""
    feature = task_bdd_to_feature(_feature_spec())
    out = tmp_path / ".archledger/candidates/al_runtime_task_0123_bdd_0001.md"
    write_archledger_candidate(feature, "bdd-0001", out)
    assert out.exists()
    content = out.read_text(encoding="utf-8")
    assert "- Task: task-0123" in content
    assert "Given a task has a proposed plan" in content


# --- helpers ---------------------------------------------------------------


def parse_feature_export(feature) -> str:  # type: ignore[no-untyped-def]
    from specweave.gherkin.writer import write_feature

    return write_feature(feature)


def _with_source_path(feature, path: Path):  # type: ignore[no-untyped-def]
    from dataclasses import replace

    return replace(feature, source_path=path)
