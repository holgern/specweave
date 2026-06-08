"""Typer command declarations for the SpecWeave CLI."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer(no_args_is_help=True)

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
