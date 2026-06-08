"""Tests for specweave doctor."""

from __future__ import annotations

from pathlib import Path

from specweave.config import SpecWeaveConfig, SpecWeavePaths
from specweave.doctor import run_doctor


class TestDoctorPasses:
    def test_passes_initialized_project(self, tmp_path: Path) -> None:
        from specweave.init import run_init

        run_init(config_path=tmp_path / ".specweave.toml", project_root=tmp_path)
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                specs_root=tmp_path / "specs" / "behavior",
                features_dir=tmp_path / "specs" / "behavior" / "features",
                behavior_readme=tmp_path / "specs" / "behavior" / "README.md",
                manifest=tmp_path / "specs" / "behavior" / "manifest.json",
                tests_dir=tmp_path / "tests",
                reports_dir=tmp_path / "reports" / "behavior",
                state_dir=tmp_path / ".specweave",
                evidence_dir=tmp_path / ".specweave" / "evidence",
                reports_state_dir=tmp_path / ".specweave" / "reports",
                mapping_dir=tmp_path / ".specweave" / "mappings",
            ),
        )
        (tmp_path / "tests").mkdir()
        result = run_doctor(config=config)
        assert result["status"] == "passed"


class TestDoctorReportsMissing:
    def test_reports_missing_features_dir(self, tmp_path: Path) -> None:
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                features_dir=tmp_path / "nonexistent" / "features",
                tests_dir=tmp_path / "also-nonexistent" / "tests",
            ),
        )
        result = run_doctor(config=config)
        assert any("SWDOC006" in item.get("code", "") for item in result["items"])

    def test_reports_missing_tests_dir(self, tmp_path: Path) -> None:
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                features_dir=tmp_path / "nonexistent" / "features",
                tests_dir=tmp_path / "also-nonexistent" / "tests",
            ),
        )
        result = run_doctor(config=config)
        assert any("SWDOC007" in item.get("code", "") for item in result["items"])

    def test_no_config_warning(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = run_doctor()
        assert any("SWDOC001" in w for w in result["warnings"])


class TestDoctorReportsDuplicateBddTags:
    def test_detects_duplicates(self, tmp_path: Path) -> None:
        features_dir = tmp_path / "features"
        features_dir.mkdir()
        auth_dir = features_dir / "auth"
        auth_dir.mkdir()
        feature_content = (
            "@feature-login\nFeature: Login\n"
            "  @rule-login\n  Rule: Login\n"
            "    @bdd-login-valid-login\n    Example: Valid login\n"
            "      Given a user\n      When login\n      Then success\n"
        )
        (auth_dir / "login.feature").write_text(feature_content)
        (auth_dir / "login2.feature").write_text(feature_content)

        config = SpecWeaveConfig(
            paths=SpecWeavePaths(features_dir=features_dir),
        )
        result = run_doctor(config=config)
        duplicate_items = [i for i in result["items"] if i["code"] == "SWDOC005"]
        assert len(duplicate_items) > 0


class TestDoctorReportsDeprecatedPaths:
    def test_detects_deprecated(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        deprecated = tmp_path / "specs" / "bdd" / "features"
        deprecated.mkdir(parents=True)

        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                features_dir=tmp_path / "specs" / "behavior" / "features",
                specs_root=tmp_path / "specs" / "behavior",
            ),
        )
        result = run_doctor(config=config)
        assert any("SWDOC004" in i["code"] for i in result["items"])


class TestDoctorFix:
    def test_fix_creates_missing_dirs(self, tmp_path: Path) -> None:
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                features_dir=tmp_path / "specs" / "behavior" / "features",
                tests_dir=tmp_path / "tests",
                reports_dir=tmp_path / "reports" / "behavior",
                evidence_dir=tmp_path / ".specweave" / "evidence",
                mapping_dir=tmp_path / ".specweave" / "mappings",
            ),
        )
        run_doctor(config=config, fix=True)
        assert (tmp_path / "specs" / "behavior" / "features").is_dir()
        assert (tmp_path / "tests").is_dir()
        assert (tmp_path / "reports" / "behavior").is_dir()
        assert (tmp_path / ".specweave" / "evidence").is_dir()
        assert (tmp_path / ".specweave" / "mappings").is_dir()
