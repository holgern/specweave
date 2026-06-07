"""Subprocess execution and capture for delegated BDD runners."""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

from specweave.runners.reports import write_summary

REPORT_DIR = Path(".specweave/reports")


def run_command(args: list[str], runner: str = "command") -> int:
    """Run a delegated command and write a normalized summary report.

    Returns the exit code of the delegated command.
    """
    stdout_path = REPORT_DIR / "stdout.txt"
    stderr_path = REPORT_DIR / "stderr.txt"
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    start = time.monotonic()

    try:
        proc = subprocess.run(
            args,
            capture_output=True,
            text=True,
            shell=False,
        )
        duration = time.monotonic() - start
        exit_code = proc.returncode

        stdout_path.write_text(proc.stdout or "", encoding="utf-8")
        stderr_path.write_text(proc.stderr or "", encoding="utf-8")

    except FileNotFoundError:
        duration = time.monotonic() - start
        exit_code = -1
        stdout_path.write_text("", encoding="utf-8")
        stderr_path.write_text(f"Command not found: {args[0]}\n", encoding="utf-8")

    write_summary(
        report_dir=REPORT_DIR,
        runner=runner,
        command=args,
        exit_code=exit_code,
        duration_seconds=duration,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
    )

    return exit_code
