"""Typer command declarations for the SpecWeave CLI."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer(no_args_is_help=True)

# Sub-app for behavior-first commands.
behavior_app = typer.Typer(
    no_args_is_help=True,
    help="Work with canonical behavior specs and plain pytest enforcement.",
)
app.add_typer(behavior_app, name="behavior")

# Sub-app for BDD conversion commands.
bdd_app = typer.Typer(
    no_args_is_help=True, help="Convert between task-BDD JSON and feature files."
)
app.add_typer(bdd_app, name="bdd")

# Sub-app for report normalization commands.
report_app = typer.Typer(no_args_is_help=True, help="Normalize runner reports.")
app.add_typer(report_app, name="report")


@app.command()
def explain(paths: list[Path]) -> None:
    """Explain Python test files as candidate behavior specs."""
    from specweave.translate.code_to_spec import explain_tests

    explain_tests(paths)


@app.command()
def draft(
    from_json: Annotated[Path | None, typer.Option("--from-json")] = None,
    task: Annotated[str | None, typer.Option("--task")] = None,
    out: Annotated[Path, typer.Option("--out")] = Path("features/specweave.feature"),
) -> None:
    """Draft a feature file from acceptance criteria."""
    from specweave.translate.spec_to_code import draft_feature

    if from_json:
        draft_feature(from_json, out)
    elif task:
        typer.echo("Drafting from task ID not yet implemented. Use --from-json.")
        raise typer.Exit(code=1)
    else:
        typer.echo("Either --from-json or --task is required.")
        raise typer.Exit(code=1)


@app.command()
def bind(
    feature_path: Path,
    backend: Annotated[
        str,
        typer.Option("--backend", help="Step backend: behave or pytest-bdd."),
    ] = "behave",
    out: Annotated[Path, typer.Option("--out")] = Path("tests/bdd/steps"),
) -> None:
    """Create missing Python step-definition skeletons."""
    from specweave.translate.spec_to_code import bind_feature

    try:
        bind_feature(feature_path, backend, out)
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc


@app.command(
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    }
)
def run(
    ctx: typer.Context,
    runner: Annotated[str, typer.Option("--runner")] = "command",
) -> None:
    """Run a delegated BDD command and normalize evidence."""
    from specweave.runners.command import run_command

    run_command(ctx.args, runner)


@app.command()
def version() -> None:
    """Print the specweave version."""
    from specweave import __version__

    typer.echo(f"specweave {__version__}")


# --- behavior subcommands ----------------------------------------------------


def _print_findings(findings) -> None:  # type: ignore[no-untyped-def]
    if not findings:
        typer.echo("No behavior lint findings.")
        return
    for finding in findings:
        location = finding.path
        if finding.line is not None:
            location = f"{location}:{finding.line}"
        typer.echo(
            f"{finding.level.upper()} {finding.code} {location} {finding.message}"
        )


def _has_errors(findings) -> bool:  # type: ignore[no-untyped-def]
    return any(finding.level == "error" for finding in findings)


def _coverage_failed(data: dict[str, object]) -> bool:
    return any(
        bool(data[key])
        for key in (
            "missing_bindings",
            "stale_bindings",
            "deprecated_paths",
            "forbidden_pytest_bdd_usages",
        )
    )


@behavior_app.command("check")
def behavior_check(
    path: Annotated[Path | None, typer.Argument()] = None,
    strict: Annotated[bool, typer.Option("--strict")] = False,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Lint behavior feature files."""
    from specweave.gherkin.lint import default_feature_files, lint_feature_files

    target_paths = (path,) if path is not None else tuple(default_feature_files())
    findings = lint_feature_files(target_paths, strict=strict)
    if json_output:
        typer.echo(
            _dump_json(
                {
                    "schema_version": 1,
                    "findings": [finding.to_dict() for finding in findings],
                }
            )
        )
    else:
        _print_findings(findings)
    if _has_errors(findings):
        raise typer.Exit(code=1)


