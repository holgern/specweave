"""Tests for behavior/common helpers."""

from __future__ import annotations

from pathlib import Path

from specweave.behavior.common import (
    canonical_test_path,
    feature_identity,
    feature_stem,
    iter_feature_scenarios,
    scenario_id_value,
    slugify,
)
from specweave.gherkin.model import Feature, Rule, Scenario, Step

FEATURE = "specs/behavior/features/common/behavior-helpers.feature.md"


class TestFeatureStem:
    # specweave: feature=specs/behavior/features/common/behavior-helpers.feature.md
    # specweave: scenario=@bdd-feature-stem-markdown
    def test_feature_md(self) -> None:
        """feature_stem handles .feature.md suffix."""
        assert feature_stem(Path("auth/login.feature.md")) == "login"

    # specweave: feature=specs/behavior/features/common/behavior-helpers.feature.md
    # specweave: scenario=@bdd-feature-stem-classic
    def test_classic_feature(self) -> None:
        """feature_stem handles .feature suffix."""
        assert feature_stem(Path("auth/login.feature")) == "login"

    def test_deep_path(self) -> None:
        """feature_stem handles .feature.md suffix in deep paths."""
        assert feature_stem(Path("a/b/c.feature.md")) == "c"

    def test_other_extension(self) -> None:
        """feature_stem handles .feature suffix (other extension)."""
        assert feature_stem(Path("test.py")) == "test"


class TestSlugify:
    # specweave: feature=specs/behavior/features/common/behavior-helpers.feature.md
    # specweave: scenario=@bdd-slugify-basic
    def test_basic(self) -> None:
        """Slugify converts text to lowercase slug."""
        assert slugify("My Feature Title") == "my-feature-title"

    # specweave: feature=specs/behavior/features/common/behavior-helpers.feature.md
    # specweave: scenario=@bdd-slugify-special-chars
    def test_special_chars(self) -> None:
        """Slugify replaces special characters with hyphens."""
        assert slugify("feature@name!") == "feature-name"

    # specweave: feature=specs/behavior/features/common/behavior-helpers.feature.md
    # specweave: scenario=@bdd-slugify-empty
    def test_empty(self) -> None:
        """Slugify returns \"behavior\" for empty input."""
        assert slugify("") == "behavior"


class TestFeatureIdentity:
    # specweave: feature=specs/behavior/features/common/behavior-helpers.feature.md
    # specweave: scenario=@bdd-feature-identity-from-path
    def test_from_path(self) -> None:
        """Feature identity derives area from parent directory."""
        area, slug = feature_identity(
            Path("specs/behavior/features/auth/login.feature")
        )
        assert area == "auth"
        assert slug == "login"

    # specweave: feature=specs/behavior/features/common/behavior-helpers.feature.md
    # specweave: scenario=@bdd-feature-identity-no-area
    def test_no_area(self) -> None:
        """Feature identity uses \"behavior\" when no area directory."""
        area, slug = feature_identity(Path("specs/behavior/features/login.feature"))
        assert area == "behavior"
        assert slug == "login"


class TestCanonicalTestPath:
    # specweave: feature=specs/behavior/features/common/behavior-helpers.feature.md
    # specweave: scenario=@bdd-canonical-test-path
    def test_derives_path(self) -> None:
        """Test path is derived from feature path."""
        result = canonical_test_path(Path("specs/behavior/features/auth/login.feature"))
        assert result == Path("tests/test_auth_login.py")


class TestIterFeatureScenarios:
    def _make_feature_with_top_level(self) -> Feature:
        return Feature(
            title="Test",
            scenarios=(
                Scenario(
                    title="Top level",
                    keyword="Example",
                    tags=("bdd-top",),
                    steps=(Step(keyword="Given", text="something"),),
                ),
            ),
            rules=(
                Rule(
                    title="Rule A",
                    scenarios=(
                        Scenario(
                            title="In rule",
                            keyword="Example",
                            tags=("bdd-in-rule",),
                            steps=(Step(keyword="Given", text="something"),),
                        ),
                    ),
                ),
            ),
        )

    # specweave: feature=specs/behavior/features/common/behavior-helpers.feature.md
    # specweave: scenario=@bdd-iter-scenarios-top-level
    def test_yields_top_level(self) -> None:
        """Iterator yields top-level scenarios."""
        feature = self._make_feature_with_top_level()
        results = list(iter_feature_scenarios(feature))
        top = [(r, s) for r, s in results if s.title == "Top level"]
        assert len(top) == 1
        assert top[0][0] is None

    # specweave: feature=specs/behavior/features/common/behavior-helpers.feature.md
    # specweave: scenario=@bdd-iter-scenarios-in-rules
    def test_yields_from_rules(self) -> None:
        """Iterator yields scenarios from rules."""
        feature = self._make_feature_with_top_level()
        results = list(iter_feature_scenarios(feature))
        in_rule = [(r, s) for r, s in results if s.title == "In rule"]
        assert len(in_rule) == 1
        assert in_rule[0][0] is not None
        assert in_rule[0][0].title == "Rule A"


class TestScenarioIdValue:
    # specweave: feature=specs/behavior/features/common/behavior-helpers.feature.md
    # specweave: scenario=@bdd-scenario-id-value
    def test_returns_first_bdd_tag(self) -> None:
        """scenario_id_value returns first @bdd-* tag."""
        scenario = Scenario(
            title="Test",
            keyword="Example",
            tags=("bdd-example", "ac-0001"),
            steps=(),
        )
        assert scenario_id_value(scenario) == "bdd-example"

    # specweave: feature=specs/behavior/features/common/behavior-helpers.feature.md
    # specweave: scenario=@bdd-scenario-id-missing
    def test_returns_empty_when_no_bdd(self) -> None:
        """scenario_id_value returns empty string when no @bdd-* tag."""
        scenario = Scenario(
            title="Test",
            keyword="Example",
            tags=("ac-0001",),
            steps=(),
        )
        assert scenario_id_value(scenario) == ""
