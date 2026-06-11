"""Typer command declarations for the SpecWeave CLI."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from specweave.cli_context import CliContext, build_cli_context

app = typer.Typer(
    no_args_is_help=True,
    help=(
        "SpecWeave keeps product behavior readable and validates it with "
        "plain pytest. Start with 'specweave review golden' for the "
        "full agent-readable health check."
    ),
)


@app.callback()
def main(
    ctx: typer.Context,
    config: Annotated[Path | None, typer.Option("--config")] = None,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Translate product behavior, pytest mappings, and evidence.

    Required input: run inside a SpecWeave project or pass --config.
    Outputs: text by default, JSON with --json for supported commands.
    Exit code: 0 means the requested check passed, 1 means gaps or invalid input.
    Next step: run 'specweave review golden' to diagnose release readiness.
    """
    ctx.obj = build_cli_context(config_path=config, json_output=json_output)


# Sub-app for behaviour-first commands.
behavior_app = typer.Typer(
    no_args_is_help=True,
    help="Work with canonical behaviour specs and plain pytest enforcement.",
)
app.add_typer(behavior_app, name="behaviour")
app.add_typer(behavior_app, name="behavior")

# Sub-app for BDD conversion commands.
bdd_app = typer.Typer(
    no_args_is_help=True, help="Convert between task-BDD JSON and feature files."
)
app.add_typer(bdd_app, name="bdd")

specifications_app = typer.Typer(
    no_args_is_help=True,
    help="Work with specification documents and requirement traceability.",
)
app.add_typer(specifications_app, name="specifications")

sdd_app = typer.Typer(
    no_args_is_help=True,
    help="Short alias for specification document commands.",
)
app.add_typer(sdd_app, name="sdd")

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
    """Explain pytest files as candidate behavior specs.

    Required input: one or more Python test files.
    Output: candidate behavior text for authoring or mapping decisions.
    Exit code: 0 means inputs were read, 1 means an input cannot be processed.
    Next step: create or map product scenarios, then run review coverage both ways.
    """
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
    spelling: Annotated[str, typer.Option("--spelling")] = "behaviour",
    mode: Annotated[str, typer.Option("--mode")] = "behaviour",
    upgrade_layout: Annotated[bool, typer.Option("--upgrade-layout")] = False,
    force: Annotated[bool, typer.Option("--force")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
) -> None:
    """Initialize a SpecWeave project configuration and directory layout."""
    from specweave.init import init_result_to_dict, run_init

    cli_ctx: CliContext = ctx.obj
    if public_config:
        config_path = Path("specweave.toml")
    elif cli_ctx.config_path is not None:
        config_path = cli_ctx.config_path
    else:
        config_path = Path("specweave.toml")
    try:
        result = run_init(
            config_path=config_path,
            spelling=spelling,
            mode=mode,
            upgrade_layout=upgrade_layout,
            force=force,
            dry_run=dry_run,
        )
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
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
    """Diagnose setup before behavior review.

    Required input: a discovered config or --config path.
    Output: setup findings, paths, and convention warnings.
    Exit code: 0 means setup is usable, 1 means errors remain.
    Next step: run with --fix for missing directories, then 'review golden'.
    """
    from specweave.doctor import run_doctor

    cli_ctx: CliContext = ctx.obj
    result = run_doctor(
        config=cli_ctx.config,
        config_path=cli_ctx.config_path,
        fix=fix,
    )
    if cli_ctx.json_output:
        typer.echo(_dump_json(result))
    else:
        status = result["status"]
        typer.echo(f"SpecWeave doctor: {status}")
        for item in result.get("items", []):
            level = item.get("level", "info")
            typer.echo(f"  {level.upper()}: {item.get('message', '')}")
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


def _required_slug(value: str, option: str) -> str:
    import re

    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        typer.echo(
            f"Error: {option} must contain at least one letter or number.",
            err=True,
        )
        raise typer.Exit(code=1)
    return slug


def _required_option(value: str, option: str, context: str) -> str:
    if not value:
        typer.echo(f"Error: {option} is required {context}.", err=True)
        raise typer.Exit(code=1)
    return value


def _coverage_failed(
    data: dict[str, object], *, include_unmapped_tests: bool = False
) -> bool:
    keys = [
        "missing_bindings",
        "stale_bindings",
        "duplicate_bindings",
        "deprecated_paths",
        "forbidden_pytest_bdd_usages",
    ]
    if include_unmapped_tests:
        keys.append("unmapped_tests")
    return any(bool(data[key]) for key in keys)


def _specifications_root(cli_ctx: CliContext) -> Path:
    if cli_ctx.config.paths.specifications is not None:
        return cli_ctx.config.paths.specifications.root
    return Path("specs/specifications")


def _specifications_readme(cli_ctx: CliContext) -> Path:
    if cli_ctx.config.paths.specifications is not None:
        return cli_ctx.config.paths.specifications.readme
    return Path("specs/specifications/README.md")


def _specifications_manifest(cli_ctx: CliContext) -> Path:
    if cli_ctx.config.paths.specifications is not None:
        return cli_ctx.config.paths.specifications.manifest
    return Path("specs/specifications/manifest.json")


def _specifications_mapping_dir(cli_ctx: CliContext) -> Path:
    if cli_ctx.config.paths.specifications is not None:
        return cli_ctx.config.paths.specifications.mappings_dir
    return Path("specs/specifications/mappings")


def _specifications_evidence_dir(cli_ctx: CliContext) -> Path:
    if cli_ctx.config.paths.specifications is not None:
        return cli_ctx.config.paths.specifications.evidence_dir
    return Path("specs/specifications/evidence")


