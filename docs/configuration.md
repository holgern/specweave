# Configuration

SpecWeave discovers configuration from `.specweave.toml` or `specweave.toml`,
walking parent directories. `.specweave.toml` takes precedence when both
exist at the same level. Use `--config PATH` to select an explicit file.

## Generate defaults

```bash
specweave init
```

This writes a `.specweave.toml` with all default values.

## Full reference

```toml
schema_version = 1
project_root = "."
spelling = "behavior"

[paths]
specs_root = "specs/behavior"
features_dir = "specs/behavior/features"
behavior_readme = "specs/behavior/README.md"
manifest = "specs/behavior/manifest.json"
tests_dir = "tests"
reports_dir = "reports/behavior"
state_dir = ".specweave"
evidence_dir = ".specweave/evidence"
reports_state_dir = ".specweave/reports"
mapping_dir = ".specweave/mappings"

gitkeep = true

[pytest]
test_globs = ["tests/test_*.py", "tests/**/*_test.py"]
ignore_globs = [".venv/**", "build/**", "dist/**"]

[gherkin]
dialect = "en"
document_format = "markdown"
feature_extension = ".feature.md"
feature_extensions = [".feature.md", ".feature"]
official_parser = false
markdown_parser = "specweave"
compile_pickles = false
default_scenario_keyword = "Example"
require_given_when_then = true
require_bdd_ids = true
id_style = "slug"
include_generated_tag = true
include_needs_review_tag = true
canonical_task_tags = false

[generation]
group_by = "file"
mode = "create"
preserve_manual_edits = true
mark_generated_from_tests = true

[commands]
test = "pytest --junitxml=reports/behavior/pytest-junit.xml"

[agent]
json_default = false
```

## Sections

### paths

Controls where SpecWeave reads and writes files. All paths are relative to
`project_root` by default.

| Key                 | Default                        | Description                     |
| ------------------- | ------------------------------ | ------------------------------- |
| `specs_root`        | `specs/behavior`               | Root of the behavior specs tree |
| `features_dir`      | `specs/behavior/features`      | Feature files directory         |
| `behavior_readme`   | `specs/behavior/README.md`     | Generated behavior index        |
| `manifest`          | `specs/behavior/manifest.json` | Generated behavior manifest     |
| `tests_dir`         | `tests`                        | Python test directory           |
| `reports_dir`       | `reports/behavior`             | Runner report directory         |
| `state_dir`         | `.specweave`                   | SpecWeave internal state        |
| `evidence_dir`      | `.specweave/evidence`          | Normalized evidence JSON        |
| `reports_state_dir` | `.specweave/reports`           | Internal report state           |
| `mapping_dir`       | `.specweave/mappings`          | Taskledger mappings             |

### gherkin

Controls Gherkin parsing, writing, and format behavior.

| Key                        | Default                       | Description                                  |
| -------------------------- | ----------------------------- | -------------------------------------------- |
| `dialect`                  | `"en"`                        | Gherkin language dialect                     |
| `document_format`          | `"markdown"`                  | Feature file format: `markdown` or `classic` |
| `feature_extension`        | `".feature.md"`               | Primary file extension                       |
| `feature_extensions`       | `[".feature.md", ".feature"]` | All recognized extensions                    |
| `official_parser`          | `false`                       | Use gherkin-official when available          |
| `markdown_parser`          | `"specweave"`                 | Markdown parser backend                      |
| `compile_pickles`          | `false`                       | Compile pickled representations              |
| `default_scenario_keyword` | `"Example"`                   | Default keyword for scenarios                |
| `require_given_when_then`  | `true`                        | Enforce Given/When/Then steps                |
| `require_bdd_ids`          | `true`                        | Enforce `@bdd-*` tags                        |
| `id_style`                 | `"slug"`                      | Auto-generated ID style                      |
| `include_generated_tag`    | `true`                        | Tag generated specs                          |
| `include_needs_review_tag` | `true`                        | Tag specs needing review                     |
| `canonical_task_tags`      | `false`                       | Include task tags in canonical output        |

### generation

Controls test and spec generation behavior.

| Key                         | Default    | Description                           |
| --------------------------- | ---------- | ------------------------------------- |
| `group_by`                  | `"file"`   | Group generated specs by file         |
| `mode`                      | `"create"` | Generation mode: `create` or `update` |
| `preserve_manual_edits`     | `true`     | Do not overwrite hand-written files   |
| `mark_generated_from_tests` | `true`     | Mark specs generated from tests       |

### commands

External command delegation.

| Key    | Default                 | Description                      |
| ------ | ----------------------- | -------------------------------- |
| `test` | `pytest --junitxml=...` | Test command for `specweave run` |

### agent

Agent-facing behavior.

| Key            | Default | Description                       |
| -------------- | ------- | --------------------------------- |
| `json_default` | `false` | Default to JSON output for agents |

## British spelling

Use `spelling = "behaviour"` to use `specs/behaviour/` paths. All path
defaults update accordingly.
