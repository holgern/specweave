# Behavior index

Generated from `specs/behavior/features`.

## backends

### pytest-bdd step-skeleton backend
- Path: `specs/behavior/features/backends/pytest-bdd.feature.md`
- Summary: SpecWeave provides a legacy/bridge backend that generates pytest-bdd step

#### Rule: Backend registry

- `bdd-backend-registry` Supported backends include behave and pytest-bdd -> `tests/test_backends_pytest_bdd.py` (missing)
- `bdd-backend-unsupported` Unsupported Cucumber backends report clear messages -> `tests/test_backends_pytest_bdd.py` (missing)

#### Rule: Generate pytest-bdd skeleton

- `bdd-backend-pytest-bdd-skeleton` Skeleton includes pytest-bdd imports, scenarios, and step decorators -> `tests/test_backends_pytest_bdd.py` (missing)
- `bdd-backend-pytest-bdd-dedup` Repeated steps appear only once in the skeleton -> `tests/test_backends_pytest_bdd.py` (missing)
- `bdd-backend-pytest-bdd-rule-scenarios` Steps inside Rule blocks are included -> `tests/test_backends_pytest_bdd.py` (missing)
- `bdd-backend-pytest-bdd-source-path` Skeleton uses the source feature filename when available -> `tests/test_backends_pytest_bdd.py` (missing)

## bdd

### Task-BDD JSON to Gherkin conversion
- Path: `specs/behavior/features/bdd/convert.feature.md`
- Summary: SpecWeave converts between its internal Task-BDD JSON model and canonical

#### Rule: Export Task-BDD spec to classic Gherkin

- `bdd-bridge-export-to-gherkin` Task-BDD spec renders as target Gherkin with all tags -> `tests/test_bdd_convert.py` (missing)

#### Rule: Round-trip preserves all IDs and content

- `bdd-bridge-roundtrip-ids` Export then import preserves task, rule, bdd, and ac ids -> `tests/test_bdd_convert.py` (missing)
- `bdd-bridge-multiple-ac` Multiple acceptance criteria and custom tags survive round-trip -> `tests/test_bdd_convert.py` (missing)

#### Rule: Top-level examples become top-level scenarios

- `bdd-bridge-top-level` Example without rule_id renders as top-level scenario -> `tests/test_bdd_convert.py` (missing)

#### Rule: And/But steps group correctly

- `bdd-bridge-and-but-steps` Multiple Given/When/Then entries render as And/But steps -> `tests/test_bdd_convert.py` (missing)

#### Rule: JSON store read/write

- `bdd-bridge-json-roundtrip` save then load is idempotent -> `tests/test_bdd_convert.py` (missing)
- `bdd-bridge-json-to-feature-to-json` JSON to feature to JSON preserves all ids -> `tests/test_bdd_convert.py` (missing)

## behavior

### Static behavior coverage checks
- Path: `specs/behavior/features/behavior/coverage.feature.md`
- Summary: specweave behavior coverage checks the mapping between behavior feature

#### Rule: Coverage identifies bound and unbound scenarios

- `bdd-coverage-bound-scenario` Coverage marks bound scenarios -> `tests/test_behavior_coverage.py::test_behavior_coverage_feature_md_bound_by_comment` (bound)
- `bdd-coverage-unbound-scenario` Coverage reports missing bindings -> `tests/test_behavior_coverage.py::test_behavior_coverage_does_not_match_by_title` (bound)
- `bdd-coverage-missing-test-file` Coverage reports missing test files -> `tests/test_behavior_coverage.py::test_coverage_missing_test_file` (bound)

#### Rule: Coverage detects stale bindings

- `bdd-coverage-stale-binding` Coverage reports bindings to non-existent features -> `tests/test_behavior_coverage.py::test_coverage_stale_feature_binding` (bound)
- `bdd-coverage-stale-scenario` Coverage reports bindings to non-existent scenarios -> `tests/test_behavior_coverage.py::test_behavior_coverage_reports_stale_markdown_mapping` (bound)

#### Rule: Coverage detects deprecated paths

- `bdd-coverage-deprecated-paths` Coverage reports deprecated feature paths -> `tests/test_behavior_coverage.py::test_coverage_deprecated_paths` (bound)

#### Rule: Coverage detects forbidden pytest-bdd usage

- `bdd-coverage-forbidden-pytest-bdd` Coverage reports pytest-bdd imports in test files -> `tests/test_behavior_coverage.py::test_behavior_coverage_reports_forbidden_pytest_bdd_usage` (bound)

#### Rule: Coverage skips manual and waived scenarios

- `bdd-coverage-manual-scenario` Coverage skips scenarios tagged @manual -> `tests/test_behavior_coverage.py::test_coverage_manual_scenario_skipped` (bound)

### Plain pytest skeleton generation
- Path: `specs/behavior/features/behavior/generation.feature.md`
- Summary: specweave behavior generate-tests creates plain pytest test skeletons

#### Rule: Generation creates pytest skeletons

- `bdd-generate-single-feature` Generation creates a test file for a feature -> `tests/test_behavior_generation.py::test_generate_single_feature` (bound)
- `bdd-generate-scenario-function` Each scenario becomes a test function -> `tests/test_behavior_generation.py::test_generate_scenario_function` (bound)
- `bdd-generate-specweave-markers` Test functions have correct specweave markers -> `tests/test_behavior_generation.py::test_generate_specweave_markers` (bound)
- `bdd-generate-docstring` Test functions have docstrings with scenario details -> `tests/test_behavior_generation.py::test_generate_docstring` (bound)
- `bdd-generate-step-comments` Test functions have step comments -> `tests/test_behavior_generation.py::test_generate_step_comments` (bound)

#### Rule: Generation derives canonical test paths

- `bdd-generate-canonical-path` Test path is derived from feature path -> `tests/test_behavior_generation.py::test_generate_canonical_path` (bound)

#### Rule: Generation handles rules

- `bdd-generate-rules` Scenarios in rules get rule markers -> `tests/test_behavior_generation.py::test_generate_rules` (bound)

#### Rule: Generation supports batch mode

