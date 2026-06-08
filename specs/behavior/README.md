# Behavior index

Generated from `specs/behavior/features`.

## behavior

### Static behavior coverage checks

- Path: `specs/behavior/features/behavior/coverage.feature`
- Summary: specweave behavior coverage checks the mapping between behavior feature

#### Rule: Coverage identifies bound and unbound scenarios

- `bdd-coverage-bound-scenario` Coverage marks bound scenarios -> `tests/test_behavior_coverage.py` (missing)
- `bdd-coverage-unbound-scenario` Coverage reports missing bindings -> `tests/test_behavior_coverage.py` (missing)
- `bdd-coverage-missing-test-file` Coverage reports missing test files -> `tests/test_behavior_coverage.py` (missing)

#### Rule: Coverage detects stale bindings

- `bdd-coverage-stale-binding` Coverage reports bindings to non-existent features -> `tests/test_behavior_coverage.py` (missing)
- `bdd-coverage-stale-scenario` Coverage reports bindings to non-existent scenarios -> `tests/test_behavior_coverage.py` (missing)

#### Rule: Coverage detects deprecated paths

- `bdd-coverage-deprecated-paths` Coverage reports deprecated feature paths -> `tests/test_behavior_coverage.py` (missing)

#### Rule: Coverage detects forbidden pytest-bdd usage

- `bdd-coverage-forbidden-pytest-bdd` Coverage reports pytest-bdd imports in test files -> `tests/test_behavior_coverage.py` (missing)

#### Rule: Coverage skips manual and waived scenarios

- `bdd-coverage-manual-scenario` Coverage skips scenarios tagged @manual -> `tests/test_behavior_coverage.py` (missing)

### Plain pytest skeleton generation

- Path: `specs/behavior/features/behavior/generation.feature`
- Summary: specweave behavior generate-tests creates plain pytest test skeletons

#### Rule: Generation creates pytest skeletons

- `bdd-generate-single-feature` Generation creates a test file for a feature -> `tests/test_behavior_generation.py` (missing)
- `bdd-generate-scenario-function` Each scenario becomes a test function -> `tests/test_behavior_generation.py` (missing)
- `bdd-generate-specweave-markers` Test functions have correct specweave markers -> `tests/test_behavior_generation.py` (missing)
- `bdd-generate-docstring` Test functions have docstrings with scenario details -> `tests/test_behavior_generation.py` (missing)
- `bdd-generate-step-comments` Test functions have step comments -> `tests/test_behavior_generation.py` (missing)

#### Rule: Generation derives canonical test paths

- `bdd-generate-canonical-path` Test path is derived from feature path -> `tests/test_behavior_generation.py` (missing)

#### Rule: Generation handles rules

- `bdd-generate-rules` Scenarios in rules get rule markers -> `tests/test_behavior_generation.py` (missing)

#### Rule: Generation supports batch mode

- `bdd-generate-batch` Generation processes all features in a directory -> `tests/test_behavior_generation.py` (missing)

### Behavior index and manifest generation

- Path: `specs/behavior/features/behavior/index.feature`
- Summary: specweave behavior index generates a Markdown index and JSON manifest

#### Rule: Index generation scans feature files

- `bdd-index-generates-markdown` Index generates Markdown with feature listing -> `tests/test_behavior_index.py` (missing)
- `bdd-index-generates-manifest` Index generates JSON manifest with scenario mappings -> `tests/test_behavior_index.py` (missing)
- `bdd-index-scenario-entries` Manifest includes scenario entries with automation status -> `tests/test_behavior_index.py` (missing)
- `bdd-index-unbound-scenario` Manifest marks unbound scenarios as missing -> `tests/test_behavior_index.py` (missing)

#### Rule: Index reflects evidence status

- `bdd-index-evidence-status` Manifest includes latest evidence status when available -> `tests/test_behavior_index.py` (missing)

#### Rule: Index supports rule blocks

- `bdd-index-rules` Manifest preserves Rule structure -> `tests/test_behavior_index.py` (missing)

### Behavior evidence import from pytest reports

