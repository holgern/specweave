"""CLI integration tests."""

from __future__ import annotations

import json

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


def _write(tmp_path, name, text):  # type: ignore[no-untyped-def]
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_bdd_export_and_import_round_trip(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """bdd export -> feature, then bdd import-feature -> JSON, preserves ids."""
    spec = {
        "task_id": "task-0123",
        "feature": "Task lifecycle gates",
        "rules": [
            {
                "id": "rule-0001",
                "title": "Implementation requires an accepted plan",
            }
        ],
        "examples": [
            {
                "id": "bdd-0001",
                "title": ("Agent cannot start implementation without an accepted plan"),
                "rule_id": "rule-0001",
                "given": ["a task has a proposed plan"],
                "when": ["the agent starts implementation"],
                "then": ["taskledger rejects the transition"],
                "acceptance_criteria": ["ac-0001"],
            }
        ],
    }
    spec_path = _write(tmp_path, "spec.json", json.dumps(spec))
    feature_out = tmp_path / "task-0123.feature"
    result = runner.invoke(
        app,
        ["bdd", "export", "--from-json", str(spec_path), "--out", str(feature_out)],
    )
    assert result.exit_code == 0, result.stdout
    feature_text = feature_out.read_text(encoding="utf-8")
    assert "@task-0123" in feature_text
    assert "  Rule: Implementation requires an accepted plan" in feature_text
    assert "    @bdd-0001 @task-0123 @rule-0001 @ac-0001" in feature_text

    json_out = tmp_path / "roundtrip.json"
    result = runner.invoke(
        app,
        ["bdd", "import-feature", str(feature_out), "--out", str(json_out)],
    )
    assert result.exit_code == 0, result.stdout
    data = json.loads(json_out.read_text(encoding="utf-8"))
    assert data["task_id"] == "task-0123"
    assert data["rules"][0]["id"] == "rule-0001"
    assert data["examples"][0]["id"] == "bdd-0001"
    assert data["examples"][0]["acceptance_criteria"] == ["ac-0001"]


def test_report_normalize_writes_json_and_exits_nonzero_on_failure(
    tmp_path,
) -> None:  # type: ignore[no-untyped-def]
    payload = [
        {
            "name": "F",
            "elements": [
                {
                    "name": "Skipped",
                    "tags": [{"name": "@bdd-0001"}, {"name": "@ac-0001"}],
                    "steps": [{"result": {"status": "skipped"}}],
                }
            ],
        }
    ]
    report_path = _write(tmp_path, "cucumber.json", json.dumps(payload))
    out = tmp_path / "normalized.json"
    result = runner.invoke(
        app,
        [
            "report",
            "normalize",
            str(report_path),
            "--format",
            "cucumber-json",
            "--out",
            str(out),
        ],
    )
    # skipped fails closed -> exit 1.
    assert result.exit_code == 1, result.stdout
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["status"] == "failed"
    assert data["schema_version"] == 2


def test_report_normalize_passing_exits_0(tmp_path) -> None:  # type: ignore[no-untyped-def]
    payload = [
        {
            "name": "F",
            "elements": [
                {
                    "name": "S",
                    "tags": [{"name": "@bdd-0001"}, {"name": "@ac-0001"}],
                    "steps": [{"result": {"status": "passed"}}],
                }
            ],
        }
    ]
    report_path = _write(tmp_path, "cucumber.json", json.dumps(payload))
    result = runner.invoke(
        app,
        [
            "report",
            "normalize",
            str(report_path),
            "--format",
            "cucumber-json",
            "--expect-ac",
            "ac-0001",
        ],
    )
    assert result.exit_code == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["status"] == "passed"


def test_report_inspect_prints_summary(tmp_path) -> None:  # type: ignore[no-untyped-def]
    payload = [
        {
            "name": "F",
            "elements": [
                {
                    "name": "S",
                    "tags": [{"name": "@bdd-0001"}, {"name": "@ac-0001"}],
                    "steps": [{"result": {"status": "passed"}}],
                }
            ],
        }
    ]
    report_path = _write(tmp_path, "cucumber.json", json.dumps(payload))
    result = runner.invoke(
        app,
        ["report", "inspect", str(report_path), "--format", "cucumber-json"],
    )
    assert result.exit_code == 0, result.stdout
    assert "status=passed" in result.stdout
    assert ":: S" in result.stdout


def test_archledger_candidate_command(tmp_path) -> None:  # type: ignore[no-untyped-def]
    feature_text = """@task-0123
Feature: Task lifecycle gates

  @rule-0001
  Rule: Implementation requires an accepted plan

    @bdd-0001 @task-0123 @rule-0001 @ac-0001
    Scenario: Agent cannot start implementation without an accepted plan
      Given a task has a proposed plan
      When the agent starts implementation
      Then taskledger rejects the transition
"""
    feature_path = _write(tmp_path, "task-0123.feature", feature_text)
    out = tmp_path / "candidate.md"
    result = runner.invoke(
        app,
        [
            "archledger",
            "--feature",
            str(feature_path),
            "--bdd",
            "bdd-0001",
            "--out",
            str(out),
        ],
    )
    assert result.exit_code == 0, result.stdout
    content = out.read_text(encoding="utf-8")
    assert "- Task: task-0123" in content
    assert "Given a task has a proposed plan" in content


def test_bind_pytest_bdd_backend(tmp_path) -> None:  # type: ignore[no-untyped-def]
    feature_text = """Feature: Password login

  Scenario: Reject invalid password
    Given a registered user exists
    When the user submits an invalid password
    Then login is rejected
"""
    feature_path = _write(tmp_path, "test.feature", feature_text)
    out_dir = tmp_path / "steps"
    result = runner.invoke(
        app,
        [
            "bind",
            str(feature_path),
            "--backend",
            "pytest-bdd",
            "--out",
            str(out_dir),
        ],
    )
    assert result.exit_code == 0, result.stdout
    step_file = out_dir / "test_steps.py"
    content = step_file.read_text(encoding="utf-8")
    assert "from pytest_bdd import" in content
