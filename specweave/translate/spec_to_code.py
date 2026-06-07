"""Generate feature files from acceptance criteria and step skeletons from features."""

from __future__ import annotations

import json
from pathlib import Path

from specweave.gherkin.model import Feature, Scenario, Step
from specweave.gherkin.parser import parse_feature
from specweave.gherkin.writer import write_feature
from specweave.translate.naming import step_function_name


def draft_feature(from_json: Path, out: Path) -> None:
    """Generate a Gherkin feature file from a JSON acceptance criteria file."""
    data = json.loads(from_json.read_text(encoding="utf-8"))

    task_id = data.get("task_id", "UNKNOWN")
    title = data.get("title", "Untitled")
    criteria = data.get("acceptance_criteria", [])

    scenarios: list[Scenario] = []

    for ac in criteria:
        ac_id = ac.get("id", "AC-001")
        ac_text = ac.get("text", "")

        steps = [
            Step(keyword="Given", text="the system is ready"),
            Step(keyword="When", text=ac_text.lower()),
            Step(keyword="Then", text="the acceptance criterion is satisfied"),
        ]
        scenario = Scenario(
            title=_criterion_to_scenario_title(ac_text),
            steps=tuple(steps),
            tags=(f"ac:{ac_id}",),
        )
        scenarios.append(scenario)

    feature = Feature(
        title=title,
        scenarios=tuple(scenarios),
        tags=(f"taskledger:{task_id}",),
    )

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(write_feature(feature), encoding="utf-8")


def _criterion_to_scenario_title(text: str) -> str:
    """Convert acceptance criterion text to a scenario title."""
    # Take the first 80 chars, capitalize
    title = text.strip().capitalize()
    if len(title) > 80:
        title = title[:80].rstrip() + "..."
    return title


def bind_feature(feature_path: Path, backend: str, out: Path) -> None:
    """Generate Python step-definition skeletons for a feature file.

    Supports ``behave`` backend.
    """
    text = feature_path.read_text(encoding="utf-8")
    feature = parse_feature(text)

    out.mkdir(parents=True, exist_ok=True)

    existing_names: set[str] = set()
    all_steps: list[Step] = []
    for scenario in feature.scenarios:
        all_steps.extend(scenario.steps)

    if backend == "behave":
        generated = _generate_behave_skeletons(feature, all_steps, existing_names)
    else:
        raise ValueError(f"Unsupported backend: {backend}")

    output_path = out / f"{feature_path.stem}_steps.py"
    output_path.write_text(generated, encoding="utf-8")


def _generate_behave_skeletons(
    feature: Feature,
    steps: list[Step],
    existing_names: set[str],
) -> str:
    """Generate behave step-definition Python code."""

    lines: list[str] = [
        f'"""Step definitions for feature: {feature.title}"""',
        "from __future__ import annotations",
        "",
        "from behave import given, then, when  # type: ignore[import-untyped]",
        "",
        f"# Feature: {feature.title}",
        "# Source: {}".format(feature.source_path or "generated"),
        "",
    ]

    decorator_map = {
        "Given": "given",
        "When": "when",
        "Then": "then",
        "And": "then",  # And/But reuse Then
        "But": "then",
    }

    seen_texts: set[str] = set()

    for step in steps:
        step_text = step.text
        keyword = step.keyword

        if step_text in seen_texts:
            continue
        seen_texts.add(step_text)

        decorator = decorator_map.get(keyword, "given")
        func_name = step_function_name(
            f"{keyword} {step_text}", existing=frozenset(existing_names)
        )
        existing_names.add(func_name)

        lines.append(f'@{decorator}("{step_text}")')
        lines.append(f"def {func_name}(context):")
        lines.append(f'    """Step: {keyword} {step_text}"""')
        lines.append('    raise NotImplementedError("Bind this step to project code.")')
        lines.append("")

    return "\n".join(lines)