- `bdd-generate-batch` Generation processes all features in a directory -> `tests/test_behavior_generation.py::test_generate_batch` (bound)

### Behavior index and manifest generation
- Path: `specs/behavior/features/behavior/index.feature.md`
- Summary: specweave behavior index generates a Markdown index and JSON manifest

#### Rule: Index generation scans feature files

- `bdd-index-generates-markdown` Index generates Markdown with feature listing -> `tests/test_behavior_index.py::test_index_generates_markdown` (bound)
- `bdd-index-generates-manifest` Index generates JSON manifest with scenario mappings -> `tests/test_behavior_index.py::test_index_generates_manifest` (bound)
- `bdd-index-scenario-entries` Manifest includes scenario entries with automation status -> `tests/test_behavior_index.py::test_index_scenario_entries` (bound)
- `bdd-index-unbound-scenario` Manifest marks unbound scenarios as missing -> `tests/test_behavior_index.py::test_index_unbound_scenario` (bound)

#### Rule: Index reflects evidence status

- `bdd-index-evidence-status` Manifest includes latest evidence status when available -> `tests/test_behavior_index.py::test_index_evidence_status` (bound)

#### Rule: Index supports rule blocks

- `bdd-index-rules` Manifest preserves Rule structure -> `tests/test_behavior_index.py::test_index_rules` (bound)

### Behavior evidence import from pytest reports
- Path: `specs/behavior/features/behavior/reporting.feature.md`
- Summary: specweave behavior import-report imports pytest/JUnit XML reports into

#### Rule: Import maps test results to scenarios

- `bdd-import-maps-by-nodeid` Import maps results by normalized nodeid -> `tests/test_behavior_reporting.py::test_import_maps_by_nodeid` (bound)
- `bdd-import-maps-by-function-name` Import falls back to function name matching -> `tests/test_behavior_reporting.py::test_import_maps_by_function_name` (bound)
- `bdd-import-maps-by-manifest` Import uses manifest mappings when available -> `tests/test_behavior_reporting.py::test_import_maps_by_manifest` (bound)

#### Rule: Import reports unmapped tests

- `bdd-import-unmapped-tests` Import reports tests without specweave markers -> `tests/test_behavior_reporting.py::test_import_unmapped_tests` (bound)

#### Rule: Import writes evidence JSON

- `bdd-import-writes-evidence` Import writes evidence to the target path -> `tests/test_behavior_reporting.py::test_import_writes_evidence` (bound)

## cli

### SpecWeave CLI contract
- Path: `specs/behavior/features/cli/cli-contract.feature.md`
- Summary: The SpecWeave CLI provides commands for behavior-driven development

#### Rule: Root options work across all commands

- `bdd-cli-config-option` --config selects an explicit config path -> `tests/test_cli_cli_contract.py::test_config_option` (bound)
- `bdd-cli-json-output` --json produces machine-readable output -> `tests/test_cli_cli_contract.py::test_json_output` (bound)
- `bdd-cli-json-init` init --json produces machine-readable output -> `tests/test_cli_cli_contract.py::test_json_init` (bound)

#### Rule: Behavior subcommands work correctly

- `bdd-cli-behavior-check` behavior check lints feature files -> `tests/test_cli_cli_contract.py::test_behavior_check_accepts_canonical_feature` (bound)
- `bdd-cli-behavior-index` behavior index generates index and manifest -> `tests/test_cli_cli_contract.py::test_behavior_index_writes_markdown_and_manifest` (bound)
- `bdd-cli-behavior-generate-tests` behavior generate-tests creates pytest skeletons -> `tests/test_cli_cli_contract.py::test_behavior_generate_tests_creates_plain_pytest` (bound)
- `bdd-cli-behavior-coverage` behavior coverage checks spec-to-test mapping -> `tests/test_cli_cli_contract.py::test_behavior_coverage_reports_bound_scenarios` (bound)
- `bdd-cli-behavior-import-report` behavior import-report imports JUnit XML -> `tests/test_cli_cli_contract.py::test_behavior_import_report_maps_pytest_nodeid` (bound)

#### Rule: BDD compatibility aliases work

- `bdd-cli-bdd-check-alias` bdd check is an alias for behavior check -> `tests/test_cli_cli_contract.py::test_bdd_check_alias` (bound)
- `bdd-cli-bdd-index-alias` bdd index is an alias for behavior index -> `tests/test_cli_cli_contract.py::test_bdd_index_alias` (bound)

#### Rule: Create subcommands work correctly

- `bdd-cli-create-feature` create feature writes a new Gherkin feature file -> `tests/test_cli_cli_contract.py::test_create_feature` (bound)
- `bdd-cli-create-gherkin` create gherkin generates features from tests -> `tests/test_cli_cli_contract.py::test_create_gherkin` (bound)
- `bdd-cli-create-plan` create plan generates an implementation plan -> `tests/test_cli_cli_contract.py::test_create_plan` (bound)

#### Rule: Exit codes reflect result status

- `bdd-cli-exit-doctor-failed` doctor exits non-zero when errors found -> `tests/test_cli_cli_contract.py::test_exit_doctor_failed` (bound)
- `bdd-cli-exit-check-errors` behavior check exits non-zero on lint errors -> `tests/test_cli_cli_contract.py::test_exit_check_errors` (bound)
- `bdd-cli-exit-normalize-failed` report normalize exits non-zero when report failed -> `tests/test_cli_cli_contract.py::test_report_normalize_writes_json_and_exits_nonzero_on_failure` (bound)

## common

### Behavior helper functions
- Path: `specs/behavior/features/common/behavior-helpers.feature.md`
- Summary: The behavior.common module provides shared helpers for slugification,

#### Rule: Slugification produces stable lowercase slugs

- `bdd-slugify-basic` Slugify converts text to lowercase slug -> `tests/test_common_behavior_helpers.py::test_basic` (bound)
- `bdd-slugify-special-chars` Slugify replaces special characters with hyphens -> `tests/test_common_behavior_helpers.py::test_special_chars` (bound)
- `bdd-slugify-empty` Slugify returns "behavior" for empty input -> `tests/test_common_behavior_helpers.py::test_empty` (bound)