@behavior_app.command("index")
def behavior_index(
    features: Annotated[Path, typer.Option("--features")] = Path(
        "specs/behavior/features"
    ),
    out: Annotated[Path, typer.Option("--out")] = Path("specs/behavior/README.md"),
    manifest: Annotated[Path, typer.Option("--manifest")] = Path(
        "specs/behavior/manifest.json"
    ),
    tests_dir: Annotated[Path, typer.Option("--tests-dir")] = Path("tests"),
) -> None:
    """Generate the behavior Markdown index and manifest."""
    from specweave.behavior.index import write_behavior_index
    from specweave.gherkin.lint import collect_feature_files, lint_feature_files

    findings = lint_feature_files(
        collect_feature_files((features,)),
        require_scenario_ids=True,
    )
    warnings = [finding for finding in findings if finding.level == "warning"]
    if warnings:
        _print_findings(warnings)
    if _has_errors(findings):
        raise typer.Exit(code=1)

    index_path, manifest_path = write_behavior_index(
        features_dir=features,
        out=out,
        manifest_path=manifest,
        tests_dir=tests_dir,
    )
    typer.echo(f"Wrote behavior index to {index_path}")
    typer.echo(f"Wrote behavior manifest to {manifest_path}")


@behavior_app.command("generate-tests")
def behavior_generate_tests(
    feature: Annotated[Path | None, typer.Argument()] = None,
    features: Annotated[Path | None, typer.Option("--features")] = None,
    out: Annotated[Path | None, typer.Option("--out")] = None,
    tests_dir: Annotated[Path, typer.Option("--tests-dir")] = Path("tests"),
) -> None:
    """Generate plain pytest skeletons from behavior feature files."""
    from specweave.behavior.generate import generate_from_paths

    if feature is not None and features is not None:
        typer.echo("Use either a feature argument or --features, not both.", err=True)
        raise typer.Exit(code=1)

    outputs = generate_from_paths(
        feature_path=feature,
        features_dir=features,
        out=out,
        tests_dir=tests_dir,
    )
    for path in outputs:
        typer.echo(f"Wrote plain pytest skeleton to {path}")


@behavior_app.command("coverage")
def behavior_coverage(
    features: Annotated[Path, typer.Option("--features")] = Path(
        "specs/behavior/features"
    ),
    tests: Annotated[Path, typer.Option("--tests")] = Path("tests"),
    json_output: Annotated[Path | None, typer.Option("--json")] = None,
) -> None:
    """Check static coverage between behavior specs and plain pytest tests."""
    from specweave.behavior.coverage import build_behavior_coverage, write_coverage_json
    from specweave.gherkin.lint import collect_feature_files, lint_feature_files

    findings = lint_feature_files(
        collect_feature_files((features,)),
        require_scenario_ids=True,
    )
    warnings = [finding for finding in findings if finding.level == "warning"]
    if warnings:
        _print_findings(warnings)
    if _has_errors(findings):
        raise typer.Exit(code=1)

    data = build_behavior_coverage(features_dir=features, tests_dir=tests)
    if json_output is None:
        typer.echo(_dump_json(data))
    else:
        write_coverage_json(data, json_output)
        typer.echo(f"Wrote behavior coverage to {json_output}")
    if _coverage_failed(data):
        raise typer.Exit(code=1)


@behavior_app.command("import-report")
def behavior_import_report(
    report: Annotated[Path, typer.Argument(help="Runner report to import.")],
    fmt: Annotated[str, typer.Option("--format")] = "junit-xml",
    out: Annotated[Path | None, typer.Option("--out")] = None,
    tests_dir: Annotated[Path, typer.Option("--tests-dir")] = Path("tests"),
    manifest: Annotated[Path, typer.Option("--manifest")] = Path(
        "specs/behavior/manifest.json"
    ),
) -> None:
    """Import a pytest/JUnit report into behavior evidence JSON."""
    from specweave.behavior.reporting import (
        import_pytest_report,
        write_pytest_evidence_json,
    )

    if fmt != "junit-xml":
        typer.echo(
            "behavior import-report currently supports only --format junit-xml.",
            err=True,
        )
        raise typer.Exit(code=1)

    payload = import_pytest_report(report, tests_dir=tests_dir, manifest_path=manifest)
    target = out or Path(".specweave/evidence") / f"{report.stem}.pytest-evidence.json"
    write_pytest_evidence_json(payload, target)
    typer.echo(f"Wrote pytest behavior evidence to {target}")
    if payload.get("unmapped"):
        raise typer.Exit(code=1)


