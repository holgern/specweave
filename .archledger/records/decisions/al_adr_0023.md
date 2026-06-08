---
schema_version: 2
id: al_adr_0023
type: adr
title: "AST-based test discovery"
status: proposed
section: architecture_decisions
order: 30
date: "2026-06-08"
deciders: []
supersedes: []
related: []
tags: []
body_format: markdown
created_at: "2026-06-08T19:08:19Z"
updated_at: "2026-06-08T19:08:19Z"
source_refs:
  - specweave/python_inspect/ast_reader.py
  - specweave/translate/pytest_to_gherkin.py
---

## Context

Brownfield projects have existing pytest tests that describe behavior
implicitly. SpecWeave needs to infer Gherkin specs from these tests without
requiring manual rewriting.

## Decision

Use Python `ast` module to parse test files statically. Extract test function
names, docstrings, markers, and assert statements. Never execute tests during
discovery.

## Consequences

- **Positive:** Fast, deterministic, safe. Works on any Python file without
  imports or execution. No side effects.
- **Negative:** Cannot capture runtime-only behavior. Inferred Gherkin may be
  low quality for poorly named tests. Marked with `@generated` and
  `@needs-review` tags.

## Alternatives considered

- Runtime introspection: rejected — slow, side effects, non-deterministic.
- Manual spec writing only: rejected — defeats the brownfield workflow purpose.
