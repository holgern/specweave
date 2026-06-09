---
schema_version: 2
id: al_adr_0027
type: adr
title: "Make gherkin-official an optional dependency"
status: proposed
section: architecture_decisions
order: 70
date: "2026-06-09"
deciders: []
supersedes: []
related: []
tags: []
body_format: markdown
created_at: "2026-06-09T05:02:53Z"
updated_at: "2026-06-09T05:02:53Z"
source_refs:
  - specweave/gherkin/official.py
  - specweave/gherkin/validation.py
  - specweave/gherkin/parser.py
  - pyproject.toml
---

## Context

SpecWeave bundles a built-in Gherkin parser (`specweave/gherkin/parser.py`) that
covers the SpecWeave canonical subset: Feature, Rule, Scenario/Example, and
Given/When/Then/And/But steps. A subset validator
(`specweave/gherkin/validation.py`) rejects unsupported constructs (Background,
Scenario Outline, data tables, doc strings, wildcard `*` steps) without any
external dependency.

The Cucumber reference parser `gherkin-official` provides full Gherkin
compatibility but is not needed for SpecWeave's canonical workflow. Requiring it
as a runtime dependency increases the install footprint for all users.

## Decision

Move `gherkin-official` to an optional extra (`pip install specweave[gherkin]`).
The adapter in `specweave/gherkin/official.py` lazy-imports the library and
raises a clear `ParseError` when it is not installed. The core SpecWeave
workflow (parse, lint, generate, convert, validate) works without it.

## Consequences

- **Positive:** Smaller default install. Only two required runtime dependencies
  (typer, click). Users needing full Cucumber compatibility opt in explicitly.
- **Positive:** The subset validator catches unsupported constructs without
  external dependencies, giving deterministic error messages.
- **Negative:** Users who relied on `gherkin-official` being installed
  automatically must now install `specweave[gherkin]` explicitly.

## Alternatives considered

- Keep `gherkin-official` required: rejected — inflates the dependency tree for
  users who only need the canonical subset.
- Bundle a vendored copy: rejected — maintenance burden, version drift.
- Bundle a vendored copy: rejected — maintenance burden, version drift.
