"""Summary JSON model and writer."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def write_summary(
    report_dir: Path,
    runner: str,
    command: list[str],
    exit_code: int,
    duration_seconds: float,
    stdout_path: Path,
    stderr_path: Path,
    scenarios: int = 0,
    failed: int = 0,
) -> dict:
    """Write a normalized summary JSON to *report_dir* and return the dict."""
    report_dir.mkdir(parents=True, exist_ok=True)

    if exit_code == 0:
        status = "passed"
    elif exit_code < 0:
        status = "error"
    else:
        status = "failed"

    started_at = datetime.now(timezone.utc)
    finished_at = started_at

    summary = {
        "schema_version": 1,
        "generated_by": "specweave",
        "runner": runner,
        "command": tuple(command),
        "exit_code": exit_code,
        "status": status,
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "duration_seconds": duration_seconds,
        "scenarios": scenarios,
        "failed": failed,
        "evidence": [
            str(report_dir / "summary.json"),
            _rel_evidence(stdout_path, report_dir),
            _rel_evidence(stderr_path, report_dir),
        ],
        "criteria": [],
    }

    summary_path = report_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def _rel_evidence(path: Path, report_dir: Path) -> str:
    """Return a relative evidence path string."""
    if path.exists():
        return str(path.relative_to(report_dir.parent))
    return str(path)