@behavior_app.command("check")
def behavior_check(
    ctx: typer.Context,
    path: Annotated[Path | None, typer.Argument()] = None,
    strict: Annotated[bool, typer.Option("--strict")] = False,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Lint behavior feature files."""
    from specweave.gherkin.lint import lint_feature_files

    cli_ctx: CliContext = ctx.obj
    target_paths = (path,) if path is not None else (cli_ctx.config.paths.features_dir,)
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
    ctx: typer.Context,
    features: Annotated[Path | None, typer.Option("--features")] = None,
    out: Annotated[Path | None, typer.Option("--out")] = None,
    manifest: Annotated[Path | None, typer.Option("--manifest")] = None,
    tests_dir: Annotated[
        Path | None,
        typer.Option(
            "--tests-dir", "--tests", help="Directory containing pytest tests."
        ),
    ] = None,
) -> None:
    """Generate the behavior Markdown index and manifest."""
    from specweave.behavior.index import write_behavior_index
    from specweave.gherkin.lint import collect_feature_files, lint_feature_files

    cli_ctx: CliContext = ctx.obj
    resolved_features = features or cli_ctx.config.paths.features_dir
    resolved_out = out or cli_ctx.config.paths.behavior_readme
    resolved_manifest = manifest or cli_ctx.config.paths.manifest
    resolved_tests_dir = tests_dir or cli_ctx.config.paths.tests_dir

    findings = lint_feature_files(
        collect_feature_files((resolved_features,)),
        require_scenario_ids=True,
    )
    warnings = [finding for finding in findings if finding.level == "warning"]
    if warnings:
        _print_findings(warnings)
    if _has_errors(findings):
        raise typer.Exit(code=1)

    index_path, manifest_path = write_behavior_index(
        features_dir=resolved_features,
        out=resolved_out,
        manifest_path=resolved_manifest,
        tests_dir=resolved_tests_dir,
    )
    typer.echo(f"Wrote behavior index to {index_path}")
    typer.echo(f"Wrote behavior manifest to {manifest_path}")


@behavior_app.command("generate-tests")
def behavior_generate_tests(
    ctx: typer.Context,
    feature: Annotated[Path | None, typer.Argument()] = None,
    features: Annotated[Path | None, typer.Option("--features")] = None,
    out: Annotated[Path | None, typer.Option("--out")] = None,
    tests_dir: Annotated[Path | None, typer.Option("--tests-dir")] = None,
) -> None:
    """Generate plain pytest skeletons from behavior feature files."""
    from specweave.behavior.generate import generate_from_paths

    if feature is not None and features is not None:
        typer.echo("Use either a feature argument or --features, not both.", err=True)
        raise typer.Exit(code=1)

    cli_ctx: CliContext = ctx.obj
    resolved_features = features or (
        cli_ctx.config.paths.features_dir if feature is None else None
    )
    resolved_tests_dir = tests_dir or cli_ctx.config.paths.tests_dir
    outputs = generate_from_paths(
        feature_path=feature,
        features_dir=resolved_features,
        out=out,
        tests_dir=resolved_tests_dir,
    )
    for path in outputs:
        typer.echo(f"Wrote plain pytest skeleton to {path}")


@behavior_app.command("coverage")
def behavior_coverage(
    ctx: typer.Context,
    features: Annotated[Path | None, typer.Option("--features")] = None,
    feature: Annotated[
        Path | None,
        typer.Option("--feature", help="Limit the report to one feature file."),
    ] = None,
    tests: Annotated[Path | None, typer.Option("--tests")] = None,
    view: Annotated[
        str,
        typer.Option("--view", help="View: feature, test, or both."),
    ] = "feature",
    test_file: Annotated[
        Path | None,
        typer.Option("--test-file", help="Limit the pytest-side report to one file."),
    ] = None,
    output_format: Annotated[
        str,
        typer.Option("--format", help="Output format: json, text, or markdown."),
    ] = "json",
    show: Annotated[
        str,
        typer.Option(
            "--show",
            help=(
                "Display filter: all, gaps, missing, unmapped, bound, stale, "
                "waived, or duplicate."
            ),
        ),
    ] = "all",
    suggestions: Annotated[
        bool,
        typer.Option("--suggestions/--no-suggestions"),
    ] = True,
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

    cli_ctx: CliContext = ctx.obj
    resolved_features = features or cli_ctx.config.paths.features_dir
    resolved_tests = tests or cli_ctx.config.paths.tests_dir
    lint_target = feature or resolved_features
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
            features_dir=resolved_features,
            tests_dir=resolved_tests,
            feature_path=feature,
            test_file=test_file,
            mapping_dir=cli_ctx.config.paths.mapping_dir,
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
            rendered = render_coverage_text(
                data,
                view=view,
                show=show,
                suggestions=suggestions,
            )
            if out is None:
                typer.echo(rendered)
            else:
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(rendered + "\n", encoding="utf-8")
                typer.echo(f"Wrote behavior coverage to {out}")
        elif output_format == "markdown":
            rendered = render_coverage_markdown(
                data,
                view=view,
                show=show,
                suggestions=suggestions,
            )
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

    if _coverage_failed(data, include_unmapped_tests=view in {"test", "both"}):
        raise typer.Exit(code=1)


@behavior_app.command("mappings")
def behavior_mappings(
    ctx: typer.Context,
    tests: Annotated[Path | None, typer.Option("--tests")] = None,
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

    cli_ctx: CliContext = ctx.obj
    resolved_tests = tests or cli_ctx.config.paths.tests_dir
    data = build_behavior_mapping_inventory(tests_dir=resolved_tests)
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


@behavior_app.command("autolink")
def behavior_autolink(
    ctx: typer.Context,
    features: Annotated[Path | None, typer.Option("--features")] = None,
    tests: Annotated[Path | None, typer.Option("--tests")] = None,
    strategy: Annotated[str, typer.Option("--strategy")] = "generated-id",
    apply: Annotated[bool, typer.Option("--apply")] = False,
    output_format: Annotated[str, typer.Option("--format")] = "text",
    out: Annotated[Path | None, typer.Option("--out")] = None,
    allow_non_generated: Annotated[bool, typer.Option("--allow-non-generated")] = False,
    max_ambiguity: Annotated[int, typer.Option("--max-ambiguity")] = 0,
    check: Annotated[bool, typer.Option("--check")] = False,
    rewrite_duplicates: Annotated[bool, typer.Option("--rewrite-duplicates")] = False,
) -> None:
    """Plan or apply explicit mappings for generated behavior scenarios."""
    from specweave.behavior.autolink import (
        autolink_generated_ids,
        autolink_result_to_dict,
        render_autolink_text,
    )

    if strategy != "generated-id":
        typer.echo("Unsupported --strategy: expected generated-id.", err=True)
        raise typer.Exit(code=1)
    if output_format not in {"text", "json"}:
        typer.echo("Unsupported --format: expected text or json.", err=True)
        raise typer.Exit(code=1)

    cli_ctx: CliContext = ctx.obj
    result = autolink_generated_ids(
        features=features or cli_ctx.config.paths.features_dir,
        tests=tests or cli_ctx.config.paths.tests_dir,
        apply=apply,
        allow_non_generated=allow_non_generated,
        rewrite_duplicates=rewrite_duplicates,
    )
    rendered = (
        _dump_json(autolink_result_to_dict(result))
        if output_format == "json"
        else render_autolink_text(result)
    )
    if out is None:
        typer.echo(rendered)
    else:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered + "\n", encoding="utf-8")
        typer.echo(f"Wrote behavior autolink report to {out}")
    if result.summary["ambiguous"] > max_ambiguity:
        raise typer.Exit(code=1)
    if check and result.summary["planned"]:
        raise typer.Exit(code=1)


@behavior_app.command("refresh")
def behavior_refresh(
    ctx: typer.Context,
    coverage: Annotated[bool, typer.Option("--coverage")] = False,
    mappings: Annotated[bool, typer.Option("--mappings")] = False,
    index: Annotated[bool, typer.Option("--index")] = False,
) -> None:
    """Refresh common behavior reports using configured paths."""
    from specweave.behavior.coverage import (
        build_behavior_coverage,
        build_behavior_mapping_inventory,
        render_coverage_markdown,
    )
    from specweave.behavior.index import write_behavior_index

    cli_ctx: CliContext = ctx.obj
    paths = cli_ctx.config.paths
    if not any((coverage, mappings, index)):
        coverage = mappings = index = True
    if coverage:
        data = build_behavior_coverage(
            features_dir=paths.features_dir,
            tests_dir=paths.tests_dir,
            mapping_dir=paths.mapping_dir,
        )
        out = paths.reports_state_dir / "coverage-gaps.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            render_coverage_markdown(data, view="both", show="gaps") + "\n",
            encoding="utf-8",
        )
        typer.echo(f"Wrote behavior coverage to {out}")
    if mappings:
        data = build_behavior_mapping_inventory(tests_dir=paths.tests_dir)
        out = paths.reports_state_dir / "mappings.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(_dump_json(data) + "\n", encoding="utf-8")
        typer.echo(f"Wrote behavior mappings to {out}")
    if index:
        index_path, manifest_path = write_behavior_index(
            features_dir=paths.features_dir,
            out=paths.behavior_readme,
            manifest_path=paths.manifest,
            tests_dir=paths.tests_dir,
        )
        typer.echo(f"Wrote behavior index to {index_path}")
        typer.echo(f"Wrote behavior manifest to {manifest_path}")


@behavior_app.command("import-report")
def behavior_import_report(
    ctx: typer.Context,
    report: Annotated[Path, typer.Argument(help="Runner report to import.")],
    fmt: Annotated[str, typer.Option("--format")] = "junit-xml",
    out: Annotated[Path | None, typer.Option("--out")] = None,
    tests_dir: Annotated[Path, typer.Option("--tests-dir")] = Path("tests"),
    manifest: Annotated[Path, typer.Option("--manifest")] = Path(
        "specs/behaviour/manifest.json"
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

    cli_ctx: CliContext = ctx.obj
    payload = import_pytest_report(report, tests_dir=tests_dir, manifest_path=manifest)
    target = out or (
        cli_ctx.config.paths.evidence_dir / f"{report.stem}.pytest-evidence.json"
    )
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


@specifications_app.command("check")
def specifications_check(
    ctx: typer.Context,
    path: Annotated[Path | None, typer.Argument()] = None,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Lint specification Markdown files."""
    from specweave.specifications.lint import lint_specification_files

    cli_ctx: CliContext = ctx.obj
    target = path or _specifications_root(cli_ctx)
    findings = lint_specification_files(
        [target],
        require_verification=(
            cli_ctx.config.specifications.require_verification
            if cli_ctx.config.specifications is not None
            else True
        ),
    )
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
        for finding in findings:
            location = finding.path
            if finding.line is not None:
                location = f"{location}:{finding.line}"
            typer.echo(
                f"{finding.level.upper()} {finding.code} {location} {finding.message}"
            )
    if any(finding.level == "error" for finding in findings):
        raise typer.Exit(code=1)


@specifications_app.command("index")
def specifications_index(
    ctx: typer.Context,
    root: Annotated[Path | None, typer.Option("--root")] = None,
    out: Annotated[Path | None, typer.Option("--out")] = None,
    manifest: Annotated[Path | None, typer.Option("--manifest")] = None,
) -> None:
    """Generate the specifications Markdown index and manifest."""
    from specweave.specifications.index import write_specification_index
    from specweave.specifications.lint import lint_specification_files

    cli_ctx: CliContext = ctx.obj
    resolved_root = root or _specifications_root(cli_ctx)
    resolved_out = out or _specifications_readme(cli_ctx)
    resolved_manifest = manifest or _specifications_manifest(cli_ctx)
    findings = lint_specification_files(
        [resolved_root],
        require_verification=(
            cli_ctx.config.specifications.require_verification
            if cli_ctx.config.specifications is not None
            else True
        ),
    )
    errors = [finding for finding in findings if finding.level == "error"]
    for finding in findings:
        if finding.level != "warning":
            continue
        location = finding.path
        if finding.line is not None:
            location = f"{location}:{finding.line}"
        typer.echo(
            f"{finding.level.upper()} {finding.code} {location} {finding.message}"
        )
    if errors:
        for finding in errors:
            location = finding.path
            if finding.line is not None:
                location = f"{location}:{finding.line}"
            typer.echo(
                f"{finding.level.upper()} {finding.code} {location} {finding.message}"
            )
        raise typer.Exit(code=1)

    index_path, manifest_path = write_specification_index(
        root=resolved_root,
        out=resolved_out,
        manifest_path=resolved_manifest,
    )
    typer.echo(f"Wrote specifications index to {index_path}")
    typer.echo(f"Wrote specifications manifest to {manifest_path}")


@specifications_app.command("coverage")
def specifications_coverage(
    ctx: typer.Context,
    root: Annotated[Path | None, typer.Option("--root")] = None,
    tests: Annotated[Path | None, typer.Option("--tests")] = None,
    view: Annotated[str, typer.Option("--view")] = "requirement",
    output_format: Annotated[str, typer.Option("--format")] = "json",
    show: Annotated[str, typer.Option("--show")] = "all",
    out: Annotated[Path | None, typer.Option("--out")] = None,
) -> None:
    """Check static coverage between specifications and plain pytest tests."""
    from specweave.specifications.coverage import (
        build_specification_coverage,
        render_specification_coverage_markdown,
        render_specification_coverage_text,
        write_specification_coverage_json,
    )

    cli_ctx: CliContext = ctx.obj
    resolved_root = root or _specifications_root(cli_ctx)
    resolved_tests = tests or cli_ctx.config.paths.tests_dir
    data = build_specification_coverage(
        root=resolved_root,
        tests_dir=resolved_tests,
        mapping_dir=_specifications_mapping_dir(cli_ctx),
    )
    if output_format == "json":
        rendered = _dump_json(data)
        if out is None:
            typer.echo(rendered)
        else:
            write_specification_coverage_json(data, out)
            typer.echo(f"Wrote specifications coverage to {out}")
    elif output_format == "text":
        rendered = render_specification_coverage_text(data, view=view, show=show)
        if out is None:
            typer.echo(rendered)
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(rendered + "\n", encoding="utf-8")
            typer.echo(f"Wrote specifications coverage to {out}")
    elif output_format == "markdown":
        rendered = render_specification_coverage_markdown(data, view=view, show=show)
        if out is None:
            typer.echo(rendered)
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(rendered + "\n", encoding="utf-8")
            typer.echo(f"Wrote specifications coverage to {out}")
    else:
        typer.echo(
            f"Unsupported --format: {output_format}; expected json, text, or markdown.",
            err=True,
        )
        raise typer.Exit(code=1)
    if data["status"] != "passed":
        raise typer.Exit(code=1)


@specifications_app.command("import-report")
def specifications_import_report(
    ctx: typer.Context,
    report: Annotated[Path, typer.Argument(help="Runner report to import.")],
    fmt: Annotated[str, typer.Option("--format")] = "junit-xml",
    out: Annotated[Path | None, typer.Option("--out")] = None,
    tests_dir: Annotated[Path | None, typer.Option("--tests-dir")] = None,
    manifest: Annotated[Path | None, typer.Option("--manifest")] = None,
) -> None:
    """Import a pytest/JUnit report into specifications evidence JSON."""
    from specweave.specifications.reporting import (
        import_pytest_report,
        write_specification_evidence_json,
    )

    if fmt != "junit-xml":
        typer.echo(
            "specifications import-report currently supports only --format junit-xml.",
            err=True,
        )
        raise typer.Exit(code=1)

    cli_ctx: CliContext = ctx.obj
    payload = import_pytest_report(
        report,
        tests_dir=tests_dir or cli_ctx.config.paths.tests_dir,
        manifest_path=manifest or _specifications_manifest(cli_ctx),
    )
    target = out or (
        _specifications_evidence_dir(cli_ctx) / f"{report.stem}.pytest-evidence.json"
    )
    write_specification_evidence_json(payload, target)
    typer.echo(f"Wrote pytest specifications evidence to {target}")
    if payload.get("unmapped"):
        raise typer.Exit(code=1)


# --- compatibility aliases ---------------------------------------------------


@bdd_app.command("check")
def bdd_check_alias(
    ctx: typer.Context,
    path: Annotated[Path | None, typer.Argument()] = None,
    strict: Annotated[bool, typer.Option("--strict")] = False,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Compatibility alias for ``specweave behavior check``."""

    behavior_check(ctx=ctx, path=path, strict=strict, json_output=json_output)


@bdd_app.command("index")
def bdd_index_alias(
    ctx: typer.Context,
    features: Annotated[Path | None, typer.Option("--features")] = None,
    out: Annotated[Path | None, typer.Option("--out")] = None,
    manifest: Annotated[Path | None, typer.Option("--manifest")] = None,
    tests_dir: Annotated[
        Path | None,
        typer.Option(
            "--tests-dir", "--tests", help="Directory containing pytest tests."
        ),
    ] = None,
) -> None:
    """Compatibility alias for ``specweave behavior index``."""

    behavior_index(
        ctx=ctx, features=features, out=out, manifest=manifest, tests_dir=tests_dir
    )


@bdd_app.command("generate-tests")
def bdd_generate_tests_alias(
    ctx: typer.Context,
    feature: Annotated[Path | None, typer.Argument()] = None,
    features: Annotated[Path | None, typer.Option("--features")] = None,
    out: Annotated[Path | None, typer.Option("--out")] = None,
    tests_dir: Annotated[Path | None, typer.Option("--tests-dir")] = None,
) -> None:
    """Compatibility alias for ``specweave behavior generate-tests``."""

    behavior_generate_tests(
        ctx=ctx,
        feature=feature,
        features=features,
        out=out,
        tests_dir=tests_dir,
    )


@bdd_app.command("coverage")
def bdd_coverage_alias(
    ctx: typer.Context,
    features: Annotated[Path | None, typer.Option("--features")] = None,
    feature: Annotated[Path | None, typer.Option("--feature")] = None,
    tests: Annotated[Path | None, typer.Option("--tests")] = None,
    view: Annotated[str, typer.Option("--view")] = "feature",
    test_file: Annotated[Path | None, typer.Option("--test-file")] = None,
    output_format: Annotated[str, typer.Option("--format")] = "json",
    show: Annotated[str, typer.Option("--show")] = "all",
    suggestions: Annotated[
        bool,
        typer.Option("--suggestions/--no-suggestions"),
    ] = True,
    json_output: Annotated[Path | None, typer.Option("--json")] = None,
    out: Annotated[Path | None, typer.Option("--out")] = None,
) -> None:
    """Compatibility alias for ``specweave behavior coverage``."""

    behavior_coverage(
        ctx=ctx,
        features=features,
        feature=feature,
        tests=tests,
        view=view,
        test_file=test_file,
        output_format=output_format,
        show=show,
        suggestions=suggestions,
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


@sdd_app.command("check")
def sdd_check_alias(
    ctx: typer.Context,
    path: Annotated[Path | None, typer.Argument()] = None,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Compatibility alias for ``specweave specifications check``."""

    specifications_check(ctx=ctx, path=path, json_output=json_output)


@sdd_app.command("index")
def sdd_index_alias(
    ctx: typer.Context,
    root: Annotated[Path | None, typer.Option("--root")] = None,
    out: Annotated[Path | None, typer.Option("--out")] = None,
    manifest: Annotated[Path | None, typer.Option("--manifest")] = None,
) -> None:
    """Compatibility alias for ``specweave specifications index``."""

    specifications_index(ctx=ctx, root=root, out=out, manifest=manifest)


@sdd_app.command("coverage")
def sdd_coverage_alias(
    ctx: typer.Context,
    root: Annotated[Path | None, typer.Option("--root")] = None,
    tests: Annotated[Path | None, typer.Option("--tests")] = None,
    view: Annotated[str, typer.Option("--view")] = "requirement",
    output_format: Annotated[str, typer.Option("--format")] = "json",
    show: Annotated[str, typer.Option("--show")] = "all",
    out: Annotated[Path | None, typer.Option("--out")] = None,
) -> None:
    """Compatibility alias for ``specweave specifications coverage``."""

    specifications_coverage(
        ctx=ctx,
        root=root,
        tests=tests,
        view=view,
        output_format=output_format,
        show=show,
        out=out,
    )


@sdd_app.command("import-report")
def sdd_import_report_alias(
    ctx: typer.Context,
    report: Annotated[Path, typer.Argument(help="Runner report to import.")],
    fmt: Annotated[str, typer.Option("--format")] = "junit-xml",
    out: Annotated[Path | None, typer.Option("--out")] = None,
    tests_dir: Annotated[Path | None, typer.Option("--tests-dir")] = None,
    manifest: Annotated[Path | None, typer.Option("--manifest")] = None,
) -> None:
    """Compatibility alias for ``specweave specifications import-report``."""

    specifications_import_report(
        ctx=ctx,
        report=report,
        fmt=fmt,
        out=out,
        tests_dir=tests_dir,
        manifest=manifest,
    )


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
        "specs/behaviour/features"
    ),
    tests: Annotated[Path, typer.Option("--tests")] = Path("tests"),
    evidence: Annotated[Path, typer.Option("--evidence")] = Path(
        "specs/behaviour/evidence"
    ),
    taskledger_mappings: Annotated[Path, typer.Option("--taskledger-mappings")] = Path(
        "specs/behaviour/mappings/taskledger"
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
        "specs/behaviour/features"
    ),
    tests: Annotated[Path, typer.Option("--tests")] = Path("tests"),
    taskledger_mappings: Annotated[Path, typer.Option("--taskledger-mappings")] = Path(
        "specs/behaviour/mappings/taskledger"
    ),
    evidence: Annotated[Path, typer.Option("--evidence")] = Path(
        "specs/behaviour/evidence"
    ),
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


def _specification_coverage_summary(
    coverage: dict[str, object] | None,
) -> dict[str, object]:
    if coverage is None:
        return {"enabled": False}
    return {
        "enabled": True,
        "documents": coverage.get("documents_total", 0),
        "requirements": coverage.get("requirements_total", 0),
        "bound": coverage.get("requirements_bound", 0),
        "missing": len(coverage.get("missing_bindings", [])),
        "pytest_tests": coverage.get("pytest_tests_total", 0),
        "pytest_unmapped": len(coverage.get("unmapped_tests", [])),
        "stale": coverage.get("pytest_mappings_stale", 0),
    }


def _task_id(report):  # type: ignore[no-untyped-def]
    from specweave.integrations.taskledger import task_id_from_report

    return task_id_from_report(report)


# --- review subcommands ----------------------------------------------------


@review_app_cli.command("coverage")
def review_coverage(
    ctx: typer.Context,
    features: Annotated[Path | None, typer.Option("--features")] = None,
    feature: Annotated[
        Path | None,
        typer.Option("--feature", help="Limit the feature-side report to one file."),
    ] = None,
    tests: Annotated[Path | None, typer.Option("--tests")] = None,
    test_file: Annotated[
        Path | None,
        typer.Option("--test-file", help="Limit the pytest-side report to one file."),
    ] = None,
    view: Annotated[str, typer.Option("--view")] = "both",
    show: Annotated[str, typer.Option("--show")] = "gaps",
    output_format: Annotated[str, typer.Option("--format")] = "text",
    out: Annotated[Path | None, typer.Option("--out")] = None,
    suggestions: Annotated[
        bool,
        typer.Option("--suggestions/--no-suggestions"),
    ] = True,
) -> None:
    """Review bidirectional behavior coverage.

    Required input: feature directory and tests directory, defaults come from config.
    Output: feature to pytest gaps and pytest to feature gaps.
    Exit code: 0 means no missing, stale, duplicate, or unmapped pytest gaps.
    Next step: add explicit SpecWeave mappings or demote helper tests with waivers.
    """
    from specweave.behavior.coverage import (
        build_behavior_coverage,
        render_coverage_markdown,
        render_coverage_text,
        write_coverage_json,
    )
    from specweave.gherkin.lint import collect_feature_files, lint_feature_files

    cli_ctx: CliContext = ctx.obj
    resolved_features = features or cli_ctx.config.paths.features_dir
    resolved_tests = tests or cli_ctx.config.paths.tests_dir
    lint_target = feature or resolved_features
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
            features_dir=resolved_features,
            tests_dir=resolved_tests,
            feature_path=feature,
            test_file=test_file,
            mapping_dir=cli_ctx.config.paths.mapping_dir,
        )
        if output_format == "json":
            rendered = _dump_json(data)
            if out is None:
                typer.echo(rendered)
            else:
                write_coverage_json(data, out)
                typer.echo(f"Wrote review coverage to {out}")
        elif output_format == "text":
            rendered = render_coverage_text(
                data,
                view=view,
                show=show,
                suggestions=suggestions,
            )
            if out is None:
                typer.echo(rendered)
            else:
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(rendered + "\n", encoding="utf-8")
                typer.echo(f"Wrote review coverage to {out}")
        elif output_format == "markdown":
            rendered = render_coverage_markdown(
                data,
                view=view,
                show=show,
                suggestions=suggestions,
            )
            if out is None:
                typer.echo(rendered)
            else:
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(rendered + "\n", encoding="utf-8")
                typer.echo(f"Wrote review coverage to {out}")
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

    if _coverage_failed(data, include_unmapped_tests=True):
        raise typer.Exit(code=1)