#### Rule: Feature identity extracts area and slug

- `bdd-feature-identity-from-path` Feature identity derives area from parent directory -> `tests/test_common_behavior_helpers.py::test_from_path` (bound)
- `bdd-feature-identity-no-area` Feature identity uses "behavior" when no area directory -> `tests/test_common_behavior_helpers.py::test_no_area` (bound)
- `bdd-feature-stem-markdown` feature_stem handles .feature.md suffix -> `tests/test_common_behavior_helpers.py::test_feature_md` (bound)
- `bdd-feature-stem-classic` feature_stem handles .feature suffix -> `tests/test_common_behavior_helpers.py::test_classic_feature` (bound)

#### Rule: Canonical test path derivation

- `bdd-canonical-test-path` Test path is derived from feature path -> `tests/test_common_behavior_helpers.py::test_derives_path` (bound)

#### Rule: Scenario iteration yields all scenarios

- `bdd-iter-scenarios-top-level` Iterator yields top-level scenarios -> `tests/test_common_behavior_helpers.py::test_yields_top_level` (bound)
- `bdd-iter-scenarios-in-rules` Iterator yields scenarios from rules -> `tests/test_common_behavior_helpers.py::test_yields_from_rules` (bound)

#### Rule: Scenario ID extraction

- `bdd-scenario-id-value` scenario_id_value returns first @bdd-\* tag -> `tests/test_common_behavior_helpers.py::test_returns_first_bdd_tag` (bound)
- `bdd-scenario-id-missing` scenario_id_value returns empty string when no @bdd-\* tag -> `tests/test_common_behavior_helpers.py::test_returns_empty_when_no_bdd` (bound)

## config

### SpecWeave configuration management
- Path: `specs/behavior/features/config/configuration.feature.md`
- Summary: SpecWeave loads project configuration from TOML files, discovers config

#### Rule: Config discovery walks parent directories

- `bdd-config-discovery-finds-dotfile` Discovery finds .specweave.toml in current directory -> `tests/test_config_configuration.py::test_prefers_explicit` (bound)
- `bdd-config-discovery-finds-public` Discovery finds specweave.toml in current directory -> `tests/test_config_configuration.py::test_finds_public_config` (bound)
- `bdd-config-discovery-prefers-dotfile` Discovery prefers .specweave.toml over specweave.toml -> `tests/test_config_configuration.py::test_prefers_dotfile_over_public` (bound)
- `bdd-config-discovery-walks-parents` Discovery walks parent directories when not found locally -> `tests/test_config_configuration.py::test_walks_up_directories` (bound)
- `bdd-config-discovery-returns-none` Discovery returns None when no config exists -> `tests/test_config_configuration.py::test_returns_none_when_missing` (bound)

#### Rule: Config loading returns defaults when no file exists

- `bdd-config-load-defaults` Loading with no file returns default config -> `tests/test_config_configuration.py::test_defaults_when_missing` (bound)
- `bdd-config-load-from-file` Loading reads values from a valid TOML file -> `tests/test_config_configuration.py::test_normalizes_paths` (bound)

#### Rule: Config rejects unsupported schema versions

- `bdd-config-rejects-unsupported-schema` Loading fails for schema_version 2 -> `tests/test_config_configuration.py::test_rejects_unsupported_schema` (bound)

#### Rule: Default config rendering is deterministic

- `bdd-config-render-behavior` Default config renders behavior spelling -> `tests/test_config_configuration.py::test_renders_behavior` (bound)
- `bdd-config-render-behaviour` Default config renders behaviour spelling -> `tests/test_config_configuration.py::test_renders_behaviour` (bound)

## doctor

### SpecWeave project diagnostics
- Path: `specs/behavior/features/doctor/diagnostics.feature.md`
- Summary: specweave doctor checks the project setup, config, paths, and feature

#### Rule: Doctor checks config presence and schema

- `bdd-doctor-missing-config` Doctor warns when no config file exists -> `tests/test_doctor_diagnostics.py::test_no_config_warning` (bound)
- `bdd-doctor-unsupported-schema` Doctor errors on unsupported schema version -> `tests/test_doctor_diagnostics.py::test_unsupported_schema` (bound)

#### Rule: Doctor checks directory existence

- `bdd-doctor-missing-directories` Doctor warns about missing directories -> `tests/test_doctor_diagnostics.py::test_reports_missing_features_dir` (bound)
- `bdd-doctor-fix-creates-directories` Doctor --fix creates missing directories -> `tests/test_doctor_diagnostics.py::test_fix_creates_missing_dirs` (bound)

#### Rule: Doctor checks for deprecated paths

- `bdd-doctor-deprecated-paths` Doctor warns about deprecated feature paths -> `tests/test_doctor_diagnostics.py::test_detects_deprecated` (bound)

#### Rule: Doctor checks for duplicate bdd tags

- `bdd-doctor-duplicate-bdd-tags` Doctor errors on duplicate @bdd-\* tags -> `tests/test_doctor_diagnostics.py::test_detects_duplicates` (bound)

#### Rule: Doctor validates feature files

- `bdd-doctor-validates-features` Doctor reports feature lint errors -> `tests/test_doctor_diagnostics.py::test_passes_initialized_project` (bound)

## exchange

### Exchange schema contracts
- Path: `specs/behavior/features/exchange/schemas.feature.md`
- Summary: SpecWeave defines JSON Schema documents for its file-based exchange

#### Rule: Schema files are valid JSON Schema documents

- `bdd-exchange-schema-valid` Each exchange schema is a valid JSON Schema -> `tests/test_exchange_schemas.py` (missing)

#### Rule: Representative payloads satisfy schema requirements

- `bdd-exchange-combi-trace-schema` Combi trace representative payload satisfies required fields -> `tests/test_exchange_schemas.py` (missing)
- `bdd-exchange-taskledger-schema` Taskledger BDD export representative payload satisfies schema -> `tests/test_exchange_schemas.py` (missing)
- `bdd-exchange-evidence-schema` Behavior evidence representative payload satisfies schema -> `tests/test_exchange_schemas.py` (missing)
- `bdd-exchange-archledger-schema` Archledger candidate representative payload satisfies schema -> `tests/test_exchange_schemas.py` (missing)

