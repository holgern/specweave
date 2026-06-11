"""SpecWeave doctor: diagnose setup and convention problems."""

from __future__ import annotations

import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from specweave.config import SpecWeaveConfig, find_config, load_config


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
                    "No config file found. Using discovered defaults."
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


def _configured_paths(config_path: Path | None) -> list[Path]:
    if config_path is None or not config_path.is_file():
        return []
    if sys.version_info >= (3, 11):
        import tomllib
    else:
        import tomli as tomllib

    raw = tomllib.loads(config_path.read_text(encoding="utf-8"))
    configured: list[Path] = []

    def walk(value: object) -> None:
        if isinstance(value, str):
            configured.append(Path(value))
        elif isinstance(value, dict):
            for nested in value.values():
                walk(nested)

    walk(raw.get("paths", {}))
    return configured


def _check_paths_relative(config_path: Path | None) -> list[DoctorItem]:
    items: list[DoctorItem] = []
    for path in _configured_paths(config_path):
        if path.is_absolute():
            items.append(
                DoctorItem(
                    code="SWDOC003",
                    level="warning",
                    message=f"Path should be relative: {path}",
                    path=str(path),
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
    for segment in deprecated_segments:
        check = Path(segment)
        if check.exists():
            items.append(
                DoctorItem(
                    code="SWDOC004",
                    level="warning",
                    message=f"Deprecated path detected: {segment}",
                    path=segment,
                )
            )
    if config.paths.behaviour.root.name == "behavior":
        items.append(
            DoctorItem(
                code="SWDOC012",
                level="warning",
                message=(
                    "Deprecated compatibility layout in use: specs/behavior."
                    " Prefer specs/behaviour for new and migrated projects."
                ),
                path=str(config.paths.behaviour.root),
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
        if finding.level == "error":
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
            for location in locations:
                items.append(
                    DoctorItem(
                        code="SWDOC005",
                        level="error",
                        message=f"Duplicate @bdd-* tag {tag}",
                        path=location,
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


def _check_specification_files(config: SpecWeaveConfig) -> list[DoctorItem]:
    items: list[DoctorItem] = []
    if config.paths.specifications is None:
        return items
    try:
        from specweave.specifications.lint import lint_specification_tree
    except ImportError:
        return items

    for finding in lint_specification_tree(
        config.paths.specifications.root,
        require_verification=(
            config.specifications.require_verification
            if config.specifications is not None
            else True
        ),
    ):
        items.append(
            DoctorItem(
                code=finding.code,
                level=finding.level,
                message=finding.message,
                path=str(finding.path),
            )
        )
    return items


def run_doctor(
    *,
    config: SpecWeaveConfig | None = None,
    config_path: Path | None = None,
    fix: bool = False,
) -> dict:
    """Run doctor checks and return a JSON-serialisable result."""
    if config_path is None:
        config_path = find_config()
    if config is None:
        config = load_config(config_path)

    items: list[DoctorItem] = []
    warnings: list[str] = []
    errors: list[str] = []

    items.extend(_check_config_exists(config, config_path))
    items.extend(_check_config_schema(config))
    items.extend(_check_paths_relative(config_path))
    items.extend(_check_deprecated_paths(config))

    dir_checks: list[tuple[Path, str, str]] = [
        (config.paths.features_dir, "Features", "SWDOC006"),
        (config.paths.tests_dir, "Tests", "SWDOC007"),
        (config.paths.reports_dir, "Reports", "SWDOC008"),
        (config.paths.evidence_dir, "Evidence", "SWDOC009"),
        (config.paths.mapping_dir, "Mapping", "SWDOC010"),
        (config.paths.reports_state_dir, "Reports state", "SWDOC011"),
    ]
    if config.paths.specifications is not None:
        dir_checks.extend(
            [
                (
                    config.paths.specifications.capabilities_dir,
                    "Specifications capabilities",
                    "SWDOC013",
                ),
                (
                    config.paths.specifications.interfaces_dir,
                    "Specifications interfaces",
                    "SWDOC014",
                ),
                (
                    config.paths.specifications.integrations_dir,
                    "Specifications integrations",
                    "SWDOC015",
                ),
                (
                    config.paths.specifications.evidence_dir,
                    "Specifications evidence",
                    "SWDOC016",
                ),
                (
                    config.paths.specifications.mappings_dir,
                    "Specifications mappings",
                    "SWDOC017",
                ),
                (
                    config.paths.specifications.reports_state_dir,
                    "Specifications reports state",
                    "SWDOC018",
                ),
            ]
        )

    for path, label, code in dir_checks:
        if not path.exists():
            items.append(
                DoctorItem(
                    code=code,
                    level="warning",
                    message=f"{label} directory does not exist: {path}",
                    path=str(path),
                )
            )
            if fix:
                path.mkdir(parents=True, exist_ok=True)
                if config.gitkeep and path in {
                    config.paths.features_dir,
                    config.paths.evidence_dir,
                    config.paths.mapping_dir,
                    config.paths.reports_state_dir,
                    *(
                        {
                            config.paths.specifications.capabilities_dir,
                            config.paths.specifications.interfaces_dir,
                            config.paths.specifications.integrations_dir,
                            config.paths.specifications.evidence_dir,
                            config.paths.specifications.mappings_dir,
                            config.paths.specifications.reports_state_dir,
                        }
                        if config.paths.specifications is not None
                        else set()
                    ),
                }:
                    (path / ".gitkeep").touch()

    if (
        config.paths.specifications is not None
        and not config.paths.specifications.product_spec.exists()
    ):
        items.append(
            DoctorItem(
                code="SWDOC019",
                level="warning",
                message=(
                    "Specifications mode is enabled but product.spec.md is missing: "
                    f"{config.paths.specifications.product_spec}"
                ),
                path=str(config.paths.specifications.product_spec),
            )
        )

    items.extend(_check_feature_files(config))
    items.extend(_check_duplicate_bdd_tags(config))
    items.extend(_check_specification_files(config))

    item_dicts: list[dict[str, str | None]] = []
    for item in items:
        item_dicts.append(asdict(item))
        if item.level == "warning":
            warnings.append(item.code)
        if item.level == "error":
            errors.append(item.code)
    status = "passed" if not errors else "failed"
    return {
        "schema_version": 1,
        "command": "doctor",
        "status": status,
        "warnings": warnings,
        "errors": errors,
        "items": item_dicts,
    }
