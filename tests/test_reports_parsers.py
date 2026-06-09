"""Tests for report format parsers (JUnit XML and Cucumber JSON)."""

from __future__ import annotations

import json

from specweave.reports.junit_xml import parse_junit_xml, parse_pytest_junit_cases
from specweave.reports.normalize import normalize_report, to_normalized_dict

# -- helpers --


def _write(tmp_path, name, text):  # type: ignore[no-untyped-def]
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def _cucumber_report_path(tmp_path, payload):  # type: ignore[no-untyped-def]
    path = tmp_path / "cucumber.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


# -- JUnit XML fixtures --

_JUNIT_PASS_FAIL_SKIP = """\
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="bdd" tests="3">
    <testcase classname="features.task_0123" name="@bdd-0001 @ac-0001 passes"/>
    <testcase classname="features.task_0123" name="@bdd-0002 @ac-0001 fails">
      <failure message="boom">assert False</failure>
    </testcase>
    <testcase classname="features.task_0123" name="@bdd-0003 @ac-0002 skipped">
      <skipped/>
    </testcase>
  </testsuite>
</testsuites>
"""

_JUNIT_ERROR = """\
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="bdd" tests="1">
    <testcase classname="features.task_0123" name="@bdd-0009 @ac-0001 errors">
      <error message="exc">traceback</error>
    </testcase>
  </testsuite>
</testsuites>
"""

_JUNIT_PROPERTIES = """\
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="bdd" tests="1">
    <testcase classname="features.task_0123" name="scenario via properties">
      <properties>
        <property name="tags" value="@bdd-0005 @ac-0003"/>
      </properties>
    </testcase>
  </testsuite>
</testsuites>
"""


# -- JUnit XML parser tests --