## gherkin

### Gherkin document format conversion
- Path: `specs/behavior/features/gherkin/convert.feature.md`
- Summary: SpecWeave converts between classic `.feature` and Markdown `.feature.md`

#### Rule: Infer format from file suffix

- `bdd-convert-infer-format` Suffix `.feature` infers classic format -> `tests/test_gherkin_convert.py` (missing)
- `bdd-convert-infer-markdown` Suffix `.feature.md` infers markdown format -> `tests/test_gherkin_convert.py` (missing)

#### Rule: Convert classic to markdown

- `bdd-convert-classic-to-markdown` Classic feature becomes markdown without losing structure -> `tests/test_gherkin_convert.py` (missing)
- `bdd-convert-default-output-path` Default output path derives from source -> `tests/test_gherkin_convert.py` (missing)

#### Rule: Protect existing output

- `bdd-convert-refuses-overwrite` Conversion refuses to overwrite existing output -> `tests/test_gherkin_convert.py` (missing)

#### Rule: Batch directory conversion

- `bdd-convert-directory` Convert all classic features in a directory tree -> `tests/test_gherkin_convert.py` (missing)
- `bdd-convert-keeps-source` Batch conversion keeps source files by default -> `tests/test_gherkin_convert.py` (missing)
- `bdd-convert-replace-source` Replace source removes classic files after success -> `tests/test_gherkin_convert.py` (missing)
- `bdd-convert-dry-run` Dry-run reports without writing files -> `tests/test_gherkin_convert.py` (missing)
- `bdd-convert-collision` Batch conversion reports collision as error -> `tests/test_gherkin_convert.py` (missing)

#### Rule: Content-based format detection

- `bdd-convert-from-content-classic` Detect classic content in a `.feature.md` file -> `tests/test_gherkin_convert.py` (missing)
- `bdd-convert-from-content-markdown` Detect markdown content already in markdown format -> `tests/test_gherkin_convert.py` (missing)

#### Rule: CLI JSON output contract

- `bdd-convert-cli-json` Single-file conversion reports JSON with format info -> `tests/test_gherkin_convert.py` (missing)
- `bdd-convert-cli-batch-json` Batch conversion with --all reports JSON summary -> `tests/test_gherkin_convert.py` (missing)

### Gherkin feature file linting
- Path: `specs/behavior/features/gherkin/lint.feature.md`
- Summary: The linter checks canonical behavior feature files for structural problems,

#### Rule: Lint checks feature structure

- `bdd-lint-single-feature` Lint errors on multiple Feature lines -> `tests/test_gherkin_lint.py::test_lint_multiple_feature_lines` (bound)
- `bdd-lint-empty-feature-title` Lint errors on empty feature title -> `tests/test_gherkin_lint.py::test_lint_empty_feature_title` (bound)
- `bdd-lint-empty-scenario-title` Lint errors on empty scenario title -> `tests/test_gherkin_lint.py::test_lint_empty_scenario_title` (bound)
- `bdd-lint-missing-given-when-then` Lint errors when Given/When/Then are missing -> `tests/test_gherkin_lint.py::test_lint_missing_given_when_then` (bound)
- `bdd-lint-empty-rule` Lint errors on Rule without scenarios -> `tests/test_gherkin_lint.py::test_lint_empty_rule` (bound)

#### Rule: Lint checks tag conventions

- `bdd-lint-duplicate-bdd-tags` Lint errors on duplicate @bdd-\* tags -> `tests/test_gherkin_lint.py::test_lint_duplicate_bdd_tags` (bound)
- `bdd-lint-missing-bdd-tag` Lint warns when scenario lacks @bdd-\* tag -> `tests/test_gherkin_lint.py::test_lint_missing_bdd_tag` (bound)
- `bdd-lint-task-tags-discouraged` Lint warns on task-specific tags in features -> `tests/test_gherkin_lint.py::test_lint_task_tags_discouraged` (bound)

#### Rule: Lint checks file paths

- `bdd-lint-canonical-path` Lint errors on features outside canonical path -> `tests/test_gherkin_lint.py::test_lint_canonical_path` (bound)
- `bdd-lint-area-subdirectory` Lint warns when feature is not in area subdirectory -> `tests/test_gherkin_lint.py::test_lint_area_subdirectory` (bound)
- `bdd-lint-deprecated-path` Lint warns on deprecated feature paths -> `tests/test_gherkin_lint.py::test_lint_deprecated_path` (bound)

#### Rule: Strict mode reports unsupported constructs

- `bdd-lint-strict-unsupported` Strict mode warns on Scenario Outline -> `tests/test_gherkin_lint.py::test_lint_strict_unsupported` (bound)

### Markdown-with-Gherkin parser and writer
- Path: `specs/behavior/features/gherkin/markdown.feature.md`
- Summary: SpecWeave parses and writes `.feature.md` files using a Markdown-with-Gherkin

#### Rule: Parse markdown feature structure

- `bdd-md-parse-feature` Parser extracts feature title and tags from markdown -> `tests/test_gherkin_markdown.py` (missing)
- `bdd-md-parse-rule-scenario` Parser extracts Rule and Scenario with tags -> `tests/test_gherkin_markdown.py` (missing)
- `bdd-md-parse-steps` Parser extracts Given, When, Then steps from bullets -> `tests/test_gherkin_markdown.py` (missing)
- `bdd-md-parse-top-level` Parser extracts top-level scenarios outside rules -> `tests/test_gherkin_markdown.py` (missing)
- `bdd-md-parse-description` Parser preserves feature description text -> `tests/test_gherkin_markdown.py` (missing)
- `bdd-md-parse-ignores-prose` Parser ignores non-Gherkin markdown around the feature -> `tests/test_gherkin_markdown.py` (missing)
- `bdd-md-parse-requires-backticked-tags` Classic @tags without backticks are not parsed as tags -> `tests/test_gherkin_markdown.py` (missing)
- `bdd-md-parse-empty-feature` Parser handles a feature with no rules or scenarios -> `tests/test_gherkin_markdown.py` (missing)

