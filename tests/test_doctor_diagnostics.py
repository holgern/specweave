"""Tests for specweave doctor."""

from __future__ import annotations

from pathlib import Path

from specweave.config import (
    SpecWeaveConfig,
    SpecWeavePaths,
    SpecWeaveSpecificationPaths,
    load_config,
)
from specweave.doctor import run_doctor

FEATURE = "specs/behavior/features/doctor/diagnostics.feature"


class TestDoctorPasses:
    # sw: f=specs/behavior/features/doctor/diagnostics.feature
    # sw: s=@bdd-doctor-validates-features
    def test_passes_initialized_project(self, tmp_path: Path) -> None:
        """Doctor reports feature lint errors."""
        from specweave.init import run_init

        run_init(config_path=tmp_path / "specweave.toml", project_root=tmp_path)
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                specs_root=tmp_path / "specs",
                features_dir=tmp_path / "specs" / "behaviour" / "features",
                behavior_readme=tmp_path / "specs" / "behaviour" / "README.md",
                manifest=tmp_path / "specs" / "behaviour" / "manifest.json",
                tests_dir=tmp_path / "tests",
                reports_dir=tmp_path / "specs" / "behaviour" / "reports",
                evidence_dir=tmp_path / "specs" / "behaviour" / "evidence",
                reports_state_dir=tmp_path
                / "specs"
                / "behaviour"
                / "reports"
                / "specweave",
                mapping_dir=tmp_path / "specs" / "behaviour" / "mappings",
            ),
        )
        (tmp_path / "tests").mkdir()
        result = run_doctor(config=config)
        assert result["status"] == "passed"

    def test_explicit_config_uses_resolved_paths_without_relative_warnings(
        self, tmp_path: Path
    ) -> None:
        project = tmp_path / "project"
        for path in (
            project / "specs/behaviour/features",
            project / "tests",
            project / "specs/behaviour/reports",
            project / "specs/behaviour/evidence",
            project / "specs/behaviour/mappings",
        ):
            path.mkdir(parents=True)
        config_path = tmp_path / "specweave.toml"
        config_path.write_text(
            'schema_version = 1\nproject_root = "project"\n',
            encoding="utf-8",
        )

        result = run_doctor(
            config=load_config(config_path),
            config_path=config_path,
        )

        assert result["status"] == "passed"
        assert not any(item["code"] == "SWDOC001" for item in result["items"])
        assert not any(item["code"] == "SWDOC003" for item in result["items"])


class TestDoctorReportsMissing:
    # sw: f=specs/behavior/features/doctor/diagnostics.feature
    # sw: s=@bdd-doctor-missing-directories
    def test_reports_missing_features_dir(self, tmp_path: Path) -> None:
        """Doctor warns about missing directories."""
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                features_dir=tmp_path / "nonexistent" / "features",
                tests_dir=tmp_path / "also-nonexistent" / "tests",
            ),
        )
        result = run_doctor(config=config)
        assert any("SWDOC006" in item.get("code", "") for item in result["items"])

    def test_reports_missing_tests_dir(self, tmp_path: Path) -> None:
        """Doctor warns about missing directories."""
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                features_dir=tmp_path / "nonexistent" / "features",
                tests_dir=tmp_path / "also-nonexistent" / "tests",
            ),
        )
        result = run_doctor(config=config)
        assert any("SWDOC007" in item.get("code", "") for item in result["items"])

    # sw: f=specs/behavior/features/doctor/diagnostics.feature
    # sw: s=@bdd-doctor-missing-config
    def test_no_config_warning(self, tmp_path: Path, monkeypatch) -> None:
        """Doctor warns when no config file exists."""
        monkeypatch.chdir(tmp_path)
        result = run_doctor()
        assert any("SWDOC001" in w for w in result["warnings"])


