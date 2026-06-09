---
schema_version: 2
id: al_content_0008
type: section
section: cross_cutting_concepts
title: Cross-cutting Concepts
order: 80
status: accepted
date: "2026-06-08"
body_format: markdown
created_at: "2026-06-08T12:58:35Z"
updated_at: "2026-06-08T18:30:00Z"
---

## Tag-based traceability

All scenario identity and acceptance-criteria linkage is tag-based:

| Tag prefix   | Purpose                   | Used by              |
| ------------ | ------------------------- | -------------------- |
| `@bdd-*`     | Stable scenario identity  | validation, evidence |
| `@ac-*`      | Acceptance criterion link | coverage, reporting  |
| `@task-*`    | Task exchange metadata    | Taskledger exchange  |
| `@rule-*`    | Rule exchange metadata    | Taskledger exchange  |
| `@area-*`    | Feature area grouping     | index, coverage      |
| `@feature-*` | Feature identity tag      | index, lint          |

Scenario titles are display/debug text only. Title matching is never used for
validation — only as a review hint with explicit uncertainty.

## Fail-closed evidence

Report normalization (`specweave/reports/normalize.py`) treats every non-passed
scenario status as blocking:

- `failed`, `undefined`, `pending`, `ambiguous` → always fail the report
- `skipped` → fails unless `--allow-skipped` is explicitly set
- Missing expected `@ac-*` → fails
- Unlinked scenarios → do not count toward acceptance criteria
- Clean command exit code alone → never sufficient evidence

## Frozen dataclass models

All public models are frozen dataclasses (`frozen=True`):

- Gherkin: `Feature`, `Rule`, `Scenario`, `Step`
- Reports: `ScenarioResult`, `CriterionResult`, `NormalizedBddReport`
- BDD: `TaskBddSpec`, `BddRule`, `BddExample`
- Config: `SpecWeaveConfig`, `SpecWeavePaths`, `SpecWeaveGherkin`, etc.

## Deterministic output

- TOML config rendering is deterministic (`specweave/config.py`).
- JSON output is sorted and indented consistently (`json.dumps(sort_keys=True)`).
- Feature files are written deterministically from models.
- Test names are derived deterministically from scenario titles via slugification.

## Dual Gherkin format

SpecWeave supports both `.feature` (classic Gherkin) and `.feature`
(Markdown-embedded Gherkin, the default). The `convert` command bridges
between formats. The Markdown parser is in `specweave/gherkin/markdown.py`.
