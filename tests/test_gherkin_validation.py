"""Tests for the strict SpecWeave subset Gherkin validator."""

from __future__ import annotations

from pathlib import Path

import pytest

from specweave.errors import ParseError
from specweave.gherkin.validation import (
    validate_classic_specweave_subset,
    validate_markdown_specweave_subset,
)

_VALID_CLASSIC = """\
Feature: Valid feature

  Scenario: A simple test
    Given a precondition
    When an action happens
    Then an outcome is verified
"""

_VALID_CLASSIC_WITH_RULE = """\
Feature: Valid feature

  Rule: A business rule
    Scenario: A simple test
      Given a precondition
      When an action happens
      Then an outcome is verified
"""

_VALID_CLASSIC_WITH_TAGS = """\
@feature-tag
Feature: Tagged feature

  @bdd-0001 @ac-0001
  Scenario: Tagged test
    Given a precondition
    When an action happens
    Then an outcome is verified
"""

_VALID_CLASSIC_WITH_DESCRIPTION = """\
Feature: Feature with description
  This is a description.

  Scenario: A test
    Given something
"""


class TestValidateClassicValid:
    def test_valid_simple_feature(self) -> None:
        validate_classic_specweave_subset(_VALID_CLASSIC)

    def test_valid_with_rule(self) -> None:
        validate_classic_specweave_subset(_VALID_CLASSIC_WITH_RULE)

    def test_valid_with_tags(self) -> None:
        validate_classic_specweave_subset(_VALID_CLASSIC_WITH_TAGS)

    def test_valid_with_description(self) -> None:
        validate_classic_specweave_subset(_VALID_CLASSIC_WITH_DESCRIPTION)

    def test_valid_with_and_but(self) -> None:
        text = """\
Feature: F
  Scenario: S
    Given a
    And b
    When c
    But d
    Then e
"""
        validate_classic_specweave_subset(text)

    def test_valid_with_example_keyword(self) -> None:
        text = """\
Feature: F
  Example: E
    Given a
    When b
    Then c
"""
        validate_classic_specweave_subset(text)

    def test_valid_with_comments(self) -> None:
        text = """\
Feature: F
  # A comment
  Scenario: S
    # Another comment
    Given a
    When b
    Then c
"""
        validate_classic_specweave_subset(text)


class TestValidateClassicUnsupported:
    def test_rejects_background(self) -> None:
        text = """\
Feature: F
  Background:
    Given a logged in user
  Scenario: S
    When they act
    Then it works
"""
        with pytest.raises(ParseError, match="Background"):
            validate_classic_specweave_subset(text)

    def test_rejects_scenario_outline(self) -> None:
        text = """\
Feature: F
  Scenario Outline: Eating
    Given there are <start> cucumbers
    When I eat <eat> cucumbers
    Then I should have <left> cucumbers
"""
        with pytest.raises(ParseError, match="Scenario Outline"):
            validate_classic_specweave_subset(text)

    def test_rejects_scenario_template(self) -> None:
        text = """\
Feature: F
  Scenario Template: Template
    Given x
"""
        with pytest.raises(ParseError, match="Scenario Template"):
            validate_classic_specweave_subset(text)

    def test_rejects_examples_keyword(self) -> None:
        text = """\
Feature: F
  Scenario: S
    Given x
    Examples:
      | a |
      | 1 |
"""
        with pytest.raises(ParseError, match="Examples"):
            validate_classic_specweave_subset(text)

    def test_rejects_data_table(self) -> None:
        text = """\
Feature: F
  Scenario: S
    Given users exist
      | name | email |
      | A    | a@x   |
    When I list users
    Then I see A
"""
        with pytest.raises(ParseError, match="[Dd]ata table"):
            validate_classic_specweave_subset(text)

    def test_rejects_doc_string(self) -> None:
        text = """\
Feature: F
  Scenario: S
    Given a document
      \"\"\"
      Hello
      \"\"\"
    When I save it
    Then it is stored
"""
        with pytest.raises(ParseError, match="[Dd]oc string"):
            validate_classic_specweave_subset(text)

    def test_rejects_wildcard_step(self) -> None:
        text = """\
Feature: F
  Scenario: S
    * a precondition
    When action
    Then result
"""
        with pytest.raises(ParseError, match="Wildcard"):
            validate_classic_specweave_subset(text)

    def test_rejects_junk_line_in_scenario_after_steps(self) -> None:
        text = """\
Feature: F
  Scenario: S
    Given x
    this is not valid Gherkin
    Then y
"""
        with pytest.raises(ParseError, match="Unsupported"):
            validate_classic_specweave_subset(text)

    def test_rejects_multiple_features(self) -> None:
        text = """\
Feature: F1
  Scenario: S
    Given x
Feature: F2
  Scenario: S2
    Given y
"""
        with pytest.raises(ParseError, match="Multiple Feature"):
            validate_classic_specweave_subset(text)

    def test_rejects_missing_feature(self) -> None:
        text = """\
  Scenario: S
    Given x
"""
        with pytest.raises(ParseError, match="Missing Feature"):
            validate_classic_specweave_subset(text)

    def test_includes_source_path_in_error(self) -> None:
        path = Path("specs/behavior/features/auth/login.feature")
        with pytest.raises(ParseError, match="login\\.feature"):
            validate_classic_specweave_subset(
                "Scenario: S\n  Given x\n", source_path=path
            )


class TestValidateMarkdownUnsupported:
    # sw: f=specs/behavior/features/gherkin/markdown.feature
    # sw: s=@bdd-validation-rejects-markdown
    def test_rejects_markdown_features(self) -> None:
        text = """\
# Feature: F
## Example: S
- Given x
"""
        with pytest.raises(ParseError, match="no longer supported"):
            validate_markdown_specweave_subset(text)