- Path: `specs/behavior/features/behavior/reporting.feature`
- Summary: specweave behavior import-report imports pytest/JUnit XML reports into

#### Rule: Import maps test results to scenarios

- `bdd-import-maps-by-nodeid` Import maps results by normalized nodeid -> `tests/test_behavior_reporting.py` (missing)
- `bdd-import-maps-by-function-name` Import falls back to function name matching -> `tests/test_behavior_reporting.py` (missing)
- `bdd-import-maps-by-manifest` Import uses manifest mappings when available -> `tests/test_behavior_reporting.py` (missing)

#### Rule: Import reports unmapped tests

- `bdd-import-unmapped-tests` Import reports tests without specweave markers -> `tests/test_behavior_reporting.py` (missing)

#### Rule: Import writes evidence JSON

- `bdd-import-writes-evidence` Import writes evidence to the target path -> `tests/test_behavior_reporting.py` (missing)

## cli

### SpecWeave CLI contract

- Path: `specs/behavior/features/cli/cli-contract.feature`
- Summary: The SpecWeave CLI provides commands for behavior-driven development

#### Rule: Root options work across all commands

- `bdd-cli-config-option` --config selects an explicit config path -> `tests/test_cli_cli_contract.py` (missing)
- `bdd-cli-json-output` --json produces machine-readable output -> `tests/test_cli_cli_contract.py` (missing)
- `bdd-cli-json-init` init --json produces machine-readable output -> `tests/test_cli_cli_contract.py` (missing)

#### Rule: Behavior subcommands work correctly

- `bdd-cli-behavior-check` behavior check lints feature files -> `tests/test_cli_cli_contract.py` (missing)
- `bdd-cli-behavior-index` behavior index generates index and manifest -> `tests/test_cli_cli_contract.py` (missing)
- `bdd-cli-behavior-generate-tests` behavior generate-tests creates pytest skeletons -> `tests/test_cli_cli_contract.py` (missing)
- `bdd-cli-behavior-coverage` behavior coverage checks spec-to-test mapping -> `tests/test_cli_cli_contract.py` (missing)
- `bdd-cli-behavior-import-report` behavior import-report imports JUnit XML -> `tests/test_cli_cli_contract.py` (missing)

#### Rule: BDD compatibility aliases work

- `bdd-cli-bdd-check-alias` bdd check is an alias for behavior check -> `tests/test_cli_cli_contract.py` (missing)
- `bdd-cli-bdd-index-alias` bdd index is an alias for behavior index -> `tests/test_cli_cli_contract.py` (missing)

#### Rule: Create subcommands work correctly

- `bdd-cli-create-feature` create feature writes a new Gherkin feature file -> `tests/test_cli_cli_contract.py` (missing)
- `bdd-cli-create-gherkin` create gherkin generates features from tests -> `tests/test_cli_cli_contract.py` (missing)
- `bdd-cli-create-plan` create plan generates an implementation plan -> `tests/test_cli_cli_contract.py` (missing)

#### Rule: Exit codes reflect result status

- `bdd-cli-exit-doctor-failed` doctor exits non-zero when errors found -> `tests/test_cli_cli_contract.py` (missing)
- `bdd-cli-exit-check-errors` behavior check exits non-zero on lint errors -> `tests/test_cli_cli_contract.py` (missing)
- `bdd-cli-exit-normalize-failed` report normalize exits non-zero when report failed -> `tests/test_cli_cli_contract.py` (missing)

## common

### Behavior helper functions

- Path: `specs/behavior/features/common/behavior-helpers.feature`
- Summary: The behavior.common module provides shared helpers for slugification,

#### Rule: Slugification produces stable lowercase slugs

- `bdd-slugify-basic` Slugify converts text to lowercase slug -> `tests/test_common_behavior_helpers.py` (missing)
- `bdd-slugify-special-chars` Slugify replaces special characters with hyphens -> `tests/test_common_behavior_helpers.py` (missing)
- `bdd-slugify-empty` Slugify returns "behavior" for empty input -> `tests/test_common_behavior_helpers.py` (missing)

#### Rule: Feature identity extracts area and slug

