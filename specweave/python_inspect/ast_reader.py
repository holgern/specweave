"""Read pytest-style tests from Python AST."""

from __future__ import annotations

import ast
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from specweave.gherkin.model import Scenario, Step
from specweave.python_inspect.assertions import describe_assert

_SPECWEAVE_COMMENT_RE = re.compile(
    r"#\s*specweave:\s*(feature|scenario)\s*=\s*(.+?)\s*$"
)


@dataclass(frozen=True)
class SpecweaveTestMapping:
    """Behavior mapping recovered from a plain pytest test function."""

    function_name: str
    test_file: str
    nodeid: str
    feature: str
    scenario: str
    line: int
    source: str


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


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _module_string_constants(tree: ast.Module) -> dict[str, str]:
    constants: dict[str, str] = {}
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            constants[node.targets[0].id] = node.value.value
    return constants


def _resolve_string(node: ast.AST, constants: dict[str, str]) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return constants.get(node.id)
    return None


def _dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _dotted_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return None


def _marker_mapping(
    node: ast.FunctionDef, constants: dict[str, str]
) -> tuple[str, str] | None:
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call):
            continue
        name = _dotted_name(decorator.func)
        if not name or not name.endswith("specweave"):
            continue
        kwargs = {kw.arg: kw.value for kw in decorator.keywords if kw.arg}
        feature = _resolve_string(kwargs.get("feature", ast.Constant(None)), constants)
        scenario = _resolve_string(
            kwargs.get("scenario", ast.Constant(None)), constants
        )
        if feature and scenario:
            return feature, scenario
    return None


def _comment_mappings(source: str) -> dict[int, tuple[str, str]]:
    mappings: dict[int, tuple[str, str]] = {}
    lines = source.splitlines()
    index = 0
    while index < len(lines):
        values: dict[str, str] = {}
        start = index
        while index < len(lines):
            match = _SPECWEAVE_COMMENT_RE.match(lines[index].strip())
            if match is None:
                break
            values[match.group(1)] = match.group(2).strip()
            index += 1
        if values:
            while index < len(lines) and lines[index].lstrip().startswith("@"):
                index += 1
            if index < len(lines):
                stripped = lines[index].lstrip()
                if stripped.startswith("def test_") or stripped.startswith(
                    "async def test_"
                ):
                    feature = values.get("feature")
                    scenario = values.get("scenario")
                    if feature and scenario:
                        mappings[index + 1] = (feature, scenario)
                    index += 1
                    continue
            index = max(index, start + 1)
            continue
        index += 1
    return mappings


def _docstring_mapping(node: ast.FunctionDef) -> tuple[str, str] | None:
    docstring = ast.get_docstring(node, clean=False)
    if not docstring:
        return None
    feature_match = re.search(r"specs/behavior/features/[^\s\"']+\.feature", docstring)
    scenario_match = re.search(r"@bdd-[A-Za-z0-9][A-Za-z0-9_-]*", docstring)
    if feature_match and scenario_match:
        return feature_match.group(0), scenario_match.group(0)
    return None


def discover_specweave_tests(path: Path) -> list[SpecweaveTestMapping]:
    """Discover plain-pytest SpecWeave mappings from *path*."""

    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    constants = _module_string_constants(tree)
    comment_mappings = _comment_mappings(source)
    test_file = _display_path(path)

    mappings: list[SpecweaveTestMapping] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef) or not node.name.startswith("test_"):
            continue
        mapping = _marker_mapping(node, constants)
        source_name = "marker"
        if mapping is None:
            mapping = comment_mappings.get(node.lineno)
            source_name = "comment"
        if mapping is None:
            mapping = _docstring_mapping(node)
            source_name = "docstring"
        if mapping is None:
            continue
        feature, scenario = mapping
        mappings.append(
            SpecweaveTestMapping(
                function_name=node.name,
                test_file=test_file,
                nodeid=f"{test_file}::{node.name}",
                feature=feature,
                scenario=scenario,
                line=node.lineno,
                source=source_name,
            )
        )
    return mappings


def collect_specweave_tests(paths: Iterable[Path]) -> list[SpecweaveTestMapping]:
    """Collect SpecWeave mappings from multiple pytest files."""

    mappings: list[SpecweaveTestMapping] = []
    for path in paths:
        mappings.extend(discover_specweave_tests(path))
    return mappings


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


def extract_module_docstring(path: Path) -> str:
    """Extract the module-level docstring from a Python file."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    docstring = ast.get_docstring(tree, clean=False)
    return docstring or ""


def extract_class_rules(path: Path) -> list[tuple[str, list[ast.FunctionDef]]]:
    """Extract test class names as rule candidates with their test methods.

    Returns a list of (class_title, test_methods) tuples.
    """
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    rules: list[tuple[str, list[ast.FunctionDef]]] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            class_title = node.name
            if class_title.startswith("Test"):
                class_title = class_title[4:]
            class_title = class_title.replace("_", " ").strip().title()
            methods = [
                child
                for child in node.body
                if isinstance(child, ast.FunctionDef) and child.name.startswith("test_")
            ]
            if methods:
                rules.append((class_title, methods))
    return rules


__all__ = [
    "SpecweaveTestMapping",
    "collect_specweave_tests",
    "discover_specweave_tests",
    "extract_test_scenarios",
    "extract_module_docstring",
    "extract_class_rules",
]