@behavior_app.command("import-taskledger")
def behavior_import_taskledger(
    source: Annotated[Path, typer.Argument(help="Taskledger acceptance export JSON.")],
    out: Annotated[Path, typer.Option("--out", help="Output canonical .feature file.")],
) -> None:
    """Create a canonical behavior feature from a Taskledger export."""
    from specweave.integrations.taskledger import write_behavior_feature_from_taskledger

    write_behavior_feature_from_taskledger(source, out)
    typer.echo(f"Wrote behavior feature to {out}")


# --- compatibility aliases ---------------------------------------------------


@bdd_app.command("check")
def bdd_check_alias(
    path: Annotated[Path | None, typer.Argument()] = None,
    strict: Annotated[bool, typer.Option("--strict")] = False,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Compatibility alias for ``specweave behavior check``."""

    behavior_check(path=path, strict=strict, json_output=json_output)


@bdd_app.command("index")
def bdd_index_alias(
    features: Annotated[Path, typer.Option("--features")] = Path(
        "specs/behavior/features"
    ),
    out: Annotated[Path, typer.Option("--out")] = Path("specs/behavior/README.md"),
    manifest: Annotated[Path, typer.Option("--manifest")] = Path(
        "specs/behavior/manifest.json"
    ),
    tests_dir: Annotated[Path, typer.Option("--tests-dir")] = Path("tests"),
) -> None:
    """Compatibility alias for ``specweave behavior index``."""

    behavior_index(features=features, out=out, manifest=manifest, tests_dir=tests_dir)


@bdd_app.command("generate-tests")
def bdd_generate_tests_alias(
    feature: Annotated[Path | None, typer.Argument()] = None,
    features: Annotated[Path | None, typer.Option("--features")] = None,
    out: Annotated[Path | None, typer.Option("--out")] = None,
    tests_dir: Annotated[Path, typer.Option("--tests-dir")] = Path("tests"),
) -> None:
    """Compatibility alias for ``specweave behavior generate-tests``."""

    behavior_generate_tests(
        feature=feature,
        features=features,
        out=out,
        tests_dir=tests_dir,
    )


@bdd_app.command("coverage")
def bdd_coverage_alias(
    features: Annotated[Path, typer.Option("--features")] = Path(
        "specs/behavior/features"
    ),
    tests: Annotated[Path, typer.Option("--tests")] = Path("tests"),
    json_output: Annotated[Path | None, typer.Option("--json")] = None,
) -> None:
    """Compatibility alias for ``specweave behavior coverage``."""

    behavior_coverage(features=features, tests=tests, json_output=json_output)


# --- report subcommands ----------------------------------------------------


@report_app.command("normalize")
def report_normalize(
    report: Path,
    fmt: Annotated[
        str,
        typer.Option(
            "--format",
            help="Report format: cucumber-json or junit-xml.",
        ),
    ],
    out: Annotated[
        Path | None,
        typer.Option("--out", help="Write the normalized report JSON to this path."),
    ] = None,
    task_id: Annotated[
        str | None,
        typer.Option(
            "--task",
            help=(
                "Task id recorded in Taskledger evidence output "
                "(defaults to task-* in tags)."
            ),
        ),
    ] = None,
    evidence: Annotated[
        bool,
        typer.Option(
            "--evidence/--no-evidence",
            help=(
                "Write the Taskledger BDD evidence JSON shape "
                "instead of the full report."
            ),
        ),
    ] = False,
    allow_skipped: Annotated[
        bool,
        typer.Option(
            "--allow-skipped", help="Do not fail the report on skipped scenarios."
        ),
    ] = False,
    expect_ac: Annotated[
        list[str] | None,
        typer.Option(
            "--expect-ac",
            help=(
                "Acceptance criterion id that must have a passing "
                "linked scenario (repeatable)."
            ),
        ),
    ] = None,
    command: Annotated[
        str | None,
        typer.Option(
            "--command", help="Original command that produced the native report."
        ),
    ] = None,
) -> None:
    """Normalize a runner-native BDD report to the SpecWeave schema (v2)."""
    from specweave.reports.normalize import (
        normalize_report,
        to_evidence_dict,
        to_normalized_dict,
        write_evidence_json,
        write_normalized_json,
    )

    command_tokens = tuple(command.split()) if command else ()
    try:
        report_obj = normalize_report(
            report,
            fmt,
            allow_skipped=allow_skipped,
            expected_ac_ids=expect_ac or (),
            command=command_tokens,
        )
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc

    if out is None:
        if evidence:
            typer.echo(
                _dump_json(
                    to_evidence_dict(report_obj, task_id or _task_id(report_obj))
                )
            )
        else:
            typer.echo(_dump_json(to_normalized_dict(report_obj)))
    elif evidence:
        write_evidence_json(report_obj, task_id or _task_id(report_obj), out)
        typer.echo(f"Wrote Taskledger evidence to {out}")
    else:
        write_normalized_json(report_obj, out)
        typer.echo(f"Wrote normalized report to {out}")

    if report_obj.status != "passed":
        raise typer.Exit(code=1)


@report_app.command("inspect")
def report_inspect(
    report: Path,
    fmt: Annotated[str, typer.Option("--format", help="cucumber-json or junit-xml.")],
) -> None:
    """Print a compact normalized view of a runner-native report."""
    from specweave.reports.normalize import normalize_report, to_normalized_dict

    try:
        report_obj = normalize_report(report, fmt)
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc

    data = to_normalized_dict(report_obj)
    typer.echo(
        f"status={data['status']} "
        f"scenarios={data['scenarios']} "
        f"passed={data['passed']} failed={data['failed']} "
        f"skipped={data['skipped']} undefined={data['undefined']} "
        f"pending={data['pending']} ambiguous={data['ambiguous']}"
    )
    for result in data["results"]:
        typer.echo(
            f"  {result['status']:<10} {result.get('feature', '')}"
            f" :: {result['scenario']}"
        )
    if report_obj.status != "passed":
        raise typer.Exit(code=1)


# --- bdd subcommands -------------------------------------------------------


@bdd_app.command("export")
def bdd_export(
    from_json: Annotated[Path, typer.Option("--from-json", help="Task-BDD JSON spec.")],
    out: Annotated[Path, typer.Option("--out", help="Output .feature file.")],
) -> None:
    """Export a task-BDD JSON spec to a target-format Gherkin feature file."""
    from specweave.bdd.convert import task_bdd_to_feature
    from specweave.bdd.store import load_task_bdd_json
    from specweave.gherkin.writer import write_feature

    spec = load_task_bdd_json(from_json)
    feature = task_bdd_to_feature(spec)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(write_feature(feature), encoding="utf-8")
    typer.echo(f"Wrote feature to {out}")


@bdd_app.command("import-feature")
def bdd_import_feature(
    feature: Annotated[Path, typer.Argument(help="Feature file to import.")],
    out: Annotated[Path, typer.Option("--out", help="Output task-BDD JSON file.")],
) -> None:
    """Import a Gherkin feature file back into a task-BDD JSON spec."""
    from specweave.bdd.convert import feature_to_task_bdd
    from specweave.bdd.store import save_task_bdd_json
    from specweave.gherkin.parser import parse_feature

    parsed = parse_feature(feature.read_text(encoding="utf-8"))
    spec = feature_to_task_bdd(parsed)
    save_task_bdd_json(spec, out)
    typer.echo(f"Wrote task-BDD spec to {out}")


# --- archledger subcommand -------------------------------------------------


@app.command("archledger")
def archledger(
    feature: Annotated[Path, typer.Option("--feature", help="Feature file.")],
    bdd: Annotated[str, typer.Option("--bdd", help="BDD example id, e.g. bdd-0001.")],
    out: Annotated[Path, typer.Option("--out", help="Output candidate markdown path.")],
) -> None:
    """Render an Archledger candidate behavior record for a BDD example."""
    from specweave.gherkin.parser import parse_feature
    from specweave.integrations.archledger import write_archledger_candidate

    try:
        write_archledger_candidate(
            parse_feature(feature.read_text(encoding="utf-8")), bdd, out
        )
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"Wrote candidate to {out}")


# --- helpers ---------------------------------------------------------------


def _dump_json(data: object) -> str:
    import json

    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)


def _task_id(report):  # type: ignore[no-untyped-def]
    from specweave.integrations.taskledger import task_id_from_report

    return task_id_from_report(report)
