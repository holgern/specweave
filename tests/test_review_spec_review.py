"""Tests for specweave review specs."""

from __future__ import annotations

from pathlib import Path

from specweave.config import SpecWeaveConfig, SpecWeavePaths
from specweave.gherkin.model import Feature, Scenario, Step
from specweave.gherkin.writer import write_feature
from specweave.review import run_review

FEATURE = "specs/behavior/features/review/spec-review.feature"


def _write_feature(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_behavior_feature(path: Path, *, scenario_id: str, title: str) -> None:
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
    path.write_text(write_feature(feature), encoding="utf-8")


class TestReviewReportsMissingBindings:
    # specweave: feature=specs/behavior/features/review/spec-review.feature
    # specweave: scenario=@bdd-review-counts
    def test_no_features(self, tmp_path: Path) -> None:
        """Review reports feature and scenario statistics."""
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                features_dir=tmp_path / "specs" / "behavior" / "features",
                tests_dir=tmp_path / "tests",
            ),
        )
        (tmp_path / "tests").mkdir()
        result = run_review(config=config)
        assert result["summary"]["features"] == 0

    # specweave: feature=specs/behavior/features/review/spec-review.feature
    # specweave: scenario=@bdd-review-missing-bindings
    def test_feature_with_no_test(self, tmp_path: Path) -> None:
        """Review warns about unbound scenarios."""
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
    # specweave: feature=specs/behavior/features/review/spec-review.feature
    # specweave: scenario=@bdd-review-needs-review
    def test_needs_review_flagged(self, tmp_path: Path) -> None:
        """Review warns about @needs-review scenarios."""
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
        """Review reports feature and scenario statistics (JSON shape)."""
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
    # specweave: feature=specs/behavior/features/review/spec-review.feature
    # specweave: scenario=@bdd-review-deprecated-paths
    def test_stale_mapping_causes_failed_review(self, tmp_path: Path) -> None:
        """Review warns about deprecated paths (stale mapping)."""
        features_dir = tmp_path / "specs" / "behavior" / "features" / "auth"
        tests_dir = tmp_path / "tests"
        _write_behavior_feature(
            features_dir / "login.feature",
            scenario_id="@bdd-login-valid-login",
            title="Valid login",
        )
        tests_dir.mkdir()
        (tests_dir / "test_auth_login.py").write_text(
            "# specweave: feature=specs/behavior/features/auth/login.feature\n"
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

    # specweave: feature=specs/behavior/features/review/spec-review.feature
    # specweave: scenario=@bdd-review-forbidden-pytest-bdd
    def test_forbidden_pytest_bdd(self, tmp_path: Path) -> None:
        """Review errors on pytest-bdd usage."""
        features_dir = tmp_path / "specs" / "behavior" / "features" / "auth"
        tests_dir = tmp_path / "tests"
        _write_behavior_feature(
            features_dir / "login.feature",
            scenario_id="@bdd-login-valid",
            title="Valid login",
        )
        tests_dir.mkdir()
        (tests_dir / "test_auth_login.py").write_text(
            'from pytest_bdd import scenarios\nscenarios("login.feature")\n',
            encoding="utf-8",
        )
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                features_dir=features_dir.parent,
                tests_dir=tests_dir,
            ),
        )
        result = run_review(config=config)
        assert any(f["code"] == "SWREV003" for f in result["findings"])

    # specweave: feature=specs/behavior/features/review/spec-review.feature
    # specweave: scenario=@bdd-review-lint-findings
    def test_lint_findings(self, tmp_path: Path) -> None:
        """Review includes lint errors and warnings."""
        features_dir = tmp_path / "specs" / "behavior" / "features" / "auth"
        features_dir.mkdir(parents=True)
        # Write a feature with no Given/When/Then steps
        (features_dir / "login.feature").write_text(
            "@area-auth @feature-login\n"
            "Feature: Login\n"
            "\n"
            "  @bdd-login-valid\n"
            "  Example: Valid login\n"
            "    A user exists\n",
            encoding="utf-8",
        )
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                features_dir=features_dir.parent,
            ),
        )
        result = run_review(config=config)
        lint_codes = [
            "SWBEH001",
            "SWBEH002",
            "SWBEH003",
            "SWBEH004",
            "SWBEH005",
            "SWBEH006",
        ]
        assert any(f["code"] in lint_codes for f in result["findings"])
