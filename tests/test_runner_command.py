"""Tests for the delegated command runner."""

from __future__ import annotations

import json
import shutil

from specweave.runners.command import REPORT_DIR, run_command


def setup_function() -> None:
    """Clean report dir before each test."""
    if REPORT_DIR.exists():
        shutil.rmtree(REPORT_DIR)


def test_run_success() -> None:
    """Run a successful command and verify summary.json."""
    exit_code = run_command(["python", "-c", "print('ok')"])
    assert exit_code == 0

    summary_path = REPORT_DIR / "summary.json"
    assert summary_path.exists()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["status"] == "passed"
    assert summary["exit_code"] == 0
    assert summary["runner"] == "command"


def test_run_failure() -> None:
    """Run a failing command and verify failed summary."""
    exit_code = run_command(["python", "-c", "exit(1)"])
    assert exit_code == 1

    summary_path = REPORT_DIR / "summary.json"
    assert summary_path.exists()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["status"] == "failed"
    assert summary["exit_code"] == 1


def test_run_not_found() -> None:
    """Run a non-existent command returns error."""
    exit_code = run_command(["nonexistent_command_xyz123"])
    assert exit_code == -1

    summary_path = REPORT_DIR / "summary.json"
    assert summary_path.exists()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["status"] == "error"


def test_run_captures_stdout_stderr() -> None:
    """Stdout and stderr are captured to files."""
    cmd = [
        "python",
        "-c",
        "import sys; sys.stdout.write('out'); sys.stderr.write('err')",
    ]
    run_command(cmd)

    stdout_path = REPORT_DIR / "stdout.txt"
    stderr_path = REPORT_DIR / "stderr.txt"
    assert stdout_path.exists()
    assert stderr_path.exists()
    assert stdout_path.read_text(encoding="utf-8") == "out"
    assert stderr_path.read_text(encoding="utf-8") == "err"
