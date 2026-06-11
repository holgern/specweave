"""Shared helpers for the behavior-first workflow."""

from __future__ import annotations

import re
from collections.abc import Iterable, Iterator
from pathlib import Path

from specweave.config import BEHAVIOR_FEATURES_DIR, PYTEST_TESTS_DIR
from specweave.gherkin.model import Feature, Rule, Scenario

_LEGACY_BEHAVIOR_FEATURES_DIR = Path("specs/behavior/features")


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


def feature_stem(path: Path) -> str:
    """Return the feature stem without ``.feature`` or legacy ``.feature.md`` suffix.

    >>> feature_stem(Path("auth/login.feature.md"))
    'login'
    >>> feature_stem(Path("auth/login.feature"))
    'login'
    """
    name = path.name
    if name.endswith(".feature.md"):
        return name[: -len(".feature.md")]
    if name.endswith(".feature"):
        return name[: -len(".feature")]
    return path.stem


def feature_identity(
    feature_path: Path, *, features_root: Path = BEHAVIOR_FEATURES_DIR
) -> tuple[str, str]:
    """Return ``(area, feature_slug)`` for *feature_path*."""

    path = Path(feature_path)
    fs = feature_stem(path)
    relative = None
    for root in (features_root, _LEGACY_BEHAVIOR_FEATURES_DIR):
        try:
            relative = path.relative_to(root)
            break
        except ValueError:
            continue
    if relative is None:
        return slugify(path.parent.name), slugify(fs)

    parent = relative.parent
    if str(parent) == ".":
        return "behavior", slugify(fs)
    area = slugify(parent.parts[0])
    feature_slug = slugify(fs)
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