class TestDoctorReportsDuplicateBddTags:
    # sw: f=specs/behavior/features/doctor/diagnostics.feature
    # sw: s=@bdd-doctor-duplicate-bdd-tags
    def test_detects_duplicates(self, tmp_path: Path) -> None:
        """Doctor errors on duplicate @bdd-* tags."""
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
    # sw: f=specs/behavior/features/doctor/diagnostics.feature
    # sw: s=@bdd-doctor-deprecated-paths
    def test_detects_deprecated(self, tmp_path: Path, monkeypatch) -> None:
        """Doctor warns about deprecated feature paths."""
        monkeypatch.chdir(tmp_path)
        deprecated = tmp_path / "specs" / "bdd" / "features"
        deprecated.mkdir(parents=True)

        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                specs_root=tmp_path / "specs",
                features_dir=tmp_path / "specs" / "behaviour" / "features",
            ),
        )
        result = run_doctor(config=config)
        assert any("SWDOC004" in i["code"] for i in result["items"])

    def test_warns_for_deprecated_specs_behavior_layout(self, tmp_path: Path) -> None:
        config = SpecWeaveConfig(
            spelling="behavior",
            paths=SpecWeavePaths(
                specs_root=tmp_path / "specs",
                features_dir=tmp_path / "specs" / "behavior" / "features",
            ),
        )

        result = run_doctor(config=config)

        assert any(i["code"] == "SWDOC012" for i in result["items"])


class TestDoctorSpecifications:
    def test_reports_missing_specifications_directories(self, tmp_path: Path) -> None:
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                specs_root=tmp_path / "specs",
                features_dir=tmp_path / "specs" / "behaviour" / "features",
                tests_dir=tmp_path / "tests",
                reports_dir=tmp_path / "specs" / "behaviour" / "reports",
                evidence_dir=tmp_path / "specs" / "behaviour" / "evidence",
                mapping_dir=tmp_path / "specs" / "behaviour" / "mappings",
                specifications=SpecWeaveSpecificationPaths(
                    root=tmp_path / "specs" / "specifications",
                    product_spec=tmp_path
                    / "specs"
                    / "specifications"
                    / "product.spec.md",
                    readme=tmp_path / "specs" / "specifications" / "README.md",
                    manifest=tmp_path / "specs" / "specifications" / "manifest.json",
                    capabilities_dir=tmp_path
                    / "specs"
                    / "specifications"
                    / "capabilities",
                    interfaces_dir=tmp_path / "specs" / "specifications" / "interfaces",
                    integrations_dir=tmp_path
                    / "specs"
                    / "specifications"
                    / "integrations",
                    mappings_dir=tmp_path / "specs" / "specifications" / "mappings",
                    evidence_dir=tmp_path / "specs" / "specifications" / "evidence",
                    reports_dir=tmp_path / "specs" / "specifications" / "reports",
                    reports_state_dir=tmp_path
                    / "specs"
                    / "specifications"
                    / "reports"
                    / "specweave",
                ),
            ),
        )
        result = run_doctor(config=config)
        assert any(i["code"] == "SWDOC013" for i in result["items"])
        assert any(i["code"] == "SWDOC019" for i in result["items"])


class TestDoctorFix:
    # sw: f=specs/behavior/features/doctor/diagnostics.feature
    # sw: s=@bdd-doctor-fix-creates-directories
    def test_fix_creates_missing_dirs(self, tmp_path: Path) -> None:
        """Doctor --fix creates missing directories."""
        config = SpecWeaveConfig(
            paths=SpecWeavePaths(
                features_dir=tmp_path / "specs" / "behaviour" / "features",
                tests_dir=tmp_path / "tests",
                reports_dir=tmp_path / "specs" / "behaviour" / "reports",
                evidence_dir=tmp_path / "specs" / "behaviour" / "evidence",
                mapping_dir=tmp_path / "specs" / "behaviour" / "mappings",
            ),
        )
        run_doctor(config=config, fix=True)
        assert (tmp_path / "specs" / "behaviour" / "features").is_dir()
        assert (tmp_path / "tests").is_dir()
        assert (tmp_path / "specs" / "behaviour" / "reports").is_dir()
        assert (tmp_path / "specs" / "behaviour" / "evidence").is_dir()
        assert (tmp_path / "specs" / "behaviour" / "mappings").is_dir()

    # sw: f=specs/behavior/features/doctor/diagnostics.feature
    # sw: s=@bdd-doctor-unsupported-schema
    def test_unsupported_schema(self, tmp_path: Path) -> None:
        """Doctor errors on unsupported schema version."""
        config = SpecWeaveConfig(schema_version=99)
        result = run_doctor(config=config)
        assert any(i["code"] == "SWDOC002" for i in result["items"])
