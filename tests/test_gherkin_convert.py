"""Tests for feature document conversion."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from specweave.cli import app
from specweave.gherkin.convert import (
    convert_feature_file,
    convert_feature_files,
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


def _write_feature_file(path: Path, content: str = _CLASSIC) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


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


def test_convert_directory_classic_to_markdown(tmp_path: Path) -> None:
    features_dir = tmp_path / "specs" / "behavior" / "features"
    _write_feature_file(features_dir / "auth" / "login.feature")
    _write_feature_file(features_dir / "config" / "nested" / "configuration.feature")

    result = convert_feature_files(
        paths=[features_dir], target_format="markdown", validate=False
    )

    assert result["status"] == "passed"
    assert result["summary"]["created"] == 2
    assert (features_dir / "auth" / "login.feature.md").exists()
    assert (features_dir / "config" / "nested" / "configuration.feature.md").exists()
    assert "# Feature: Login" in (features_dir / "auth" / "login.feature.md").read_text(
        encoding="utf-8"
    )


def test_convert_directory_keeps_source_by_default(tmp_path: Path) -> None:
    features_dir = tmp_path / "specs" / "behavior" / "features"
    source = _write_feature_file(features_dir / "auth" / "login.feature")

    result = convert_feature_files(
        paths=[features_dir], target_format="markdown", validate=False
    )

    assert result["status"] == "passed"
    assert source.exists()
    assert (features_dir / "auth" / "login.feature.md").exists()


def test_convert_directory_replace_source_removes_classic_after_success(
    tmp_path: Path,
) -> None:
    features_dir = tmp_path / "specs" / "behavior" / "features"
    source = _write_feature_file(features_dir / "auth" / "login.feature")

    result = convert_feature_files(
        paths=[features_dir],
        target_format="markdown",
        validate=False,
        replace_source=True,
    )

    assert result["status"] == "passed"
    assert not source.exists()
    assert result["summary"]["deleted_sources"] == 1
    assert (features_dir / "auth" / "login.feature.md").exists()


def test_convert_directory_dry_run_writes_nothing(tmp_path: Path) -> None:
    features_dir = tmp_path / "specs" / "behavior" / "features"
    source = _write_feature_file(features_dir / "auth" / "login.feature")

    result = convert_feature_files(
        paths=[features_dir],
        target_format="markdown",
        validate=False,
        dry_run=True,
        replace_source=True,
    )

    assert result["status"] == "dry-run"
    assert source.exists()
    assert not (features_dir / "auth" / "login.feature.md").exists()
    assert result["items"][0]["would_delete_source"] is True


def test_convert_directory_reports_collision_without_force(tmp_path: Path) -> None:
    features_dir = tmp_path / "specs" / "behavior" / "features"
    source = _write_feature_file(features_dir / "auth" / "login.feature")
    _write_feature_file(
        features_dir / "auth" / "login.feature.md", "# Feature: Different\n"
    )

    result = convert_feature_files(
        paths=[features_dir], target_format="markdown", validate=False
    )

    assert result["status"] == "failed"
    assert result["summary"]["errors"] == 1
    assert any(
        item["source_path"] == str(source) and item["status"] == "error"
        for item in result["items"]
    )


def test_cli_convert_all_json_summary(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    features_dir = tmp_path / "specs" / "behavior" / "features"
    _write_feature_file(features_dir / "auth" / "login.feature")
    _write_feature_file(features_dir / "config" / "configuration.feature")

    result = runner.invoke(
        app,
        ["--json", "convert", "--all", "--to", "markdown", "--no-validate"],
    )

    assert result.exit_code == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["mode"] == "batch"
    assert data["summary"]["created"] == 2
    assert data["summary"]["errors"] == 0
    assert data["source_count"] == 2
    assert len(data["items"]) == 2


def test_create_feature_uses_markdown_default(tmp_path: Path, monkeypatch) -> None:
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


class TestSWBEH016FormatMismatch:
    """Tests for the SWBEH016 lint diagnostic.

    Detects classic Gherkin syntax in .feature.md files.
    """

    def test_classic_at_tag_in_feature_md(self, tmp_path: Path) -> None:
        from specweave.gherkin.lint import lint_feature_files

        path = tmp_path / "auth" / "login.feature.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "@area-auth @feature-login\nFeature: Login\n  Users can log in.\n",
            encoding="utf-8",
        )
        findings = lint_feature_files([path])
        codes = [f.code for f in findings]
        assert "SWBEH016" in codes, f"Expected SWBEH016 in {codes}"
        mismatch = [f for f in findings if f.code == "SWBEH016"][0]
        assert "--from classic --to markdown --force" in mismatch.message

    def test_classic_feature_heading_in_feature_md(self, tmp_path: Path) -> None:
        from specweave.gherkin.lint import lint_feature_files

        path = tmp_path / "auth" / "login.feature.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "Feature: Login\n  Users can log in.\n",
            encoding="utf-8",
        )
        findings = lint_feature_files([path])
        codes = [f.code for f in findings]
        assert "SWBEH016" in codes

    def test_valid_markdown_feature_md_no_mismatch(self, tmp_path: Path) -> None:
        from specweave.gherkin.lint import lint_feature_files

        path = tmp_path / "auth" / "login.feature.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "`@area-auth`\n# Feature: Login\n\n* Given x\n* When y\n* Then z\n",
            encoding="utf-8",
        )
        findings = lint_feature_files([path])
        codes = [f.code for f in findings]
        assert "SWBEH016" not in codes

    def test_classic_feature_file_no_mismatch(self, tmp_path: Path) -> None:
        from specweave.gherkin.lint import lint_feature_files

        path = tmp_path / "auth" / "login.feature"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "@area-auth\nFeature: Login\n  Users can log in.\n",
            encoding="utf-8",
        )
        findings = lint_feature_files([path])
        codes = [f.code for f in findings]
        assert "SWBEH016" not in codes


class TestConvertFromContent:
    """Tests for --from content mode in convert."""

    def test_from_content_detects_classic_in_feature_md(self, tmp_path: Path) -> None:
        source = tmp_path / "auth" / "login.feature.md"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(
            "@area-auth @feature-login\nFeature: Login\n  Users can log in.\n",
            encoding="utf-8",
        )
        result = convert_feature_file(
            source_path=source,
            source_format="content",
            target_format="markdown",
            force=True,
            validate=False,
        )
        assert result["source_format"] == "classic"
        assert result["target_format"] == "markdown"
        assert result["status"] == "updated"
        text = source.read_text(encoding="utf-8")
        assert "# Feature: Login" in text

    def test_from_content_detects_markdown_in_feature_md(self, tmp_path: Path) -> None:
        source = tmp_path / "auth" / "login.feature.md"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(
            "`@area-auth`\n# Feature: Login\n\n* Given x\n",
            encoding="utf-8",
        )
        result = convert_feature_file(
            source_path=source,
            source_format="content",
            target_format="markdown",
            validate=False,
        )
        assert result["source_format"] == "markdown"
        assert result["status"] == "unchanged"

    def test_cli_from_content(self, tmp_path: Path) -> None:
        source = tmp_path / "auth" / "login.feature.md"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(
            "@area-auth\nFeature: Login\n  Users can log in.\n",
            encoding="utf-8",
        )
        result = runner.invoke(
            app,
            [
                "--json",
                "convert",
                str(source),
                "--from",
                "content",
                "--to",
                "markdown",
                "--force",
                "--no-validate",
            ],
        )

        assert result.exit_code == 0, result.stdout
        data = json.loads(result.stdout)
        assert data["source_format"] == "classic"
        assert data["target_format"] == "markdown"
