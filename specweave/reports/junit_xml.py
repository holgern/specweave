"""Parse JUnit XML reports into :class:`ScenarioResult` lists.

JUnit XML has no native per-scenario status beyond pass/fail/error/skipped, so
the status vocabulary here is limited to ``passed``, ``failed``, and
``skipped``. BDD tags are recovered by scanning ``classname``, ``name``, and
``<property>`` values for ``@token`` patterns.

Status mapping:

- a ``<failure>`` or ``<error>`` child -> ``failed``
- a ``<skipped>`` child -> ``skipped``
- otherwise -> ``passed``
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from specweave.reports.model import ScenarioResult

_TAG_TOKEN_RE = re.compile(r"@(\S+)")


@dataclass(frozen=True)
class PytestJunitCase:
    """A single testcase row parsed from pytest's JUnit XML."""

    name: str
    classname: str
    status: str
    test_file: str
    nodeid: str
    properties: dict[str, str]
    time: str


def _tags_from_text(*texts: str | None) -> tuple[str, ...]:
    tags: list[str] = []
    for text in texts:
        if not text:
            continue
        tags.extend(m.group(1) for m in _TAG_TOKEN_RE.finditer(text))
    return tuple(tags)


def _status_of(testcase: ET.Element) -> str:
    child_tags = {child.tag for child in testcase}
    if "failure" in child_tags or "error" in child_tags:
        return "failed"
    if "skipped" in child_tags:
        return "skipped"
    return "passed"


def _collect_properties(testcase: ET.Element) -> dict[str, str]:
    properties: dict[str, str] = {}
    for prop in testcase.iterfind("properties/property"):
        name = prop.get("name")
        value = prop.get("value")
        if isinstance(name, str) and isinstance(value, str):
            properties[name] = value
    return properties


def _collect_property_values(testcase: ET.Element) -> str:
    return " ".join(_collect_properties(testcase).values())


def _nodeid_of(testcase: ET.Element, properties: dict[str, str]) -> str:
    nodeid = properties.get("nodeid")
    if isinstance(nodeid, str) and nodeid:
        return nodeid
    name = testcase.get("name", "")
    if "::" in name:
        return name
    file_path = testcase.get("file", "")
    if file_path and name:
        return f"{file_path}::{name}"
    return name


def parse_pytest_junit_cases(path: str | Path) -> tuple[PytestJunitCase, ...]:
    """Parse JUnit XML at *path* into pytest-oriented testcase records."""

    tree = ET.parse(Path(path))
    root = tree.getroot()
    cases: list[PytestJunitCase] = []
    for testcase in root.iter("testcase"):
        properties = _collect_properties(testcase)
        cases.append(
            PytestJunitCase(
                name=testcase.get("name", ""),
                classname=testcase.get("classname", ""),
                status=_status_of(testcase),
                test_file=testcase.get("file", ""),
                nodeid=_nodeid_of(testcase, properties),
                properties=properties,
                time=testcase.get("time", ""),
            )
        )
    return tuple(cases)


def _parse_duration_ms(time_str: str) -> int | None:
    """Convert a JUnit ``time`` attribute (seconds) to milliseconds."""
    if not time_str:
        return None
    try:
        return int(float(time_str) * 1000)
    except (ValueError, TypeError):
        return None


def parse_junit_xml(path: str | Path) -> tuple[ScenarioResult, ...]:
    """Parse a JUnit XML report at *path* into scenario results."""
    evidence = (str(path),)

    results: list[ScenarioResult] = []
    for case in parse_pytest_junit_cases(path):
        feature = case.properties.get("specweave_feature", "")
        scenario_name = case.properties.get("specweave_scenario", case.name)
        duration_ms = _parse_duration_ms(case.time)
        results.append(
            ScenarioResult(
                name=scenario_name,
                status=case.status,
                tags=_tags_from_text(
                    case.name,
                    case.classname,
                    " ".join(case.properties.values()),
                ),
                feature=feature or case.classname.rsplit(".", 1)[-1],
                rule=case.properties.get("specweave_rule"),
                evidence=evidence,
                test_file=case.test_file,
                nodeid=case.nodeid,
                duration_ms=duration_ms,
            )
        )
    return tuple(results)
