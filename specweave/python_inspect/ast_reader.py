"""Read pytest-style tests from Python AST."""

from __future__ import annotations

import ast
from pathlib import Path

from specweave.gherkin.model import Scenario, Step
from specweave.python_inspect.assertions import describe_assert


def extract_test_scenarios(path: Path) -> list[Scenario]:
    """Parse a Python file and extract test functions as candidate Scenarios.

    Detects ``def test_*`` functions and maps their ``assert`` statements
    into candidate ``Then`` clauses.
    """
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    scenarios: list[Scenario] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            scenario = _function_to_scenario(node)
            if scenario:
                scenarios.append(scenario)

    return scenarios


def _function_to_scenario(node: ast.FunctionDef) -> Scenario | None:
    """Convert a single test function to a Scenario."""
    title = _function_name_to_title(node.name)
    steps: list[Step] = []

    # Add a When step from the function name
    steps.append(Step(keyword="When", text=_scenario_when_text(node.name)))
    has_assertion = False

    for child in ast.walk(node):
        if isinstance(child, ast.Assert):
            clause = describe_assert(child)
            if clause:
                steps.append(Step(keyword="Then", text=clause))
                has_assertion = True

    if not has_assertion:
        return None

    return Scenario(title=title, steps=tuple(steps))


def _function_name_to_title(name: str) -> str:
    """Convert ``test_rejects_invalid_password`` to ``Rejects invalid password``."""
    # Remove test_ prefix
    if name.startswith("test_"):
        name = name[5:]
    # Replace underscores with spaces and title-case
    return name.replace("_", " ").strip().title()


def _scenario_when_text(name: str) -> str:
    """Derive a When clause from the test function name."""
    # Remove test_ prefix
    if name.startswith("test_"):
        name = name[5:]
    readable = name.replace("_", " ").strip()
    return f"{readable} is executed"
