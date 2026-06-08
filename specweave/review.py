"""SpecWeave review: aggregate lint, coverage, evidence, and convention findings."""

from __future__ import annotations

from specweave.config import SpecWeaveConfig


def run_review(
    *,
    config: SpecWeaveConfig | None = None,
) -> dict:
    """Run a comprehensive spec review and return a JSON-serialisable result.

    Reuses existing lint, coverage, and index modules.
    """
    if config is None:
        config = SpecWeaveConfig()

    features_dir = config.paths.features_dir
    tests_dir = config.paths.tests_dir

    findings: list[dict] = []
    warnings_count = 0
    errors_count = 0

    # 1. Feature file discovery
    from specweave.gherkin.lint import collect_feature_files

    feature_files = collect_feature_files((features_dir,))

    # 2. Lint
    from specweave.gherkin.lint import lint_feature_files

    lint_results = lint_feature_files(
        (features_dir,),
        strict=False,
        require_scenario_ids=True,
    )
    for finding in lint_results:
        entry = {
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

    # 3. Coverage
    from specweave.behavior.coverage import build_behavior_coverage

    coverage = build_behavior_coverage(
        features_dir=features_dir,
        tests_dir=tests_dir,
    )

    features_total = coverage["features_total"]
    scenarios_total = coverage["scenarios_total"]
    scenarios_bound = coverage["scenarios_bound"]
    missing_bindings = coverage["missing_bindings"]

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
            entry["message"] = f"@{scenario} has no bound pytest test found."
        findings.append(entry)
        warnings_count += 1

    # 4. Needs-review check
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

    # 5. Deprecated paths
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

    # 6. Forbidden pytest-bdd usage
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

    status = "passed" if errors_count == 0 and missing_bindings == [] else "failed"

    return {
        "schema_version": 1,
        "command": "review specs",
        "status": status,
        "summary": {
            "features": features_total,
            "scenarios": scenarios_total,
            "bound": scenarios_bound,
            "missing_bindings": len(missing_bindings),
            "needs_review": sum(1 for f in findings if f["code"] == "SWREV001"),
            "errors": errors_count,
            "warnings": warnings_count,
        },
        "findings": findings,
    }
