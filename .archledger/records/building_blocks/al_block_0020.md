---
schema_version: 2
id: al_block_0020
type: black_box
title: "Integrations"
status: proposed
section: building_block_view
level: 2
parent: al_block_0013
order: 70
date: "2026-06-08"
diagram: null
quality_characteristics: []
tags: []
body_format: markdown
created_at: "2026-06-08T19:08:12Z"
updated_at: "2026-06-08T19:08:12Z"
source_refs:
  - specweave/integrations/
  - specweave/integrations/taskledger.py
  - specweave/integrations/archledger.py
  - specweave/integrations/combi.py
---

## Responsibility

File-based exchange with Taskledger and Archledger, plus cross-ledger
integration auditing. SpecWeave never calls Taskledger or Archledger APIs;
all exchange is through local JSON and Markdown files.

## Key files

- `specweave/integrations/taskledger.py` (184 lines) — task-BDD JSON import,
  evidence JSON export, `task_id_from_report()`
- `specweave/integrations/archledger.py` — candidate markdown rendering from
  feature + `@bdd-*`
- `specweave/integrations/combi.py` — `run_combi_check()` cross-ledger audit

## Interfaces

- **Inbound:** CLI `archledger`, `behavior import-taskledger`, `combi check`, `trace`
- **Outbound:** Writes JSON (Taskledger) and Markdown (Archledger) to filesystem
- **Boundary:** Never imports Taskledger or Archledger as Python packages
