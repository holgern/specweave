"""pytest-bdd step-skeleton backend.

Generates ``pytest-bdd``-style step definitions using ``@given``/``@when``/
``@then`` with ``parsers`` for flexible matching, plus a ``scenarios(...)``
binding call. Step functions raise ``NotImplementedError`` stubs and use
``target_fixture`` so fixtures are exposed across steps.
"""

from __future__ import annotations

from specweave.backends._helpers import collect_steps
from specweave.gherkin.model import Feature
from specweave.translate.naming import step_function_name

_DECORATOR_MAP = {
    "Given": "given",
    "When": "when",
    "Then": "then",
    # Without section state we attach And/But to the previous section; default
    # to ``given`` so the generated function stays bound to a known decorator.
    "And": "given",
    "But": "given",
}


def _module_docstring(feature: Feature) -> str:
    return f'"""Step definitions for feature: {feature.title} (pytest-bdd backend)."""'


def _feature_filename(feature: Feature) -> str:
    if feature.source_path is not None:
        return feature.source_path.name
    return f"{feature.title.replace(' ', '_').lower()}.feature"


def _scenarios_call(feature: Feature) -> str:
    """Render the ``scenarios(...)`` binding that ties this module to a feature."""
    filename = _feature_filename(feature)
    return f'scenarios("{filename}")'


def _scenario_names(feature: Feature) -> list[str]:
    names: list[str] = []
    for scenario in feature.scenarios:
        names.append(scenario.title)
    for rule in feature.rules:
        for scenario in rule.scenarios:
            names.append(scenario.title)
    return names


def _iter_scenarios(feature: Feature):  # type: ignore[no-untyped-def]
    for scenario in feature.scenarios:
        yield scenario
    for rule in feature.rules:
        for scenario in rule.scenarios:
            yield scenario


def generate_pytest_bdd(feature: Feature) -> str:
    """Render pytest-bdd step-definition skeletons for *feature*."""
    steps = collect_steps(feature)
    existing_names: set[str] = set()

    header: list[str] = [
        _module_docstring(feature),
        "from __future__ import annotations",
        "",
        "from pytest_bdd import (  # type: ignore[import-untyped]",
        "    given,",
        "    parsers,",
        "    scenarios,",
        "    then,",
        "    when,",
        ")",
        "",
        "# Bind every scenario declared in the feature file to this module.",
        _scenarios_call(feature),
        "",
    ]

    seen_texts: set[str] = set()
    body: list[str] = []
    for step in steps:
        step_text = step.text
        keyword = step.keyword
        if step_text in seen_texts:
            continue
        seen_texts.add(step_text)

        decorator = _DECORATOR_MAP.get(keyword, "given")
        func_name = step_function_name(
            f"{keyword} {step_text}", existing=frozenset(existing_names)
        )
        existing_names.add(func_name)
        fixture = (
            func_name[len("step_") :] if func_name.startswith("step_") else func_name
        )

        body.append(
            f'@{decorator}(parsers.parse("{step_text}"), target_fixture="{fixture}")'
        )
        body.append(f"def {func_name}():")
        body.append(f'    """Step: {keyword} {step_text}."""')
        body.append('    raise NotImplementedError("Bind this step to project code.")')
        body.append("")

    return "\n".join([*header, *body]).rstrip() + "\n"


__all__ = ["generate_pytest_bdd"]
