"""Tests for the Gherkin writer."""

from __future__ import annotations

from specweave.gherkin.model import Feature, Rule, Scenario, Step
from specweave.gherkin.parser import parse_feature
from specweave.gherkin.writer import write_feature


def test_writes_tags_feature_scenario_steps() -> None:
    """Writer produces tags, Feature, Scenario, steps, and final newline."""
    feature = Feature(
        title="Authentication",
        tags=("taskledger:TL-0042",),
        scenarios=(
            Scenario(
                title="Reject invalid password",
                tags=("ac:AC-001",),
                steps=(
                    Step(keyword="Given", text="a registered user exists"),
                    Step(keyword="When", text="the user submits an invalid password"),
                    Step(keyword="Then", text="login is rejected"),
                ),
            ),
        ),
    )

    output = write_feature(feature)

    assert "@taskledger:TL-0042" in output
    assert "Feature: Authentication" in output
    assert "  @ac:AC-001" in output
    assert "  Scenario: Reject invalid password" in output
    assert "    Given a registered user exists" in output
    assert "    When the user submits an invalid password" in output
    assert "    Then login is rejected" in output
    assert output.endswith("\n")


def test_scenario_without_tags() -> None:
    """Scenario tags are omitted when empty."""
    feature = Feature(
        title="Minimal",
        scenarios=(
            Scenario(
                title="Do something",
                steps=(Step(keyword="Given", text="a precondition"),),
            ),
        ),
    )
    output = write_feature(feature)
    assert "  Scenario: Do something" in output
    assert "    Given a precondition" in output


def test_multiple_scenarios() -> None:
    """Multiple scenarios are rendered correctly."""
    feature = Feature(
        title="Multi",
        scenarios=(
            Scenario(
                title="First",
                steps=(Step(keyword="Given", text="step one"),),
            ),
            Scenario(
                title="Second",
                steps=(Step(keyword="When", text="step two"),),
            ),
        ),
    )
    output = write_feature(feature)
    assert output.count("Scenario:") == 2
    assert output.index("Scenario: First") < output.index("Scenario: Second")


def test_multi_tag_scenario_on_one_line() -> None:
    """Multiple scenario tags render on a single space-joined line."""
    feature = Feature(
        title="Multi tag",
        scenarios=(
            Scenario(
                title="Tagged",
                tags=("bdd-0001", "task-0123", "rule-0001", "ac-0001"),
                steps=(Step(keyword="Given", text="a step"),),
            ),
        ),
    )
    output = write_feature(feature)
    assert "  @bdd-0001 @task-0123 @rule-0001 @ac-0001" in output
    # no second tag line for the same scenario
    assert output.count("@bdd-0001") == 1


def test_writes_rule_block() -> None:
    """Rule blocks render with rule tags, header, and indented scenarios."""
    feature = Feature(
        title="Task lifecycle gates",
        tags=("task-0123",),
        rules=(
            Rule(
                title="Implementation requires an accepted plan",
                tags=("rule-0001",),
                scenarios=(
                    Scenario(
                        title=(
                            "Agent cannot start implementation without an accepted plan"
                        ),
                        tags=("bdd-0001", "task-0123", "rule-0001", "ac-0001"),
                        steps=(
                            Step(keyword="Given", text="a task has a proposed plan"),
                            Step(
                                keyword="When", text="the agent starts implementation"
                            ),
                            Step(
                                keyword="Then", text="taskledger rejects the transition"
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )
    output = write_feature(feature)
    assert "@task-0123" in output
    assert "Feature: Task lifecycle gates" in output
    assert "  @rule-0001" in output
    assert "  Rule: Implementation requires an accepted plan" in output
    assert "    @bdd-0001 @task-0123 @rule-0001 @ac-0001" in output
    assert (
        "    Scenario: Agent cannot start implementation without an accepted plan"
        in output
    )
    assert "      Given a task has a proposed plan" in output
    assert "      When the agent starts implementation" in output
    assert "      Then taskledger rejects the transition" in output


def test_rule_round_trips() -> None:
    """A feature with a rule round-trips through writer + parser."""
    feature = Feature(
        title="RT",
        tags=("task-0001",),
        rules=(
            Rule(
                title="R1",
                tags=("rule-0001",),
                scenarios=(
                    Scenario(
                        title="S1",
                        tags=("bdd-0001", "task-0001", "rule-0001", "ac-0001"),
                        steps=(Step(keyword="Given", text="x"),),
                    ),
                ),
            ),
        ),
    )
    reparsed = parse_feature(write_feature(feature))
    assert reparsed.tags == ("task-0001",)
    assert len(reparsed.rules) == 1
    assert reparsed.rules[0].title == "R1"
    assert reparsed.rules[0].tags == ("rule-0001",)
    assert reparsed.rules[0].scenarios[0].tags == (
        "bdd-0001",
        "task-0001",
        "rule-0001",
        "ac-0001",
    )


def test_feature_description_rendered() -> None:
    """Feature description is indented under Feature:."""
    feature = Feature(
        title="Documented",
        description="As a user\nI want docs",
        scenarios=(Scenario(title="S", steps=(Step(keyword="Given", text="x"),)),),
    )
    output = write_feature(feature)
    assert "  As a user" in output
    assert "  I want docs" in output
