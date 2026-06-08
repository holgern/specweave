---
schema_version: 2
id: al_block_0013
type: white_box
title: "Overall System"
status: proposed
section: building_block_view
level: 1
parent: null
order: 10
date: "2026-06-08"
diagram: null
quality_characteristics: []
tags: []
body_format: markdown
created_at: "2026-06-08T19:08:12Z"
updated_at: "2026-06-08T19:08:12Z"
source_refs:
  - specweave/
---

## Motivation

SpecWeave decomposes into seven primary black boxes, each owning a clear
domain. The decomposition keeps Gherkin parsing separate from behavior
workflow logic, separate from report normalization, and separate from
external integrations.

## Contained building blocks

- **CLI Layer** (al_block_0014) — Typer command dispatch, context, and output formatting
- **Gherkin Layer** (al_block_0015) — Model, parser, writer, linter, and format conversion
- **Behavior Workflow** (al_block_0016) — Index, coverage, test generation, report import
- **Report Normalization** (al_block_0017) — Native report parsing, normalization, evidence assembly
- **Translation Layer** (al_block_0018) — pytest-to-Gherkin, spec-to-code, code-to-spec
- **Python AST Inspection** (al_block_0019) — Static test discovery and mapping extraction
- **Integrations** (al_block_0020) — Taskledger exchange, Archledger candidates, combi check

## Important interfaces

- CLI → all other layers via lazy imports in command handlers
- Behavior Workflow → Gherkin Layer for parsing and linting
- Report Normalization → Gherkin Layer for tag-based mapping
- Translation → Gherkin Layer for writing, AST Inspection for reading
- Integrations → Behavior Workflow, Reports, and Gherkin models
