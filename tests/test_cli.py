"""CLI integration tests."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from specweave.cli import app
from specweave.gherkin.model import Feature, Scenario, Step
from specweave.gherkin.writer import write_feature

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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _write_markdown_behavior_feature(
    tmp_path: Path,
    *,
    relative_path: str,
    title: str,
    scenario_id: str,
    scenario_title: str,
) -> Path:
    path = tmp_path / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    feature = Feature(
        title=title,
        scenarios=(
            Scenario(
                title=scenario_title,
                keyword="Example",
                tags=(scenario_id.removeprefix("@"),),
                steps=(
                    Step(keyword="Given", text="a registered user exists"),
                    Step(keyword="When", text="the user submits credentials"),
                    Step(keyword="Then", text="the outcome is observable"),
                ),
            ),
        ),
    )
    path.write_text(
        write_feature(feature, document_format="markdown"), encoding="utf-8"
    )
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


def _write_behavior_feature(
    tmp_path: Path,
    *,
    relative_path: str = "specs/behavior/features/task-management/plan-gates.feature",
) -> Path:
    path = tmp_path / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """@area-task-management @feature-plan-gates
Feature: Plan gates
  Implementation must not start before a plan is accepted.

  @rule-accepted-plan-required
  Rule: Implementation requires an accepted plan

    @bdd-implementation-blocked-before-plan-acceptance
    Example: Agent cannot start implementation before plan approval
      Given a task has a proposed plan
      When the agent starts implementation
      Then implementation is blocked
""",
        encoding="utf-8",
    )
    return path


def test_behavior_check_accepts_canonical_feature(tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.chdir(tmp_path)
    _write_behavior_feature(tmp_path)
    result = runner.invoke(app, ["behavior", "check"])
    assert result.exit_code == 0, result.stdout
    assert "No behavior lint findings." in result.stdout


def test_behavior_check_warns_on_deprecated_specs_bdd_path(
    tmp_path, monkeypatch
) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.chdir(tmp_path)
    feature_path = _write_behavior_feature(
        tmp_path,
        relative_path="specs/bdd/features/task-management/plan-gates.feature",
    )
    result = runner.invoke(app, ["behavior", "check", str(feature_path)])
    assert result.exit_code == 0, result.stdout
    assert "SWBEH015" in result.stdout


def test_behavior_generate_tests_creates_plain_pytest(tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.chdir(tmp_path)
    feature_path = _write_behavior_feature(tmp_path)
    result = runner.invoke(app, ["behavior", "generate-tests", str(feature_path)])
    assert result.exit_code == 0, result.stdout
    test_file = tmp_path / "tests/test_task_management_plan_gates.py"
    content = test_file.read_text(encoding="utf-8")
    assert "import pytest" in content
    assert "@pytest.mark.specweave" in content
    assert (
        "# specweave: feature="
        "specs/behavior/features/task-management/plan-gates.feature" in content
    )
    assert "pytest_bdd" not in content
    assert "scenarios(" not in content


def test_behavior_index_writes_markdown_and_manifest(tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.chdir(tmp_path)
    feature_path = _write_behavior_feature(tmp_path)
    generate_result = runner.invoke(
        app, ["behavior", "generate-tests", str(feature_path)]
    )
    assert generate_result.exit_code == 0, generate_result.stdout
    result = runner.invoke(app, ["behavior", "index"])
    assert result.exit_code == 0, result.stdout
    index_path = tmp_path / "specs/behavior/README.md"
    manifest_path = tmp_path / "specs/behavior/manifest.json"
    assert index_path.exists()
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert (
        manifest["features"][0]["path"]
        == "specs/behavior/features/task-management/plan-gates.feature"
    )
    scenario = manifest["features"][0]["rules"][0]["scenarios"][0]
    assert scenario["automation"]["backend"] == "pytest"
    assert scenario["automation"]["status"] == "bound"


def test_behavior_coverage_reports_bound_scenarios(tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.chdir(tmp_path)
    feature_path = _write_behavior_feature(tmp_path)
    generate_result = runner.invoke(
        app, ["behavior", "generate-tests", str(feature_path)]
    )
    assert generate_result.exit_code == 0, generate_result.stdout
    result = runner.invoke(app, ["behavior", "coverage"])
    assert result.exit_code == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["features_total"] == 1
    assert data["scenarios_total"] == 1
    assert data["features_bound"] == 1
    assert data["scenarios_bound"] == 1


def test_behavior_coverage_text_shows_missing(tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.chdir(tmp_path)
    _write_markdown_behavior_feature(
        tmp_path,
        relative_path="specs/behavior/features/auth/login.feature.md",
        title="Login",
        scenario_id="@bdd-login-rejects-invalid-password",
        scenario_title="Reject invalid password",
    )
    result = runner.invoke(
        app,
        [
            "behavior",
            "coverage",
            "--features",
            "specs/behavior/features",
            "--tests",
            "tests",
            "--format",
            "text",
            "--show",
            "missing",
        ],
    )

    assert result.exit_code == 1, result.stdout
    assert "@bdd-login-rejects-invalid-password" in result.stdout
    assert "expected: tests/test_auth_login.py" in result.stdout


def test_behavior_coverage_feature_filter(tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.chdir(tmp_path)
    first = _write_markdown_behavior_feature(
        tmp_path,
        relative_path="specs/behavior/features/auth/login.feature.md",
        title="Login",
        scenario_id="@bdd-login-rejects-invalid-password",
        scenario_title="Reject invalid password",
    )
    _write_markdown_behavior_feature(
        tmp_path,
        relative_path="specs/behavior/features/config/configuration.feature.md",
        title="Configuration",
        scenario_id="@bdd-loads-config",
        scenario_title="Loads config",
    )
    _write(
        tmp_path,
        "tests/test_auth_login.py",
        """
