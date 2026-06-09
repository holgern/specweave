"""Tests for root --json CLI output and init command."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from specweave.cli import app

runner = CliRunner()


class TestRootJson:
    def test_json_version(self) -> None:
        result = runner.invoke(app, ["--json", "version"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["schema_version"] == 1
        assert data["command"] == "version"
        assert data["status"] == "ok"
        assert "version" in data

    def test_human_version(self) -> None:
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "specweave" in result.output

    def test_json_init_dry_run(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["--json", "init", "--dry-run"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["command"] == "init"
        assert data["status"] == "ok"
        assert len(data["created"]) > 0
        # Nothing should be written
        assert not (tmp_path / "specweave.toml").exists()

    def test_human_init(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0
        assert (tmp_path / "specweave.toml").exists()

    def test_json_init_british(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(
            app, ["--json", "init", "--spelling", "behaviour", "--dry-run"]
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert any("behaviour" in p for p in data["created"])

    def test_json_doctor(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["--json", "doctor"])
        data = json.loads(result.output)
        assert data["schema_version"] == 1
        assert data["command"] == "doctor"
        assert "status" in data

    def test_json_review_specs(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["--json", "review", "specs"])
        data = json.loads(result.output)
        assert data["schema_version"] == 1
        assert data["command"] == "review specs"

    def test_config_option(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        config_file = tmp_path / "specweave.toml"
        config_file.write_text("schema_version = 1\n")
        result = runner.invoke(app, ["--config", str(config_file), "--json", "version"])
        assert result.exit_code == 0


class TestInitIdempotency:
    def test_init_twice_no_force(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        result1 = runner.invoke(app, ["init"])
        assert result1.exit_code == 0
        result2 = runner.invoke(app, ["init"])
        assert result2.exit_code == 0
        # Config should not have been overwritten
        assert "already exists" in result2.output or "Existing" in result2.output
