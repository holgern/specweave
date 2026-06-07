"""Convert Python AST observations to feature candidates (``explain``)."""

from __future__ import annotations

from pathlib import Path

from specweave.gherkin.model import Feature
from specweave.python_inspect.ast_reader import extract_test_scenarios


def explain_tests(paths: list[Path]) -> None:
    """Read Python test files and print candidate Gherkin features to stdout."""
    from typer import echo

    for path in paths:
        if not path.exists():
            echo(f"Error: {path} does not exist")
            continue
        if not path.suffix == ".py":
            echo(f"Error: {path} is not a Python file")
            continue

        scenarios = extract_test_scenarios(path)
        if not scenarios:
            echo(f"# {path}: no test functions found")
            continue

        feature_name = _derive_feature_name(path)
        feature = Feature(title=feature_name, scenarios=tuple(scenarios))

        from specweave.gherkin.writer import write_feature

        echo(write_feature(feature))


def _derive_feature_name(path: Path) -> str:
    """Derive a candidate feature name from a test file path."""
    stem = path.stem
    # Remove test_ prefix
    if stem.startswith("test_"):
        stem = stem[5:]
    # Remove _test suffix
    if stem.endswith("_test"):
        stem = stem[:-5]
    return stem.replace("_", " ").strip().title()
