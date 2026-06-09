---
schema_version: 2
id: al_block_0015
type: black_box
title: "Gherkin Layer"
status: proposed
section: building_block_view
level: 2
parent: al_block_0013
order: 20
date: "2026-06-08"
diagram: null
quality_characteristics: []
tags: []
body_format: markdown
created_at: "2026-06-08T19:08:12Z"
updated_at: "2026-06-08T19:08:12Z"
source_refs:
  - specweave/gherkin/
  - specweave/gherkin/model.py
  - specweave/gherkin/parser.py
  - specweave/gherkin/writer.py
  - specweave/gherkin/lint.py
  - specweave/gherkin/convert.py
  - specweave/gherkin/markdown.py
  - specweave/gherkin/tags.py
  - specweave/gherkin/draft.py
  - specweave/gherkin/official.py
  - specweave/gherkin/validation.py
---

## Responsibility

Owns the Gherkin data model, parsing, writing, linting, format conversion, and
validation. Supports both classic `.feature` and Markdown `.feature.md` formats.
The built-in parser and subset validator work without external dependencies.
The optional `gherkin-official` backend (`pip install specweave[gherkin]`)
provides full Cucumber Gherkin compatibility.

## Key files

- `specweave/gherkin/model.py` — `Feature`, `Rule`, `Scenario`, `Step` frozen dataclasses
- `specweave/gherkin/parser.py` (257 lines) — Gherkin text → `Feature` model
- `specweave/gherkin/writer.py` — `Feature` model → Gherkin text
- `specweave/gherkin/lint.py` (410 lines) — linting, duplicate ID detection, path checks
- `specweave/gherkin/convert.py` (378 lines) — classic ↔ Markdown conversion
- `specweave/gherkin/markdown.py` (463 lines) — Markdown `.feature.md` parser/writer
- `specweave/gherkin/tags.py` — tag parsing/filtering helpers
- `specweave/gherkin/draft.py` — feature draft loading from JSON
- `specweave/gherkin/official.py` — adapter for optional `gherkin-official` parser
- `specweave/gherkin/validation.py` — SpecWeave subset validator (no external deps)

## Interfaces

- **Inbound:** Called by CLI, Behavior Workflow, Translation, and Integrations
- **Outbound:** Pure data transformations; optional `gherkin-official` backend
  (lazy-imported, only when installed)
