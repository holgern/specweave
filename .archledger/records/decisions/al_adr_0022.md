---
schema_version: 2
id: al_adr_0022
type: adr
title: "Plain pytest as canonical enforcement"
status: proposed
section: architecture_decisions
order: 20
date: "2026-06-08"
deciders: []
supersedes: []
related: []
tags: []
body_format: markdown
created_at: "2026-06-08T19:08:19Z"
updated_at: "2026-06-08T19:08:19Z"
source_refs:
  - specweave/behavior/generate.py
  - specweave/behavior/coverage.py
  - specweave/python_inspect/ast_reader.py
---

## Context

Existing Python BDD tools (pytest-bdd, behave) couple tests to
step-definition modules and require framework-specific boilerplate. This
creates a barrier to adoption and makes tests dependent on BDD infrastructure.

## Decision

Generate standard `test_*.py` files with `@specweave` markers and
source-mapping comments (`# specweave: scenario=...`). No step definitions
required. Tests are runnable without SpecWeave installed.

## Consequences

- **Positive:** Lower barrier to adoption. Tests work with standard pytest.
  SpecWeave is a development tool, not a test framework dependency.
- **Negative:** Static coverage checks require SpecWeave-specific markers.
  Teams using pytest-bdd or behave need the bridge/legacy path.

## Alternatives considered

- pytest-bdd as canonical: rejected — adds runtime dependency and step-module coupling.
- behave as canonical: rejected — different test runner, more coupling.
