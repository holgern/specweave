"""Typer command declarations for the SpecWeave CLI."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer(no_args_is_help=True)


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
    backend: Annotated[str, typer.Option("--backend")] = "behave",
    out: Annotated[Path, typer.Option("--out")] = Path("tests/bdd/steps"),
) -> None:
    """Create missing Python step-definition skeletons."""
    from specweave.translate.spec_to_code import bind_feature

    bind_feature(feature_path, backend, out)


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
