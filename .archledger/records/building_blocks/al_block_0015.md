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
---

## Responsibility

Owns the Gherkin data model, parsing, writing, linting, and format conversion.
Supports both classic `.feature` and Markdown `.feature.md` formats.

## Key files

- `specweave/gherkin/model.py` — `Feature`, `Rule`, `Scenario`, `Step` frozen dataclasses
- `specweave/gherkin/parser.py` (257 lines) — Gherkin text → `Feature` model
- `specweave/gherkin/writer.py` — `Feature` model → Gherkin text
- `specweave/gherkin/lint.py` (410 lines) — linting, duplicate ID detection, path checks
- `specweave/gherkin/convert.py` (378 lines) — classic ↔ Markdown conversion
- `specweave/gherkin/markdown.py` (463 lines) — Markdown `.feature.md` parser/writer
- `specweave/gherkin/tags.py` — tag parsing/filtering helpers
- `specweave/gherkin/draft.py` — feature draft loading from JSON

## Interfaces

- **Inbound:** Called by CLI, Behavior Workflow, Translation, and Integrations
- **Outbound:** Pure data transformations; no external calls
