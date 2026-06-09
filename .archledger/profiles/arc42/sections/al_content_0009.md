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

## AD-7: Optional gherkin-official dependency

**Context:** `gherkin-official` (the Cucumber reference parser) was previously
listed as a required runtime dependency. However, SpecWeave's built-in parser
and subset validator (`specweave/gherkin/validation.py`) cover the canonical
subset without external help. Only users needing full Cucumber Gherkin
compatibility require the official parser.

**Decision:** Move `gherkin-official` to an optional extra
(`pip install specweave[gherkin]`). The adapter in
`specweave/gherkin/official.py` lazy-imports the library and raises a clear
error when it is not installed. The core SpecWeave workflow (parse, lint,
generate, convert, validate) works without it.

**Consequences:** Smaller default install footprint. Users who need full
Cucumber compatibility opt in explicitly. The built-in subset validator
catches unsupported constructs (Background, Scenario Outline, tables, doc
strings) without any external dependency.