#### Rule: Write markdown feature output

- `bdd-md-write-feature` Writer produces properly formatted markdown -> `tests/test_gherkin_markdown.py` (missing)
- `bdd-md-write-roundtrip` Parse-write-parse round-trip preserves model -> `tests/test_gherkin_markdown.py` (missing)

#### Rule: Convert markdown to classic

- `bdd-md-to-classic` Markdown feature converts to classic Gherkin -> `tests/test_gherkin_markdown.py` (missing)
- `bdd-md-to-classic-validates` Converted classic text validates with official parser -> `tests/test_gherkin_markdown.py` (missing)

#### Rule: Tag helper utilities

- `bdd-md-has-backticked-tags` Detect backticked tags on a line -> `tests/test_gherkin_markdown.py` (missing)
- `bdd-md-parse-backticked-tags` Extract tag names from backticked tag text -> `tests/test_gherkin_markdown.py` (missing)

### Official Cucumber Gherkin parser adapter
- Path: `specs/behavior/features/gherkin/official.feature.md`
- Summary: SpecWeave wraps the official `gherkin-official` parser to validate classic

#### Rule: Parse classic Gherkin with the official parser

- `bdd-official-parse-simple` Official parser extracts feature title, tags, and description -> `tests/test_gherkin_official.py` (missing)
- `bdd-official-parse-rules` Official parser extracts Rule blocks with tags -> `tests/test_gherkin_official.py` (missing)
- `bdd-official-parse-no-tags` Official parser handles features without tags -> `tests/test_gherkin_official.py` (missing)
- `bdd-official-source-path` Official parser stores the source path when provided -> `tests/test_gherkin_official.py` (missing)
- `bdd-official-compile-pickles` Official parser supports pickle compilation mode -> `tests/test_gherkin_official.py` (missing)

#### Rule: Validate classic Gherkin syntax

- `bdd-official-validate-valid` Validation succeeds for valid Gherkin -> `tests/test_gherkin_official.py` (missing)
- `bdd-official-validate-invalid` Validation fails for invalid Gherkin -> `tests/test_gherkin_official.py` (missing)

#### Rule: Reject invalid Gherkin on parse

- `bdd-official-reject-invalid` Parser raises ParseError for invalid input -> `tests/test_gherkin_official.py` (missing)
- `bdd-official-preserve-description` Parser preserves multi-line descriptions through official parser -> `tests/test_gherkin_official.py` (missing)

### Gherkin feature file parsing
- Path: `specs/behavior/features/gherkin/parser.feature.md`
- Summary: The Gherkin parser reads feature text and produces Feature/Rule/Scenario/Step

#### Rule: Classic Gherkin parsing extracts structure

- `bdd-parser-classic-feature` Parser extracts feature title and scenarios -> `tests/test_gherkin_parser.py::test_parse_simple_feature` (bound)
- `bdd-parser-classic-rules` Parser extracts Rule blocks -> `tests/test_gherkin_parser.py::test_parse_rule_block` (bound)
- `bdd-parser-classic-tags` Parser preserves tags on features, rules, and scenarios -> `tests/test_gherkin_parser.py::test_parse_no_tags` (bound)
- `bdd-parser-classic-description` Parser preserves feature and scenario descriptions -> `tests/test_gherkin_parser.py::test_parse_feature_description` (bound)
- `bdd-parser-classic-top-level-scenarios` Parser handles top-level scenarios outside rules -> `tests/test_gherkin_parser.py::test_top_level_scenario_before_rule_stays_top_level` (bound)

#### Rule: Markdown Gherkin parsing

- `bdd-parser-markdown-feature` Parser extracts structure from markdown format -> `tests/test_gherkin_parser.py::test_parse_markdown_feature` (bound)

#### Rule: Parser dispatches by format

- `bdd-parser-dispatch-by-suffix` Parser selects markdown parser for .feature.md files -> `tests/test_gherkin_parser.py::test_parser_dispatch_markdown_suffix` (bound)
- `bdd-parser-dispatch-classic` Parser selects classic parser for .feature files -> `tests/test_gherkin_parser.py::test_parser_dispatch_classic_suffix` (bound)

#### Rule: Parser requires Feature line

- `bdd-parser-requires-feature-line` Parser raises ValueError without Feature line -> `tests/test_gherkin_parser.py::test_parse_missing_feature_raises` (bound)

### Gherkin feature file writing
- Path: `specs/behavior/features/gherkin/writer.feature.md`
- Summary: The Gherkin writer serializes Feature dataclass instances back to

#### Rule: Writer produces canonical Gherkin output

- `bdd-writer-basic-feature` Writer serializes a feature with scenarios -> `tests/test_gherkin_writer.py::test_writes_tags_feature_scenario_steps` (bound)
- `bdd-writer-rules` Writer serializes Rule blocks -> `tests/test_gherkin_writer.py::test_writes_rule_block` (bound)
- `bdd-writer-tags` Writer preserves tags at all levels -> `tests/test_gherkin_writer.py::test_scenario_without_tags` (bound)
- `bdd-writer-descriptions` Writer preserves descriptions -> `tests/test_gherkin_writer.py::test_feature_description_rendered` (bound)
- `bdd-writer-roundtrip` Parsing then writing produces equivalent output -> `tests/test_gherkin_writer.py::test_rule_round_trips` (bound)

## init

### SpecWeave project initialization
- Path: `specs/behavior/features/init/initialization.feature.md`
- Summary: specweave init creates the config file and directory layout for a new

#### Rule: Init creates config and directories

- `bdd-init-creates-dotfile` Init creates .specweave.toml by default -> `tests/test_init_initialization.py::test_creates_default_config_and_layout` (bound)
- `bdd-init-creates-public-config` Init creates specweave.toml with --public-config -> `tests/test_init_initialization.py::test_writes_specweave_toml` (bound)
- `bdd-init-creates-readme` Init creates a managed README in specs root -> `tests/test_init_initialization.py::test_nonexistent` (bound)
- `bdd-init-creates-gitkeep` Init creates .gitkeep in features directory -> `tests/test_init_initialization.py::test_creates_behavior_paths` (bound)