# specweave: feature=specs/behavior/features/reports/parsers.feature
# specweave: scenario=@bdd-junit-parse-cases
def test_parse_junit_pass_fail_skip(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Parser extracts test cases from JUnit XML."""
    path = _write(tmp_path, "junit.xml", _JUNIT_PASS_FAIL_SKIP)
    results = parse_junit_xml(path)
    assert [r.status for r in results] == ["passed", "failed", "skipped"]
    assert results[0].tags == ("bdd-0001", "ac-0001")
    assert results[1].tags == ("bdd-0002", "ac-0001")
    assert results[2].tags == ("bdd-0003", "ac-0002")


# specweave: feature=specs/behavior/features/reports/parsers.feature
# specweave: scenario=@bdd-junit-parse-statuses
def test_junit_error_counts_as_failed(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Parser maps JUnit statuses correctly."""
    path = _write(tmp_path, "junit.xml", _JUNIT_ERROR)
    results = parse_junit_xml(path)
    assert results[0].status == "failed"
    assert results[0].tags == ("bdd-0009", "ac-0001")


def test_junit_tags_from_properties(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Parser extracts test cases from JUnit XML via properties."""
    path = _write(tmp_path, "junit.xml", _JUNIT_PROPERTIES)
    results = parse_junit_xml(path)
    assert results[0].tags == ("bdd-0005", "ac-0003")


def test_normalize_junit_skipped_fails_closed(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Parser maps JUnit statuses correctly (skipped fails closed)."""
    path = _write(tmp_path, "junit.xml", _JUNIT_PASS_FAIL_SKIP)
    report = normalize_report(path, "junit-xml")
    assert report.status == "failed"
    assert report.runner == "junit-xml"
    assert report.passed == 1
    assert report.failed == 1
    assert report.skipped == 1
    # ac-0001 has a passing scenario (bdd-0001) but also a failing one
    # (bdd-0002), so the criterion must fail.
    criterion = next(c for c in report.criteria if c.criterion_id == "ac-0001")
    assert criterion.status == "failed"
    assert set(criterion.scenario_ids) == {"bdd-0001", "bdd-0002"}


def test_normalize_junit_all_passed(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Parser maps JUnit statuses correctly (all passed)."""
    text = """\
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="bdd" tests="1">
    <testcase classname="features.task_0123" name="@bdd-0001 @ac-0001 ok"/>
  </testsuite>
</testsuites>
"""
    path = _write(tmp_path, "junit.xml", text)
    report = normalize_report(path, "junit-xml")
    assert report.status == "passed"
    assert report.criteria[0].status == "passed"


def test_parse_pytest_junit_case_nodeid_and_file(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Parser extracts test cases from JUnit XML with nodeid and file."""
    text = """\
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="pytest" tests="1">
    <testcase classname="tests.test_sync_git_sync"
              file="tests/test_sync_git_sync.py"
              name="test_imports_pytest_report"/>
  </testsuite>
</testsuites>
"""
    path = _write(tmp_path, "junit.xml", text)
    cases = parse_pytest_junit_cases(path)
    assert cases[0].test_file == "tests/test_sync_git_sync.py"
    assert cases[0].nodeid == "tests/test_sync_git_sync.py::test_imports_pytest_report"


def test_parse_junit_preserves_nodeid_and_test_file(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Parser extracts test cases from JUnit XML with preserved nodeid."""
    text = """\
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="pytest" tests="1">
    <testcase classname="tests.test_sync_git_sync"
              file="tests/test_sync_git_sync.py"
              name="test_imports_pytest_report">
      <properties>
        <property
          name="specweave_feature"
          value="specs/behavior/features/sync/git-sync.feature"
        />
        <property name="specweave_scenario" value="@bdd-imports-pytest-report"/>
      </properties>
    </testcase>
  </testsuite>
</testsuites>
"""
    path = _write(tmp_path, "junit.xml", text)
    results = parse_junit_xml(path)
    assert results[0].feature == "specs/behavior/features/sync/git-sync.feature"
    assert results[0].name == "@bdd-imports-pytest-report"
    assert results[0].test_file == "tests/test_sync_git_sync.py"
    assert (
        results[0].nodeid == "tests/test_sync_git_sync.py::test_imports_pytest_report"
    )


# -- Cucumber JSON parser tests --


# specweave: feature=specs/behavior/features/reports/parsers.feature
# specweave: scenario=@bdd-cucumber-parse-scenarios
def test_cucumber_json_passing_scenario(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Parser extracts scenarios from Cucumber JSON."""
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
    """Parser extracts scenarios from Cucumber JSON (skipped fails closed)."""
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
    """Parser extracts scenarios from Cucumber JSON (allow_skipped)."""
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
    """Parser extracts scenarios from Cucumber JSON (failed step)."""
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


# specweave: feature=specs/behavior/features/reports/parsers.feature
# specweave: scenario=@bdd-cucumber-parse-tags
def test_behear_string_tags_and_inline_status(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Parser extracts tags from Cucumber scenarios (behave style)."""
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
    """Parser extracts scenarios from Cucumber JSON (normalized dict shape)."""
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
    """Parser rejects unsupported formats."""
    path = tmp_path / "x.json"
    path.write_text("[]", encoding="utf-8")
    try:
        normalize_report(path, "csv")
    except ValueError as exc:
        assert "csv" in str(exc)
    else:  # pragma: no cover - defensive
        raise AssertionError("expected ValueError for unsupported format")


# specweave: feature=specs/behavior/features/reports/parsers.feature
# specweave: scenario=@bdd-junit-parse-duration
def test_junit_parse_duration(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Parser extracts test duration from JUnit XML."""
    text = """\
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="bdd" tests="1">
    <testcase classname="features.task_0123" name="@bdd-0001 @ac-0001 ok"
              time="0.123"/>
  </testsuite>
</testsuites>
"""
    path = _write(tmp_path, "junit.xml", text)
    results = parse_junit_xml(path)
    assert results[0].duration_ms == 123