# specweave: feature=specs/behavior/features/auth/login.feature.md
# specweave: scenario=@bdd-login-rejects-invalid-password
def test_rejects_invalid_password() -> None:
    pass
""",
    )

    result = runner.invoke(
        app,
        [
            "behavior",
            "coverage",
            "--features",
            "specs/behavior/features",
            "--feature",
            str(first),
            "--tests",
            "tests",
            "--format",
            "text",
        ],
    )

    assert "specs/behavior/features/auth/login.feature.md" in result.stdout
    assert (
        "specs/behavior/features/config/configuration.feature.md" not in result.stdout
    )


def test_behavior_mappings_lists_comment_and_marker_sources(
    tmp_path, monkeypatch
) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.chdir(tmp_path)
    _write(
        tmp_path,
        "tests/test_auth_login.py",
        """
# specweave: feature=specs/behavior/features/auth/login.feature.md
# specweave: scenario=@bdd-login-rejects-invalid-password
def test_rejects_invalid_password() -> None:
    pass
""",
    )
    _write(
        tmp_path,
        "tests/test_config.py",
        """
import pytest

SPECWEAVE_FEATURE = "specs/behavior/features/config/configuration.feature.md"


@pytest.mark.specweave(
    feature=SPECWEAVE_FEATURE,
    scenario="@bdd-loads-config",
)
def test_loads_config() -> None:
    pass
""",
    )

    result = runner.invoke(
        app,
        [
            "behavior",
            "mappings",
            "--tests",
            "tests",
            "--format",
            "text",
        ],
    )

    assert result.exit_code == 0, result.stdout
    assert "comment" in result.stdout
    assert "marker" in result.stdout
    assert "tests/test_auth_login.py::test_rejects_invalid_password" in result.stdout
    assert "tests/test_config.py::test_loads_config" in result.stdout


def test_behavior_import_report_maps_pytest_nodeid(tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.chdir(tmp_path)
    feature_path = _write_behavior_feature(tmp_path)
    generate_result = runner.invoke(
        app, ["behavior", "generate-tests", str(feature_path)]
    )
    assert generate_result.exit_code == 0, generate_result.stdout
    report_path = tmp_path / "reports/behavior/task-management-plan-gates-junit.xml"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="pytest" tests="1">
    <testcase classname="tests.test_task_management_plan_gates"
              file="tests/test_task_management_plan_gates.py"
              name="test_agent_cannot_start_implementation_before_plan_approval"/>
  </testsuite>
</testsuites>
""",
        encoding="utf-8",
    )
    result = runner.invoke(
        app,
        [
            "behavior",
            "import-report",
            str(report_path),
            "--format",
            "junit-xml",
            "--out",
            str(tmp_path / ".specweave/evidence/plan-gates.pytest-evidence.json"),
        ],
    )
    assert result.exit_code == 0, result.stdout
    payload = json.loads(
        (tmp_path / ".specweave/evidence/plan-gates.pytest-evidence.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["backend"] == "pytest"
    assert (
        payload["results"][0]["feature"]
        == "specs/behavior/features/task-management/plan-gates.feature"
    )
    assert (
        payload["results"][0]["scenario"]
        == "@bdd-implementation-blocked-before-plan-acceptance"
    )