#### Rule: Init is idempotent

- `bdd-init-idempotent` Running init twice does not fail -> `tests/test_init_initialization.py::test_does_not_overwrite_existing_config` (bound)

#### Rule: Init supports British spelling

- `bdd-init-british-spelling` Init creates behaviour layout with --spelling behaviour -> `tests/test_init_initialization.py::test_creates_behaviour_layout` (bound)

#### Rule: Init supports dry-run mode

- `bdd-init-dry-run` Dry-run reports paths without writing -> `tests/test_init_initialization.py::test_writes_nothing` (bound)

#### Rule: Init refuses to overwrite non-managed README

- `bdd-init-refuses-overwrite-readme` Init skips non-SpecWeave README -> `tests/test_init_initialization.py::test_does_not_overwrite_non_specweave_readme` (bound)
- `bdd-init-force-overwrites-readme` Init overwrites managed README with --force -> `tests/test_init_initialization.py::test_force_overwrites_generated_config_only` (bound)

#### Rule: Init warns about existing config

- `bdd-init-warns-existing-config` Init warns when config already exists -> `tests/test_init_initialization.py::test_reports_existing_directories` (bound)

## integrations

### Archledger integration
- Path: `specs/behavior/features/integrations/archledger.feature.md`
- Summary: SpecWeave generates Archledger candidate markdown for scenarios that are

#### Rule: Archledger candidate generation

- `bdd-archledger-candidate` archledger command renders candidate markdown -> `tests/test_integrations_archledger.py::test_render_candidate_markdown` (bound)
- `bdd-archledger-unknown-bdd` archledger errors on unknown @bdd-\* id -> `tests/test_integrations_archledger.py::test_unknown_bdd_id_raises` (bound)

#### Rule: Archledger does not write accepted records by default

- `bdd-archledger-candidate-only` archledger produces candidates, not accepted records -> `tests/test_integrations_archledger.py::test_write_candidate_file` (bound)

### Combined cross-tool diagnostics
- Path: `specs/behavior/features/integrations/combi.feature.md`
- Summary: SpecWeave combi check performs a cross-cutting diagnostic that validates

#### Rule: Combi check identifies missing mappings and evidence

- `bdd-combi-check-gaps` Scenario without pytest mapping or evidence reports gaps -> `tests/test_integrations_combi.py` (missing)

#### Rule: Strict mode fails on missing bdd ids

- `bdd-combi-check-strict` Scenario without @bdd-* tag fails in strict mode -> `tests/test_integrations_combi.py` (missing)

### Taskledger integration
- Path: `specs/behavior/features/integrations/taskledger.feature.md`
- Summary: SpecWeave exchanges files with Taskledger for task drafts and behavior

#### Rule: Taskledger task draft generation

- `bdd-taskledger-draft` create taskledger-task generates a draft JSON -> `tests/test_integrations_taskledger.py::test_no_taskledger_import_required` (bound)
- `bdd-taskledger-draft-ac-mapping` Draft maps @ac-\* tags to acceptance criteria -> `tests/test_integrations_taskledger.py::test_taskledger_draft_ac_mapping` (bound)

#### Rule: Taskledger behavior import

- `bdd-taskledger-import` import-taskledger creates a feature from Taskledger export -> `tests/test_integrations_taskledger.py::test_load_rich_shape` (bound)

#### Rule: Taskledger evidence generation

- `bdd-taskledger-evidence` report normalize generates Taskledger-compatible evidence -> `tests/test_integrations_taskledger.py::test_task_id_from_report` (bound)

## planning

### Implementation plan generation from features
- Path: `specs/behavior/features/planning/create-plan.feature.md`
- Summary: SpecWeave generates implementation-plan Markdown from a Gherkin feature

#### Rule: Create plan from a feature file

- `bdd-plan-create` Plan includes feature title and implementation TODOs -> `tests/test_planning_create_plan.py` (missing)
- `bdd-plan-includes-scenario-steps` Plan includes Given, When, Then steps from the feature -> `tests/test_planning_create_plan.py` (missing)
- `bdd-plan-validation-commands` Plan includes specweave validation command references -> `tests/test_planning_create_plan.py` (missing)

## python-inspect

### AST-based Python test inspection
- Path: `specs/behavior/features/python-inspect/ast-reader.feature.md`
- Summary: SpecWeave inspects Python test files via AST (abstract syntax tree) without

#### Rule: Discover test functions via AST

- `bdd-ast-extract-test-functions` AST reader finds test_* functions in a Python file -> `tests/test_python_inspect_ast_reader.py` (missing)
- `bdd-ast-ignores-non-test` AST reader ignores helper functions and non-test functions -> `tests/test_python_inspect_ast_reader.py` (missing)

#### Rule: Convert assertions to plain English

- `bdd-ast-assert-equals` Equality assertion becomes "x equals 42" -> `tests/test_python_inspect_ast_reader.py` (missing)
- `bdd-ast-assert-is-none` Identity assertion becomes "session is None" -> `tests/test_python_inspect_ast_reader.py` (missing)
- `bdd-ast-assert-truthy` Truthiness assertion becomes "user is truthy" -> `tests/test_python_inspect_ast_reader.py` (missing)
- `bdd-ast-assert-call` Call assertion becomes "func_name succeeds" -> `tests/test_python_inspect_ast_reader.py` (missing)

#### Rule: Discover SpecWeave pytest marker mappings

- `bdd-ast-discover-marker` AST reader extracts @pytest.mark.specweave mappings -> `tests/test_python_inspect_ast_reader.py` (missing)
- `bdd-ast-discover-comment` AST reader extracts # specweave: comment mappings -> `tests/test_python_inspect_ast_reader.py` (missing)
- `bdd-ast-discover-docstring` AST reader extracts docstring-based SpecWeave mappings -> `tests/test_python_inspect_ast_reader.py` (missing)

