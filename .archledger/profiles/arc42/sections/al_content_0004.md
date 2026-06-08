---
schema_version: 2
id: al_content_0004
type: section
section: solution_strategy
title: Solution Strategy
order: 40
status: accepted
date: "2026-06-08"
body_format: markdown
created_at: "2026-06-08T12:58:35Z"
updated_at: "2026-06-08T18:30:00Z"
---

## Key decisions

1. **Tag-based traceability, not title-based.** Scenario identity is anchored
   on `@bdd-*` tags. Acceptance criteria are anchored on `@ac-*` tags. Scenario
   titles are display/debug text only. This makes validation deterministic and
   rename-safe.

2. **Plain pytest as the canonical enforcement path.** SpecWeave generates
   standard `test_*.py` files with `@specweave` markers and source-mapping
   comments. No `pytest-bdd` step definitions, no `behave` step modules, no
   `tests/bdd/` directory are required.

3. **Fail-closed evidence.** Report normalization treats every non-passed
   scenario status (failed, skipped, pending, undefined, ambiguous, missing,
   unlinked) as blocking. A clean command exit code is never sufficient
   evidence.

4. **Frozen dataclass models throughout.** `Feature`, `Rule`, `Scenario`,
   `Step`, `ScenarioResult`, `NormalizedBddReport`, `TaskBddSpec`, and
   configuration classes are all immutable frozen dataclasses. This prevents
   accidental mutation during pipeline transforms.

5. **Dual Gherkin format.** SpecWeave supports both classic `.feature` and
   Markdown `.feature.md` files. The default is `.feature.md`. A `convert`
   command bridges between formats.

6. **Layered architecture.** The code is organized into Gherkin model/parser/
   writer, behavior workflow, translation, report normalization, Python AST
   inspection, integrations, and CLI. Each layer owns its domain; cross-layer
   calls go through well-defined module boundaries.

7. **AST-based discovery, not test execution.** The brownfield workflow
   (`create gherkin --from-tests`) reads Python AST to infer behavior from
   test names, docstrings, markers, and assertions. Tests are never executed
   during discovery.