- `bdd-feature-identity-from-path` Feature identity derives area from parent directory -> `tests/test_common_behavior_helpers.py` (missing)
- `bdd-feature-identity-no-area` Feature identity uses "behavior" when no area directory -> `tests/test_common_behavior_helpers.py` (missing)
- `bdd-feature-stem-markdown` feature_stem handles .feature.md suffix -> `tests/test_common_behavior_helpers.py` (missing)
- `bdd-feature-stem-classic` feature_stem handles .feature suffix -> `tests/test_common_behavior_helpers.py` (missing)

#### Rule: Canonical test path derivation

- `bdd-canonical-test-path` Test path is derived from feature path -> `tests/test_common_behavior_helpers.py` (missing)

#### Rule: Scenario iteration yields all scenarios

- `bdd-iter-scenarios-top-level` Iterator yields top-level scenarios -> `tests/test_common_behavior_helpers.py` (missing)
- `bdd-iter-scenarios-in-rules` Iterator yields scenarios from rules -> `tests/test_common_behavior_helpers.py` (missing)

#### Rule: Scenario ID extraction

- `bdd-scenario-id-value` scenario_id_value returns first @bdd-\* tag -> `tests/test_common_behavior_helpers.py` (missing)
- `bdd-scenario-id-missing` scenario_id_value returns empty string when no @bdd-\* tag -> `tests/test_common_behavior_helpers.py` (missing)

## config

### SpecWeave configuration management

- Path: `specs/behavior/features/config/configuration.feature`
- Summary: SpecWeave loads project configuration from TOML files, discovers config

#### Rule: Config discovery walks parent directories

- `bdd-config-discovery-finds-dotfile` Discovery finds .specweave.toml in current directory -> `tests/test_config_configuration.py` (missing)
- `bdd-config-discovery-finds-public` Discovery finds specweave.toml in current directory -> `tests/test_config_configuration.py` (missing)
- `bdd-config-discovery-prefers-dotfile` Discovery prefers .specweave.toml over specweave.toml -> `tests/test_config_configuration.py` (missing)
- `bdd-config-discovery-walks-parents` Discovery walks parent directories when not found locally -> `tests/test_config_configuration.py` (missing)
- `bdd-config-discovery-returns-none` Discovery returns None when no config exists -> `tests/test_config_configuration.py` (missing)

#### Rule: Config loading returns defaults when no file exists

- `bdd-config-load-defaults` Loading with no file returns default config -> `tests/test_config_configuration.py` (missing)
- `bdd-config-load-from-file` Loading reads values from a valid TOML file -> `tests/test_config_configuration.py` (missing)

#### Rule: Config rejects unsupported schema versions

- `bdd-config-rejects-unsupported-schema` Loading fails for schema_version 2 -> `tests/test_config_configuration.py` (missing)

#### Rule: Default config rendering is deterministic

- `bdd-config-render-behavior` Default config renders behavior spelling -> `tests/test_config_configuration.py` (missing)
- `bdd-config-render-behaviour` Default config renders behaviour spelling -> `tests/test_config_configuration.py` (missing)

## doctor

### SpecWeave project diagnostics

- Path: `specs/behavior/features/doctor/diagnostics.feature`
- Summary: specweave doctor checks the project setup, config, paths, and feature

#### Rule: Doctor checks config presence and schema

- `bdd-doctor-missing-config` Doctor warns when no config file exists -> `tests/test_doctor_diagnostics.py` (missing)
- `bdd-doctor-unsupported-schema` Doctor errors on unsupported schema version -> `tests/test_doctor_diagnostics.py` (missing)

#### Rule: Doctor checks directory existence

- `bdd-doctor-missing-directories` Doctor warns about missing directories -> `tests/test_doctor_diagnostics.py` (missing)
- `bdd-doctor-fix-creates-directories` Doctor --fix creates missing directories -> `tests/test_doctor_diagnostics.py` (missing)

#### Rule: Doctor checks for deprecated paths

- `bdd-doctor-deprecated-paths` Doctor warns about deprecated feature paths -> `tests/test_doctor_diagnostics.py` (missing)

#### Rule: Doctor checks for duplicate bdd tags

