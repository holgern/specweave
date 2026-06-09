# Development

## Setup

```bash
pip install -e ".[dev]"
```

This installs SpecWeave with all development dependencies including the
`docs` and `gherkin` extras.

## Run tests

```bash
pytest -q
```

## Lint and format

```bash
ruff check .
ruff format --check .
```

## Type check

```bash
mypy specweave
```

## Build docs

```bash
pip install -e ".[docs]"
python -m sphinx -b html docs docs/_build/html
```

For strict builds (warnings as errors):

```bash
python -m sphinx -W -b html docs docs/_build/html
```

## Optional extras

| Extra     | Install                          | Description                      |
| --------- | -------------------------------- | -------------------------------- |
| `gherkin` | `pip install specweave[gherkin]` | Official Cucumber Gherkin parser |
| `docs`    | `pip install specweave[docs]`    | Sphinx, MyST parser, theme       |
| `dev`     | `pip install specweave[dev]`     | All development tools            |
