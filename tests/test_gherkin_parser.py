"""Tests for the Gherkin parser."""

from __future__ import annotations

import pytest

from specweave.gherkin.parser import parse_feature
from specweave.gherkin.writer import write_feature


def test_parse_simple_feature() -> None:
    """Parse a basic feature with tags and steps."""
    text = """@taskledger:TL-0042
Feature: Password login

  @ac:AC-001
  Scenario: Reject invalid password
    Given a registered user exists
    When the user submits an invalid password
    Then login is rejected
"""
    feature = parse_feature(text)
    assert feature.title == "Password login"
    assert feature.tags == ("taskledger:TL-0042",)
    assert len(feature.scenarios) == 1
    scenario = feature.scenarios[0]
    assert scenario.title == "Reject invalid password"
    assert scenario.tags == ("ac:AC-001",)
    assert len(scenario.steps) == 3
    assert scenario.steps[0].keyword == "Given"
    assert scenario.steps[0].text == "a registered user exists"
    assert scenario.steps[1].keyword == "When"
    assert scenario.steps[1].text == "the user submits an invalid password"
    assert scenario.steps[2].keyword == "Then"
    assert scenario.steps[2].text == "login is rejected"


def test_parse_ignores_comments_and_blanks() -> None:
    """Blank lines and comments are ignored."""
    text = """# This is a comment
Feature: With comments

  # Another comment
  Scenario: A scenario
    Given something
"""
    feature = parse_feature(text)
    assert feature.title == "With comments"
    assert len(feature.scenarios) == 1
    assert feature.scenarios[0].steps[0].text == "something"


def test_parse_no_tags() -> None:
    """Feature without tags parses correctly."""
    text = """Feature: No tags
  Scenario: Simple
    Given a step
"""
    feature = parse_feature(text)
    assert feature.tags == ()


def test_parse_missing_feature_raises() -> None:
    """Missing Feature: line raises ValueError."""
    with pytest.raises(ValueError, match="Expected 'Feature:'"):
        parse_feature("Scenario: Orphan\n    Given x")


def test_parse_multiple_scenarios() -> None:
    """Multiple scenarios are parsed."""
    text = """Feature: Two scenarios
  Scenario: First
    Given step a
  Scenario: Second
    When step b
"""
    feature = parse_feature(text)
    assert len(feature.scenarios) == 2
    assert feature.scenarios[0].title == "First"
    assert feature.scenarios[1].title == "Second"


def test_parse_and_but_keywords() -> None:
    """And/But steps are accepted."""
    text = """Feature: And/But
  Scenario: Full flow
    Given a user
    And they are logged in
    When they click
    Then they see a page
    But no error
"""
    feature = parse_feature(text)
    steps = feature.scenarios[0].steps
    assert len(steps) == 5
    assert steps[1].keyword == "And"
    assert steps[4].keyword == "But"


def test_parse_multi_tag_line() -> None:
    """Multiple tags on one line are all captured."""
    text = """Feature: Multi tag
  @bdd-0001 @task-0123 @rule-0001 @ac-0001
  Scenario: Tagged
    Given a step
"""
    feature = parse_feature(text)
    assert feature.scenarios[0].tags == (
        "bdd-0001",
        "task-0123",
        "rule-0001",
        "ac-0001",
    )


def test_parse_mixed_tag_styles() -> None:
    """One-tag-per-line and multi-tag-per-line both work and accumulate."""
    text = """Feature: Mixed
  @ac-0001
  @bdd-0001 @rule-0001
  Scenario: Tagged
    Given a step
"""
    feature = parse_feature(text)
    assert feature.scenarios[0].tags == ("ac-0001", "bdd-0001", "rule-0001")


