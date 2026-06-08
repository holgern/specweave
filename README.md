# specweave

SpecWeave translates between Python tests, Gherkin/Cucumber feature files,
plain-English behavior descriptions, and normalized BDD execution evidence.

It is not a task ledger, architecture ledger, or CI system.

## MVP commands

- `specweave explain PATH...` — Inspect Python test files and produce candidate
  Gherkin behavior descriptions using AST analysis.

- `specweave draft --from-json task.json --out features/task.feature` — Create
  a Gherkin `.feature` file from a JSON acceptance criteria document.

- `specweave bind features/task.feature --backend behave --out tests/bdd/steps/`
  — Generate Python step-definition skeletons from a feature file. Backends:
  `behave` (default) and `pytest-bdd`. Scenarios inside `Rule:` blocks are
  bound as well.

- `specweave run --runner command -- <external test command>` — Execute a
  delegated BDD command, capture stdout/stderr, and write a normalized summary
  report to `.specweave/reports/summary.json`.

- `specweave version` — Print the installed version.

## BDD workflow commands

SpecWeave owns the BDD bridge between project tests, task acceptance criteria,
and (optional) Taskledger/Archledger records. Taskledger and Archledger are
**optional, file-based integrations** — SpecWeave never imports them as hard
Python dependencies.

- `specweave bdd export --from-json task-bdd.json --out features/task.feature`
  — Export a task-BDD JSON spec (`task_id`, `feature`, `rules`, `examples`) to
  a target-format Gherkin feature file with canonical
  `@task-*`/`@rule-*`/`@bdd-*`/`@ac-*` tags.

- `specweave bdd import-feature features/task.feature --out task-bdd.json`
  — Import a feature file back into a task-BDD JSON spec, preserving
  task/rule/bdd/ac ids.

- `specweave report normalize REPORT --format cucumber-json|junit-xml [--out OUT] [--evidence] [--task task-0123] [--allow-skipped] [--expect-ac ac-0001]`
  — Normalize a runner-native report to the SpecWeave schema (v2). Status is
  **fail-closed**: `failed`/`undefined`/`pending`/`ambiguous` (and `skipped`
  unless `--allow-skipped`) mark the report `failed`. Exit code is non-zero on
  failure. Use `--evidence` to emit the Taskledger BDD evidence JSON shape.

- `specweave report inspect REPORT --format cucumber-json|junit-xml` — Print a
  compact one-line summary of the normalized report.

- `specweave archledger candidate --feature features/task.feature --bdd bdd-0001 --out .archledger/candidates/al_candidate.md` — Render an Archledger
  candidate behavior record (Source / Behavior / Rationale) for a BDD example.
  Candidate-only; Archledger decides whether to accept and persist it.

### Data exchange contracts

```text
input from Taskledger:   .taskledger/exports/task-0123.acceptance.json
output to Taskledger:    .specweave/evidence/task-0123.bdd-evidence.json
```

Acceptance criteria may be supplied in either the rich task-BDD shape
(`task_id`, `feature`, `rules`, `examples`) or the legacy MVP shape
(`task_id`, `title`, `acceptance_criteria`).

## Installation

```bash
pip install specweave
```

Or install from source with development dependencies:

```bash
pip install -e ".[dev]"
```

## Example workflow

```bash
# 1. Draft a feature from acceptance criteria
specweave draft --from-json examples/task_TL-0042.json --out features/tl_0042.feature

# 2. Generate step definition skeletons
specweave bind features/tl_0042.feature --backend behave --out tests/bdd/steps/

# 3. Implement production code and step definitions
# (hand-coded by the developer)

# 4. Run the BDD tests and normalize evidence
specweave run --runner behave -- behave --format json -o .specweave/reports/behave.json

# 5. Pass the evidence to Taskledger for validation tracking
taskledger validate check --criterion AC-001 --status pass --evidence .specweave/reports/summary.json
```

## Development

```bash
pip install -e ".[dev]"
pytest -q
ruff check .
ruff format --check .
mypy specweave
```

## License

Apache 2.0
