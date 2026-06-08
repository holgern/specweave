---
schema_version: 2
id: al_block_0014
type: black_box
title: "CLI Layer"
status: proposed
section: building_block_view
level: 2
parent: al_block_0013
order: 10
date: "2026-06-08"
diagram: null
quality_characteristics: []
tags: []
body_format: markdown
created_at: "2026-06-08T19:08:12Z"
updated_at: "2026-06-08T19:08:12Z"
source_refs:
  - specweave/cli.py
  - specweave/cli_context.py
  - specweave/launcher.py
  - specweave/__main__.py
---

## Responsibility

Root Typer application with sub-apps for `behavior`, `bdd`, `report`,
`create`, `review`, and `combi` command groups. Handles root `--config`
(explicit config path) and `--json` (machine-readable output) options.
Constructs `CliContext` with loaded config and JSON-output flag.

## Key files

- `specweave/cli.py` (1321 lines) — all command declarations
- `specweave/cli_context.py` — `CliContext` and `build_cli_context()`
- `specweave/launcher.py` — `main()` entry point
- `specweave/__main__.py` — `python -m specweave` support

## Interfaces

- **Inbound:** Developer invokes `specweave` console script
- **Outbound:** Lazy imports to all other layers from command handlers
- **Output:** Human text to stdout, JSON to stdout when `--json` is set
