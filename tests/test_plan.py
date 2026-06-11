"""Tests for specweave create plan."""

from __future__ import annotations

from pathlib import Path

from specweave.config import SpecWeaveConfig, SpecWeavePaths
from specweave.planning import create_plan


def _write_feature(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "@area-billing @feature-invoice-export\n"
        "Feature: Invoice export\n"
        "  Export invoices.\n"
        "\n"
        "  @rule-invoice-export\n"
        "  Rule: Users can export completed invoices\n"
        "\n"
        "    @bdd-invoice-export-user-exports-paid-invoice\n"
        "    Example: User exports a paid invoice\n"
        "      Given a paid invoice exists\n"
        "      When the user exports the invoice as PDF\n"
        "      Then a PDF file is generated\n",
        encoding="utf-8",
    )


class TestCreatePlan:
    # sw: f=specs/behavior/features/planning/create-plan.feature
    # sw: s=@bdd-plan-create
    def test_creates_plan_from_feature(self, tmp_path: Path) -> None:
        features_dir = tmp_path / "specs" / "behavior" / "features"
        feature_path = features_dir / "billing" / "invoice-export.feature"
        _write_feature(feature_path)
        out_path = tmp_path / "plan.md"

        config = SpecWeaveConfig(paths=SpecWeavePaths(features_dir=features_dir))
        create_plan(feature_path=feature_path, out_path=out_path, config=config)
        assert out_path.exists()
        content = out_path.read_text()
        assert "Invoice export" in content
        assert "Implementation TODOs" in content
        assert "Validation" in content

    # sw: f=specs/behavior/features/planning/create-plan.feature
    # sw: s=@bdd-plan-includes-scenario-steps
    def test_plan_includes_scenario_steps(self, tmp_path: Path) -> None:
        features_dir = tmp_path / "specs" / "behavior" / "features"
        feature_path = features_dir / "billing" / "invoice-export.feature"
        _write_feature(feature_path)
        out_path = tmp_path / "plan.md"

        create_plan(feature_path=feature_path, out_path=out_path)
        content = out_path.read_text()
        assert "Given a paid invoice exists" in content
        assert "When the user exports" in content
        assert "Then a PDF file is generated" in content

    # sw: f=specs/behavior/features/planning/create-plan.feature
    # sw: s=@bdd-plan-validation-commands
    def test_plan_includes_validation_commands(self, tmp_path: Path) -> None:
        features_dir = tmp_path / "specs" / "behavior" / "features"
        feature_path = features_dir / "billing" / "invoice-export.feature"
        _write_feature(feature_path)
        out_path = tmp_path / "plan.md"

        create_plan(feature_path=feature_path, out_path=out_path)
        content = out_path.read_text()
        assert "specweave doctor" in content
        assert "specweave review specs" in content