## reports

### Fail-closed evidence semantics
- Path: `specs/behavior/features/reports/fail-closed.feature.md`
- Summary: SpecWeave enforces fail-closed semantics for acceptance criteria. A

#### Rule: Blocking statuses fail linked criteria

- `bdd-fail-closed-failed-scenario` Failed scenario fails the linked criterion -> `tests/test_reports_fail_closed.py::test_failed_scenario_fails_criterion` (bound)
- `bdd-fail-closed-skipped-scenario` Skipped scenario fails the criterion by default -> `tests/test_reports_fail_closed.py::test_skipped_scenario_fails_criterion` (bound)
- `bdd-fail-closed-undefined-scenario` Undefined scenario fails the criterion -> `tests/test_reports_fail_closed.py::test_criterion_requires_passing_native_result` (bound)
- `bdd-fail-closed-pending-scenario` Pending scenario fails the criterion -> `tests/test_reports_fail_closed.py::test_pending_scenario_fails_criterion` (bound)
- `bdd-fail-closed-ambiguous-scenario` Ambiguous scenario fails the criterion -> `tests/test_reports_fail_closed.py::test_ambiguous_scenario_fails_criterion` (bound)

#### Rule: Only passing scenarios satisfy criteria

- `bdd-fail-closed-passed-scenario` Passed scenario satisfies the criterion -> `tests/test_reports_fail_closed.py::test_evidence_records_command_source_and_paths` (bound)

#### Rule: Unlinked scenarios do not affect criteria

- `bdd-fail-closed-unlinked-scenario` Unlinked scenario does not satisfy any criterion -> `tests/test_reports_fail_closed.py::test_missing_expected_coverage_fails` (bound)

#### Rule: Multiple scenarios for one criterion

- `bdd-fail-closed-multiple-scenarios` One failed scenario fails the whole criterion -> `tests/test_reports_fail_closed.py::test_criterion_fails_when_sibling_undefined` (bound)

#### Rule: Exit code alone is not sufficient evidence

- `bdd-fail-closed-exit-code-not-evidence` Passing exit code does not override failed scenarios -> `tests/test_reports_fail_closed.py::test_exit_code_not_used_as_evidence` (bound)

### Report tag mapping and acceptance coverage
- Path: `specs/behavior/features/reports/mapping.feature.md`
- Summary: The reports.mapping module extracts BDD and acceptance criterion IDs

#### Rule: Tag extraction identifies BDD and AC IDs

- `bdd-tag-extraction-bdd` Extraction finds @bdd-\* tags -> `tests/test_reports_mapping.py::test_extract_ids_partitions_by_prefix` (bound)
- `bdd-tag-extraction-ac` Extraction finds @ac-\* tags -> `tests/test_reports_mapping.py::test_extract_ac_ids_from_tags` (bound)
- `bdd-tag-extraction-empty` Extraction returns empty lists when no matching tags -> `tests/test_reports_mapping.py::test_unlinked_scenarios_are_ignored` (bound)

#### Rule: Criteria summarization groups by AC ID

- `bdd-criteria-summary` Summarization groups scenarios by acceptance criterion -> `tests/test_reports_mapping.py::test_summarize_passes_when_linked_scenario_passed` (bound)
- `bdd-criteria-fail-closed` Failed scenarios fail the linked criterion -> `tests/test_reports_mapping.py::test_summarize_fails_when_linked_scenario_failed` (bound)
- `bdd-criteria-missing-coverage` Expected AC with no scenarios fails coverage -> `tests/test_reports_mapping.py::test_require_expected_coverage_missing_fails` (bound)

