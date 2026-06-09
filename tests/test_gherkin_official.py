"""Tests for the official Cucumber Gherkin parser adapter."""

from __future__ import annotations

from pathlib import Path

import pytest

gherkin = pytest.importorskip("gherkin")  # noqa: F841

from specweave.errors import ParseError  # noqa: E402
from specweave.gherkin.official import (  # noqa: E402
    parse_classic_with_official,
    validate_classic_with_official,
)

_SIMPLE_FEATURE = """\
@feature-tag
Feature: Hello
  Some description.

  @scenario-tag
  Scenario: A simple test
    Given a precondition
    When an action happens
    Then an outcome is verified
"""


_RULE_FEATURE = """\
Feature: With rules

  @rule-a
  Rule: Rule A

    @scenario-a1
    Scenario: First scenario
      Given something
      When it happens
      Then it works
"""


class TestParseClassicWithOfficial:
    def test_parses_simple_feature(self) -> None:
        f = parse_classic_with_official(_SIMPLE_FEATURE)
        assert f.title == "Hello"
        assert f.tags == ("feature-tag",)
        assert f.description == "Some description."
        assert len(f.scenarios) == 1
        assert f.scenarios[0].title == "A simple test"
        assert f.scenarios[0].keyword == "Scenario"
        assert f.scenarios[0].tags == ("scenario-tag",)
        assert len(f.scenarios[0].steps) == 3
        assert f.scenarios[0].steps[0].keyword == "Given"
        assert f.scenarios[0].steps[0].text == "a precondition"

    def test_parses_rule_and_scenario_tags(self) -> None:
        f = parse_classic_with_official(_RULE_FEATURE)
        assert f.title == "With rules"
        assert len(f.rules) == 1
        rule = f.rules[0]
        assert rule.title == "Rule A"
        assert rule.tags == ("rule-a",)
        assert len(rule.scenarios) == 1
        assert rule.scenarios[0].title == "First scenario"
        assert rule.scenarios[0].tags == ("scenario-a1",)

    def test_rejects_invalid_gherkin(self) -> None:
        with pytest.raises(ParseError):
            parse_classic_with_official("Not valid gherkin content")

    def test_accepts_source_path(self) -> None:
        path = Path("specs/behavior/features/auth/login.feature")
        f = parse_classic_with_official(_SIMPLE_FEATURE, source_path=path)
        assert f.source_path == path

    def test_compile_pickles_smoke(self) -> None:
        f = parse_classic_with_official(_SIMPLE_FEATURE, compile_pickles=True)
        assert f.title == "Hello"

    def test_empty_feature_tags(self) -> None:
        src = "Feature: No tags\n  Scenario: Bare\n    Given x\n"
        f = parse_classic_with_official(src)
        assert f.tags == ()

    def test_preserves_description(self) -> None:
        f = parse_classic_with_official(_SIMPLE_FEATURE)
        assert "description." in f.description


class TestValidateClassicWithOfficial:
    def test_validates_valid(self) -> None:
        validate_classic_with_official(_SIMPLE_FEATURE)

    def test_validates_invalid(self) -> None:
        with pytest.raises(ParseError):
            validate_classic_with_official("bogus")


class TestMissingOfficialDependency:
    """Tests for the error message when gherkin-official is not installed."""

    def test_import_error_message_mentions_extra(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """When gherkin is not importable, the error mentions specweave[gherkin]."""
        import importlib

        # Force the import to fail by removing the module if present
        monkeypatch.setitem(__import__("sys").modules, "gherkin", None)
        monkeypatch.setattr(
            importlib,
            "import_module",
            lambda name: (_ for _ in ()).throw(
                ImportError(f"No module named {name!r}")
            ),
        )

        from specweave.gherkin.official import _gherkin_imports

        with pytest.raises(ParseError, match="specweave\\[gherkin\\]"):
            _gherkin_imports()
