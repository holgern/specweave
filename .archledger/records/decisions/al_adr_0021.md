---
schema_version: 2
id: al_adr_0021
type: adr
title: "Tag-based scenario identity"
status: proposed
section: architecture_decisions
order: 10
date: "2026-06-08"
deciders: []
supersedes: []
related: []
tags: []
body_format: markdown
created_at: "2026-06-08T19:08:19Z"
updated_at: "2026-06-08T19:08:19Z"
source_refs:
  - specweave/gherkin/tags.py
  - specweave/behavior/common.py
  - specweave/reports/mapping.py
---

## Context

Scenario titles change frequently during editing. Using them as validation
keys would cause false negatives in evidence mapping and coverage checks.
Teams need stable identifiers that survive renames, restructuring, and
translation between formats.

## Decision

Anchor all validation on `@bdd-*` tags. Use `@ac-*` for acceptance-criteria
linkage. Scenario titles are display/debug text only.

Enforced by `require_bdd_ids = true` in config and by lint checks in
`specweave/gherkin/lint.py`.

## Consequences

- **Positive:** Deterministic, rename-safe validation. Evidence mapping works
  across format conversions and language changes.
- **Negative:** Teams must maintain tags manually. Missing or duplicate tags
  are lint errors.

## Alternatives considered

- Title-based matching: rejected — fragile, causes false negatives on renames.
- UUID-based IDs: rejected — less human-readable in Gherkin source.