@review_app_cli.command("golden")
def review_golden(
    ctx: typer.Context,
    out_dir: Annotated[
        Path,
        typer.Option("--out-dir", help="Directory for generated review artifacts."),
    ] = Path("specs/behavior/reports/specweave"),
) -> None:
    """Run the golden-path agent review.

    Aggregates doctor, behavior check, bidirectional coverage, pytest mappings,
    and spec review. Required input: configured project with features and tests.
    Outputs: coverage-gaps.md, mappings.json, review.json, and console summary.
    Exit code: 0 means all gates passed, 1 means the reports contain next steps.
    Next step: fix the first reported gap, then rerun this command.
    """
    from specweave.behavior.coverage import (
        build_behavior_coverage,
        render_coverage_markdown,
    )
    from specweave.behavior.coverage import build_behavior_mapping_inventory
    from specweave.doctor import run_doctor
    from specweave.gherkin.lint import collect_feature_files, lint_feature_files
    from specweave.review import run_review
    from specweave.specifications.coverage import (
        build_specification_coverage,
        render_specification_coverage_markdown,
    )

    cli_ctx: CliContext = ctx.obj
    out_dir.mkdir(parents=True, exist_ok=True)

    doctor_result = run_doctor(
        config=cli_ctx.config,
        config_path=cli_ctx.config_path,
        fix=False,
    )
    feature_files = collect_feature_files((cli_ctx.config.paths.features_dir,))
    lint_findings = lint_feature_files(feature_files, require_scenario_ids=True)
    coverage = build_behavior_coverage(
        features_dir=cli_ctx.config.paths.features_dir,
        tests_dir=cli_ctx.config.paths.tests_dir,
        mapping_dir=cli_ctx.config.paths.mapping_dir,
    )
    mappings = build_behavior_mapping_inventory(tests_dir=cli_ctx.config.paths.tests_dir)
    review_result = run_review(config=cli_ctx.config, mode="both")
    specifications_root = _specifications_root(cli_ctx)
    specification_coverage = None
    if specifications_root.exists():
        specification_coverage = build_specification_coverage(
            root=specifications_root,
            tests_dir=cli_ctx.config.paths.tests_dir,
            mapping_dir=_specifications_mapping_dir(cli_ctx),
        )

    coverage_path = out_dir / "coverage-gaps.md"
    specification_coverage_path = out_dir / "specification-coverage-gaps.md"
    mappings_path = out_dir / "mappings.json"
    review_path = out_dir / "review.json"
    coverage_path.write_text(
        render_coverage_markdown(
            coverage, view="both", show="gaps", suggestions=True
        )
        + "\n",
        encoding="utf-8",
    )
    if specification_coverage is not None:
        specification_coverage_path.write_text(
            render_specification_coverage_markdown(
                specification_coverage, view="both", show="gaps"
            )
            + "\n",
            encoding="utf-8",
        )
    mappings_path.write_text(_dump_json(mappings) + "\n", encoding="utf-8")
    review_path.write_text(_dump_json(review_result) + "\n", encoding="utf-8")

    errors = [finding for finding in lint_findings if finding.level == "error"]
    failed = (
        doctor_result["status"] != "passed"
        or bool(errors)
        or _coverage_failed(coverage, include_unmapped_tests=True)
        or (
            specification_coverage is not None
            and specification_coverage["status"] != "passed"
        )
        or review_result["status"] != "passed"
    )
    if cli_ctx.json_output:
        typer.echo(
            _dump_json(
                {
                    "schema_version": 1,
                    "command": "review golden",
                    "status": "failed" if failed else "passed",
                    "doctor": doctor_result,
                    "behavior_check": {
                        "errors": len(errors),
                        "warnings": sum(
                            1 for finding in lint_findings if finding.level == "warning"
                        ),
                    },
                    "coverage": coverage.get("summary", {}),
                    "mappings": {"mappings_total": mappings.get("mappings_total", 0)},
                    "specification_coverage": _specification_coverage_summary(
                        specification_coverage
                    ),
                    "review": review_result,
                    "outputs": {
                        "coverage": str(coverage_path),
                        "mappings": str(mappings_path),
                        "specification_coverage": str(specification_coverage_path),
                        "review": str(review_path),
                    },
                }
            )
        )
    else:
        typer.echo("SpecWeave golden review: " + ("failed" if failed else "passed"))
        typer.echo(f"doctor: {doctor_result['status']}")
        typer.echo(f"behavior check: errors={len(errors)}")
        typer.echo(
            "coverage: "
            f"scenarios={coverage.get('scenarios_total', 0)} "
            f"missing={len(coverage.get('missing_bindings', []))} "
            f"unmapped={len(coverage.get('unmapped_tests', []))} "
            f"stale={coverage.get('pytest_mappings_stale', 0)}"
        )
        if specification_coverage is not None:
            typer.echo(
                "specification coverage: "
                f"requirements={specification_coverage.get('requirements_total', 0)} "
                f"missing={len(specification_coverage.get('missing_bindings', []))} "
                f"unmapped={len(specification_coverage.get('unmapped_tests', []))} "
                f"stale={specification_coverage.get('pytest_mappings_stale', 0)}"
            )
        typer.echo(
            "mappings: "
            f"{mappings.get('mappings_total', 0)} pytest mappings discovered"
        )
        typer.echo(f"spec review: {review_result['status']}")
        typer.echo(
            "outputs: "
            f"{coverage_path}, {specification_coverage_path}, "
            f"{mappings_path}, {review_path}"
        )

    if failed:
        raise typer.Exit(code=1)

