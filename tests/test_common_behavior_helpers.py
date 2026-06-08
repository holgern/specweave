"""Tests for behavior/common helpers."""

from __future__ import annotations

from pathlib import Path

from specweave.behavior.common import feature_stem

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
