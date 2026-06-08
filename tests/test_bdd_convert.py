"""Tests for the task-BDD model, conversion, and JSON store."""

from __future__ import annotations

import json

from specweave.bdd.convert import feature_to_task_bdd, task_bdd_to_feature
from specweave.bdd.model import BddExample, BddRule, TaskBddSpec
from specweave.bdd.store import load_task_bdd_json, save_task_bdd_json
from specweave.gherkin.writer import write_feature


def _sample_spec() -> TaskBddSpec:
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


def test_export_to_target_gherkin() -> None:
    """A task BDD spec exports to the guide's target Gherkin format."""
    feature = task_bdd_to_feature(_sample_spec())
    output = write_feature(feature)
    assert "@task-0123" in output
    assert "Feature: Task lifecycle gates" in output
    assert "  @rule-0001" in output
    assert "  Rule: Implementation requires an accepted plan" in output
    assert "    @bdd-0001 @task-0123 @rule-0001 @ac-0001" in output
    assert (
        "    Scenario: Agent cannot start implementation "
        "without an accepted plan" in output
    )
    assert "      Given a task has a proposed plan" in output
    assert "      When the agent starts implementation" in output
    assert "      Then taskledger rejects the transition" in output


def test_round_trip_preserves_ids() -> None:
    """Export then import preserves task/rule/bdd/ac ids."""
    spec = _sample_spec()
    feature = task_bdd_to_feature(spec)
    reimported = feature_to_task_bdd(feature)
    assert reimported.task_id == "task-0123"
    assert reimported.feature == "Task lifecycle gates"
    assert reimported.rules[0].id == "rule-0001"
    assert reimported.rules[0].title == "Implementation requires an accepted plan"
    example = reimported.examples[0]
    assert example.id == "bdd-0001"
    assert example.rule_id == "rule-0001"
    assert example.acceptance_criteria == ("ac-0001",)
    assert example.given == ("a task has a proposed plan",)
    assert example.when == ("the agent starts implementation",)
    assert example.then == ("taskledger rejects the transition",)


def test_multiple_ac_tags_and_extra_tags() -> None:
    """Multiple ac-* tags and custom tags survive a round trip."""
    spec = TaskBddSpec(
        task_id="task-0002",
        feature="Coverage",
        rules=(BddRule(id="rule-0001", title="R1"),),
        examples=(
            BddExample(
                id="bdd-0001",
                title="Multi",
                rule_id="rule-0001",
                given=("g",),
                when=("w",),
                then=("t",),
                acceptance_criteria=("ac-0001", "ac-0002"),
                tags=("smoke",),
            ),
        ),
    )
    reimported = feature_to_task_bdd(task_bdd_to_feature(spec))
    example = reimported.examples[0]
    assert example.acceptance_criteria == ("ac-0001", "ac-0002")
    assert "smoke" in example.tags
    assert example.id == "bdd-0001"


def test_top_level_examples_become_top_level_scenarios() -> None:
    """An example without a rule_id renders as a top-level scenario."""
    spec = TaskBddSpec(
        task_id="task-0003",
        feature="Top level",
        rules=(),
        examples=(
            BddExample(
                id="bdd-0001",
                title="Loose",
                given=("g",),
                when=("w",),
                then=("t",),
                acceptance_criteria=("ac-0001",),
            ),
        ),
    )
    feature = task_bdd_to_feature(spec)
    assert feature.rules == ()
    assert len(feature.scenarios) == 1
    assert feature.scenarios[0].title == "Loose"


def test_and_but_steps_group_correctly() -> None:
    """And/But steps continue the previous Given/When/Then section."""
    spec = TaskBddSpec(
        task_id="task-0004",
        feature="Grouped steps",
        examples=(
            BddExample(
                id="bdd-0001",
                title="Grouped",
                given=("a user", "a session"),
                when=("they act", "they confirm"),
                then=("it works", "no error"),
                acceptance_criteria=("ac-0001",),
            ),
        ),
    )
    reimported = feature_to_task_bdd(task_bdd_to_feature(spec))
    example = reimported.examples[0]
    assert example.given == ("a user", "a session")
    assert example.when == ("they act", "they confirm")
    assert example.then == ("it works", "no error")


def test_json_round_trip(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """save_task_bdd_json + load_task_bdd_json is idempotent."""
    spec = _sample_spec()
    path = tmp_path / "task-0123.bdd.json"
    save_task_bdd_json(spec, path)
    loaded = load_task_bdd_json(path)
    assert loaded == spec
    # File contents are valid JSON with stable keys.
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["task_id"] == "task-0123"
    assert data["examples"][0]["acceptance_criteria"] == ["ac-0001"]


def test_json_to_feature_to_json_round_trip(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Acceptance criteria JSON -> feature -> back to JSON keeps ids."""
    src = tmp_path / "in.json"
    src.write_text(
        json.dumps(
            {
                "task_id": "task-0123",
                "feature": "Task lifecycle gates",
                "rules": [
                    {
                        "id": "rule-0001",
                        "title": "Implementation requires an accepted plan",
                    }
                ],
                "examples": [
                    {
                        "id": "bdd-0001",
                        "title": (
                            "Agent cannot start implementation without an accepted plan"
                        ),
                        "rule_id": "rule-0001",
                        "given": ["a task has a proposed plan"],
                        "when": ["the agent starts implementation"],
                        "then": ["taskledger rejects the transition"],
                        "acceptance_criteria": ["ac-0001"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    spec = load_task_bdd_json(src)
    reimported = feature_to_task_bdd(task_bdd_to_feature(spec))
    out = tmp_path / "out.json"
    save_task_bdd_json(reimported, out)
    final = load_task_bdd_json(out)
    assert final.task_id == "task-0123"
    assert final.rules[0].id == "rule-0001"
    assert final.examples[0].id == "bdd-0001"
    assert final.examples[0].acceptance_criteria == ("ac-0001",)
