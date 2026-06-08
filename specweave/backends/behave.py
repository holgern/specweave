"""behave step-skeleton backend.

Generates behave-style step definitions with ``@given``/``@when``/``@then``
decorators and ``NotImplementedError`` stubs. Output is identical to the
original MVP ``_generate_behave_skeletons`` implementation so existing
generated step files remain stable.
"""

from __future__ import annotations

from specweave.backends._helpers import collect_steps
from specweave.gherkin.model import Feature
from specweave.translate.naming import step_function_name

#: ``And``/``But`` reuse the most recent section. Without section state we
#: default to ``then`` (matching the original MVP behaviour) so generated
#: functions remain attached to a known decorator.
_DECORATOR_MAP = {
    "Given": "given",
    "When": "when",
    "Then": "then",
    "And": "then",
    "But": "then",
}


def generate_behave(feature: Feature) -> str:
    """Render behave step-definition skeletons for *feature*."""
    steps = collect_steps(feature)
    existing_names: set[str] = set()

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

    seen_texts: set[str] = set()
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

        lines.append(f'@{decorator}("{step_text}")')
        lines.append(f"def {func_name}(context):")
        lines.append(f'    """Step: {keyword} {step_text}"""')
        lines.append('    raise NotImplementedError("Bind this step to project code.")')
        lines.append("")

    return "\n".join(lines)
