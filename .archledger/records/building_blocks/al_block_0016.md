---
schema_version: 2
id: al_block_0016
type: black_box
title: "Behavior Workflow"
status: proposed
section: building_block_view
level: 2
parent: al_block_0013
order: 30
date: "2026-06-08"
diagram: null
quality_characteristics: []
tags: []
body_format: markdown
created_at: "2026-06-08T19:08:12Z"
updated_at: "2026-06-08T19:08:12Z"
source_refs:
  - specweave/behavior/
  - specweave/behavior/common.py
  - specweave/behavior/index.py
  - specweave/behavior/generate.py
  - specweave/behavior/coverage.py
  - specweave/behavior/reporting.py
---

## Responsibility

Orchestrates the canonical behavior workflow: lint specs, generate index and
manifest, generate plain pytest skeletons, check static coverage, and import
pytest/JUnit reports into evidence JSON.

## Key files

- `specweave/behavior/common.py` — shared paths, slugs, feature identity, scenario IDs
- `specweave/behavior/index.py` (246 lines) — README and manifest generation
- `specweave/behavior/generate.py` — plain pytest skeleton generation
- `specweave/behavior/coverage.py` (538 lines) — static mapping and coverage checks
- `specweave/behavior/reporting.py` (180 lines) — report import and evidence mapping

## Interfaces

- **Inbound:** CLI `behavior` subcommands
- **Outbound:** Gherkin Layer (parsing, linting), Python AST Inspection (coverage), Reports (evidence)
