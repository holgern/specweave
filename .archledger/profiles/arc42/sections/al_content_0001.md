---
schema_version: 2
id: al_content_0001
type: section
section: introduction_and_goals
title: Introduction and Goals
order: 10
status: accepted
date: "2026-06-08"
body_format: markdown
created_at: "2026-06-08T12:58:35Z"
updated_at: "2026-06-08T18:30:00Z"
---

## Overview

SpecWeave is a Python CLI and library that translates between canonical Gherkin
behavior specifications, plain pytest enforcement, and normalized BDD execution
evidence. It is not a task ledger, architecture ledger, or CI system.

## Goals

1. **Keep behavior intent readable.** Gherkin `.feature.md` (Markdown) files
   under `specs/behavior/features/<area>/` serve as the human-readable source of
   truth for what a system should do.
2. **Keep executable validation traceable.** Plain pytest tests under `tests/`
   are the default enforcement path. SpecWeave maps between Gherkin scenarios
   and pytest via stable `@bdd-*` tags, not scenario titles.
3. **Fail closed on incomplete or ambiguous evidence.** A passing command exit
   code alone is never sufficient evidence when a native report is available.
   Skipped, pending, undefined, ambiguous, and missing results block acceptance.
4. **Bridge brownfield pytest into structured behavior specs.** The
   `create gherkin --from-tests` workflow uses AST-based discovery to generate
   draft Gherkin from existing tests without executing them.
5. **Exchange normalized evidence with external tools.** SpecWeave produces
   Taskledger-compatible evidence JSON and Archledger candidate records through
   file-based integrations, without making those tools runtime dependencies.

## Non-goals

- SpecWeave does not own task lifecycle, plan approval, or user gates
  (Taskledger owns those).
- SpecWeave does not own durable architecture records (Archledger owns those).
- SpecWeave does not orchestrate CI pipelines.
- SpecWeave does not require `pytest-bdd`, `behave`, or step-definition modules
  for its canonical workflow.
