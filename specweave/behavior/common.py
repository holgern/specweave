"""Shared helpers for the behavior-first workflow."""

from __future__ import annotations

import re
from collections.abc import Iterable, Iterator
from pathlib import Path

from specweave.config import BEHAVIOR_FEATURES_DIR, PYTEST_TESTS_DIR
from specweave.gherkin.model import Feature, Rule, Scenario


def display_path(path: Path) -> str:
    """Return *path* relative to the current directory when possible."""

    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def slugify(value: str) -> str:
    """Convert *value* to a stable lowercase slug."""

    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "behavior"


def iter_feature_scenarios(feature: Feature) -> Iterator[tuple[Rule | None, Scenario]]:
    """Yield ``(rule, scenario)`` pairs for *feature*."""

    for scenario in feature.scenarios:
        yield None, scenario
    for rule in feature.rules:
        for scenario in rule.scenarios:
            yield rule, scenario


def scenario_id_value(scenario: Scenario) -> str:
    """Return the first stable ``bdd-*`` id from *scenario*, or an empty string."""

    for tag in scenario.tags:
        if tag.startswith("bdd-"):
            return tag
    return ""


def scenario_identifier(scenario: Scenario) -> str:
    """Return the marker/comment identifier for *scenario*."""

    bdd_id = scenario_id_value(scenario)
    return f"@{bdd_id}" if bdd_id else scenario.title


def feature_identity(
    feature_path: Path, *, features_root: Path = BEHAVIOR_FEATURES_DIR
) -> tuple[str, str]:
    """Return ``(area, feature_slug)`` for *feature_path*."""

    path = Path(feature_path)
    try:
        relative = path.relative_to(features_root)
    except ValueError:
        return slugify(path.parent.name), slugify(path.stem)

    parts = relative.with_suffix("").parts
    if not parts:
        return "behavior", slugify(path.stem)
    if len(parts) == 1:
        return "behavior", slugify(parts[0])
    area = slugify(parts[0])
    feature_slug = slugify("-".join(parts[1:]))
    return area, feature_slug


def canonical_test_path(
    feature_path: Path, *, tests_dir: Path = PYTEST_TESTS_DIR
) -> Path:
    """Return the canonical pytest path for *feature_path*."""

    area, feature_slug = feature_identity(feature_path)
    filename = f"test_{area.replace('-', '_')}_{feature_slug.replace('-', '_')}.py"
    return tests_dir / filename


def test_function_name(title: str, existing: Iterable[str]) -> str:
    """Create a stable, unique pytest function name for *title*."""

    base = f"test_{slugify(title).replace('-', '_')}"
    candidate = base
    suffix = 2
    used = set(existing)
    while candidate in used:
        candidate = f"{base}_{suffix}"
        suffix += 1
    return candidate
