---
title: Classic `.feature` is the canonical behavior format
status: accepted
date: 2026-06-09
---

# ADR 0025: Classic `.feature` is the canonical behavior format

## Decision

Use classic Gherkin `.feature` files as the only canonical behavior-spec
format in SpecWeave.

Durable SpecWeave-owned JSON artifacts live under `specs/behavior/`:

- `specs/behavior/evidence`
- `specs/behavior/mappings`

Generated runner output lives under:

- `reports/behavior`
- `reports/behavior/specweave`

## Rationale

- one syntax is easier for humans, tools, and coding agents
- classic Gherkin maps directly to existing ecosystem tooling
- removing Markdown feature mode eliminates duplicate parser and writer paths
- readable durable artifacts belong with the behavior specs, not under a hidden
  state directory

## Consequences

- legacy `.feature.md` files are not canonical and are rejected
- `specweave.toml` is the default config file
- `.specweave.toml` remains a compatibility discovery path for existing
  projects
