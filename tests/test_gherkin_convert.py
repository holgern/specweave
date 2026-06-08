"""Tests for feature document conversion."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from specweave.cli import app
from specweave.gherkin.convert import (
    convert_feature_file,
    default_output_path,
    infer_document_format,
)

runner = CliRunner()

_CLASSIC = """@area-auth @feature-login
Feature: Login
  Users can log in.

  @rule-password
  Rule: Password checks

    @bdd-login-rejects-invalid-password
    Example: Reject invalid password
      Given a registered user exists
      When the user submits an invalid password
      Then login is rejected
"""


def test_infer_document_format_from_suffix() -> None:
    assert infer_document_format(Path("login.feature")) == "classic"
    assert infer_document_format(Path("login.feature.md")) == "markdown"


def test_default_output_path_classic_to_markdown() -> None:
    assert default_output_path(Path("login.feature"), "markdown") == Path(
        "login.feature.md"
    )


def test_convert_classic_to_markdown_no_validation(tmp_path: Path) -> None:
    source = tmp_path / "login.feature"
    source.write_text(_CLASSIC, encoding="utf-8")

    result = convert_feature_file(source_path=source, validate=False)

    target = tmp_path / "login.feature.md"
    assert result["status"] == "created"
    assert result["output_path"] == str(target)
    text = target.read_text(encoding="utf-8")
    assert "# Feature: Login" in text
    assert "## Rule: Password checks" in text
    assert "### Example: Reject invalid password" in text
    assert "`@bdd-login-rejects-invalid-password`" in text


def test_convert_refuses_existing_output_without_force(tmp_path: Path) -> None:
    source = tmp_path / "login.feature"
    source.write_text(_CLASSIC, encoding="utf-8")
    target = tmp_path / "login.feature.md"
    target.write_text("existing", encoding="utf-8")

    try:
        convert_feature_file(source_path=source, validate=False)
    except ValueError as exc:
        assert "Use --force" in str(exc)
    else:  # pragma: no cover - defensive
        raise AssertionError("expected overwrite refusal")


def test_cli_convert_json(tmp_path: Path) -> None:
    source = tmp_path / "login.feature"
    source.write_text(_CLASSIC, encoding="utf-8")
    result = runner.invoke(
        app,
        ["--json", "convert", str(source), "--no-validate"],
    )

    assert result.exit_code == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["command"] == "convert"
    assert data["source_format"] == "classic"
    assert data["target_format"] == "markdown"
    assert Path(data["output_path"]).name == "login.feature.md"


def test_create_feature_uses_markdown_default(
    tmp_path: Path, monkeypatch
) -> None:
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
    feature_path = tmp_path / "specs/behavior/features/auth/password-login.feature.md"
    assert feature_path.exists()
    assert "# Feature: Password login" in feature_path.read_text(encoding="utf-8")
