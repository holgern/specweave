---
schema_version: 2
id: al_block_0019
type: black_box
title: "Python AST Inspection"
status: proposed
section: building_block_view
level: 2
parent: al_block_0013
order: 60
date: "2026-06-08"
diagram: null
quality_characteristics: []
tags: []
body_format: markdown
created_at: "2026-06-08T19:08:12Z"
updated_at: "2026-06-08T19:08:12Z"
source_refs:
  - specweave/python_inspect/
  - specweave/python_inspect/ast_reader.py
  - specweave/python_inspect/assertions.py
---

## Responsibility

Static analysis of Python test files using the `ast` module. Discovers test
functions, extracts `@specweave` markers and source-mapping comments, and
converts assert statements into candidate `Then` clauses.

## Key files

- `specweave/python_inspect/ast_reader.py` (303 lines) — `extract_test_scenarios()`,
  `collect_specweave_tests()`, `SpecweaveTestMapping` dataclass
- `specweave/python_inspect/assertions.py` — `describe_assert()` for
  assertion-to-English rendering

## Interfaces

- **Inbound:** Called by Translation Layer and Behavior Coverage
- **Outbound:** Returns `Scenario` and `SpecweaveTestMapping` objects; no filesystem writes
