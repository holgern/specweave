"""Read pytest-style tests from Python AST."""

from __future__ import annotations

import ast
import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

from specweave.gherkin.model import Scenario, Step
from specweave.python_inspect.assertions import describe_assert

_SPECWEAVE_COMMENT_RE = re.compile(r"#\s*(?:specweave|sw):\s*(.*?)\s*$")
_SPECWEAVE_BLOCK_RE = re.compile(
    r"#\s*(feature|scenario|spec|requirement|f|s|unmapped|u)\s*:\s*(.*?)\s*$"
)
_SPECWEAVE_FEATURE_RE = re.compile(
    r"specs/behavio(?:r|ur)/features/[^\s\"']+\.feature(?:\.md)?"
)
_SPECWEAVE_SPEC_RE = re.compile(r"specs/specifications/[^\s\"']+\.spec\.md")
_SPECWEAVE_REQUIREMENT_RE = re.compile(
    r"\b(?:REQ|INV|IF|DATA|NFR|NGOAL|RISK|OPEN)-[A-Z0-9-]+\b"
)
_SPECWEAVE_PAIR_RE = re.compile(
    r"(?P<key>feature|scenario|spec|requirement|f|s|unmapped|u)\s*=\s*"
    r"(?P<value>.*?)(?=(?:\s+(?:feature|scenario|spec|requirement|f|s|unmapped|u)\s*=)|$)"
)


@dataclass(frozen=True)
class SpecweaveTestMapping:
    """Behavior mapping recovered from a plain pytest test function."""

    function_name: str
    test_file: str
    nodeid: str
    line: int
    source: str
    feature: str | None = None
    scenario: str | None = None
    spec: str | None = None
    requirement: str | None = None
    diagnostics: tuple[str, ...] = ()


@dataclass(frozen=True)
class PytestTestItem:
    """Pytest test function discovered from a Python module."""

    function_name: str
    test_file: str
    nodeid: str
    line: int
    insert_line: int
    indent: str
    class_name: str | None = None
    unmapped_reason: str | None = None
    unmapped_source: str | None = None


def extract_test_scenarios(path: Path) -> list[Scenario]:
    """Parse a Python file and extract test functions as candidate Scenarios.

    Detects ``def test_*`` functions and maps their ``assert`` statements
    into candidate ``Then`` clauses.
    """
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    scenarios: list[Scenario] = []

    for node in ast.walk(tree):
        if isinstance(
            node, (ast.FunctionDef, ast.AsyncFunctionDef)
        ) and node.name.startswith("test_"):
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


def _resolve_project_relative(
    path_text: str, reference_path: Path | None
) -> Path | None:
    candidate = Path(path_text)
    if candidate.exists():
        return candidate
    if candidate.is_absolute() or reference_path is None:
        return None
    for ancestor in (reference_path.parent, *reference_path.parents):
        resolved = ancestor / candidate
        if resolved.exists():
            return resolved
    return None


def _normalize_feature_mapping(
    feature: str, *, reference_path: Path | None = None
) -> str:
    candidate = Path(feature)
    if candidate.exists():
        return _display_path(candidate)
    resolved = _resolve_project_relative(feature, reference_path)
    if resolved is not None:
        return _display_path(resolved)
    return feature


def _normalize_spec_mapping(spec: str, *, reference_path: Path | None = None) -> str:
    candidate = Path(spec)
    if candidate.exists():
        return _display_path(candidate)
    resolved = _resolve_project_relative(spec, reference_path)
    if resolved is not None:
        return _display_path(resolved)
    return spec


def _mapping_entries(
    *,
    feature: str | None = None,
    scenario: str | None = None,
    spec: str | None = None,
    requirement: str | None = None,
    reference_path: Path | None = None,
) -> tuple[list[dict[str, str]], tuple[str, ...]]:
    entries: list[dict[str, str]] = []
    diagnostics: list[str] = []
    if feature is not None or scenario is not None:
        if feature and scenario:
            entries.append(
                {
                    "feature": _normalize_feature_mapping(
                        feature, reference_path=reference_path
                    ),
                    "scenario": scenario,
                }
            )
        else:
            diagnostics.append(
                "Incomplete behaviour mapping requires both feature and scenario."
            )
    if spec is not None or requirement is not None:
        if spec and requirement:
            entries.append(
                {
                    "spec": _normalize_spec_mapping(
                        spec, reference_path=reference_path
                    ),
                    "requirement": requirement,
                }
            )
        else:
            diagnostics.append(
                "Incomplete specifications mapping requires both spec and requirement."
            )
    return entries, tuple(diagnostics)