- `bdd-doctor-duplicate-bdd-tags` Doctor errors on duplicate @bdd-\* tags -> `tests/test_doctor_diagnostics.py` (missing)

#### Rule: Doctor validates feature files

- `bdd-doctor-validates-features` Doctor reports feature lint errors -> `tests/test_doctor_diagnostics.py` (missing)

## gherkin

### Gherkin feature file linting

- Path: `specs/behavior/features/gherkin/lint.feature`
- Summary: The linter checks canonical behavior feature files for structural problems,

#### Rule: Lint checks feature structure

- `bdd-lint-single-feature` Lint errors on multiple Feature lines -> `tests/test_gherkin_lint.py` (missing)
- `bdd-lint-empty-feature-title` Lint errors on empty feature title -> `tests/test_gherkin_lint.py` (missing)
- `bdd-lint-empty-scenario-title` Lint errors on empty scenario title -> `tests/test_gherkin_lint.py` (missing)
- `bdd-lint-missing-given-when-then` Lint errors when Given/When/Then are missing -> `tests/test_gherkin_lint.py` (missing)
- `bdd-lint-empty-rule` Lint errors on Rule without scenarios -> `tests/test_gherkin_lint.py` (missing)

#### Rule: Lint checks tag conventions

- `bdd-lint-duplicate-bdd-tags` Lint errors on duplicate @bdd-\* tags -> `tests/test_gherkin_lint.py` (missing)
- `bdd-lint-missing-bdd-tag` Lint warns when scenario lacks @bdd-\* tag -> `tests/test_gherkin_lint.py` (missing)
- `bdd-lint-task-tags-discouraged` Lint warns on task-specific tags in features -> `tests/test_gherkin_lint.py` (missing)

#### Rule: Lint checks file paths

- `bdd-lint-canonical-path` Lint errors on features outside canonical path -> `tests/test_gherkin_lint.py` (missing)
- `bdd-lint-area-subdirectory` Lint warns when feature is not in area subdirectory -> `tests/test_gherkin_lint.py` (missing)
- `bdd-lint-deprecated-path` Lint warns on deprecated feature paths -> `tests/test_gherkin_lint.py` (missing)

#### Rule: Strict mode reports unsupported constructs

- `bdd-lint-strict-unsupported` Strict mode warns on Scenario Outline -> `tests/test_gherkin_lint.py` (missing)

### Gherkin feature file parsing

- Path: `specs/behavior/features/gherkin/parser.feature`
- Summary: The Gherkin parser reads feature text and produces Feature/Rule/Scenario/Step

#### Rule: Classic Gherkin parsing extracts structure

- `bdd-parser-classic-feature` Parser extracts feature title and scenarios -> `tests/test_gherkin_parser.py` (missing)
- `bdd-parser-classic-rules` Parser extracts Rule blocks -> `tests/test_gherkin_parser.py` (missing)
- `bdd-parser-classic-tags` Parser preserves tags on features, rules, and scenarios -> `tests/test_gherkin_parser.py` (missing)
- `bdd-parser-classic-description` Parser preserves feature and scenario descriptions -> `tests/test_gherkin_parser.py` (missing)
- `bdd-parser-classic-top-level-scenarios` Parser handles top-level scenarios outside rules -> `tests/test_gherkin_parser.py` (missing)

#### Rule: Markdown Gherkin parsing

- `bdd-parser-markdown-feature` Parser extracts structure from markdown format -> `tests/test_gherkin_parser.py` (missing)

#### Rule: Parser dispatches by format

- `bdd-parser-dispatch-by-suffix` Parser selects markdown parser for .feature.md files -> `tests/test_gherkin_parser.py` (missing)
- `bdd-parser-dispatch-classic` Parser selects classic parser for .feature files -> `tests/test_gherkin_parser.py` (missing)

#### Rule: Parser requires Feature line

- `bdd-parser-requires-feature-line` Parser raises ValueError without Feature line -> `tests/test_gherkin_parser.py` (missing)

### Gherkin feature file writing

- Path: `specs/behavior/features/gherkin/writer.feature`
- Summary: The Gherkin writer serializes Feature dataclass instances back to

