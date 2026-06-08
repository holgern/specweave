"""Typer command declarations for the SpecWeave CLI."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from specweave.cli_context import CliContext, build_cli_context

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main(
    ctx: typer.Context,
    config: Annotated[Path | None, typer.Option("--config")] = None,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """SpecWeave CLI: translate between Python tests, Gherkin behavior
    specs, and BDD execution evidence."""
    ctx.obj = build_cli_context(config_path=config, json_output=json_output)


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

# Sub-app for create commands.
create_app = typer.Typer(
    no_args_is_help=True, help="Create Gherkin features, plans, and drafts."
)
app.add_typer(create_app, name="create")

# Sub-app for review commands.
review_app_cli = typer.Typer(
    no_args_is_help=True, help="Review and diagnose SpecWeave projects."
)
app.add_typer(review_app_cli, name="review")

combi_app = typer.Typer(
    no_args_is_help=True, help="Read-only cross-ledger integration diagnostics."
)
app.add_typer(combi_app, name="combi")


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
def version(ctx: typer.Context) -> None:
    """Print the specweave version."""
    from specweave import __version__

    cli_ctx: CliContext = ctx.obj
    if cli_ctx.json_output:
        typer.echo(
            _dump_json(
                {
                    "schema_version": 1,
                    "command": "version",
                    "status": "ok",
                    "version": __version__,
                }
            )
        )
    else:
        typer.echo(f"specweave {__version__}")


# --- init command -----------------------------------------------------------


@app.command()
def init(
    ctx: typer.Context,
    public_config: Annotated[bool, typer.Option("--public-config")] = False,
    spelling: Annotated[str, typer.Option("--spelling")] = "behavior",
    force: Annotated[bool, typer.Option("--force")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
) -> None:
    """Initialize a SpecWeave project configuration and directory layout."""
    from specweave.init import init_result_to_dict, run_init

    cli_ctx: CliContext = ctx.obj
    config_path = Path("specweave.toml") if public_config else Path(".specweave.toml")
    result = run_init(
        config_path=config_path,
        spelling=spelling,
        force=force,
        dry_run=dry_run,
    )
    if cli_ctx.json_output:
        typer.echo(_dump_json(init_result_to_dict(result)))
    else:
        for p in result.created:
            typer.echo(f"Created {p}")
        for p in result.existing:
            typer.echo(f"Existing {p}")
        for p in result.skipped:
            typer.echo(f"Skipped {p}")
        for w in result.warnings:
            typer.echo(f"Warning: {w}")


# --- doctor command ---------------------------------------------------------


@app.command()
def doctor(
    ctx: typer.Context,
    fix: Annotated[bool, typer.Option("--fix")] = False,
) -> None:
    """Diagnose SpecWeave setup and convention problems."""
    from specweave.doctor import run_doctor

    cli_ctx: CliContext = ctx.obj
    result = run_doctor(config=cli_ctx.config, fix=fix)
    if cli_ctx.json_output:
        typer.echo(_dump_json(result))
    else:
        status = result["status"]
        typer.echo(f"SpecWeave doctor: {status}")
        for item in result.get("items", []):
            level = item.get("level", "info")
            typer.echo(f"  {level.upper()}: {item.get('message', '')}")
        for w in result.get("warnings", []):
            typer.echo(f"  WARNING: {w}")
        for e in result.get("errors", []):
            typer.echo(f"  ERROR: {e}")
    if result["status"] != "passed":
        raise typer.Exit(code=1)


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
    feature: Annotated[
        Path | None,
        typer.Option("--feature", help="Limit the report to one feature file."),
    ] = None,
    tests: Annotated[Path, typer.Option("--tests")] = Path("tests"),
    output_format: Annotated[
        str,
        typer.Option("--format", help="Output format: json, text, or markdown."),
    ] = "json",
    show: Annotated[
        str,
        typer.Option(
            "--show", help="Display filter: all, missing, bound, stale, or waived."
        ),
    ] = "all",
    json_output: Annotated[Path | None, typer.Option("--json")] = None,
    out: Annotated[
        Path | None,
        typer.Option("--out", help="Write the selected output format to this path."),
    ] = None,
) -> None:
    """Check static coverage between behavior specs and plain pytest tests."""
    from specweave.behavior.coverage import (
        build_behavior_coverage,
        render_coverage_markdown,
        render_coverage_text,
        write_coverage_json,
    )
    from specweave.gherkin.lint import collect_feature_files, lint_feature_files

    if json_output is not None and out is not None:
        typer.echo("Use either --json or --out, not both.", err=True)
        raise typer.Exit(code=1)
    if json_output is not None and output_format != "json":
        typer.echo("--json can only be used with --format json.", err=True)
        raise typer.Exit(code=1)

    lint_target = feature or features
    findings = lint_feature_files(
        collect_feature_files((lint_target,)),
        require_scenario_ids=True,
    )
    warnings = [finding for finding in findings if finding.level == "warning"]
    if warnings:
        _print_findings(warnings)
    if _has_errors(findings):
        raise typer.Exit(code=1)

    try:
        data = build_behavior_coverage(
            features_dir=features,
            tests_dir=tests,
            feature_path=feature,
        )
        if output_format == "json":
            rendered = _dump_json(data)
            output_path = json_output or out
            if output_path is None:
                typer.echo(rendered)
            else:
                write_coverage_json(data, output_path)
                typer.echo(f"Wrote behavior coverage to {output_path}")
        elif output_format == "text":
            rendered = render_coverage_text(data, show=show)
            if out is None:
                typer.echo(rendered)
            else:
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(rendered + "\n", encoding="utf-8")
                typer.echo(f"Wrote behavior coverage to {out}")
        elif output_format == "markdown":
            rendered = render_coverage_markdown(data, show=show)
            if out is None:
                typer.echo(rendered)
            else:
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(rendered + "\n", encoding="utf-8")
                typer.echo(f"Wrote behavior coverage to {out}")
        else:
            typer.echo(
                "Unsupported --format: "
                f"{output_format}; expected json, text, or markdown.",
                err=True,
            )
            raise typer.Exit(code=1)
    except ValueError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    if _coverage_failed(data):
        raise typer.Exit(code=1)


@behavior_app.command("mappings")
def behavior_mappings(
    tests: Annotated[Path, typer.Option("--tests")] = Path("tests"),
    output_format: Annotated[
        str,
        typer.Option("--format", help="Output format: text or json."),
    ] = "text",
) -> None:
    """List explicit SpecWeave pytest mappings discovered from tests."""
    from specweave.behavior.coverage import (
        build_behavior_mapping_inventory,
        render_mapping_inventory_text,
    )

    data = build_behavior_mapping_inventory(tests_dir=tests)
    if output_format == "json":
        typer.echo(_dump_json(data))
        return
    if output_format != "text":
        typer.echo(
            f"Unsupported --format: {output_format}; expected text or json.",
            err=True,
        )
        raise typer.Exit(code=1)
    typer.echo(render_mapping_inventory_text(data))


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
    feature: Annotated[Path | None, typer.Option("--feature")] = None,
    tests: Annotated[Path, typer.Option("--tests")] = Path("tests"),
    output_format: Annotated[str, typer.Option("--format")] = "json",
    show: Annotated[str, typer.Option("--show")] = "all",
    json_output: Annotated[Path | None, typer.Option("--json")] = None,
    out: Annotated[Path | None, typer.Option("--out")] = None,
) -> None:
    """Compatibility alias for ``specweave behavior coverage``."""

    behavior_coverage(
        features=features,
        feature=feature,
        tests=tests,
        output_format=output_format,
        show=show,
        json_output=json_output,
        out=out,
    )


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


@app.command("trace")
def trace_command(
    target: str,
    format_name: Annotated[str, typer.Option("--format")] = "json",
    features: Annotated[Path, typer.Option("--features")] = Path(
        "specs/behavior/features"
    ),
    tests: Annotated[Path, typer.Option("--tests")] = Path("tests"),
    evidence: Annotated[Path, typer.Option("--evidence")] = Path(".specweave/evidence"),
    taskledger_mappings: Annotated[Path, typer.Option("--taskledger-mappings")] = Path(
        ".specweave/mappings/taskledger"
    ),
) -> None:
    """Emit a normalized behavior-centered trace bundle."""

    from specweave.trace import build_trace_bundle

    if format_name != "json":
        typer.echo("Only --format json is supported.", err=True)
        raise typer.Exit(code=1)
    typer.echo(
        _dump_json(
            build_trace_bundle(
                target,
                features_dir=features,
                tests_dir=tests,
                evidence_dir=evidence,
                taskledger_mappings=taskledger_mappings,
            )
        )
    )


@combi_app.command("check")
def combi_check(
    features: Annotated[Path, typer.Option("--features")] = Path(
        "specs/behavior/features"
    ),
    tests: Annotated[Path, typer.Option("--tests")] = Path("tests"),
    taskledger_mappings: Annotated[Path, typer.Option("--taskledger-mappings")] = Path(
        ".specweave/mappings/taskledger"
    ),
    evidence: Annotated[Path, typer.Option("--evidence")] = Path(".specweave/evidence"),
    archledger: Annotated[Path, typer.Option("--archledger")] = Path(".archledger"),
    json_path: Annotated[Path | None, typer.Option("--json")] = None,
    strict: Annotated[bool, typer.Option("--strict")] = False,
) -> None:
    """Audit SpecWeave links without mutating external ledgers."""

    from specweave.integrations.combi import run_combi_check

    result = run_combi_check(
        features_dir=features,
        tests_dir=tests,
        taskledger_mappings=taskledger_mappings,
        evidence_dir=evidence,
        archledger_dir=archledger,
    )
    if json_path is not None:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(_dump_json(result) + "\n", encoding="utf-8")
    typer.echo(
        "Combi check: "
        f"{result['summary']['scenario_count']} scenarios, "
        f"{result['summary']['gap_count']} gaps"
    )
    for gap in result["gaps"]:
        ref = f" {gap['ref']}" if gap.get("ref") else ""
        typer.echo(f"{gap['severity'].upper()} {gap['code']}{ref}: {gap['message']}")
    if strict and result["summary"]["error_count"]:
        raise typer.Exit(code=1)


# --- helpers ---------------------------------------------------------------


def _dump_json(data: object) -> str:
    import json

    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)


def _task_id(report):  # type: ignore[no-untyped-def]
    from specweave.integrations.taskledger import task_id_from_report

    return task_id_from_report(report)


@app.command("convert")
def convert(
    ctx: typer.Context,
    paths: Annotated[
        list[Path] | None,
        typer.Argument(help="Feature file(s) or directories to convert."),
    ] = None,
    all_features: Annotated[
        bool,
        typer.Option(
            "--all",
            help=(
                "Convert all configured behavior features under the configured "
                "features directory."
            ),
        ),
    ] = False,
    out: Annotated[
        Path | None, typer.Option("--out", help="Output feature path.")
    ] = None,
    to_format: Annotated[
        str | None,
        typer.Option("--to", help="Target format: markdown or classic."),
    ] = None,
    from_format: Annotated[
        str,
        typer.Option("--from", help="Source format: auto, markdown, or classic."),
    ] = "auto",
    force: Annotated[bool, typer.Option("--force")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
    replace_source: Annotated[
        bool,
        typer.Option(
            "--replace-source/--keep-source",
            help=(
                "Delete converted classic source files after successful "
                "non-dry-run conversion."
            ),
        ),
    ] = False,
    validate: Annotated[
        bool,
        typer.Option(
            "--validate/--no-validate", help="Validate with gherkin-official."
        ),
    ] = True,
) -> None:
    """Convert classic .feature and Markdown .feature.md files."""
    from specweave.gherkin.convert import convert_feature_file, convert_feature_files

    cli_ctx: CliContext = ctx.obj
    resolved_paths = list(paths or [])
    if all_features:
        resolved_paths.append(cli_ctx.config.paths.features_dir)
    if not resolved_paths:
        typer.echo("Provide at least one feature path or use --all.", err=True)
        raise typer.Exit(code=1)

    batch_mode = (
        all_features
        or len(resolved_paths) > 1
        or any(path.is_dir() for path in resolved_paths)
    )
    if batch_mode and out is not None:
        typer.echo("--out is supported only for single-file conversion.", err=True)
        raise typer.Exit(code=1)

    try:
        if batch_mode:
            result = convert_feature_files(
                paths=resolved_paths,
                target_format=to_format,
                source_format=from_format,
                force=force,
                dry_run=dry_run,
                validate=validate,
                replace_source=replace_source,
                config=cli_ctx.config,
            )
        else:
            feature = resolved_paths[0]
            result = convert_feature_file(
                source_path=feature,
                out_path=out,
                target_format=to_format,
                source_format=from_format,
                force=force,
                dry_run=dry_run,
                validate=validate,
                config=cli_ctx.config,
            )
            deletable = (
                replace_source
                and result["source_format"] == "classic"
                and result["target_format"] == "markdown"
                and result["source_path"] != result["output_path"]
            )
            result["deleted_source"] = False
            if dry_run and deletable:
                result["would_delete_source"] = True
            elif deletable:
                Path(result["source_path"]).unlink()
                result["deleted_source"] = True
    except ValueError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=3) from exc

    if cli_ctx.json_output:
        typer.echo(_dump_json(result))
    else:
        if batch_mode:
            summary = result["summary"]
            typer.echo(
                f"{result['status']}: "
                f"{summary['created']} created, "
                f"{summary['updated']} updated, "
                f"{summary['unchanged']} unchanged, "
                f"{summary['errors']} errors"
            )
            if summary["deleted_sources"]:
                typer.echo(f"deleted sources: {summary['deleted_sources']}")
            for error in result["errors"]:
                typer.echo(
                    "ERROR "
                    f"{error['source_path']} -> {error['output_path']} "
                    f"{error['error']}"
                )
        else:
            typer.echo(f"{result['status']}: {result['output_path']}")
            typer.echo(f"{result['source_format']} -> {result['target_format']}")
            if result.get("deleted_source"):
                typer.echo(f"deleted source: {result['source_path']}")
            elif result.get("would_delete_source"):
                typer.echo(f"would delete source: {result['source_path']}")
    if batch_mode and result["errors"]:
        raise typer.Exit(code=3)


# --- review subcommands ----------------------------------------------------


@review_app_cli.command("specs")
def review_specs(
    ctx: typer.Context,
) -> None:
    """Review behavior specs for gaps and convention issues."""
    from specweave.review import run_review

    cli_ctx: CliContext = ctx.obj
    result = run_review(config=cli_ctx.config)
    if cli_ctx.json_output:
        typer.echo(_dump_json(result))
    else:
        summary = result["summary"]
        status = result["status"]
        typer.echo(
            f"SpecWeave review: {status}\n"
            f"features: {summary['features']}, "
            f"scenarios: {summary['scenarios']}, "
            f"bound: {summary['bound']}, "
            f"missing bindings: {summary['missing_bindings']}"
        )
        warnings_count = summary.get("warnings", 0)
        errors_count = summary.get("errors", 0)
        if warnings_count or errors_count:
            typer.echo(f"warnings: {warnings_count}, errors: {errors_count}")
        typer.echo("")
        for finding in result.get("findings", []):
            level = finding.get("level", "info").upper()
            code = finding.get("code", "")
            path = finding.get("path", "")
            scenario = finding.get("scenario", "")
            message = finding.get("message", "")
            parts = [level, code, path]
            if scenario:
                parts.append(scenario)
            parts.append(message)
            typer.echo(" ".join(parts))
    if result["status"] != "passed":
        raise typer.Exit(code=1)


# --- create subcommands ----------------------------------------------------


@create_app.command("gherkin")
def create_gherkin(
    ctx: typer.Context,
    from_tests: Annotated[list[Path], typer.Option("--from-tests")],
    out: Annotated[Path, typer.Option("--out")] = Path("specs/behavior/features"),
    group_by: Annotated[str, typer.Option("--group-by")] = "file",
    mode: Annotated[str, typer.Option("--mode")] = "create",
    force: Annotated[bool, typer.Option("--force")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
) -> None:
    """Create or update .feature files from existing pytest tests."""
    from specweave.translate.pytest_to_gherkin import generate_gherkin_from_tests

    cli_ctx: CliContext = ctx.obj
    result = generate_gherkin_from_tests(
        test_paths=from_tests,
        out_dir=out,
        group_by=group_by,
        mode=mode,
        force=force,
        dry_run=dry_run,
        config=cli_ctx.config,
    )
    if cli_ctx.json_output:
        typer.echo(_dump_json(result))
    else:
        for item in result.get("results", []):
            status = item["status"]
            path = item["feature_path"]
            typer.echo(f"{status}: {path}")
        for w in result.get("warnings", []):
            typer.echo(f"Warning: {w}")
    if result.get("errors"):
        raise typer.Exit(code=1)


@app.command("update")
def update_specs(
    ctx: typer.Context,
    from_tests: Annotated[list[Path], typer.Option("--from-tests")],
    out: Annotated[Path, typer.Option("--out")] = Path("specs/behavior/features"),
) -> None:
    """Alias for ``create gherkin --mode update``."""
    create_gherkin(
        ctx=ctx,
        from_tests=from_tests,
        out=out,
        group_by="file",
        mode="update",
        force=False,
        dry_run=False,
    )


@create_app.command("feature")
def create_feature(
    ctx: typer.Context,
    area: Annotated[str, typer.Option("--area")],
    title: Annotated[str, typer.Option("--title")],
    scenario: Annotated[str, typer.Option("--scenario")],
    given: Annotated[str, typer.Option("--given")],
    when: Annotated[str, typer.Option("--when")],
    then: Annotated[str, typer.Option("--then")],
    rule: Annotated[str | None, typer.Option("--rule")] = None,
    out: Annotated[Path | None, typer.Option("--out")] = None,
    force: Annotated[bool, typer.Option("--force")] = False,
) -> None:
    """Create a new Gherkin feature file from structured inputs."""
    import re

    from specweave.gherkin.model import Feature, Rule, Scenario, Step
    from specweave.gherkin.writer import write_feature

    cli_ctx: CliContext = ctx.obj
    feature_slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    scenario_slug = re.sub(r"[^a-z0-9]+", "-", scenario.lower()).strip("-")
    rule_slug = re.sub(r"[^a-z0-9]+", "-", (rule or title).lower()).strip("-")

    feature_tags = (f"area-{area}", f"feature-{feature_slug}")
    rule_tags = (f"rule-{rule_slug}",)
    scenario_tags = (f"bdd-{feature_slug}-{scenario_slug}",)

    s = Scenario(
        title=scenario,
        steps=(
            Step(keyword="Given", text=given),
            Step(keyword="When", text=when),
            Step(keyword="Then", text=then),
        ),
        tags=scenario_tags,
        keyword=cli_ctx.config.gherkin.default_scenario_keyword,
    )
    r = Rule(title=rule or title, scenarios=(s,), tags=rule_tags)
    f = Feature(title=title, rules=(r,), tags=feature_tags)

    feature_text = write_feature(
        f, document_format=cli_ctx.config.gherkin.document_format
    )
    if out is None:
        features_dir = cli_ctx.config.paths.features_dir
        out = (
            features_dir
            / area
            / f"{feature_slug}{cli_ctx.config.gherkin.feature_extension}"
        )

    if out.exists() and not force:
        typer.echo(f"Error: {out} already exists. Use --force to overwrite.", err=True)
        raise typer.Exit(code=3)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(feature_text, encoding="utf-8")

    if cli_ctx.json_output:
        typer.echo(
            _dump_json(
                {
                    "schema_version": 1,
                    "command": "create feature",
                    "status": "created",
                    "feature_path": str(out),
                    "feature_id": f"feature-{feature_slug}",
                    "scenario_ids": [f"bdd-{feature_slug}-{scenario_slug}"],
                    "warnings": [],
                }
            )
        )
    else:
        typer.echo(f"Created feature at {out}")


@create_app.command("plan")
def create_plan(
    ctx: typer.Context,
    feature: Annotated[Path, typer.Option("--feature")],
    out: Annotated[Path, typer.Option("--out")] = Path("plan.md"),
) -> None:
    """Create a deterministic implementation plan from a feature file."""
    from specweave.planning import create_plan as _create_plan

    cli_ctx: CliContext = ctx.obj
    _create_plan(feature_path=feature, out_path=out, config=cli_ctx.config)
    if cli_ctx.json_output:
        typer.echo(
            _dump_json(
                {
                    "schema_version": 1,
                    "command": "create plan",
                    "status": "created",
                    "plan_path": str(out),
                }
            )
        )
    else:
        typer.echo(f"Wrote plan to {out}")


@create_app.command("taskledger-task")
def create_taskledger_task(
    ctx: typer.Context,
    feature: Annotated[Path, typer.Option("--feature")],
    out: Annotated[Path, typer.Option("--out")] = Path(
        ".specweave/mappings/taskledger/draft.json"
    ),
) -> None:
    """Create a Taskledger task draft JSON from a feature file."""
    from specweave.planning import create_taskledger_draft

    cli_ctx: CliContext = ctx.obj
    create_taskledger_draft(feature_path=feature, out_path=out, config=cli_ctx.config)
    if cli_ctx.json_output:
        typer.echo(
            _dump_json(
                {
                    "schema_version": 1,
                    "command": "create taskledger-task",
                    "status": "created",
                    "draft_path": str(out),
                }
            )
        )
    else:
        typer.echo(f"Wrote Taskledger task draft to {out}")