def _marker_mappings(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    constants: dict[str, str],
    *,
    source_path: Path,
) -> tuple[list[dict[str, str]], tuple[str, ...]]:
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
        spec = _resolve_string(kwargs.get("spec", ast.Constant(None)), constants)
        requirement = _resolve_string(
            kwargs.get("requirement", ast.Constant(None)), constants
        )
        return _mapping_entries(
            feature=feature,
            scenario=scenario,
            spec=spec,
            requirement=requirement,
            reference_path=source_path,
        )
    return [], ()


def _canonical_comment_key(key: str) -> str:
    return {"f": "feature", "s": "scenario", "u": "unmapped"}.get(key, key)


def _inline_comment_values(line: str) -> dict[str, str]:
    values: dict[str, str] = {}
    match = _SPECWEAVE_COMMENT_RE.match(line.strip())
    if match is None:
        return values
    for pair in _SPECWEAVE_PAIR_RE.finditer(match.group(1).strip()):
        values[_canonical_comment_key(pair.group("key"))] = pair.group("value").strip()
    return values


def _comment_values(lines: list[str], index: int) -> tuple[dict[str, str], int]:
    values: dict[str, str] = {}
    inline_values = _inline_comment_values(lines[index])
    if inline_values:
        while index < len(lines):
            current_values = _inline_comment_values(lines[index])
            if not current_values:
                break
            values.update(current_values)
            index += 1
        return values, index

    stripped = lines[index].strip()
    if stripped not in {"# specweave:", "# sw:"}:
        return values, index
    index += 1
    while index < len(lines):
        match = _SPECWEAVE_BLOCK_RE.match(lines[index].strip())
        if match is None:
            break
        values[_canonical_comment_key(match.group(1))] = match.group(2).strip()
        index += 1
    return values, index


def _comment_metadata(source: str) -> dict[int, dict[str, str]]:
    metadata: dict[int, dict[str, str]] = {}
    lines = source.splitlines()
    index = 0
    while index < len(lines):
        start = index
        values, index = _comment_values(lines, index)
        if values:
            while index < len(lines) and lines[index].lstrip().startswith("@"):
                index += 1
            if index < len(lines):
                stripped = lines[index].lstrip()
                if stripped.startswith("def test_") or stripped.startswith(
                    "async def test_"
                ):
                    metadata[index + 1] = dict(values)
                    index += 1
                    continue
            index = max(index, start + 1)
            continue
        index += 1
    return metadata


def _comment_mappings(source: str) -> dict[int, dict[str, str]]:
    mappings: dict[int, dict[str, str]] = {}
    for line, values in _comment_metadata(source).items():
        if values:
            mappings[line] = dict(values)
    return mappings


def _docstring_mapping(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    *,
    source_path: Path,
) -> tuple[list[dict[str, str]], tuple[str, ...]]:
    docstring = ast.get_docstring(node, clean=False)
    if not docstring:
        return [], ()
    feature_match = _SPECWEAVE_FEATURE_RE.search(docstring)
    scenario_match = re.search(r"@bdd-[A-Za-z0-9][A-Za-z0-9_-]*", docstring)
    spec_match = _SPECWEAVE_SPEC_RE.search(docstring)
    requirement_match = _SPECWEAVE_REQUIREMENT_RE.search(docstring)
    return _mapping_entries(
        feature=feature_match.group(0) if feature_match else None,
        scenario=scenario_match.group(0) if scenario_match else None,
        spec=spec_match.group(0) if spec_match else None,
        requirement=requirement_match.group(0) if requirement_match else None,
        reference_path=source_path,
    )


def _pytest_test_functions(
    tree: ast.Module,
) -> Iterator[tuple[ast.FunctionDef | ast.AsyncFunctionDef, str | None]]:
    """Yield pytest tests with the class segment used in their node IDs."""

    for node in tree.body:
        if isinstance(
            node, (ast.FunctionDef, ast.AsyncFunctionDef)
        ) and node.name.startswith("test_"):
            yield node, None
            continue
        if not isinstance(node, ast.ClassDef) or not node.name.startswith("Test"):
            continue
        for child in node.body:
            if isinstance(
                child, (ast.FunctionDef, ast.AsyncFunctionDef)
            ) and child.name.startswith("test_"):
                yield child, node.name


