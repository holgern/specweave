---
schema_version: 2
id: al_content_0011
type: section
section: risks_and_technical_debt
title: Risks and Technical Debt
order: 110
status: accepted
date: "2026-06-08"
body_format: markdown
created_at: "2026-06-08T12:58:35Z"
updated_at: "2026-06-08T18:30:00Z"
---

## Risks

1. **Tag discipline required.** If teams neglect `@bdd-*` tags, static
   coverage and evidence mapping break. Mitigated by `require_bdd_ids = true`
   and lint enforcement.

2. **Dual format complexity.** Supporting both `.feature` and `.feature`
   doubles the parser surface. The `convert` command and `gherkin/markdown.py`
   must stay in sync with the classic parser.

3. **Brownfield inference quality.** AST-based test discovery may produce
   low-quality Gherkin from poorly named tests. Marked with `@generated` and
   `@needs-review` tags to flag human review.

4. **Cross-tool format drift.** Taskledger and Archledger JSON shapes may
   evolve independently. SpecWeave must track compatible shapes without
   coupling to their internals.

5. **Report format coverage.** Only `junit-xml` and `cucumber-json` report
   formats are supported. Projects using other runners (e.g., `pytest-cucumber`)
   may need adapter work.

## Technical debt

1. **Bridge/legacy commands.** `bdd export`, `bdd import-feature`,
   `report normalize`, `archledger`, `draft`, `bind`, and `run` are legacy or
   bridge commands. They must stay working but should not grow new features.

2. **Compatibility aliases.** `bdd check`, `bdd index`, `bdd generate-tests`,
   and `bdd coverage` are aliases for `behavior` commands. They add CLI
   surface area without new functionality.

3. **Backends module.** `specweave/backends/behave.py` and
   `specweave/backends/pytest_bdd.py` generate step-definition skeletons for
   non-canonical workflows. These may lag behind the canonical path.

4. **Config backward compatibility.** Constants like `FEATURES_DIR`,
   `BDD_INDEX_PATH`, `BDD_MANIFEST_PATH` in `specweave/config.py` are
   compatibility aliases that older code paths rely on.
