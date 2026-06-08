---
schema_version: 2
id: al_adr_0024
type: adr
title: "Fail-closed evidence normalization"
status: proposed
section: architecture_decisions
order: 40
date: "2026-06-08"
deciders: []
supersedes: []
related: []
tags: []
body_format: markdown
created_at: "2026-06-08T19:08:19Z"
updated_at: "2026-06-08T19:08:19Z"
source_refs:
  - specweave/reports/normalize.py
  - specweave/reports/model.py
  - specweave/reports/mapping.py
---

## Context

BDD evidence is used for acceptance decisions. If the normalization layer
is lenient, teams may accept incomplete or misleading evidence.

## Decision

Every non-passed scenario status (failed, skipped, pending, undefined,
ambiguous, missing, unlinked) blocks the report. Missing expected `@ac-*`
coverage blocks. A clean command exit code alone is never sufficient evidence.

## Consequences

- **Positive:** High confidence in "passed" evidence. No false positives in
  acceptance decisions.
- **Negative:** May require teams to explicitly address skipped tests or
  flaky suites before evidence passes.

## Alternatives considered

- Fail-open (only hard failures block): rejected — undermines evidence trust.
- Configurable per-status defaults: rejected — too easy to weaken by accident.
