"""SpecWeave review: aggregate lint, coverage, evidence, and convention findings."""

from __future__ import annotations

from specweave.config import SpecWeaveConfig


def _run_behaviour_review(config: SpecWeaveConfig) -> dict:
    features_dir = config.paths.features_dir
    tests_dir = config.paths.tests_dir

    findings: list[dict] = []
    warnings_count = 0
    errors_count = 0

    from specweave.gherkin.lint import collect_feature_files, lint_feature_files

    feature_files = collect_feature_files((features_dir,))
    lint_results = lint_feature_files(
        (features_dir,),
        strict=False,
        require_scenario_ids=True,
    )
    for finding in lint_results:
        entry: dict[str, object] = {
            "code": finding.code,
            "level": finding.level,
            "path": finding.path,
            "message": finding.message,
        }
        if finding.line is not None:
            entry["line"] = finding.line
        findings.append(entry)
        if finding.level == "error":
            errors_count += 1
        else:
            warnings_count += 1

    from specweave.behavior.coverage import build_behavior_coverage

    coverage = build_behavior_coverage(
        features_dir=features_dir,
        tests_dir=tests_dir,
        mapping_dir=config.paths.mapping_dir,
    )

    features_total = coverage["features_total"]
    scenarios_total = coverage["scenarios_total"]
    scenarios_bound = coverage["scenarios_bound"]
    pytest_tests_total = coverage["pytest_tests_total"]
    pytest_tests_mapped = coverage["pytest_tests_mapped"]
    pytest_tests_unmapped = coverage["pytest_tests_unmapped"]
    pytest_tests_waived = coverage.get("pytest_tests_waived", 0)
    missing_bindings = coverage["missing_bindings"]
    stale_bindings = coverage.get("stale_bindings", [])
    duplicate_bindings = coverage.get("duplicate_bindings", [])

    for binding in missing_bindings:
        scenario = binding.get("scenario", "")
        entry = {
            "code": "SWCOV001",
            "level": "warning",
            "path": binding.get("feature", ""),
            "message": "No bound pytest test found.",
        }
        if scenario:
            entry["scenario"] = scenario
        findings.append(entry)
        warnings_count += 1

    for binding in stale_bindings:
        findings.append(
            {
                "code": "SWCOV002",
                "level": "warning",
                "path": binding.get("test_file", ""),
                "scenario": binding.get("scenario", ""),
                "message": (
                    "Stale pytest mapping points to a missing feature or scenario."
                ),
            }
        )
        warnings_count += 1

    for binding in duplicate_bindings:
        findings.append(
            {
                "code": "SWCOV003",
                "level": "warning",
                "path": binding.get("feature", ""),
                "scenario": binding.get("scenario", ""),
                "message": (
                    "Multiple explicit pytest mappings target the same scenario."
                ),
            }
        )
        warnings_count += 1

    for feature_path in feature_files:
        try:
            text = feature_path.read_text(encoding="utf-8")
        except OSError:
            continue
        if "@needs-review" in text:
            from specweave.gherkin.lint import iter_feature_scenarios
            from specweave.gherkin.parser import parse_feature

            try:
                feature = parse_feature(text)
            except ValueError:
                continue
            for scenario in iter_feature_scenarios(feature):
                if "needs-review" in scenario.tags:
                    findings.append(
                        {
                            "code": "SWREV001",
                            "level": "warning",
                            "path": str(feature_path),
                            "scenario": (
                                f"@{scenario.tags[0]}"
                                if scenario.tags
                                else scenario.title
                            ),
                            "message": "still has @needs-review",
                        }
                    )
                    warnings_count += 1

    for dep_path in coverage.get("deprecated_paths", []):
        findings.append(
            {
                "code": "SWREV002",
                "level": "warning",
                "path": dep_path,
                "message": "Deprecated path detected.",
            }
        )
        warnings_count += 1

    for usage in coverage.get("forbidden_pytest_bdd_usages", []):
        findings.append(
            {
                "code": "SWREV003",
                "level": "error",
                "path": usage,
                "message": "Forbidden pytest-bdd usage detected in plain pytest mode.",
            }
        )
        errors_count += 1

    coverage_failed = bool(
        missing_bindings
        or stale_bindings
        or pytest_tests_unmapped
        or coverage.get("deprecated_paths")
        or coverage.get("forbidden_pytest_bdd_usages")
    )
    status = "passed" if errors_count == 0 and not coverage_failed else "failed"

    return {
        "schema_version": 1,
        "command": "review behaviour",
        "status": status,
        "summary": {
            "features": features_total,
            "scenarios": scenarios_total,
            "bound": scenarios_bound,
            "pytest_tests": pytest_tests_total,
            "pytest_mapped": pytest_tests_mapped,
            "pytest_unmapped": pytest_tests_unmapped,
            "pytest_waived": pytest_tests_waived,
            "missing_bindings": len(missing_bindings),
            "stale_bindings": len(stale_bindings),
            "duplicate_bindings": len(duplicate_bindings),
            "needs_review": sum(1 for f in findings if f["code"] == "SWREV001"),
            "errors": errors_count,
            "warnings": warnings_count,
        },
        "findings": findings,
    }


def run_review(
    *,
    config: SpecWeaveConfig | None = None,
    mode: str = "both",
) -> dict:
    """Run a behaviour/specifications review and return a JSON-serialisable result."""
    if config is None:
        config = SpecWeaveConfig()

    normalized_mode = {
        "behavior": "behaviour",
        "bdd": "behaviour",
        "sdd": "specifications",
        "specs": "both",
    }.get(mode, mode)

    if normalized_mode == "behaviour":
        return _run_behaviour_review(config)

    if normalized_mode == "specifications":
        if config.paths.specifications is None:
            return {
                "schema_version": 1,
                "command": "review specifications",
                "status": "passed",
                "summary": {
                    "documents": 0,
                    "requirements": 0,
                    "verified": 0,
                    "missing": 0,
                    "reverse_gaps": 0,
                    "warnings": 0,
                    "errors": 0,
                },
                "findings": [],
            }
        from specweave.specifications.review import run_specifications_review

        return run_specifications_review(
            root=config.paths.specifications.root,
            tests_dir=config.paths.tests_dir,
            mapping_dir=config.paths.specifications.mappings_dir,
            require_verification=(
                config.specifications.require_verification
                if config.specifications is not None
                else True
            ),
        )

    if config.paths.specifications is None:
        result = _run_behaviour_review(config)
        result["command"] = "review specs"
        return result

    behaviour_review = _run_behaviour_review(config)
    specifications_review = (
        run_review(config=config, mode="specifications")
        if config.paths.specifications is not None
        else None
    )

    status = "passed"
    if behaviour_review["status"] != "passed":
        status = "failed"
    if (
        specifications_review is not None
        and specifications_review["status"] != "passed"
    ):
        status = "failed"

    return {
        "schema_version": 1,
        "command": "review specs",
        "status": status,
        "summary": {
            "behaviour": behaviour_review["summary"],
            "specifications": (
                specifications_review["summary"]
                if specifications_review is not None
                else None
            ),
            "warnings": behaviour_review["summary"].get("warnings", 0)
            + (
                specifications_review["summary"].get("warnings", 0)
                if specifications_review is not None
                else 0
            ),
            "errors": behaviour_review["summary"].get("errors", 0)
            + (
                specifications_review["summary"].get("errors", 0)
                if specifications_review is not None
                else 0
            ),
        },
        "modes": {
            "behaviour": behaviour_review,
            "specifications": specifications_review,
        },
        "findings": behaviour_review["findings"]
        + ([] if specifications_review is None else specifications_review["findings"]),
    }
