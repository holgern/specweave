---
schema_version: 2
id: al_adr_0025
type: adr
title: "Classic `.feature` is the canonical behavior format"
status: accepted
section: architecture_decisions
order: 10
date: "2026-06-09"
deciders: []
supersedes: []
related: []
tags: []
body_format: markdown
created_at: "2026-06-09T00:00:00Z"
updated_at: "2026-06-09T00:00:00Z"
source_refs:
  - specweave/gherkin/parser.py
  - specweave/gherkin/writer.py
---


## Context

SpecWeave previously supported both classic Gherkin `.feature` and Markdown-embedded `.feature.md` as behavior spec formats. Maintaining two parser and writer paths adds complexity for humans, tools, and coding agents.

## Decision

Use classic Gherkin `.feature` files as the only canonical behavior-spec format in SpecWeave.

Durable SpecWeave-owned JSON artifacts live under `specs/behavior/`:

- `specs/behavior/evidence`
- `specs/behavior/mappings`

Generated runner output lives under:

- `reports/behavior`
- `reports/behavior/specweave`

## Alternatives considered

- Continue supporting `.feature.md` alongside `.feature`: rejected — two parser and writer paths add maintenance burden without sufficient benefit.
- Migrate `.feature.md` to a separate plugin: rejected — not enough usage to justify the indirection.
## Consequences

- legacy `.feature.md` files are not canonical and are rejected
- `specweave.toml` is the default config file
- `.specweave.toml` remains a compatibility discovery path for existing
  projects