def test_parse_rule_block() -> None:
    """Rule: blocks group scenarios and carry tags."""
    text = """@task-0123
Feature: Task lifecycle gates

  @rule-0001
  Rule: Implementation requires an accepted plan

    @bdd-0001 @task-0123 @rule-0001 @ac-0001
    Scenario: Agent cannot start implementation without an accepted plan
      Given a task has a proposed plan
      When the agent starts implementation
      Then taskledger rejects the transition
"""
    feature = parse_feature(text)
    assert feature.title == "Task lifecycle gates"
    assert feature.tags == ("task-0123",)
    assert feature.scenarios == ()
    assert len(feature.rules) == 1
    rule = feature.rules[0]
    assert rule.title == "Implementation requires an accepted plan"
    assert rule.tags == ("rule-0001",)
    assert len(rule.scenarios) == 1
    scenario = rule.scenarios[0]
    assert (
        scenario.title == "Agent cannot start implementation without an accepted plan"
    )
    assert scenario.tags == ("bdd-0001", "task-0123", "rule-0001", "ac-0001")
    assert [s.keyword for s in scenario.steps] == ["Given", "When", "Then"]


def test_parse_multiple_rules_and_scenarios() -> None:
    """Several rules each group their own scenarios."""
    text = """Feature: Many rules

  Rule: First rule
    Scenario: S1
      Given x

  Rule: Second rule
    Scenario: S2
      When y
"""
    feature = parse_feature(text)
    assert [r.title for r in feature.rules] == ["First rule", "Second rule"]
    assert feature.rules[0].scenarios[0].title == "S1"
    assert feature.rules[1].scenarios[0].title == "S2"


def test_scenario_after_rule_belongs_to_rule() -> None:
    """Standard Gherkin: a scenario after a Rule belongs to that Rule.

    A rule absorbs following scenarios until the next Rule/Feature/EOF, matching
    Cucumber semantics. Use a new ``Rule:`` to start a separate group.
    """
    text = """Feature: Absorbed

  Rule: R1
    Scenario: Inside one
      Given x
    Scenario: Inside two
      When y
"""
    feature = parse_feature(text)
    assert len(feature.rules) == 1
    assert [s.title for s in feature.rules[0].scenarios] == ["Inside one", "Inside two"]
    assert feature.scenarios == ()


def test_top_level_scenario_before_rule_stays_top_level() -> None:
    """A top-level scenario that appears before any rule stays top-level."""
    text = """Feature: Before rule

  Scenario: Top
    Given x

  Rule: R1
    Scenario: Inside
      When y
"""
    feature = parse_feature(text)
    assert [s.title for s in feature.scenarios] == ["Top"]
    assert len(feature.rules) == 1
    assert feature.rules[0].scenarios[0].title == "Inside"


def test_parse_feature_description() -> None:
    """Free-text description after Feature: is captured."""
    text = """Feature: Documented

  As a developer
  I want rules

  Rule: R1
    Scenario: S
      Given x
"""
    feature = parse_feature(text)
    assert "As a developer" in feature.description
    assert "I want rules" in feature.description


def test_parse_target_example_round_trip() -> None:
    """The guide target example round-trips through writer + parser."""
    text = """@task-0123
Feature: Task lifecycle gates

  @rule-0001
  Rule: Implementation requires an accepted plan

    @bdd-0001 @task-0123 @rule-0001 @ac-0001
    Scenario: Agent cannot start implementation without an accepted plan
      Given a task has a proposed plan
      When the agent starts implementation
      Then taskledger rejects the transition
"""
    feature = parse_feature(text)
    rendered = write_feature(feature)
    reparsed = parse_feature(rendered)
    assert reparsed.rules[0].scenarios[0].tags == (
        "bdd-0001",
        "task-0123",
        "rule-0001",
        "ac-0001",
    )
    assert reparsed.tags == ("task-0123",)
    assert reparsed.rules[0].tags == ("rule-0001",)
    assert reparsed.rules[0].scenarios[0].steps == feature.rules[0].scenarios[0].steps


def test_parse_example_keyword_and_line_numbers() -> None:
    text = """@area-task-management @feature-plan-gates
Feature: Plan gates

  @rule-accepted-plan-required
  Rule: Implementation requires an accepted plan

    @bdd-implementation-blocked-before-plan-acceptance
    Example: Agent cannot start implementation before plan approval
      Given a task has a proposed plan
      When the agent starts implementation
      Then implementation is blocked
"""
    feature = parse_feature(text)
    scenario = feature.rules[0].scenarios[0]
    assert feature.line == 2
    assert feature.rules[0].line == 5
    assert scenario.keyword == "Example"
    assert scenario.line == 8
    assert scenario.tags == ("bdd-implementation-blocked-before-plan-acceptance",)