### Report normalization and evidence generation
- Path: `specs/behavior/features/reports/normalization.feature.md`
- Summary: specweave report normalize parses runner-native reports (JUnit XML,

#### Rule: Normalization parses supported formats

- `bdd-normalize-junit-xml` Normalization parses JUnit XML reports -> `tests/test_reports_normalization.py::test_normalize_junit_xml` (bound)
- `bdd-normalize-cucumber-json` Normalization parses Cucumber JSON reports -> `tests/test_reports_normalization.py::test_normalize_cucumber_json` (bound)
- `bdd-normalize-unsupported-format` Normalization rejects unsupported formats -> `tests/test_reports_normalization.py::test_normalize_unsupported_format` (bound)

#### Rule: Normalization computes overall status

- `bdd-normalize-all-passed` Report status is passed when all scenarios pass -> `tests/test_reports_normalization.py::test_normalize_all_passed` (bound)
- `bdd-normalize-any-failed` Report status is failed when any scenario fails -> `tests/test_reports_normalization.py::test_normalize_any_failed` (bound)
- `bdd-normalize-skipped-fails-by-default` Skipped scenarios fail the report by default -> `tests/test_reports_normalization.py::test_normalize_skipped_fails_by_default` (bound)
- `bdd-normalize-allow-skipped` Skipped scenarios pass with --allow-skipped -> `tests/test_reports_normalization.py::test_normalize_allow_skipped` (bound)

#### Rule: Normalization enforces acceptance criteria coverage

- `bdd-normalize-missing-ac-coverage` Report fails when expected AC has no passing scenario -> `tests/test_reports_normalization.py::test_normalize_missing_ac_coverage` (bound)
- `bdd-normalize-ac-covered` Report passes when expected AC has a passing scenario -> `tests/test_reports_normalization.py::test_normalize_ac_covered` (bound)

#### Rule: Normalization generates evidence JSON

- `bdd-normalize-evidence-json` Normalization writes Taskledger evidence JSON -> `tests/test_reports_normalization.py::test_normalize_evidence_json` (bound)

### Report format parsers
- Path: `specs/behavior/features/reports/parsers.feature.md`
- Summary: SpecWeave parses JUnit XML and Cucumber JSON reports into ScenarioResult

#### Rule: JUnit XML parser extracts test cases

- `bdd-junit-parse-cases` Parser extracts test cases from JUnit XML -> `tests/test_reports_parsers.py::test_parse_junit_pass_fail_skip` (bound)
- `bdd-junit-parse-statuses` Parser maps JUnit statuses correctly -> `tests/test_reports_parsers.py::test_junit_error_counts_as_failed` (bound)
- `bdd-junit-parse-duration` Parser extracts test duration -> `tests/test_reports_parsers.py::test_junit_parse_duration` (bound)

#### Rule: Cucumber JSON parser extracts scenarios

- `bdd-cucumber-parse-scenarios` Parser extracts scenarios from Cucumber JSON -> `tests/test_reports_parsers.py::test_cucumber_json_passing_scenario` (bound)
- `bdd-cucumber-parse-tags` Parser extracts tags from Cucumber scenarios -> `tests/test_reports_parsers.py::test_behear_string_tags_and_inline_status` (bound)

## review

### Behavior spec review
- Path: `specs/behavior/features/review/spec-review.feature.md`
- Summary: specweave review specs aggregates lint, coverage, and convention findings

#### Rule: Review reports feature and scenario counts

- `bdd-review-counts` Review reports feature and scenario statistics -> `tests/test_review_spec_review.py::test_no_features` (bound)

#### Rule: Review reports missing bindings

- `bdd-review-missing-bindings` Review warns about unbound scenarios -> `tests/test_review_spec_review.py::test_feature_with_no_test` (bound)

#### Rule: Review reports needs-review tags

- `bdd-review-needs-review` Review warns about @needs-review scenarios -> `tests/test_review_spec_review.py::test_needs_review_flagged` (bound)

#### Rule: Review reports deprecated paths

- `bdd-review-deprecated-paths` Review warns about deprecated paths -> `tests/test_review_spec_review.py::test_stale_mapping_causes_failed_review` (bound)

#### Rule: Review reports forbidden pytest-bdd usage

- `bdd-review-forbidden-pytest-bdd` Review errors on pytest-bdd usage -> `tests/test_review_spec_review.py::test_forbidden_pytest_bdd` (bound)

#### Rule: Review aggregates lint findings

- `bdd-review-lint-findings` Review includes lint errors and warnings -> `tests/test_review_spec_review.py::test_lint_findings` (bound)

## runners

### Delegated command runner
- Path: `specs/behavior/features/runners/command.feature.md`
- Summary: SpecWeave delegates external command execution through a runner that

#### Rule: Run successful commands

- `bdd-runner-success` Successful command writes passed summary -> `tests/test_runners_command.py` (missing)

#### Rule: Run failing commands

- `bdd-runner-failure` Failing command writes failed summary -> `tests/test_runners_command.py` (missing)

#### Rule: Run command-not-found

- `bdd-runner-not-found` Non-existent command returns error status -> `tests/test_runners_command.py` (missing)

#### Rule: Capture stdout and stderr

- `bdd-runner-capture` Stdout and stderr are captured to separate files -> `tests/test_runners_command.py` (missing)

## trace

### End-to-end traceability bundle extraction
- Path: `specs/behavior/features/trace/trace.feature.md`
- Summary: SpecWeave trace extracts a traceability bundle for a given `@bdd-*` id

#### Rule: Trace by bdd-id reports full mapping chain

- `bdd-trace-by-id` Trace by bdd-id finds feature, ac tags, test references, and gaps -> `tests/test_trace_trace.py` (missing)

#### Rule: Trace by feature path supports markdown features

- `bdd-trace-by-path` Trace by .feature.md path reports feature metadata and bdd-ids -> `tests/test_trace_trace.py` (missing)

## translation

### Brownfield pytest-to-Gherkin generation
- Path: `specs/behavior/features/translation/pytest-to-gherkin.feature.md`
- Summary: specweave create gherkin generates draft Gherkin feature files from

#### Rule: Generation discovers tests via AST

- `bdd-translate-discovers-tests` Generation finds test functions in pytest files -> `tests/test_translation_pytest_to_gherkin.py::test_basic` (bound)
- `bdd-translate-group-by-file` Generation groups scenarios by test file -> `tests/test_translation_pytest_to_gherkin.py::test_simple` (bound)

#### Rule: Generation preserves existing features

- `bdd-translate-preserve-manual` Generation does not overwrite manual feature files -> `tests/test_translation_pytest_to_gherkin.py::test_skips_manual_file_without_force` (bound)
- `bdd-translate-force-overwrite` Generation overwrites with --force -> `tests/test_translation_pytest_to_gherkin.py::test_force_overwrites_manual` (bound)

#### Rule: Generation marks drafts appropriately

- `bdd-translate-marks-generated` Generated features have @generated tag -> `tests/test_translation_pytest_to_gherkin.py::test_marks_needs_review` (bound)

#### Rule: Generation supports dry-run mode

- `bdd-translate-dry-run` Dry-run reports without writing files -> `tests/test_translation_pytest_to_gherkin.py::test_writes_nothing` (bound)

### Gherkin-to-test skeleton generation
- Path: `specs/behavior/features/translation/spec-to-code.feature.md`
- Summary: SpecWeave generates test skeletons from Gherkin features. It produces step

#### Rule: Generate deterministic step function names

- `bdd-spec-to-code-step-name` Step function name derives from keyword and text -> `tests/test_translation_spec_to_code.py` (missing)
- `bdd-spec-to-code-dedup` Duplicate step texts get unique suffixes -> `tests/test_translation_spec_to_code.py` (missing)

#### Rule: Draft feature from JSON input

- `bdd-spec-to-code-draft` draft_feature creates a valid feature file from JSON -> `tests/test_translation_spec_to_code.py` (missing)

#### Rule: Bind feature to a backend step skeleton

- `bdd-spec-to-code-bind-behave` bind_feature creates a behave step skeleton -> `tests/test_translation_spec_to_code.py` (missing)
- `bdd-spec-to-code-bind-pytest-bdd` bind_feature creates a pytest-bdd step skeleton -> `tests/test_translation_spec_to_code.py` (missing)
- `bdd-spec-to-code-bind-unsupported` Unsupported backend raises clear error -> `tests/test_translation_spec_to_code.py` (missing)
