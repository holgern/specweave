"""Tests for Cucumber/Behave JSON report normalization."""

from __future__ import annotations

import json

from specweave.reports.normalize import normalize_report, to_normalized_dict


def _cucumber_report_path(tmp_path, payload):  # type: ignore[no-untyped-def]
    path = tmp_path / "cucumber.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_cucumber_json_passing_scenario(tmp_path) -> None:  # type: ignore[no-untyped-def]
    payload = [
        {
            "name": "Task lifecycle gates",
            "tags": [{"name": "@task-0123"}],
            "elements": [
                {
                    "name": (
                        "Agent cannot start implementation without an accepted plan"
                    ),
                    "rule": "Implementation requires an accepted plan",
                    "tags": [
                        {"name": "@bdd-0001"},
                        {"name": "@task-0123"},
                        {"name": "@rule-0001"},
                        {"name": "@ac-0001"},
                    ],
                    "steps": [
                        {"result": {"status": "passed", "duration": 12_000_000}},
                        {"result": {"status": "passed", "duration": 5_000_000}},
                        {"result": {"status": "passed", "duration": 3_000_000}},
                    ],
                }
            ],
        }
    ]
    path = _cucumber_report_path(tmp_path, payload)
    report = normalize_report(
        path, "cucumber-json", command=["behave", "tests/bdd/features"]
    )
    assert report.status == "passed"
    assert report.scenarios == 1
    assert report.passed == 1
    assert report.failed == 0
    result = report.results[0]
    assert result.status == "passed"
    assert result.tags == ("bdd-0001", "task-0123", "rule-0001", "ac-0001")
    assert result.rule == "Implementation requires an accepted plan"
    assert result.duration_ms == 12
    assert report.criteria[0].criterion_id == "ac-0001"
    assert report.criteria[0].status == "passed"
    assert report.criteria[0].scenario_ids == ("bdd-0001",)
    assert report.command == ("behave", "tests/bdd/features")
    assert report.source_report == str(path)


def test_skipped_fails_closed_by_default(tmp_path) -> None:  # type: ignore[no-untyped-def]
    payload = [
        {
            "name": "F",
            "elements": [
                {
                    "name": "Skipped scenario",
                    "tags": [{"name": "@bdd-0001"}, {"name": "@ac-0001"}],
                    "steps": [{"result": {"status": "skipped"}}],
                }
            ],
        }
    ]
    path = _cucumber_report_path(tmp_path, payload)
    report = normalize_report(path, "cucumber-json")
    assert report.status == "failed"
    assert report.results[0].status == "skipped"  # native status preserved
    assert report.skipped == 1


def test_allow_skipped_does_not_fail(tmp_path) -> None:  # type: ignore[no-untyped-def]
    payload = [
        {
            "name": "F",
            "elements": [
                {
                    "name": "Skipped scenario",
                    "tags": [{"name": "@bdd-0001"}, {"name": "@ac-0001"}],
                    "steps": [{"result": {"status": "skipped"}}],
                }
            ],
        }
    ]
    path = _cucumber_report_path(tmp_path, payload)
    report = normalize_report(path, "cucumber-json", allow_skipped=True)
    assert report.status == "passed"
    assert report.results[0].status == "skipped"


def test_failed_step_fails_scenario_and_report(tmp_path) -> None:  # type: ignore[no-untyped-def]
    payload = [
        {
            "name": "F",
            "elements": [
                {
                    "name": "Mixed",
                    "tags": [{"name": "@bdd-0001"}, {"name": "@ac-0001"}],
                    "steps": [
                        {"result": {"status": "passed"}},
                        {"result": {"status": "failed"}},
                        {"result": {"status": "skipped"}},  # skipped due to failure
                    ],
                }
            ],
        }
    ]
    path = _cucumber_report_path(tmp_path, payload)
    report = normalize_report(path, "cucumber-json")
    assert report.results[0].status == "failed"
    assert report.status == "failed"
    assert report.criteria[0].status == "failed"


def test_behear_string_tags_and_inline_status(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """behave json uses string tags and step['status'] rather than result."""
    payload = [
        {
            "name": "F",
            "elements": [
                {
                    "name": "Behave style",
                    "tags": ["@bdd-0001", "@ac-0001"],
                    "steps": [
                        {"status": "passed"},
                        {"status": "passed"},
                    ],
                }
            ],
        }
    ]
    path = _cucumber_report_path(tmp_path, payload)
    report = normalize_report(path, "cucumber-json")
    assert report.results[0].status == "passed"
    assert report.results[0].tags == ("bdd-0001", "ac-0001")


def test_normalized_dict_shape(tmp_path) -> None:  # type: ignore[no-untyped-def]
    payload = [
        {
            "name": "F",
            "elements": [
                {
                    "name": "S",
                    "tags": [{"name": "@bdd-0001"}, {"name": "@ac-0001"}],
                    "steps": [{"result": {"status": "passed", "duration": 1_000_000}}],
                }
            ],
        }
    ]
    path = _cucumber_report_path(tmp_path, payload)
    report = normalize_report(path, "cucumber-json")
    data = to_normalized_dict(report)
    assert data["schema_version"] == 2
    assert data["generated_by"] == "specweave"
    assert data["runner"] == "cucumber-json"
    assert data["status"] == "passed"
    assert data["results"][0]["bdd_ids"] == ["bdd-0001"]
    assert data["results"][0]["acceptance_criteria"] == ["ac-0001"]
    assert data["results"][0]["duration_ms"] == 1
    assert data["criteria"][0]["scenario_ids"] == ["bdd-0001"]


def test_unsupported_format_raises(tmp_path) -> None:  # type: ignore[no-untyped-def]
    path = tmp_path / "x.json"
    path.write_text("[]", encoding="utf-8")
    try:
        normalize_report(path, "csv")
    except ValueError as exc:
        assert "csv" in str(exc)
    else:  # pragma: no cover - defensive
        raise AssertionError("expected ValueError for unsupported format")
