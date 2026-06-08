---
schema_version: 2
id: al_adr_0025
type: adr
title: "Markdown feature.md as default format"
status: proposed
section: architecture_decisions
order: 50
date: "2026-06-08"
deciders: []
supersedes: []
related: []
tags: []
body_format: markdown
created_at: "2026-06-08T19:08:19Z"
updated_at: "2026-06-08T19:08:19Z"
source_refs:
  - specweave/gherkin/markdown.py
  - specweave/gherkin/convert.py
  - specweave/config.py
---

## Context

Classic `.feature` files have no native Markdown support. They render as
plain text in GitHub, IDE previews, and agent contexts, reducing readability.

## Decision

Default to `.feature.md` with embedded Gherkin inside Markdown code fences.
Support classic `.feature` as a first-class alternative. Provide a `convert`
command to bridge between formats.

## Consequences

- **Positive:** Better readability in modern tooling. Natural fit for
  Markdown-centric workflows and coding agents.
- **Negative:** Doubles the parser surface. `gherkin/markdown.py` must stay
  in sync with the classic parser.

## Alternatives considered

- Classic only: rejected — poor readability in Markdown-native contexts.
- External converter dependency: rejected — adds a dependency for a core need.
