"""Tests for the --from-json feature draft rendering."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from specweave.cli import app
from specweave.gherkin.draft import load_feature_draft, parse_feature_draft
from specweave.gherkin.writer import write_feature

runner = CliRunner()

_DRAFT_JSON = {
    "area": "ids",
    "title": "Ledger ID format and parsing",
    "description": "Ledger IDs follow a configurable prefix_width pattern.",
    "tags": ["area-ids", "feature-ledger-id-format"],
    "rules": [
        {
            "title": "Ledger IDs are zero-padded integers with a configurable prefix",
            "tags": ["rule-format"],
            "scenarios": [
                {
                    "title": "Format pads numbers with leading zeros",
                    "keyword": "Example",
                    "tags": ["bdd-ids-format-zero-pad"],
                    "steps": [
                        ["Given", 'a LedgerIdFormat with prefix "al" and width 4'],
                        ["When", "format is called with number 7"],
                        ["Then", 'the result is "al_0007"'],
                    ],
                },
                {
                    "title": "Custom prefix is used",
                    "keyword": "Example",
                    "tags": ["bdd-ids-format-custom-prefix"],
                    "steps": [
                        ["Given", 'a LedgerIdFormat with prefix "tl" and width 4'],
                        ["When", "format is called with number 1"],
                        ["Then", 'the result is "tl_0001"'],
                    ],
                },
            ],
        }
    ],
}


def _write_draft(path: Path, data: dict | None = None) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data or _DRAFT_JSON, indent=2), encoding="utf-8")
    return path


class TestParseFeatureDraft:
    def test_parses_title_and_tags(self) -> None:
        f = parse_feature_draft(_DRAFT_JSON)
        assert f.title == "Ledger ID format and parsing"
        assert "area-ids" in f.tags
        assert "feature-ledger-id-format" in f.tags

    def test_parses_rules_and_scenarios(self) -> None:
        f = parse_feature_draft(_DRAFT_JSON)
        assert len(f.rules) == 1
        rule = f.rules[0]
        assert (
            rule.title
            == "Ledger IDs are zero-padded integers with a configurable prefix"
        )
        assert rule.tags == ("rule-format",)
        assert len(rule.scenarios) == 2
        s = rule.scenarios[0]
        assert s.title == "Format pads numbers with leading zeros"
        assert s.keyword == "Example"
        assert "bdd-ids-format-zero-pad" in s.tags

    def test_parses_steps(self) -> None:
        f = parse_feature_draft(_DRAFT_JSON)
        s = f.rules[0].scenarios[0]
        assert len(s.steps) == 3
        assert s.steps[0].keyword == "Given"
        assert s.steps[0].text == 'a LedgerIdFormat with prefix "al" and width 4'

    def test_load_from_file(self, tmp_path: Path) -> None:
        path = _write_draft(tmp_path / "draft.json")
        f = load_feature_draft(path)
        assert f.title == "Ledger ID format and parsing"


class TestWriteDraftFeature:
    def test_writes_classic_feature(self) -> None:
        f = parse_feature_draft(_DRAFT_JSON)
        text = write_feature(f)
        assert "Feature: Ledger ID format and parsing" in text
        assert "@area-ids @feature-ledger-id-format" in text
        assert "Rule:" in text
        assert "Example: Format pads numbers with leading zeros" in text


class TestCreateFeatureFromJson:
    def test_cli_from_json(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        draft_path = _write_draft(tmp_path / "draft.json")
        result = runner.invoke(
            app,
            [
                "--json",
                "create",
                "feature",
                "--from-json",
                str(draft_path),
                "--out",
                str(
                    tmp_path
                    / "specs/behavior/features"
                    / "ids/ledger-id-format.feature"
                ),
            ],
        )
        assert result.exit_code == 0, result.stdout
        data = json.loads(result.stdout)
        assert data["status"] == "created"
        assert "feature-ledger-id-format" in data["feature_id"]
        assert "bdd-ids-format-zero-pad" in data["scenario_ids"]

        feature_path = Path(data["feature_path"])
        assert feature_path.exists()
        text = feature_path.read_text(encoding="utf-8")
        assert "Feature: Ledger ID format and parsing" in text

    def test_cli_from_json_dry_run(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        draft_path = _write_draft(tmp_path / "draft.json")
        out_path = tmp_path / "specs/behavior/features/ids/ledger-id-format.feature"
        result = runner.invoke(
            app,
            [
                "--json",
                "create",
                "feature",
                "--from-json",
                str(draft_path),
                "--out",
                str(out_path),
                "--dry-run",
            ],
        )
        assert result.exit_code == 0, result.stdout
        data = json.loads(result.stdout)
        assert data["status"] == "dry-run"
        assert not out_path.exists()

    def test_cli_from_json_refuses_existing(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        draft_path = _write_draft(tmp_path / "draft.json")
        out_path = tmp_path / "specs/behavior/features/ids/ledger-id-format.feature"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("existing", encoding="utf-8")

        result = runner.invoke(
            app,
            [
                "--json",
                "create",
                "feature",
                "--from-json",
                str(draft_path),
                "--out",
                str(out_path),
            ],
        )
        assert result.exit_code == 3

    def test_cli_from_json_force_overwrites(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        draft_path = _write_draft(tmp_path / "draft.json")
        out_path = tmp_path / "specs/behavior/features/ids/ledger-id-format.feature"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("existing", encoding="utf-8")

        result = runner.invoke(
            app,
            [
                "--json",
                "create",
                "feature",
                "--from-json",
                str(draft_path),
                "--out",
                str(out_path),
                "--force",
            ],
        )
        assert result.exit_code == 0, result.stdout
        text = out_path.read_text(encoding="utf-8")
        assert "Feature: Ledger ID format and parsing" in text

    def test_cli_legacy_path_still_works(self, tmp_path: Path, monkeypatch) -> None:
        """Verify the existing --area/--title/--scenario path is not broken."""
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(
            app,
            [
                "create",
                "feature",
                "--area",
                "auth",
                "--title",
                "Password login",
                "--scenario",
                "Reject invalid password",
                "--given",
                "a registered user exists",
                "--when",
                "the user submits an invalid password",
                "--then",
                "login is rejected",
            ],
        )
        assert result.exit_code == 0, result.stdout
        feature_path = tmp_path / "specs/behavior/features/auth/password-login.feature"
        assert feature_path.exists()
        assert "Feature: Password login" in feature_path.read_text(encoding="utf-8")

    def test_cli_legacy_dry_run_writes_nothing(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        out_path = tmp_path / "login.feature"
        result = runner.invoke(
            app,
            [
                "--json",
                "create",
                "feature",
                "--area",
                "auth",
                "--title",
                "Login",
                "--scenario",
                "Reject",
                "--given",
                "x",
                "--when",
                "y",
                "--then",
                "z",
                "--out",
                str(out_path),
                "--dry-run",
            ],
        )
        assert result.exit_code == 0, result.stdout
        assert json.loads(result.stdout)["status"] == "dry-run"
        assert not out_path.exists()

    def test_cli_legacy_rejects_empty_area(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(
            app,
            [
                "create",
                "feature",
                "--title",
                "Login",
                "--scenario",
                "Reject",
            ],
        )
        assert result.exit_code == 1
        assert "--area" in result.output
