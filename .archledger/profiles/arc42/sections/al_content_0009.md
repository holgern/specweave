---
schema_version: 2
id: al_content_0009
type: section
section: architecture_decisions
title: Architecture Decisions
order: 90
status: accepted
date: "2026-06-08"
body_format: markdown
created_at: "2026-06-08T12:58:35Z"
updated_at: "2026-06-08T18:30:00Z"
---

## AD-1: Tag-based identity, not title-based

**Context:** Scenario titles change frequently during editing. Using them as
validation keys would cause false negatives.

**Decision:** Anchor all validation on `@bdd-*` tags. Use `@ac-*` for
acceptance-criteria linkage. Titles are display-only.

**Consequences:** Stable validation across renames. Requires discipline to
maintain tags, but this is enforced by `require_bdd_ids = true` in config.

## AD-2: Plain pytest as the canonical enforcement path

**Context:** Existing BDD tools in Python (pytest-bdd, behave) couple tests to
step-definition modules and require framework-specific boilerplate.

**Decision:** Generate standard `test_*.py` files with `@specweave` markers and
source-mapping comments. No step definitions required.

**Consequences:** Lower barrier to adoption. Tests are runnable without
SpecWeave installed. But SpecWeave-specific markers are needed for static
coverage checks.

## AD-3: AST-based test discovery, not execution

**Context:** Inferring behavior from existing tests could be done by running
them and inspecting results, or by static analysis.

**Decision:** Use Python AST parsing (`specweave/python_inspect/ast_reader.py`)
to discover tests. Never execute tests during discovery.

**Consequences:** Fast, deterministic, safe. But inferred Gherkin may miss
runtime-only behavior.

## AD-4: Fail-closed report normalization

**Context:** BDD evidence must be reliable for acceptance decisions.

**Decision:** Every non-passed status blocks. Missing scenarios block. Missing
acceptance criteria block. Exit code alone is insufficient.

**Consequences:** High confidence in "passed" evidence. May require teams to
explicitly allow skipped tests or address flaky suites.

## AD-5: File-based Taskledger/Archledger integration

**Context:** SpecWeave needs to exchange data with Taskledger and Archledger but
must not become coupled to their internals.

**Decision:** JSON file exchange. SpecWeave reads task-BDD JSON and writes
evidence JSON. No runtime dependency on either tool.

**Consequences:** Clean boundaries. SpecWeave can run without Taskledger or
Archledger installed. Exchange format changes require coordination.

## AD-6: Markdown .feature.md as default format

**Context:** Classic `.feature` files have no native Markdown support, making
them harder to read in GitHub, IDEs, and agent contexts.

**Decision:** Default to `.feature.md` with embedded Gherkin inside Markdown
code fences. Support classic `.feature` as a first-class alternative.

**Consequences:** Better readability in modern tooling. Requires a Markdown
parser alongside the standard Gherkin parser. The `convert` command bridges
formats.
