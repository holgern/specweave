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
  — Generate Python step-definition skeletons from a feature file. The `behave`
  backend produces `@given`/`@when`/`@then` decorated functions.

- `specweave run --runner command -- <external test command>` — Execute a
  delegated BDD command, capture stdout/stderr, and write a normalized summary
  report to `.specweave/reports/summary.json`.

- `specweave version` — Print the installed version.

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
