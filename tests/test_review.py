"""Tests for specweave review specs."""

from __future__ import annotations

from pathlib import Path

from specweave.config import SpecWeaveConfig, SpecWeavePaths
from specweave.gherkin.model import Feature, Scenario, Step
from specweave.gherkin.writer import write_feature
from specweave.review import run_review


def _write_feature(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_markdown_feature(path: Path, *, scenario_id: str, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    feature = Feature(
        title="Login",
        scenarios=(
            Scenario(
                title=title,
                keyword="Example",
                tags=(scenario_id.removeprefix("@"),),
                steps=(
                    Step(keyword="Given", text="a user exists"),
                    Step(keyword="When", text="the user signs in"),
                    Step(keyword="Then", text="the result is visible"),
                ),
            ),
        ),
    )
    path.write_text(
        write_feature(feature, document_format="markdown"), encoding="utf-8"
    )


class TestReviewReportsMissingBindings:
    def test_no_features(self, tmp_path: Path) -> None:
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                features_dir=tmp_path / "specs" / "behavior" / "features",
                tests_dir=tmp_path / "tests",
            ),
        )
        (tmp_path / "tests").mkdir()
        result = run_review(config=config)
        assert result["summary"]["features"] == 0

    def test_feature_with_no_test(self, tmp_path: Path) -> None:
        features_dir = tmp_path / "specs" / "behavior" / "features" / "auth"
        _write_feature(
            features_dir / "login.feature",
            "@feature-login\nFeature: Login\n"
            "  @rule-login\n  Rule: Login\n"
            "    @bdd-login-valid-login\n    Example: Valid login\n"
            "      Given a user\n      When login\n      Then success\n",
        )
        (tmp_path / "tests").mkdir()
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                features_dir=features_dir.parent,
                tests_dir=tmp_path / "tests",
            ),
        )
        result = run_review(config=config)
        assert result["summary"]["missing_bindings"] > 0


class TestReviewReportsNeedsReview:
    def test_needs_review_flagged(self, tmp_path: Path) -> None:
        features_dir = tmp_path / "specs" / "behavior" / "features" / "auth"
        _write_feature(
            features_dir / "login.feature",
            "@generated @needs-review @feature-login\nFeature: Login\n"
            "  @rule-login\n  Rule: Login\n"
            "    @bdd-login-valid-login @needs-review\n    Example: Valid login\n"
            "      Given a user\n      When login\n      Then success\n",
        )
        (tmp_path / "tests").mkdir()
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                features_dir=features_dir.parent,
                tests_dir=tmp_path / "tests",
            ),
        )
        result = run_review(config=config)
        assert result["summary"]["needs_review"] > 0
        needs_review_findings = [
            f for f in result["findings"] if f["code"] == "SWREV001"
        ]
        assert len(needs_review_findings) > 0


class TestReviewJsonShape:
    def test_json_shape(self, tmp_path: Path) -> None:
        (tmp_path / "tests").mkdir()
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                features_dir=tmp_path / "specs" / "behavior" / "features",
                tests_dir=tmp_path / "tests",
            ),
        )
        result = run_review(config=config)
        assert result["schema_version"] == 1
        assert result["command"] == "review specs"
        assert "status" in result
        assert "summary" in result
        assert "findings" in result
        summary = result["summary"]
        assert "features" in summary
        assert "scenarios" in summary
        assert "bound" in summary
        assert "missing_bindings" in summary


class TestReviewAggregatesCoverage:
    def test_stale_mapping_causes_failed_review(self, tmp_path: Path) -> None:
        features_dir = tmp_path / "specs" / "behavior" / "features" / "auth"
        tests_dir = tmp_path / "tests"
        _write_markdown_feature(
            features_dir / "login.feature.md",
            scenario_id="@bdd-login-valid-login",
            title="Valid login",
        )
        tests_dir.mkdir()
        (tests_dir / "test_auth_login.py").write_text(
            "# specweave: feature=specs/behavior/features/auth/login.feature.md\n"
            "# specweave: scenario=@bdd-login-stale\n"
            "def test_valid_login() -> None:\n"
            "    pass\n",
            encoding="utf-8",
        )
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                features_dir=features_dir.parent,
                tests_dir=tests_dir,
            ),
        )

        result = run_review(config=config)

        assert result["status"] == "failed"
        assert result["summary"]["stale_bindings"] == 1
        assert any(finding["code"] == "SWCOV002" for finding in result["findings"])
