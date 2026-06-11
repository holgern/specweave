# Configuration

SpecWeave discovers configuration from `specweave.toml` or `.specweave.toml`,
walking parent directories. `specweave.toml` takes precedence when both exist.
Use `--config PATH` to select an explicit file.

`specweave init` writes `specweave.toml` by default and can materialize
behaviour mode, specifications mode, or both.

## Default config

```toml
schema_version = 1
project_root = "."
spelling = "behaviour"

[paths]
specs_root = "specs"
tests_dir = "tests"

[paths.behaviour]
root = "specs/behaviour"
features_dir = "specs/behaviour/features"
readme = "specs/behaviour/README.md"
manifest = "specs/behaviour/manifest.json"
mappings_dir = "specs/behaviour/mappings"
evidence_dir = "specs/behaviour/evidence"
reports_dir = "specs/behaviour/reports"
reports_state_dir = "specs/behaviour/reports/specweave"

[paths.specifications]
root = "specs/specifications"
product_spec = "specs/specifications/product.spec.md"
readme = "specs/specifications/README.md"
manifest = "specs/specifications/manifest.json"
capabilities_dir = "specs/specifications/capabilities"
interfaces_dir = "specs/specifications/interfaces"
integrations_dir = "specs/specifications/integrations"
mappings_dir = "specs/specifications/mappings"
evidence_dir = "specs/specifications/evidence"
reports_dir = "specs/specifications/reports"
reports_state_dir = "specs/specifications/reports/specweave"

gitkeep = true

[pytest]
test_globs = ["tests/test_*.py", "tests/**/*_test.py"]
ignore_globs = [".venv/**", "build/**", "dist/**"]

[gherkin]
dialect = "en"
official_parser = false
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
test = "pytest --junitxml=specs/behaviour/reports/pytest-junit.xml"

[agent]
json_default = false
```

## Notes

- classic `.feature` is the only canonical feature format
- new projects should prefer `specs/behaviour/...`
- existing flat `[paths]` fields such as `features_dir`, `behavior_readme`, and
  `mapping_dir` still load for compatibility
- specifications mode is enabled when `[paths.specifications]` or
  `[specifications]` is present
