"""Generate plain pytest test skeletons from behavior features."""

from __future__ import annotations

from pathlib import Path

from specweave.behavior.common import (
    canonical_test_path,
    display_path,
    iter_feature_scenarios,
    scenario_identifier,
    test_function_name,
)
from specweave.config import PYTEST_TESTS_DIR
from specweave.gherkin.lint import collect_feature_files
from specweave.gherkin.model import Feature, Scenario
from specweave.gherkin.parser import parse_feature


def _docstring_lines(scenario: Scenario) -> list[str]:
    lines = [f"{scenario.keyword}: {scenario.title}."]
    if scenario.description:
        lines.append("")
        lines.extend(scenario.description.splitlines())
    if scenario.steps:
        lines.append("")
        lines.extend(f"{step.keyword} {step.text}" for step in scenario.steps)
    return lines


def _comment_lines(feature_ref: str, scenario_ref: str) -> list[str]:
    return [
        f"# specweave: feature={feature_ref}",
        f"# specweave: scenario={scenario_ref}",
    ]


def generate_pytest_skeleton(feature: Feature, feature_path: Path) -> str:
    """Render *feature* as a plain pytest skeleton module."""

    feature_ref = display_path(feature_path)
    lines: list[str] = [
        f'"""Plain pytest enforcement for {feature_ref}."""',
        "",
        "from __future__ import annotations",
        "",
        "import pytest",
        "",
        f'SPECWEAVE_FEATURE = "{feature_ref}"',
        "",
    ]

    existing_names: set[str] = set()
    for rule, scenario in iter_feature_scenarios(feature):
        scenario_ref = scenario_identifier(scenario)
        function_name = test_function_name(scenario.title, existing_names)
        existing_names.add(function_name)
        lines.extend(_comment_lines(feature_ref, scenario_ref))
        lines.append("@pytest.mark.specweave(")
        lines.append("    feature=SPECWEAVE_FEATURE,")
        lines.append(f'    scenario="{scenario_ref}",')
        if rule is not None and rule.title:
            lines.append(f'    rule="{rule.title}",')
        lines.append(")")
        lines.append(f"def {function_name}() -> None:")
        doc = _docstring_lines(scenario)
        lines.append(f'    """{doc[0]}')
        for line in doc[1:]:
            lines.append(f"    {line}")
        lines.append('    """')
        for step in scenario.steps:
            phase = {
                "Given": "Arrange",
                "When": "Act",
                "Then": "Assert",
            }.get(step.keyword, "Continue")
            lines.append(f"    # {phase}: {step.keyword} {step.text}")
        lines.append(
            f'    raise NotImplementedError("Implement behavior from {feature_ref}")'
        )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_pytest_skeleton(
    feature_path: Path,
    *,
    out: Path | None = None,
    tests_dir: Path = PYTEST_TESTS_DIR,
) -> Path:
    """Write a pytest skeleton for *feature_path* and return the output path."""

    feature = parse_feature(
        feature_path.read_text(encoding="utf-8"),
        source_path=feature_path,
    )
    output_path = out or canonical_test_path(feature_path, tests_dir=tests_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        generate_pytest_skeleton(feature, feature_path),
        encoding="utf-8",
    )
    return output_path


def generate_from_paths(
    *,
    feature_path: Path | None = None,
    features_dir: Path | None = None,
    out: Path | None = None,
    tests_dir: Path = PYTEST_TESTS_DIR,
) -> list[Path]:
    """Generate one or more pytest skeletons."""

    if feature_path is not None:
        return [write_pytest_skeleton(feature_path, out=out, tests_dir=tests_dir)]

    root = features_dir or Path("specs/behavior/features")
    outputs: list[Path] = []
    for candidate in collect_feature_files((root,)):
        outputs.append(write_pytest_skeleton(candidate, tests_dir=tests_dir))
    return outputs
