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
from pathlib import Path

from specweave.reports.model import ScenarioResult

_TAG_TOKEN_RE = re.compile(r"@(\S+)")


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


def _collect_property_values(testcase: ET.Element) -> str:
    parts: list[str] = []
    for prop in testcase.iterfind("properties/property"):
        value = prop.get("value")
        if isinstance(value, str):
            parts.append(value)
    return " ".join(parts)


def parse_junit_xml(path: str | Path) -> tuple[ScenarioResult, ...]:
    """Parse a JUnit XML report at *path* into scenario results."""
    tree = ET.parse(Path(path))
    root = tree.getroot()
    evidence = (str(path),)

    results: list[ScenarioResult] = []
    # testcases may live directly under testsuites/testsuite, or nested deeper.
    for testcase in root.iter("testcase"):
        name = testcase.get("name", "")
        classname = testcase.get("classname", "")
        feature = classname.rsplit(".", 1)[-1] if classname else ""
        results.append(
            ScenarioResult(
                name=name,
                status=_status_of(testcase),
                tags=_tags_from_text(
                    name, classname, _collect_property_values(testcase)
                ),
                feature=feature,
                rule=None,
                evidence=evidence,
            )
        )
    return tuple(results)