@review_app_cli.command("specs")
def review_specs(
    ctx: typer.Context,
) -> None:
    """Review enabled behavior and specification modes.

    Required input: configured SpecWeave project.
    Output: aggregate counts, findings, and the detailed coverage command.
    Exit code: 0 means no release-blocking gaps, 1 means findings need action.
    Next step: run 'review coverage --view both --show gaps' for mapping detail.
    """
    from specweave.review import run_review

    cli_ctx: CliContext = ctx.obj
    result = run_review(config=cli_ctx.config, mode="both")
    if cli_ctx.json_output:
        typer.echo(_dump_json(result))
    else:
        summary = result["summary"]
        status = result["status"]
        typer.echo(f"SpecWeave review: {status}")
        if "behaviour" in summary:
            behaviour = summary["behaviour"]
            typer.echo(
                "behaviour: "
                f"features={behaviour['features']} "
                f"scenarios={behaviour['scenarios']} "
                f"bound={behaviour['bound']} "
                f"missing={behaviour['missing_bindings']}"
            )
            specifications = summary.get("specifications")
            if specifications is not None:
                typer.echo(
                    "specifications: "
                    f"documents={specifications['documents']} "
                    f"requirements={specifications['requirements']} "
                    f"verified={specifications['verified']} "
                    f"missing={specifications['missing']}"
                )
        else:
            typer.echo(
                f"features: {summary['features']}, "
                f"scenarios: {summary['scenarios']}, "
                f"bound: {summary['bound']}, "
                f"missing bindings: {summary['missing_bindings']}"
            )
            typer.echo(
                f"pytest tests: {summary['pytest_tests']}, "
                f"mapped: {summary['pytest_mapped']}, "
                f"unmapped: {summary['pytest_unmapped']}, "
                f"stale mappings: {summary['stale_bindings']}"
            )
        warnings_count = summary.get("warnings", 0)
        errors_count = summary.get("errors", 0)
        if warnings_count or errors_count:
            typer.echo(f"warnings={warnings_count} errors={errors_count}")
        typer.echo("")
        typer.echo("Run detailed coverage:")
        typer.echo("  specweave review coverage --view both --show gaps")
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


