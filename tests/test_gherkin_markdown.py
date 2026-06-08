"""Tests for the Markdown-with-Gherkin parser/writer adapter."""

from __future__ import annotations

from specweave.gherkin.markdown import (
    _has_backticked_tags,
    _parse_backticked_tags,
    markdown_to_classic,
    parse_markdown_feature,
    write_markdown_feature,
)
from specweave.gherkin.official import parse_classic_with_official

_MDG_FEATURE = """\
`@area-auth` `@feature-password-login` `@generated`
# Feature: Password login

Generated from pytest tests.

`@rule-password-login`
## Rule: Password login

`@bdd-password-login-reject-invalid-password` `@needs-review`
### Example: Reject invalid password

* Given the pytest test setup is prepared
* When the invalid password behavior is exercised
* Then the test completes successfully

`@bdd-top-level`
## Scenario: Top level test

* Given something
* When something happens
* Then something is true
"""


class TestTagHelpers:
    def test_has_backticked_tags(self) -> None:
        assert _has_backticked_tags("`@tag1` `@tag2`")
        assert not _has_backticked_tags("plain text")
        assert not _has_backticked_tags("# Feature: heading")

    def test_parse_backticked_tags(self) -> None:
        assert _parse_backticked_tags("`@tag1` `@tag2`") == ["tag1", "tag2"]
        assert _parse_backticked_tags("`@tag-name`") == ["tag-name"]


class TestParseMarkdownFeature:
    def test_parses_feature(self) -> None:
        f = parse_markdown_feature(_MDG_FEATURE)
        assert f.title == "Password login"
        assert "area-auth" in f.tags
        assert "feature-password-login" in f.tags
        assert "generated" in f.tags

    def test_parses_rule_and_scenario_tags(self) -> None:
        f = parse_markdown_feature(_MDG_FEATURE)
        assert len(f.rules) == 1
        rule = f.rules[0]
        assert rule.title == "Password login"
        assert rule.tags == ("rule-password-login",)
        assert len(rule.scenarios) == 1
        s = rule.scenarios[0]
        assert s.title == "Reject invalid password"
        assert s.keyword == "Example"
        assert "bdd-password-login-reject-invalid-password" in s.tags
        assert "needs-review" in s.tags

    def test_parses_steps(self) -> None:
        f = parse_markdown_feature(_MDG_FEATURE)
        s = f.rules[0].scenarios[0]
        assert len(s.steps) == 3
        assert s.steps[0].keyword == "Given"
        assert s.steps[0].text == "the pytest test setup is prepared"
        assert s.steps[1].keyword == "When"
        assert s.steps[2].keyword == "Then"

    def test_top_level_scenarios(self) -> None:
        f = parse_markdown_feature(_MDG_FEATURE)
        assert len(f.scenarios) == 1
        s = f.scenarios[0]
        assert s.title == "Top level test"
        assert s.keyword == "Scenario"
        assert "bdd-top-level" in s.tags

    def test_description_preserved(self) -> None:
        f = parse_markdown_feature(_MDG_FEATURE)
        assert "Generated from" in f.description

    def test_ignores_non_gherkin_prose(self) -> None:
        md = "Some random markdown.\n\n`@tag`\n# Feature: Test\n\n* Given x\n"
        f = parse_markdown_feature(md)
        assert f.title == "Test"

    def test_requires_backticked_tags(self) -> None:
        # Classic @tags without backticks should not be parsed as tags
        text = "@tag\n# Feature: Test\n"
        f = parse_markdown_feature(text)
        assert f.tags == ()

    def test_feature_without_rules_no_scenarios(self) -> None:
        f = parse_markdown_feature("# Feature: Empty\n")
        assert f.title == "Empty"
        assert f.scenarios == ()
        assert f.rules == ()


class TestWriteMarkdownFeature:
    def test_writes_feature(self) -> None:
        f = parse_markdown_feature(_MDG_FEATURE)
        out = write_markdown_feature(f)
        assert "`@area-auth`" in out
        assert "`@feature-password-login`" in out
        assert "# Feature: Password login" in out
        assert "## Rule: Password login" in out
        assert "### Example: Reject invalid password" in out
        assert "* Given the pytest test setup is prepared" in out

    def test_round_trip_internal_model(self) -> None:
        f = parse_markdown_feature(_MDG_FEATURE)
        out = write_markdown_feature(f)
        f2 = parse_markdown_feature(out)
        assert f2.title == f.title
        assert f2.tags == f.tags
        assert len(f2.rules) == len(f.rules)
        assert len(f2.scenarios) == len(f.scenarios)
        if f2.rules and f.rules:
            assert f2.rules[0].title == f.rules[0].title
            assert f2.rules[0].tags == f.rules[0].tags
            assert len(f2.rules[0].scenarios) == len(f.rules[0].scenarios)
            if f2.rules[0].scenarios:
                s = f2.rules[0].scenarios[0]
                assert s.title == f.rules[0].scenarios[0].title
                assert s.keyword == f.rules[0].scenarios[0].keyword
                assert len(s.steps) == len(f.rules[0].scenarios[0].steps)


class TestMarkdownToClassic:
    def test_converts_to_classic(self) -> None:
        classic = markdown_to_classic(_MDG_FEATURE)
        assert "Feature: Password login" in classic
        assert "Scenario: Top level test" in classic
        assert "Given the pytest test setup is prepared" in classic

    def test_validates_with_official(self) -> None:
        classic = markdown_to_classic(_MDG_FEATURE)
        f = parse_classic_with_official(classic)
        assert f.title == "Password login"
