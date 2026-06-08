"""CLI context object shared across all SpecWeave commands."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from specweave.config import SpecWeaveConfig, load_config


@dataclass(frozen=True)
class CliContext:
    """Resolved context attached to ``typer.Context.obj``."""

    config_path: Path | None
    config: SpecWeaveConfig
    json_output: bool


def build_cli_context(
    config_path: Path | None,
    json_output: bool,
) -> CliContext:
    """Build a ``CliContext`` from CLI flags."""
    config = load_config(config_path)
    return CliContext(
        config_path=config_path,
        config=config,
        json_output=json_output,
    )