#### Rule: Writer produces canonical Gherkin output

- `bdd-writer-basic-feature` Writer serializes a feature with scenarios -> `tests/test_gherkin_writer.py` (missing)
- `bdd-writer-rules` Writer serializes Rule blocks -> `tests/test_gherkin_writer.py` (missing)
- `bdd-writer-tags` Writer preserves tags at all levels -> `tests/test_gherkin_writer.py` (missing)
- `bdd-writer-descriptions` Writer preserves descriptions -> `tests/test_gherkin_writer.py` (missing)
- `bdd-writer-roundtrip` Parsing then writing produces equivalent output -> `tests/test_gherkin_writer.py` (missing)

## init

### SpecWeave project initialization

- Path: `specs/behavior/features/init/initialization.feature`
- Summary: specweave init creates the config file and directory layout for a new

#### Rule: Init creates config and directories

- `bdd-init-creates-dotfile` Init creates .specweave.toml by default -> `tests/test_init_initialization.py` (missing)
- `bdd-init-creates-public-config` Init creates specweave.toml with --public-config -> `tests/test_init_initialization.py` (missing)
- `bdd-init-creates-readme` Init creates a managed README in specs root -> `tests/test_init_initialization.py` (missing)
- `bdd-init-creates-gitkeep` Init creates .gitkeep in features directory -> `tests/test_init_initialization.py` (missing)

#### Rule: Init is idempotent

- `bdd-init-idempotent` Running init twice does not fail -> `tests/test_init_initialization.py` (missing)

#### Rule: Init supports British spelling

- `bdd-init-british-spelling` Init creates behaviour layout with --spelling behaviour -> `tests/test_init_initialization.py` (missing)

#### Rule: Init supports dry-run mode

- `bdd-init-dry-run` Dry-run reports paths without writing -> `tests/test_init_initialization.py` (missing)

#### Rule: Init refuses to overwrite non-managed README

- `bdd-init-refuses-overwrite-readme` Init skips non-SpecWeave README -> `tests/test_init_initialization.py` (missing)
- `bdd-init-force-overwrites-readme` Init overwrites managed README with --force -> `tests/test_init_initialization.py` (missing)

#### Rule: Init warns about existing config

- `bdd-init-warns-existing-config` Init warns when config already exists -> `tests/test_init_initialization.py` (missing)

## integrations

### Archledger integration

- Path: `specs/behavior/features/integrations/archledger.feature`
- Summary: SpecWeave generates draft Archledger candidate markdown for scenarios that are selected for durable traceability. It does not write accepted Archledger records.

#### Rule: Archledger candidate generation

- `bdd-archledger-candidate` archledger command renders candidate markdown -> `tests/test_integrations_archledger.py` (missing)
- `bdd-archledger-unknown-bdd` archledger errors on unknown @bdd-\* id -> `tests/test_integrations_archledger.py` (missing)

#### Rule: Archledger does not write accepted records by default

- `bdd-archledger-candidate-only` archledger produces candidates, not accepted records -> `tests/test_integrations_archledger.py` (missing)

### Taskledger integration

- Path: `specs/behavior/features/integrations/taskledger.feature`
- Summary: SpecWeave treats Taskledger exports as input artifacts and writes evidence as output artifact data. Taskledger remains responsible for importing validation evidence into task state.

#### Rule: Taskledger task draft generation

- `bdd-taskledger-draft` create taskledger-task generates a draft JSON -> `tests/test_integrations_taskledger.py` (missing)
- `bdd-taskledger-draft-ac-mapping` Draft maps @ac-\* tags to acceptance criteria -> `tests/test_integrations_taskledger.py` (missing)

#### Rule: Taskledger behavior import

- `bdd-taskledger-import` import-taskledger creates a feature from Taskledger export -> `tests/test_integrations_taskledger.py` (missing)

#### Rule: Taskledger evidence generation

- `bdd-taskledger-evidence` report normalize generates Taskledger-compatible evidence -> `tests/test_integrations_taskledger.py` (missing)

#### Rule: Cross-ledger trace diagnostics

