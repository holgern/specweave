"""Stable function and file naming helpers."""

from __future__ import annotations

import re


def step_function_name(step_text: str, existing: frozenset[str] = frozenset()) -> str:
    """Generate a stable Python function name from a Gherkin step text.

    Rules:

    - lowercase the text;
    - replace non-alphanumeric groups with ``_``;
    - strip leading/trailing ``_``;
    - prefix with ``step_``;
    - ensure uniqueness by appending ``_N`` if needed.
    """
    name = step_text.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = name.strip("_")
    name = f"step_{name}"

    if name in existing:
        suffix = 2
        while f"{name}_{suffix}" in existing:
            suffix += 1
        name = f"{name}_{suffix}"

    return name
