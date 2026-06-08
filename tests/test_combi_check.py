from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from specweave.cli import app

runner = CliRunner()


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_combi_check_writes_json_and_human_diagnostics(tmp_path: Path) -> None:
    _write(
        tmp_path / "specs/behavior/features/core/login.feature",
        "Feature: Login\n\n"
        "  @bdd-login-success @ac-0001\n"
        "  Example: Successful login\n"
        "    Given a user exists\n"
        "    When credentials are submitted\n"
        "    Then access is granted\n",
    )
    output = tmp_path / ".specweave/reports/combi-check.json"

    result = runner.invoke(
        app,
        [
            "combi",
            "check",
            "--features",
            str(tmp_path / "specs/behavior/features"),
            "--tests",
            str(tmp_path / "tests"),
            "--taskledger-mappings",
            str(tmp_path / ".specweave/mappings/taskledger"),
            "--evidence",
            str(tmp_path / ".specweave/evidence"),
            "--archledger",
            str(tmp_path / ".archledger"),
            "--json",
            str(output),
        ],
    )

    assert result.exit_code == 0
    assert "Combi check: 1 scenarios" in result.stdout
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["summary"]["gap_count"] == 2
    assert {gap["code"] for gap in payload["gaps"]} == {
        "missing_pytest_mapping",
        "missing_evidence",
    }


def test_combi_check_strict_fails_on_missing_bdd_id(tmp_path: Path) -> None:
    _write(
        tmp_path / "specs/behavior/features/core/login.feature",
        "Feature: Login\n\n"
        "  Example: Successful login\n"
        "    Given a user exists\n"
        "    When credentials are submitted\n"
        "    Then access is granted\n",
    )

    result = runner.invoke(
        app,
        [
            "combi",
            "check",
            "--features",
            str(tmp_path / "specs/behavior/features"),
            "--tests",
            str(tmp_path / "tests"),
            "--strict",
        ],
    )

    assert result.exit_code == 1
    assert "ERROR missing_bdd_id" in result.stdout