def discover_specweave_tests(path: Path) -> list[SpecweaveTestMapping]:
    """Discover plain-pytest SpecWeave mappings from *path*."""

    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    constants = _module_string_constants(tree)
    comment_mappings = _comment_mappings(source)
    test_file = _display_path(path)

    mappings: list[SpecweaveTestMapping] = []

    for node, class_name in _pytest_test_functions(tree):
        mapping_entries, diagnostics = _marker_mappings(
            node, constants, source_path=path
        )
        source_name = "marker"
        if not mapping_entries and not diagnostics:
            values = comment_mappings.get(node.lineno)
            if values is not None:
                mapping_entries, diagnostics = _mapping_entries(
                    feature=values.get("feature"),
                    scenario=values.get("scenario"),
                    spec=values.get("spec"),
                    requirement=values.get("requirement"),
                    reference_path=path,
                )
            source_name = "comment"
        if not mapping_entries and not diagnostics:
            mapping_entries, diagnostics = _docstring_mapping(node, source_path=path)
            source_name = "docstring"
        if not mapping_entries:
            continue
        qualname = f"{class_name}::{node.name}" if class_name else node.name
        for entry in mapping_entries:
            mappings.append(
                SpecweaveTestMapping(
                    function_name=node.name,
                    test_file=test_file,
                    nodeid=f"{test_file}::{qualname}",
                    feature=entry.get("feature"),
                    scenario=entry.get("scenario"),
                    spec=entry.get("spec"),
                    requirement=entry.get("requirement"),
                    line=node.lineno,
                    source=source_name,
                    diagnostics=diagnostics,
                )
            )
    return mappings


def _pytest_test_items(
    tree: ast.Module, test_file: str, source: str
) -> list[PytestTestItem]:
    lines = source.splitlines()
    comment_metadata = _comment_metadata(source)
    items: list[PytestTestItem] = []

    for node, class_name in _pytest_test_functions(tree):
        decorator_lines = [decorator.lineno for decorator in node.decorator_list]
        insert_line = min(decorator_lines, default=node.lineno)
        source_line = lines[node.lineno - 1] if node.lineno <= len(lines) else ""
        indent = source_line[: len(source_line) - len(source_line.lstrip())]
        qualname = f"{class_name}::{node.name}" if class_name else node.name
        metadata = comment_metadata.get(node.lineno, {})
        unmapped_reason = metadata.get("unmapped")
        if unmapped_reason is not None:
            unmapped_reason = unmapped_reason.strip() or "intentional-unmapped"
        items.append(
            PytestTestItem(
                function_name=node.name,
                test_file=test_file,
                nodeid=f"{test_file}::{qualname}",
                line=node.lineno,
                insert_line=insert_line,
                indent=indent,
                class_name=class_name,
                unmapped_reason=unmapped_reason,
                unmapped_source="comment" if unmapped_reason else None,
            )
        )
    return sorted(items, key=lambda item: item.line)


def discover_pytest_tests(path: Path) -> list[PytestTestItem]:
    """Discover plain pytest test functions from *path*."""

    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    test_file = _display_path(path)
    return _pytest_test_items(tree, test_file, source)


def collect_specweave_tests(paths: Iterable[Path]) -> list[SpecweaveTestMapping]:
    """Collect SpecWeave mappings from multiple pytest files."""

    mappings: list[SpecweaveTestMapping] = []
    for path in paths:
        mappings.extend(discover_specweave_tests(path))
    return mappings


def collect_pytest_tests(paths: Iterable[Path]) -> list[PytestTestItem]:
    """Collect plain pytest test functions from multiple Python files."""

    items: list[PytestTestItem] = []
    for path in paths:
        items.extend(discover_pytest_tests(path))
    return items


def is_behavior_mapping(mapping: SpecweaveTestMapping) -> bool:
    """Return true when *mapping* targets a behaviour scenario."""

    return mapping.feature is not None and mapping.scenario is not None


def is_specification_mapping(mapping: SpecweaveTestMapping) -> bool:
    """Return true when *mapping* targets a specification requirement."""

    return mapping.spec is not None and mapping.requirement is not None


def _function_to_scenario(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> Scenario | None:
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
    "PytestTestItem",
    "SpecweaveTestMapping",
    "collect_pytest_tests",
    "collect_specweave_tests",
    "discover_pytest_tests",
    "discover_specweave_tests",
    "extract_test_scenarios",
    "is_behavior_mapping",
    "is_specification_mapping",
    "extract_module_docstring",
    "extract_class_rules",
]
