# specweave

SpecWeave translates between canonical Gherkin behavior specs, plain pytest
enforcement, and normalized execution evidence.

It is not a task ledger, architecture ledger, or CI system.

## Canonical layout

```text
specs/behavior/features/<area>/<feature>.feature.md
specs/behavior/features/<area>/<feature>.feature
tests/test_<area>_<feature>.py
reports/behavior/*.xml
.specweave/reports/*.json
.specweave/evidence/*.json
.specweave/mappings/taskledger/*.json
```

Canonical behavior specs live under `specs/behavior/features`. When
`[gherkin].document_format = "markdown"` (the default), agents must create
`.feature.md` files. If a classic `.feature` file is produced, run:

```bash
specweave convert <file> --to markdown
specweave convert --all --to markdown
```

and review the resulting `.feature.md` before committing. Executable
enforcement is plain pytest directly under `tests/`.

SpecWeave does **not** require:

- pytest-bdd
- behave
- step-definition modules
- `tests/bdd/`
- `tests/behavior/`
- Taskledger as a Python dependency

## Behavior workflow

### 1. Lint behavior specs

```bash
specweave behavior check
```

### 2. Generate the behavior index and manifest

```bash
specweave behavior index \
  --features specs/behavior/features \
  --out specs/behavior/README.md \
  --manifest specs/behavior/manifest.json
```

### 3. Generate plain pytest skeletons

Single feature:

```bash
specweave behavior generate-tests \
  specs/behavior/features/task-management/plan-gates.feature \
  --out tests/test_task_management_plan_gates.py
```

Whole tree:

```bash
specweave behavior generate-tests \
  --features specs/behavior/features \
  --tests-dir tests
```

### 4. Check static behavior coverage

```bash
specweave behavior coverage \
  --features specs/behavior/features \
  --tests tests \
  --format text
```

Write JSON or Markdown artifacts when needed:

```bash
specweave behavior coverage \
  --features specs/behavior/features \
  --tests tests \
  --json .specweave/reports/behavior-coverage.json

specweave behavior coverage \
  --features specs/behavior/features \
  --tests tests \
  --format markdown \
  --out .specweave/reports/behavior-coverage.md
```

List the raw explicit pytest mappings discovered by the scanner:

```bash
specweave behavior mappings --tests tests --format text
```

### 5. Import pytest/JUnit evidence

```bash
pytest tests/test_task_management_plan_gates.py \
  --junitxml=reports/behavior/task-management-plan-gates-junit.xml

specweave behavior import-report \
  reports/behavior/task-management-plan-gates-junit.xml \
  --format junit-xml \
  --out .specweave/evidence/task-management-plan-gates.pytest-evidence.json
```

## Optional Taskledger integration

Taskledger integration is file-based and optional. SpecWeave can import a
Taskledger acceptance export into a canonical behavior feature:

```bash
specweave behavior import-taskledger \
  .specweave/mappings/taskledger/task-0123.json \
  --out specs/behavior/features/task-management/plan-gates.feature
```

This does not make Taskledger the canonical owner of the behavior file.

## Compatibility aliases

These aliases point to the behavior workflow:

```bash
specweave bdd check
specweave bdd index
specweave bdd generate-tests
specweave bdd coverage
```

Legacy `draft`, `bind`, `report`, and other bridge commands remain available
for older experiments, but they are not the canonical SpecWeave workflow.


## Converting feature files

Convert between classic `.feature` and Markdown `.feature.md` formats:

```bash
specweave convert specs/behavior/features/auth/login.feature
specweave convert specs/behavior/features --to markdown
specweave convert --all --to markdown
specweave --json convert specs/behavior/features/auth/login.feature
specweave convert login.feature.md --to classic
specweave convert login.feature --dry-run
specweave convert specs/behavior/features --to markdown --replace-source
```

Source files are kept by default. Use `--replace-source` only when you want to
delete successfully converted classic `.feature` sources after the Markdown
target exists. After a bulk conversion, run `specweave behavior coverage` or
`specweave review specs` to catch stale explicit mappings that still point to
classic paths.

## Installation

```bash
pip install specweave
```

Or install from source with development dependencies:

```bash
pip install -e ".[dev]"
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