- `bdd-trace-json` trace emits a behavior-centered trace bundle -> `tests/test_trace.py`
- `bdd-combi-check` combi check audits Taskledger, SpecWeave, pytest, evidence, and Archledger links without mutating ledgers -> `tests/test_combi_check.py`

## reports

### Fail-closed evidence semantics

- Path: `specs/behavior/features/reports/fail-closed.feature`
- Summary: SpecWeave enforces fail-closed semantics for acceptance criteria. A

#### Rule: Blocking statuses fail linked criteria

- `bdd-fail-closed-failed-scenario` Failed scenario fails the linked criterion -> `tests/test_reports_fail_closed.py` (missing)
- `bdd-fail-closed-skipped-scenario` Skipped scenario fails the criterion by default -> `tests/test_reports_fail_closed.py` (missing)
- `bdd-fail-closed-undefined-scenario` Undefined scenario fails the criterion -> `tests/test_reports_fail_closed.py` (missing)
- `bdd-fail-closed-pending-scenario` Pending scenario fails the criterion -> `tests/test_reports_fail_closed.py` (missing)
- `bdd-fail-closed-ambiguous-scenario` Ambiguous scenario fails the criterion -> `tests/test_reports_fail_closed.py` (missing)

#### Rule: Only passing scenarios satisfy criteria

- `bdd-fail-closed-passed-scenario` Passed scenario satisfies the criterion -> `tests/test_reports_fail_closed.py` (missing)

#### Rule: Unlinked scenarios do not affect criteria

- `bdd-fail-closed-unlinked-scenario` Unlinked scenario does not satisfy any criterion -> `tests/test_reports_fail_closed.py` (missing)

#### Rule: Multiple scenarios for one criterion

- `bdd-fail-closed-multiple-scenarios` One failed scenario fails the whole criterion -> `tests/test_reports_fail_closed.py` (missing)

#### Rule: Exit code alone is not sufficient evidence

- `bdd-fail-closed-exit-code-not-evidence` Passing exit code does not override failed scenarios -> `tests/test_reports_fail_closed.py` (missing)

### Report tag mapping and acceptance coverage

- Path: `specs/behavior/features/reports/mapping.feature`
- Summary: The reports.mapping module extracts BDD and acceptance criterion IDs

#### Rule: Tag extraction identifies BDD and AC IDs

- `bdd-tag-extraction-bdd` Extraction finds @bdd-\* tags -> `tests/test_reports_mapping.py` (missing)
- `bdd-tag-extraction-ac` Extraction finds @ac-\* tags -> `tests/test_reports_mapping.py` (missing)
- `bdd-tag-extraction-empty` Extraction returns empty lists when no matching tags -> `tests/test_reports_mapping.py` (missing)

#### Rule: Criteria summarization groups by AC ID

- `bdd-criteria-summary` Summarization groups scenarios by acceptance criterion -> `tests/test_reports_mapping.py` (missing)
- `bdd-criteria-fail-closed` Failed scenarios fail the linked criterion -> `tests/test_reports_mapping.py` (missing)
- `bdd-criteria-missing-coverage` Expected AC with no scenarios fails coverage -> `tests/test_reports_mapping.py` (missing)

### Report normalization and evidence generation

