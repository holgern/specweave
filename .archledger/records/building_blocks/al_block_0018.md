---
schema_version: 2
id: al_block_0018
type: black_box
title: "Translation Layer"
status: proposed
section: building_block_view
level: 2
parent: al_block_0013
order: 50
date: "2026-06-08"
diagram: null
quality_characteristics: []
tags: []
body_format: markdown
created_at: "2026-06-08T19:08:12Z"
updated_at: "2026-06-08T19:08:12Z"
source_refs:
  - specweave/translate/
  - specweave/translate/pytest_to_gherkin.py
  - specweave/translate/spec_to_code.py
  - specweave/translate/code_to_spec.py
  - specweave/translate/naming.py
---

## Responsibility

Bidirectional translation between Python tests and Gherkin behavior specs:

- **pytest → Gherkin:** Brownfield workflow. Uses AST Inspection to discover
  tests, then generates draft `.feature` files.
- **Gherkin → pytest:** New-feature workflow. Generates plain pytest skeletons
  from canonical feature files.
- **Code → Spec explanation:** Explains Python test files as candidate behavior
  specs.

Also handles step/backend binding for legacy `behave` and `pytest-bdd`
workflows via `specweave/backends/`.

## Key files

- `specweave/translate/pytest_to_gherkin.py` (273 lines) — brownfield generation
- `specweave/translate/spec_to_code.py` — feature drafting and binding
- `specweave/translate/code_to_spec.py` — test explanation
- `specweave/translate/naming.py` — naming conventions
- `specweave/backends/behave.py` — behave step skeleton generation
- `specweave/backends/pytest_bdd.py` — pytest-bdd step skeleton generation

## Interfaces

- **Inbound:** CLI `create gherkin`, `create feature`, `bind`, `explain`
- **Outbound:** Gherkin Layer (writing), Python AST Inspection (reading), backends
