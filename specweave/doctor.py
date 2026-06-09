"""SpecWeave doctor: diagnose setup and convention problems."""

from __future__ import annotations

import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from specweave.config import SpecWeaveConfig, find_config


@dataclass(frozen=True)
class DoctorItem:
    """A single doctor finding."""

    code: str
    level: str
    message: str
    path: str | None = None


def _check_config_exists(
    config: SpecWeaveConfig, config_path: Path | None
) -> list[DoctorItem]:
    items: list[DoctorItem] = []
    if config_path is None and find_config() is None:
        items.append(
            DoctorItem(
                code="SWDOC001",
                level="warning",
                message=(
                    "No config file found. Using defaults."
                    " Run 'specweave init' to create one."
                ),
            )
        )
    return items


def _check_config_schema(config: SpecWeaveConfig) -> list[DoctorItem]:
    items: list[DoctorItem] = []
    if config.schema_version != 1:
        items.append(
            DoctorItem(
                code="SWDOC002",
                level="error",
                message=(
                    f"Unsupported config schema_version: {config.schema_version}."
                    " Only version 1 is supported."
                ),
            )
        )
    return items


def _check_dir_exists(path: Path, label: str, code: str) -> list[DoctorItem]:
    items: list[DoctorItem] = []
    if not path.exists():
        items.append(
            DoctorItem(
                code=code,
                level="warning",
                message=f"{label} directory does not exist: {path}",
                path=str(path),
            )
        )
    return items


def _configured_paths(config: SpecWeaveConfig, config_path: Path | None) -> list[Path]:
    if config_path is None or not config_path.is_file():
        return [
            config.paths.specs_root,
            config.paths.features_dir,
            config.paths.tests_dir,
            config.paths.reports_dir,
        ]
    if sys.version_info >= (3, 11):
        import tomllib
    else:
        import tomli as tomllib

    raw = tomllib.loads(config_path.read_text(encoding="utf-8"))
    paths = raw.get("paths", {})
    return [Path(value) for value in paths.values() if isinstance(value, str)]


def _check_paths_relative(
    config: SpecWeaveConfig, config_path: Path | None
) -> list[DoctorItem]:
    items: list[DoctorItem] = []
    for p in _configured_paths(config, config_path):
        if p.is_absolute():
            items.append(
                DoctorItem(
                    code="SWDOC003",
                    level="warning",
                    message=f"Path should be relative: {p}",
                    path=str(p),
                )
            )
    return items


def _check_deprecated_paths(config: SpecWeaveConfig) -> list[DoctorItem]:
    items: list[DoctorItem] = []
    deprecated_segments = [
        "specs/bdd/features",
        "tests/bdd/features",
        "tests/behavior/features",
    ]
    features_dir = config.paths.features_dir
    for segment in deprecated_segments:
        check = Path(segment)
        if check.exists() and check != features_dir:
            items.append(
                DoctorItem(
                    code="SWDOC004",
                    level="warning",
                    message=f"Deprecated path detected: {segment}",
                    path=segment,
                )
            )
    return items


def _check_feature_files(config: SpecWeaveConfig) -> list[DoctorItem]:
    items: list[DoctorItem] = []
    features_dir = config.paths.features_dir
    if not features_dir.exists():
        return items

    from specweave.gherkin.lint import collect_feature_files, lint_feature_files

    feature_files = collect_feature_files((features_dir,))
    if not feature_files:
        return items

    findings = lint_feature_files(
        feature_files, strict=False, require_scenario_ids=True
    )
    for finding in findings:
        level = finding.level
        if level == "error":
            items.append(
                DoctorItem(
                    code=finding.code,
                    level="error",
                    message=finding.message,
                    path=finding.path,
                )
            )
    return items


def _check_duplicate_bdd_tags(config: SpecWeaveConfig) -> list[DoctorItem]:
    items: list[DoctorItem] = []
    features_dir = config.paths.features_dir
    if not features_dir.exists():
        return items

    from collections import defaultdict

    from specweave.gherkin.lint import collect_feature_files
    from specweave.gherkin.parser import parse_feature

    feature_files = collect_feature_files((features_dir,))
    bdd_tags: dict[str, list[str]] = defaultdict(list)

    for path in feature_files:
        try:
            text = path.read_text(encoding="utf-8")
            feature = parse_feature(text)
        except (ValueError, OSError):
            continue
        _collect_bdd_tags(feature, str(path), bdd_tags)

    for tag, locations in sorted(bdd_tags.items()):
        if len(locations) > 1:
            for loc in locations:
                items.append(
                    DoctorItem(
                        code="SWDOC005",
                        level="error",
                        message=f"Duplicate @bdd-* tag {tag}",
                        path=loc,
                    )
                )
    return items


def _collect_bdd_tags(feature: object, path: str, tags: dict[str, list[str]]) -> None:
    from specweave.gherkin.lint import iter_feature_scenarios
    from specweave.gherkin.model import Feature

    typed_feature = feature if isinstance(feature, Feature) else None
    if typed_feature is None:
        return
    for scenario in iter_feature_scenarios(typed_feature):
        for tag in scenario.tags:
            if tag.startswith("bdd-"):
                tags[tag].append(path)


def run_doctor(
    *,
    config: SpecWeaveConfig | None = None,
    config_path: Path | None = None,
    fix: bool = False,
) -> dict:
    """Run doctor checks and return a JSON-serialisable result.

    Parameters
    ----------
    config:
        Loaded config. If None, loads from discovery.
    fix:
        When true, create missing directories.
    """
    if config is None:
        config = SpecWeaveConfig()

    if config_path is None:
        config_path = find_config()
    items: list[DoctorItem] = []
    warnings: list[str] = []
    errors: list[str] = []

    items.extend(_check_config_exists(config, config_path))
    items.extend(_check_config_schema(config))
    items.extend(_check_paths_relative(config, config_path))

    # Directory checks
    dir_checks = [
        (config.paths.features_dir, "Features", "SWDOC006"),
        (config.paths.tests_dir, "Tests", "SWDOC007"),
        (config.paths.reports_dir, "Reports", "SWDOC008"),
        (config.paths.reports_state_dir, "Reports state", "SWDOC011"),
        (config.paths.evidence_dir, "Evidence", "SWDOC009"),
        (config.paths.mapping_dir, "Mapping", "SWDOC010"),
    ]
    for dir_path, label, code in dir_checks:
        if not dir_path.exists():
            items.append(
                DoctorItem(
                    code=code,
                    level="warning",
                    message=f"{label} directory does not exist: {dir_path}",
                    path=str(dir_path),
                )
            )
            if fix:
                dir_path.mkdir(parents=True, exist_ok=True)
                if config.gitkeep and dir_path in {
                    config.paths.features_dir,
                    config.paths.evidence_dir,
                    config.paths.mapping_dir,
                    config.paths.reports_state_dir,
                }:
                    (dir_path / ".gitkeep").touch()
                warnings.append(f"Created {dir_path}")

    items.extend(_check_deprecated_paths(config))
    items.extend(_check_feature_files(config))
    items.extend(_check_duplicate_bdd_tags(config))

    has_errors = any(item.level == "error" for item in items)

    for item in items:
        if item.level == "error":
            errors.append(f"{item.code}: {item.message}")
        elif item.level == "warning":
            warnings.append(f"{item.code}: {item.message}")

    return {
        "schema_version": 1,
        "command": "doctor",
        "status": "passed" if not has_errors else "failed",
        "summary": {
            "checks": len(items),
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "items": [asdict(item) for item in items],
        "warnings": warnings,
        "errors": errors,
    }
