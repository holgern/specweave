---
schema_version: 2
id: al_content_0012
type: section
section: glossary
title: Glossary
order: 120
status: accepted
date: "2026-06-08"
body_format: markdown
created_at: "2026-06-08T12:58:35Z"
updated_at: "2026-06-08T18:30:00Z"
---

| Term                 | Definition                                                                  |
| -------------------- | --------------------------------------------------------------------------- |
| Behavior spec        | A Gherkin `.feature.md` or `.feature` file describing expected behavior     |
| Canonical layout     | The default directory structure: `specs/behavior/features/`, `tests/`, etc. |
| Brownfield workflow  | Generating specs from existing pytest tests (tests → specs)                 |
| New-feature workflow | Writing specs first, then generating test skeletons (spec → tests)          |
| `@bdd-*` tag         | Stable scenario identity tag used for validation traceability               |
| `@ac-*` tag          | Acceptance criterion linkage tag                                            |
| `@task-*` tag        | Task exchange metadata tag (Taskledger)                                     |
| `@rule-*` tag        | Rule exchange metadata tag (Taskledger)                                     |
| Fail-closed          | Evidence normalization that treats every non-passed status as blocking      |
| Plain pytest         | Standard `test_*.py` files without pytest-bdd or behave dependencies        |
| Manifest             | `specs/behavior/manifest.json` — generated index of all features/scenarios  |
| Evidence JSON        | Normalized test execution evidence in `.specweave/evidence/`                |
| Task-BDD JSON        | Portable BDD representation used for Taskledger exchange                    |
| Feature Markdown     | `.feature.md` format — Gherkin embedded in Markdown code fences             |
| Source mapping       | `@specweave` markers and comments in generated tests linking to scenarios   |
| Building block       | A top-level architectural module or subsystem within SpecWeave              |
| Archledger           | External tool that owns durable architecture and specification records      |
| Taskledger           | External tool that owns task lifecycle, plans, and acceptance criteria      |
| Combi check          | Cross-ledger integration audit without mutating external ledgers            |
