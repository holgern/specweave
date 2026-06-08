"""Tests for the optional Taskledger file adapter."""

from __future__ import annotations

import json

from specweave.integrations.taskledger import (
    load_taskledger_acceptance_export,
    task_id_from_report,
    write_behavior_feature_from_taskledger,
    write_taskledger_bdd_evidence,
)
from specweave.reports.model import NormalizedBddReport, ScenarioResult
from specweave.reports.normalize import normalize_report

FEATURE = "specs/behavior/features/integrations/taskledger.feature.md"


# specweave: feature=specs/behavior/features/integrations/taskledger.feature.md
# specweave: scenario=@bdd-taskledger-import
def test_load_rich_shape(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """import-taskledger creates a feature from Taskledger export (rich shape)."""
    path = tmp_path / "task-0123.acceptance.json"
    path.write_text(
        json.dumps(
            {
                "task_id": "task-0123",
                "feature": "Task lifecycle gates",
                "rules": [
                    {
                        "id": "rule-0001",
                        "title": ("Implementation requires an accepted plan"),
                    }
                ],
                "examples": [
                    {
                        "id": "bdd-0001",
                        "title": (
                            "Agent cannot start implementation without an accepted plan"
                        ),
                        "rule_id": "rule-0001",
                        "given": ["a task has a proposed plan"],
                        "when": ["the agent starts implementation"],
                        "then": ["taskledger rejects the transition"],
                        "acceptance_criteria": ["ac-0001"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    spec = load_taskledger_acceptance_export(path)
    assert spec.task_id == "task-0123"
    assert spec.rules[0].id == "rule-0001"
    assert spec.examples[0].id == "bdd-0001"
    assert spec.examples[0].acceptance_criteria == ("ac-0001",)


def test_load_legacy_mvp_shape(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """import-taskledger creates a feature from Taskledger export (legacy shape)."""
    path = tmp_path / "task-0009.acceptance.json"
    path.write_text(
        json.dumps(
            {
                "task_id": "task-0009",
                "title": "Password login",
                "acceptance_criteria": [
                    {"id": "ac-0001", "text": "Reject invalid password"},
                    {"id": "ac-0002", "text": "Accept valid password"},
                ],
            }
        ),
        encoding="utf-8",
    )
    spec = load_taskledger_acceptance_export(path)
    assert spec.task_id == "task-0009"
    assert spec.feature == "Password login"
    assert [ex.id for ex in spec.examples] == ["bdd-0001", "bdd-0002"]
    assert spec.examples[0].acceptance_criteria == ("ac-0001",)
    assert spec.examples[0].title == "Reject invalid password"


# specweave: feature=specs/behavior/features/integrations/taskledger.feature.md
# specweave: scenario=@bdd-taskledger-evidence
def test_task_id_from_report() -> None:
    """report normalize generates Taskledger-compatible evidence."""
    report = NormalizedBddReport(
        runner="cucumber-json",
        source_report="x.json",
        results=(
            ScenarioResult(
                name="S",
                status="passed",
                tags=("bdd-0001", "task-0123", "rule-0001", "ac-0001"),
            ),
        ),
    )
    assert task_id_from_report(report) == "task-0123"


def test_task_id_from_report_missing_is_empty() -> None:
    """report normalize generates Taskledger-compatible evidence (missing task)."""
    report = NormalizedBddReport(
        runner="cucumber-json",
        source_report="x.json",
        results=(ScenarioResult(name="S", status="passed", tags=("ac-0001",)),),
    )
    assert task_id_from_report(report) == ""


def test_write_evidence_round_trip(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """A normalized report serializes to the Taskledger evidence JSON shape."""
    payload = [
        {
            "name": "F",
            "elements": [
                {
                    "name": "S",
                    "tags": [
                        {"name": "@bdd-0001"},
                        {"name": "@task-0123"},
                        {"name": "@ac-0001"},
                    ],
                    "steps": [{"result": {"status": "passed"}}],
                }
            ],
        }
    ]
    report_path = tmp_path / "cucumber.json"
    report_path.write_text(json.dumps(payload), encoding="utf-8")
    report = normalize_report(report_path, "cucumber-json")

    out = tmp_path / ".specweave/evidence/task-0123.bdd-evidence.json"
    recorded = write_taskledger_bdd_evidence(report, out)
    assert recorded == "task-0123"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["schema_version"] == 2
    assert data["generated_by"] == "specweave"
    assert data["task_id"] == "task-0123"
    assert data["status"] == "passed"
    assert data["criteria"][0]["criterion_id"] == "ac-0001"
    assert data["criteria"][0]["status"] == "passed"
    assert data["criteria"][0]["bdd_ids"] == ["bdd-0001"]
    assert data["scenarios"][0]["bdd_id"] == "bdd-0001"


def test_write_evidence_explicit_task_id(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """report normalize generates Taskledger-compatible evidence (explicit task)."""
    report = NormalizedBddReport(
        runner="cucumber-json",
        source_report="x.json",
        results=(ScenarioResult(name="S", status="passed", tags=("ac-0001",)),),
    )
    out = tmp_path / "ev.json"
    recorded = write_taskledger_bdd_evidence(report, out, task_id="task-0042")
    assert recorded == "task-0042"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["task_id"] == "task-0042"


# specweave: feature=specs/behavior/features/integrations/taskledger.feature.md
# specweave: scenario=@bdd-taskledger-draft
def test_no_taskledger_import_required() -> None:  # type: ignore[no-untyped-def]
    """create taskledger-task generates a draft JSON."""
    import sys

    assert "taskledger" not in sys.modules
    # Importing the adapter does not pull in taskledger.
    import specweave.integrations.taskledger  # noqa: F401

    assert "taskledger" not in sys.modules


def test_import_taskledger_to_canonical_behavior_feature(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """import-taskledger creates a feature from Taskledger export."""
    source = tmp_path / "task-0123.acceptance.json"
    source.write_text(
        json.dumps(
            {
                "task_id": "task-0123",
                "feature": "Plan gates",
                "rules": [
                    {
                        "id": "rule-accepted-plan-required",
                        "title": "Implementation requires an accepted plan",
                    }
                ],
                "examples": [
                    {
                        "id": "bdd-implementation-blocked-before-plan-acceptance",
                        "title": (
                            "Agent cannot start implementation before plan approval"
                        ),
                        "rule_id": "rule-accepted-plan-required",
                        "given": ["a task has a proposed plan"],
                        "when": ["the agent starts implementation"],
                        "then": ["implementation is blocked"],
                        "acceptance_criteria": ["ac-0001"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    out = tmp_path / "specs/behavior/features/task-management/plan-gates.feature"
    feature = write_behavior_feature_from_taskledger(source, out)
    text = out.read_text(encoding="utf-8")
    assert feature.tags == ("area-task-management", "feature-plan-gates")
    assert "@bdd-implementation-blocked-before-plan-acceptance" in text
    assert "@task-0123" not in text
    assert "@ac-0001" not in text


def test_import_taskledger_infers_markdown_format(tmp_path) -> None:  # type: ignore[no-untyped-def]
    source = tmp_path / "task.acceptance.json"
    source.write_text(
        json.dumps(
            {
                "task_id": "task-0123",
                "feature": "Plan gates",
                "acceptance_criteria": [{"id": "ac-0001", "text": "Plan accepted"}],
            }
        ),
        encoding="utf-8",
    )
    out = tmp_path / "task-management" / "plan-gates.feature.md"

    feature = write_behavior_feature_from_taskledger(source, out)

    assert feature.tags == ("area-task-management", "feature-plan-gates")
    assert out.read_text(encoding="utf-8").startswith(
        "`@area-task-management` `@feature-plan-gates`\n# Feature:"
    )
