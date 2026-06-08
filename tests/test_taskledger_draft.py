"""Tests for specweave create taskledger-task draft."""

from __future__ import annotations

import json
from pathlib import Path

from specweave.planning import create_taskledger_draft


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


class TestTaskledgerDraft:
    def test_creates_draft_from_feature(self, tmp_path: Path) -> None:
        feature_path = (
            tmp_path
            / "specs"
            / "behavior"
            / "features"
            / "billing"
            / "invoice-export.feature"
        )
        _write_feature(feature_path)
        out_path = tmp_path / "draft.json"

        create_taskledger_draft(
            feature_path=feature_path,
            out_path=out_path,
        )
        assert out_path.exists()
        draft = json.loads(out_path.read_text())
        assert draft["source"] == "specweave"
        assert draft["title"] == "Implement Invoice export behavior"
        assert len(draft["acceptance_criteria"]) == 1
        ac = draft["acceptance_criteria"][0]
        assert ac["bdd_id"] == "bdd-invoice-export-user-exports-paid-invoice"
        assert len(draft["suggested_validation"]) > 0

    def test_draft_does_not_require_taskledger_import(self) -> None:
        """Verify the module imports without taskledger."""
        import specweave.planning

        assert "create_taskledger_draft" in dir(specweave.planning)

    def test_draft_json_is_valid(self, tmp_path: Path) -> None:
        feature_path = (
            tmp_path
            / "specs"
            / "behavior"
            / "features"
            / "billing"
            / "invoice-export.feature"
        )
        _write_feature(feature_path)
        out_path = tmp_path / "draft.json"

        create_taskledger_draft(feature_path=feature_path, out_path=out_path)
        draft = json.loads(out_path.read_text())
        assert draft["schema_version"] == 1
        assert "feature" in draft
        assert "acceptance_criteria" in draft