@review_app_cli.command("behaviour")
def review_behaviour(
    ctx: typer.Context,
) -> None:
    """Review only behaviour specs for gaps and convention issues."""
    from specweave.review import run_review

    cli_ctx: CliContext = ctx.obj
    result = run_review(config=cli_ctx.config, mode="behaviour")
    if cli_ctx.json_output:
        typer.echo(_dump_json(result))
    else:
        summary = result["summary"]
        typer.echo(
            f"SpecWeave review: {result['status']}\n"
            f"features: {summary['features']}, "
            f"scenarios: {summary['scenarios']}, "
            f"bound: {summary['bound']}, "
            f"missing bindings: {summary['missing_bindings']}"
        )
        typer.echo(
            f"pytest tests: {summary['pytest_tests']}, "
            f"mapped: {summary['pytest_mapped']}, "
            f"unmapped: {summary['pytest_unmapped']}, "
            f"stale mappings: {summary['stale_bindings']}"
        )
    if result["status"] != "passed":
        raise typer.Exit(code=1)


@review_app_cli.command("bdd")
def review_bdd_alias(ctx: typer.Context) -> None:
    """Compatibility alias for ``specweave review behaviour``."""

    review_behaviour(ctx=ctx)


@review_app_cli.command("specifications")
def review_specifications(ctx: typer.Context) -> None:
    """Review only specification documents for gaps and convention issues."""
    from specweave.review import run_review

    cli_ctx: CliContext = ctx.obj
    result = run_review(config=cli_ctx.config, mode="specifications")
    if cli_ctx.json_output:
        typer.echo(_dump_json(result))
    else:
        summary = result["summary"]
        typer.echo(
            f"SpecWeave review: {result['status']}\n"
            f"documents: {summary['documents']}, "
            f"requirements: {summary['requirements']}, "
            f"verified: {summary['verified']}, "
            f"missing: {summary['missing']}, "
            f"reverse gaps: {summary['reverse_gaps']}"
        )
    if result["status"] != "passed":
        raise typer.Exit(code=1)


