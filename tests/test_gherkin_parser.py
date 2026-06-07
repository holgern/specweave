"""Tests for the Gherkin parser."""

from __future__ import annotations

import pytest

from specweave.gherkin.parser import parse_feature


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
