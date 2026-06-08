---
schema_version: 2
id: al_adr_0026
type: adr
title: "File-based Taskledger and Archledger integration"
status: proposed
section: architecture_decisions
order: 60
date: "2026-06-08"
deciders: []
supersedes: []
related: []
tags: []
body_format: markdown
created_at: "2026-06-08T19:08:19Z"
updated_at: "2026-06-08T19:08:19Z"
source_refs:
  - specweave/integrations/taskledger.py
  - specweave/integrations/archledger.py
  - specweave/integrations/combi.py
---

## Context

SpecWeave needs to exchange data with Taskledger (task lifecycle, plans,
acceptance criteria) and Archledger (architecture records) but must not
become coupled to their internals or require their installation.

## Decision

All integration is file-based JSON and Markdown exchange. SpecWeave reads
task-BDD JSON and writes evidence JSON for Taskledger. It renders candidate
Markdown for Archledger. Neither tool is a Python dependency.

## Consequences

- **Positive:** Clean boundaries. SpecWeave runs independently. No version
  coupling with external tools.
- **Negative:** Format changes in Taskledger or Archledger require coordinated
  updates. No runtime validation against external tool schemas.

## Alternatives considered

- Direct API integration: rejected — tight coupling, version fragility.
- Shared database: rejected — violates the "no database" constraint.
