"""CLI integration tests."""

from __future__ import annotations

from typer.testing import CliRunner

from specweave.cli import app

runner = CliRunner()


def test_help_exits_0() -> None:
    """``specweave --help`` exits 0."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout


def test_version_exits_0() -> None:
    """``specweave version`` prints version."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "specweave" in result.stdout