@review_app_cli.command("sdd")
def review_sdd_alias(ctx: typer.Context) -> None:
    """Compatibility alias for ``specweave review specifications``."""

    review_specifications(ctx=ctx)


# --- create subcommands ----------------------------------------------------


@create_app.command("gherkin")
def create_gherkin(
    ctx: typer.Context,
    from_tests: Annotated[list[Path], typer.Option("--from-tests")],
    out: Annotated[Path, typer.Option("--out")] = Path("specs/behaviour/features"),
    group_by: Annotated[str | None, typer.Option("--group-by")] = None,
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
        group_by=group_by or cli_ctx.config.generation.group_by,
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
    out: Annotated[Path, typer.Option("--out")] = Path("specs/behaviour/features"),
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
    from_json: Annotated[Path | None, typer.Option("--from-json")] = None,
    area: Annotated[str, typer.Option("--area")] = "",
    title: Annotated[str, typer.Option("--title")] = "",
    scenario: Annotated[str, typer.Option("--scenario")] = "",
    given: Annotated[str, typer.Option("--given")] = "",
    when: Annotated[str, typer.Option("--when")] = "",
    then: Annotated[str, typer.Option("--then")] = "",
    rule: Annotated[str | None, typer.Option("--rule")] = None,
    out: Annotated[Path | None, typer.Option("--out")] = None,
    force: Annotated[bool, typer.Option("--force")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
) -> None:
    """Create a new Gherkin feature file from structured inputs or a JSON draft."""
    import re

    from specweave.gherkin.draft import load_feature_draft
    from specweave.gherkin.model import Feature, Rule, Scenario, Step
    from specweave.gherkin.writer import write_feature

    cli_ctx: CliContext = ctx.obj

    if from_json is not None:
        # JSON draft path
        f = load_feature_draft(from_json)
        feature_slug = re.sub(r"[^a-z0-9]+", "-", f.title.lower()).strip("-")
        # Derive area from tags if present
        area_name = ""
        for tag in f.tags:
            if tag.startswith("area-"):
                area_name = tag[len("area-") :]
                break

        feature_text = write_feature(f)
        if out is None:
            features_dir = cli_ctx.config.paths.features_dir
            out = features_dir / area_name / f"{feature_slug}.feature"

        if out.exists() and not force:
            typer.echo(
                f"Error: {out} already exists. Use --force to overwrite.",
                err=True,
            )
            raise typer.Exit(code=3)

        if not dry_run:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(feature_text, encoding="utf-8")

        # Collect scenario IDs
        scenario_ids: list[str] = []
        for s in f.scenarios:
            for tag in s.tags:
                if tag.startswith("bdd-"):
                    scenario_ids.append(tag)
                    break
        for r in f.rules:
            for s in r.scenarios:
                for tag in s.tags:
                    if tag.startswith("bdd-"):
                        scenario_ids.append(tag)
                        break

        if cli_ctx.json_output:
            typer.echo(
                _dump_json(
                    {
                        "schema_version": 1,
                        "command": "create feature",
                        "status": "dry-run" if dry_run else "created",
                        "feature_path": str(out),
                        "feature_id": f"feature-{feature_slug}",
                        "scenario_ids": scenario_ids,
                        "warnings": [],
                    }
                )
            )
        else:
            status = "Dry-run feature at" if dry_run else "Created feature at"
            typer.echo(f"{status} {out}")
        return

    # Legacy positional path
    title = _required_option(title, "--title", "when --from-json is not used")
    scenario = _required_option(scenario, "--scenario", "when --from-json is not used")
    area_slug = _required_slug(area, "--area")

    feature_slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    scenario_slug = re.sub(r"[^a-z0-9]+", "-", scenario.lower()).strip("-")
    rule_slug = re.sub(r"[^a-z0-9]+", "-", (rule or title).lower()).strip("-")

    feature_tags = (f"area-{area_slug}", f"feature-{feature_slug}")
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

    feature_text = write_feature(f)
    if out is None:
        features_dir = cli_ctx.config.paths.features_dir
        out = features_dir / area_slug / f"{feature_slug}.feature"

    if out.exists() and not force:
        typer.echo(
            f"Error: {out} already exists. Use --force to overwrite.",
            err=True,
        )
        raise typer.Exit(code=3)

    if not dry_run:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(feature_text, encoding="utf-8")

    if cli_ctx.json_output:
        typer.echo(
            _dump_json(
                {
                    "schema_version": 1,
                    "command": "create feature",
                    "status": "dry-run" if dry_run else "created",
                    "feature_path": str(out),
                    "feature_id": f"feature-{feature_slug}",
                    "scenario_ids": [f"bdd-{feature_slug}-{scenario_slug}"],
                    "warnings": [],
                }
            )
        )
    else:
        status = "Dry-run feature at" if dry_run else "Created feature at"
        typer.echo(f"{status} {out}")


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
        "specs/behaviour/mappings/taskledger/draft.json"
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
