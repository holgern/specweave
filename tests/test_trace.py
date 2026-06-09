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


def test_trace_by_bdd_id_reports_mapping_and_missing_evidence_gap(
    tmp_path: Path,
) -> None:
    feature = _write(
        tmp_path / "specs/behavior/features/core/login.feature",
        "Feature: Login\n\n"
        "  @bdd-login-success @ac-0001\n"
        "  Example: Successful login\n"
        "    Given a user exists\n"
        "    When credentials are submitted\n"
        "    Then access is granted\n",
    )
    _write(
        tmp_path / "tests/test_core_login.py",
        "import pytest\n\n"
        f'@pytest.mark.specweave(feature="{feature.as_posix()}", '
        'scenario="@bdd-login-success")\n'
        "def test_successful_login():\n"
        "    assert True\n",
    )

    result = runner.invoke(
        app,
        [
            "trace",
            "bdd-login-success",
            "--format",
            "json",
            "--features",
            str(tmp_path / "specs/behavior/features"),
            "--tests",
            str(tmp_path / "tests"),
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    trace = payload["traces"][0]
    assert trace["bdd_ids"] == ["bdd-login-success"]
    assert trace["ac_ids"] == ["ac-0001"]
    assert trace["test_refs"][0]["function_name"] == "test_successful_login"
    assert trace["gaps"] == [
        {
            "code": "missing_evidence",
            "message": "No imported evidence references this scenario.",
        }
    ]


def test_trace_rejects_markdown_feature_path(tmp_path: Path) -> None:
    feature = _write(
        tmp_path / "specs/behavior/features/core/login.feature.md",
        "# Feature: Login\n\n"
        "`@bdd-md-login`\n"
        "## Example: Markdown login\n\n"
        "- Given a user exists\n"
        "- When credentials are submitted\n"
        "- Then access is granted\n",
    )

    result = runner.invoke(app, ["trace", str(feature), "--format", "json"])

    assert result.exit_code != 0
    assert result.exception is not None
    assert "no longer supported" in str(result.exception)
