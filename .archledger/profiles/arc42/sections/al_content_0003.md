---
schema_version: 2
id: al_content_0003
type: section
section: context_and_scope
title: Context and Scope
order: 30
status: accepted
date: "2026-06-08"
body_format: markdown
created_at: "2026-06-08T12:58:35Z"
updated_at: "2026-06-08T18:30:00Z"
---

## System boundary

SpecWeave is a developer CLI tool. It runs in a project checkout directory,
reads and writes local files, and delegates test execution to an external
command (typically `pytest`). It does not listen on ports, run as a daemon, or
expose a network API.

## External actors

```text
┌─────────────┐     reads/writes      ┌───────────────┐
│   Developer  │◄─────────────────────►│   Filesystem  │
│  (CLI user)  │                       │  (.specweave, │
└──────┬───────┘                       │   specs/,     │
       │ invokes                       │   tests/,     │
       ▼                               │   reports/)   │
┌─────────────┐     delegates          └───────────────┘
│  SpecWeave   │──► pytest (external)
│    CLI       │
└──────┬───────┘
       │ file exchange
       ▼
┌──────────────┐  ┌──────────────┐
│  Taskledger   │  │  Archledger  │
│ (task state)  │  │  (arch docs) │
└──────────────┘  └──────────────┘
```

## Interfaces

- **CLI** (`specweave` console script): Typer-based CLI with `--config`,
  `--json` root options. Human and machine-readable output.
- **Filesystem**: canonical layout of `specs/behavior/features/<area>/`,
  `tests/`, `reports/behavior/`, `.specweave/`.
- **Taskledger integration**: file-based JSON exchange
  (`specweave/integrations/taskledger.py`). SpecWeave reads task-BDD JSON and
  writes evidence JSON. It never approves plans or manages task lifecycle.
- **Archledger integration**: candidate markdown rendering
  (`specweave/integrations/archledger.py`). SpecWeave writes candidate files
  when explicitly requested; it never creates accepted records implicitly.
