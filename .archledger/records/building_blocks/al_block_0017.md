---
schema_version: 2
id: al_block_0017
type: black_box
title: "Report Normalization"
status: proposed
section: building_block_view
level: 2
parent: al_block_0013
order: 40
date: "2026-06-08"
diagram: null
quality_characteristics: []
tags: []
body_format: markdown
created_at: "2026-06-08T19:08:12Z"
updated_at: "2026-06-08T19:08:12Z"
source_refs:
  - specweave/reports/
  - specweave/reports/model.py
  - specweave/reports/normalize.py
  - specweave/reports/cucumber_json.py
  - specweave/reports/junit_xml.py
  - specweave/reports/mapping.py
---

## Responsibility

Parses native runner reports (Cucumber JSON, JUnit XML), normalizes them into a
unified `NormalizedBddReport` model, maps scenario results to `@bdd-*` and
`@ac-*` tags, and assembles fail-closed evidence JSON.

## Key files

- `specweave/reports/model.py` — `ScenarioResult`, `CriterionResult`, `NormalizedBddReport`, status constants
- `specweave/reports/normalize.py` (233 lines) — report normalization pipeline
- `specweave/reports/cucumber_json.py` — Cucumber JSON parser
- `specweave/reports/junit_xml.py` — JUnit XML parser
- `specweave/reports/mapping.py` — tag-based trace extraction, AC coverage summarization

## Interfaces

- **Inbound:** CLI `report` subcommands, Behavior Workflow `import-report`
- **Outbound:** Writes normalized JSON and Taskledger evidence JSON to filesystem