- Path: `specs/behavior/features/reports/normalization.feature`
- Summary: specweave report normalize parses runner-native reports (JUnit XML,

#### Rule: Normalization parses supported formats

- `bdd-normalize-junit-xml` Normalization parses JUnit XML reports -> `tests/test_reports_normalization.py` (missing)
- `bdd-normalize-cucumber-json` Normalization parses Cucumber JSON reports -> `tests/test_reports_normalization.py` (missing)
- `bdd-normalize-unsupported-format` Normalization rejects unsupported formats -> `tests/test_reports_normalization.py` (missing)

#### Rule: Normalization computes overall status

- `bdd-normalize-all-passed` Report status is passed when all scenarios pass -> `tests/test_reports_normalization.py` (missing)
- `bdd-normalize-any-failed` Report status is failed when any scenario fails -> `tests/test_reports_normalization.py` (missing)
- `bdd-normalize-skipped-fails-by-default` Skipped scenarios fail the report by default -> `tests/test_reports_normalization.py` (missing)
- `bdd-normalize-allow-skipped` Skipped scenarios pass with --allow-skipped -> `tests/test_reports_normalization.py` (missing)

#### Rule: Normalization enforces acceptance criteria coverage

- `bdd-normalize-missing-ac-coverage` Report fails when expected AC has no passing scenario -> `tests/test_reports_normalization.py` (missing)
- `bdd-normalize-ac-covered` Report passes when expected AC has a passing scenario -> `tests/test_reports_normalization.py` (missing)

#### Rule: Normalization generates evidence JSON

- `bdd-normalize-evidence-json` Normalization writes Taskledger evidence JSON -> `tests/test_reports_normalization.py` (missing)

### Report format parsers

- Path: `specs/behavior/features/reports/parsers.feature`
- Summary: SpecWeave parses JUnit XML and Cucumber JSON reports into ScenarioResult

#### Rule: JUnit XML parser extracts test cases

- `bdd-junit-parse-cases` Parser extracts test cases from JUnit XML -> `tests/test_reports_parsers.py` (missing)
- `bdd-junit-parse-statuses` Parser maps JUnit statuses correctly -> `tests/test_reports_parsers.py` (missing)
- `bdd-junit-parse-duration` Parser extracts test duration -> `tests/test_reports_parsers.py` (missing)

#### Rule: Cucumber JSON parser extracts scenarios

- `bdd-cucumber-parse-scenarios` Parser extracts scenarios from Cucumber JSON -> `tests/test_reports_parsers.py` (missing)
- `bdd-cucumber-parse-tags` Parser extracts tags from Cucumber scenarios -> `tests/test_reports_parsers.py` (missing)

## review

### Behavior spec review

- Path: `specs/behavior/features/review/spec-review.feature`
- Summary: specweave review specs aggregates lint, coverage, and convention findings

#### Rule: Review reports feature and scenario counts

- `bdd-review-counts` Review reports feature and scenario statistics -> `tests/test_review_spec_review.py` (missing)

#### Rule: Review reports missing bindings

- `bdd-review-missing-bindings` Review warns about unbound scenarios -> `tests/test_review_spec_review.py` (missing)

#### Rule: Review reports needs-review tags

- `bdd-review-needs-review` Review warns about @needs-review scenarios -> `tests/test_review_spec_review.py` (missing)

#### Rule: Review reports deprecated paths

- `bdd-review-deprecated-paths` Review warns about deprecated paths -> `tests/test_review_spec_review.py` (missing)

#### Rule: Review reports forbidden pytest-bdd usage

- `bdd-review-forbidden-pytest-bdd` Review errors on pytest-bdd usage -> `tests/test_review_spec_review.py` (missing)

#### Rule: Review aggregates lint findings

- `bdd-review-lint-findings` Review includes lint errors and warnings -> `tests/test_review_spec_review.py` (missing)

## translation

### Brownfield pytest-to-Gherkin generation

- Path: `specs/behavior/features/translation/pytest-to-gherkin.feature`
- Summary: specweave create gherkin generates draft Gherkin feature files from

#### Rule: Generation discovers tests via AST

- `bdd-translate-discovers-tests` Generation finds test functions in pytest files -> `tests/test_translation_pytest_to_gherkin.py` (missing)
- `bdd-translate-group-by-file` Generation groups scenarios by test file -> `tests/test_translation_pytest_to_gherkin.py` (missing)

#### Rule: Generation preserves existing features

- `bdd-translate-preserve-manual` Generation does not overwrite manual feature files -> `tests/test_translation_pytest_to_gherkin.py` (missing)
- `bdd-translate-force-overwrite` Generation overwrites with --force -> `tests/test_translation_pytest_to_gherkin.py` (missing)

#### Rule: Generation marks drafts appropriately

- `bdd-translate-marks-generated` Generated features have @generated tag -> `tests/test_translation_pytest_to_gherkin.py` (missing)

#### Rule: Generation supports dry-run mode

- `bdd-translate-dry-run` Dry-run reports without writing files -> `tests/test_translation_pytest_to_gherkin.py` (missing)
