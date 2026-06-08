"""Tests for JUnit XML report normalization."""

from __future__ import annotations

from specweave.reports.junit_xml import parse_junit_xml
from specweave.reports.normalize import normalize_report

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


def _write(tmp_path, name, text):  # type: ignore[no-untyped-def]
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_parse_junit_pass_fail_skip(tmp_path) -> None:  # type: ignore[no-untyped-def]
    path = _write(tmp_path, "junit.xml", _JUNIT_PASS_FAIL_SKIP)
    results = parse_junit_xml(path)
    assert [r.status for r in results] == ["passed", "failed", "skipped"]
    assert results[0].tags == ("bdd-0001", "ac-0001")
    assert results[1].tags == ("bdd-0002", "ac-0001")
    assert results[2].tags == ("bdd-0003", "ac-0002")


def test_junit_error_counts_as_failed(tmp_path) -> None:  # type: ignore[no-untyped-def]
    path = _write(tmp_path, "junit.xml", _JUNIT_ERROR)
    results = parse_junit_xml(path)
    assert results[0].status == "failed"
    assert results[0].tags == ("bdd-0009", "ac-0001")


def test_junit_tags_from_properties(tmp_path) -> None:  # type: ignore[no-untyped-def]
    path = _write(tmp_path, "junit.xml", _JUNIT_PROPERTIES)
    results = parse_junit_xml(path)
    assert results[0].tags == ("bdd-0005", "ac-0003")


def test_normalize_junit_skipped_fails_closed(tmp_path) -> None:  # type: ignore[no-untyped-def]
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
