"""Tests for behavior/common helpers."""

from __future__ import annotations

from pathlib import Path

from specweave.behavior.common import feature_stem


class TestFeatureStem:
    def test_feature_md(self) -> None:
        assert feature_stem(Path("auth/login.feature.md")) == "login"

    def test_classic_feature(self) -> None:
        assert feature_stem(Path("auth/login.feature")) == "login"

    def test_deep_path(self) -> None:
        assert feature_stem(Path("a/b/c.feature.md")) == "c"

    def test_other_extension(self) -> None:
        assert feature_stem(Path("test.py")) == "test"
