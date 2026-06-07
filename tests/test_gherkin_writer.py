"""Tests for the Gherkin writer."""

from __future__ import annotations

from specweave.gherkin.model import Feature, Scenario, Step
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
