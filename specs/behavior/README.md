# Behavior index

Generated from `specs/behavior/features`.

## backends

### pytest-bdd step-skeleton backend
- Path: `specs/behavior/features/backends/pytest-bdd.feature`
- Summary: SpecWeave provides a legacy/bridge backend that generates pytest-bdd step

#### Rule: Backend registry

- `bdd-backend-registry` Supported backends include behave and pytest-bdd -> `tests/test_backends_pytest_bdd.py::test_backend_registry_contents` (bound)
- `bdd-backend-unsupported` Unsupported Cucumber backends report clear messages -> `tests/test_backends_pytest_bdd.py::test_unsupported_cucumber_backends_message` (bound)

#### Rule: Generate pytest-bdd skeleton

- `bdd-backend-pytest-bdd-skeleton` Skeleton includes pytest-bdd imports, scenarios, and step decorators -> `tests/test_backends_pytest_bdd.py::test_pytest_bdd_skeleton_shape` (bound)
- `bdd-backend-pytest-bdd-dedup` Repeated steps appear only once in the skeleton -> `tests/test_backends_pytest_bdd.py::test_pytest_bdd_dedups_repeated_steps` (bound)
- `bdd-backend-pytest-bdd-rule-scenarios` Steps inside Rule blocks are included -> `tests/test_backends_pytest_bdd.py::test_pytest_bdd_collects_rule_scenarios` (bound)
- `bdd-backend-pytest-bdd-source-path` Skeleton uses the source feature filename when available -> `tests/test_backends_pytest_bdd.py::test_pytest_bdd_uses_source_path_filename` (bound)

## bdd

### Task-BDD JSON to Gherkin conversion
- Path: `specs/behavior/features/bdd/convert.feature`
- Summary: SpecWeave converts between its internal Task-BDD JSON model and canonical

#### Rule: Export Task-BDD spec to classic Gherkin

- `bdd-bridge-export-to-gherkin` Task-BDD spec renders as target Gherkin with all tags -> `tests/test_bdd_convert.py::test_export_to_target_gherkin` (bound)

#### Rule: Round-trip preserves all IDs and content

- `bdd-bridge-roundtrip-ids` Export then import preserves task, rule, bdd, and ac ids -> `tests/test_bdd_convert.py::test_round_trip_preserves_ids` (bound)
- `bdd-bridge-multiple-ac` Multiple acceptance criteria and custom tags survive round-trip -> `tests/test_bdd_convert.py::test_multiple_ac_tags_and_extra_tags` (bound)

#### Rule: Top-level examples become top-level scenarios

- `bdd-bridge-top-level` Example without rule_id renders as top-level scenario -> `tests/test_bdd_convert.py::test_top_level_examples_become_top_level_scenarios` (bound)

#### Rule: And/But steps group correctly

- `bdd-bridge-and-but-steps` Multiple Given/When/Then entries render as And/But steps -> `tests/test_bdd_convert.py::test_and_but_steps_group_correctly` (bound)

#### Rule: JSON store read/write

- `bdd-bridge-json-roundtrip` save then load is idempotent -> `tests/test_bdd_convert.py::test_json_round_trip` (bound)
- `bdd-bridge-json-to-feature-to-json` JSON to feature to JSON preserves all ids -> `tests/test_bdd_convert.py::test_json_to_feature_to_json_round_trip` (bound)

## behavior

### Behavior autolink
- Path: `specs/behavior/features/behavior/autolink.feature`
- Summary: SpecWeave can convert high-confidence generated scenario ids into explicit pytest mappings.

#### Rule: Generated id autolinking

- `bdd-autolink-generated-id-dry-run` Dry-run reports generated id mappings without writing files -> `tests/test_behavior_autolink.py::test_autolink_dry_run_does_not_write` (bound)
- `bdd-autolink-generated-id-apply` Apply writes explicit mapping metadata -> `tests/test_behavior_autolink.py::test_autolink_apply_writes_mapping_comments` (bound)
- `bdd-autolink-ambiguous-candidate` Ambiguous matches are reported instead of guessed -> `tests/test_behavior_autolink.py::test_autolink_reports_ambiguous_equal_score` (bound)
- `bdd-autolink-refresh-wrapper` Refresh regenerates common behavior artifacts -> `tests/test_behavior_autolink.py::test_autolink_uses_config_paths` (bound)

### Static behavior coverage checks
- Path: `specs/behavior/features/behavior/coverage.feature`
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

#### Rule: Coverage can be viewed from pytest back to features

- `bdd-coverage-class-method-mapping` Coverage matches mappings on pytest class methods -> `tests/test_behavior_coverage.py::test_coverage_matches_mapping_on_class_test_method` (bound)
- `bdd-coverage-pytest-unmapped` Coverage reports unmapped pytest tests -> `tests/test_behavior_coverage.py::test_coverage_lists_unmapped_pytest_tests` (bound)
- `bdd-coverage-pytest-stale` Coverage reports stale pytest mappings in the pytest view -> `tests/test_behavior_coverage.py::test_coverage_marks_stale_pytest_test_in_reverse_inventory` (bound)
- `bdd-coverage-both-directions-render` Coverage renders feature and pytest directions together -> `tests/test_behavior_coverage.py::test_render_coverage_text_both_directions` (bound)

#### Rule: Coverage reasons are actionable

- `bdd-coverage-missing-test-file-reason` Coverage distinguishes a missing expected test file -> `tests/test_behavior_coverage.py::test_behavior_coverage_ignores_pytest_bdd_text` (bound)
- `bdd-coverage-candidate-tests` Coverage suggests candidate tests without binding by title -> `tests/test_behavior_coverage.py::test_coverage_candidate_tests_are_hints_not_bindings` (bound)

### Plain pytest skeleton generation
- Path: `specs/behavior/features/behavior/generation.feature`
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
- Path: `specs/behavior/features/behavior/index.feature`
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
- Path: `specs/behavior/features/behavior/reporting.feature`
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
- Path: `specs/behavior/features/cli/cli-contract.feature`
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
- `bdd-cli-review-coverage-both-directions` review coverage shows both feature and pytest directions -> `tests/test_cli_cli_contract.py::test_review_coverage_both_directions_text` (bound)
- `bdd-cli-behavior-coverage-view-test-json` behavior coverage emits pytest-side JSON -> `tests/test_cli_cli_contract.py::test_behavior_coverage_view_test_json` (bound)
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
- Path: `specs/behavior/features/common/behavior-helpers.feature`
- Summary: The behavior.common module provides shared helpers for slugification,

#### Rule: Slugification produces stable lowercase slugs

- `bdd-slugify-basic` Slugify converts text to lowercase slug -> `tests/test_common_behavior_helpers.py::TestSlugify::test_basic` (bound)
- `bdd-slugify-special-chars` Slugify replaces special characters with hyphens -> `tests/test_common_behavior_helpers.py::TestSlugify::test_special_chars` (bound)
- `bdd-slugify-empty` Slugify returns "behavior" for empty input -> `tests/test_common_behavior_helpers.py::TestSlugify::test_empty` (bound)

#### Rule: Feature identity extracts area and slug

- `bdd-feature-identity-from-path` Feature identity derives area from parent directory -> `tests/test_common_behavior_helpers.py::TestFeatureIdentity::test_from_path` (bound)
- `bdd-feature-identity-no-area` Feature identity uses "behavior" when no area directory -> `tests/test_common_behavior_helpers.py::TestFeatureIdentity::test_no_area` (bound)
- `bdd-feature-stem-classic` feature_stem handles .feature suffix -> `tests/test_common_behavior_helpers.py::TestFeatureStem::test_classic_feature` (bound)
- `bdd-feature-stem-legacy-markdown` feature_stem tolerates legacy .feature.md suffix for path helpers -> `tests/test_common_behavior_helpers.py::TestFeatureStem::test_feature_md` (bound)

#### Rule: Canonical test path derivation

- `bdd-canonical-test-path` Test path is derived from feature path -> `tests/test_common_behavior_helpers.py::TestCanonicalTestPath::test_derives_path` (bound)

#### Rule: Scenario iteration yields all scenarios

- `bdd-iter-scenarios-top-level` Iterator yields top-level scenarios -> `tests/test_common_behavior_helpers.py::TestIterFeatureScenarios::test_yields_top_level` (bound)
- `bdd-iter-scenarios-in-rules` Iterator yields scenarios from rules -> `tests/test_common_behavior_helpers.py::TestIterFeatureScenarios::test_yields_from_rules` (bound)

#### Rule: Scenario ID extraction

- `bdd-scenario-id-value` scenario_id_value returns first @bdd-\* tag -> `tests/test_common_behavior_helpers.py::TestScenarioIdValue::test_returns_first_bdd_tag` (bound)
- `bdd-scenario-id-missing` scenario_id_value returns empty string when no @bdd-\* tag -> `tests/test_common_behavior_helpers.py::TestScenarioIdValue::test_returns_empty_when_no_bdd` (bound)

## config

### SpecWeave configuration management
- Path: `specs/behavior/features/config/configuration.feature`
- Summary: SpecWeave loads project configuration from TOML files, discovers config

#### Rule: Config discovery walks parent directories

- `bdd-config-discovery-finds-public` Discovery finds specweave.toml in current directory -> `tests/test_config_configuration.py::TestFindConfig::test_prefers_explicit` (bound)
- `bdd-config-discovery-finds-dotfile` Discovery still finds .specweave.toml when it is the only config -> `tests/test_config_configuration.py::TestFindConfig::test_finds_hidden_config` (bound)
- `bdd-config-discovery-prefers-public` Discovery prefers specweave.toml over .specweave.toml -> `tests/test_config_configuration.py::TestFindConfig::test_prefers_public_over_dotfile` (bound)
- `bdd-config-discovery-walks-parents` Discovery walks parent directories when not found locally -> `tests/test_config_configuration.py::TestFindConfig::test_walks_up_directories` (bound)
- `bdd-config-discovery-returns-none` Discovery returns None when no config exists -> `tests/test_config_configuration.py::TestFindConfig::test_returns_none_when_missing` (bound)

#### Rule: Config loading returns defaults when no file exists

- `bdd-config-load-defaults` Loading with no file returns default config -> `tests/test_config_configuration.py::TestLoadConfig::test_defaults_when_missing` (bound)
- `bdd-config-load-from-file` Loading reads values from a valid TOML file -> `tests/test_config_configuration.py::TestLoadConfig::test_normalizes_paths` (bound)

#### Rule: Config rejects unsupported schema versions

- `bdd-config-rejects-unsupported-schema` Loading fails for schema_version 2 -> `tests/test_config_configuration.py::TestLoadConfig::test_rejects_unsupported_schema` (bound)

#### Rule: Default config rendering is deterministic

- `bdd-config-render-behavior` Default config renders behavior spelling -> `tests/test_config_configuration.py::TestRenderDefaultConfig::test_renders_behavior` (bound)
- `bdd-config-render-behaviour` Default config renders behaviour spelling -> `tests/test_config_configuration.py::TestRenderDefaultConfig::test_renders_behaviour` (bound)

## doctor

### SpecWeave project diagnostics
- Path: `specs/behavior/features/doctor/diagnostics.feature`
- Summary: specweave doctor checks the project setup, config, paths, and feature

#### Rule: Doctor checks config presence and schema

- `bdd-doctor-missing-config` Doctor warns when no config file exists -> `tests/test_doctor_diagnostics.py::TestDoctorReportsMissing::test_no_config_warning` (bound)
- `bdd-doctor-unsupported-schema` Doctor errors on unsupported schema version -> `tests/test_doctor_diagnostics.py::TestDoctorFix::test_unsupported_schema` (bound)

#### Rule: Doctor checks directory existence

- `bdd-doctor-missing-directories` Doctor warns about missing directories -> `tests/test_doctor_diagnostics.py::TestDoctorReportsMissing::test_reports_missing_features_dir` (bound)
- `bdd-doctor-fix-creates-directories` Doctor --fix creates missing directories -> `tests/test_doctor_diagnostics.py::TestDoctorFix::test_fix_creates_missing_dirs` (bound)

#### Rule: Doctor checks for deprecated paths

- `bdd-doctor-deprecated-paths` Doctor warns about deprecated feature paths -> `tests/test_doctor_diagnostics.py::TestDoctorReportsDeprecatedPaths::test_detects_deprecated` (bound)

#### Rule: Doctor checks for duplicate bdd tags

- `bdd-doctor-duplicate-bdd-tags` Doctor errors on duplicate @bdd-\* tags -> `tests/test_doctor_diagnostics.py::TestDoctorReportsDuplicateBddTags::test_detects_duplicates` (bound)

#### Rule: Doctor validates feature files

- `bdd-doctor-validates-features` Doctor reports feature lint errors -> `tests/test_doctor_diagnostics.py::TestDoctorPasses::test_passes_initialized_project` (bound)

## exchange

### Exchange schema contracts
- Path: `specs/behavior/features/exchange/schemas.feature`
- Summary: SpecWeave defines JSON Schema documents for its file-based exchange

#### Rule: Schema files are valid JSON Schema documents

- `bdd-exchange-schema-valid` Each exchange schema is a valid JSON Schema -> `tests/test_exchange_schemas.py::test_exchange_schemas_are_json_schema_documents` (bound)

#### Rule: Representative payloads satisfy schema requirements

- `bdd-exchange-combi-trace-schema` Combi trace representative payload satisfies required fields -> `tests/test_exchange_schemas.py::test_trace_schema_representative_payload_contract` (bound)
- `bdd-exchange-taskledger-schema` Taskledger BDD export representative payload satisfies schema -> `tests/test_exchange_schemas.py::test_taskledger_schema_representative_payload_contract` (bound)
- `bdd-exchange-evidence-schema` Behavior evidence representative payload satisfies schema -> `tests/test_exchange_schemas.py::test_evidence_schema_representative_payload_contract` (bound)
- `bdd-exchange-archledger-schema` Archledger candidate representative payload satisfies schema -> `tests/test_exchange_schemas.py::test_archledger_schema_representative_payload_contract` (bound)

## gherkin

### Gherkin feature file linting
- Path: `specs/behavior/features/gherkin/lint.feature`
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

### Legacy Markdown feature files are rejected
- Path: `specs/behavior/features/gherkin/markdown.feature`
- Summary: SpecWeave uses classic `.feature` files as the only canonical behavior-spec

#### Rule: Parser rejects markdown feature files

- `bdd-markdown-parser-rejects-path` Parser rejects a .feature.md source path -> `tests/test_gherkin_parser.py::test_parser_rejects_markdown_feature_path` (bound)

#### Rule: Lint reports unsupported markdown files

- `bdd-lint-rejects-markdown-file` Lint returns an explicit unsupported-format finding -> `tests/test_gherkin_lint.py::test_lint_rejects_markdown_feature_file` (bound)

#### Rule: Validation rejects markdown feature syntax

- `bdd-validation-rejects-markdown` Markdown validation fails closed -> `tests/test_gherkin_validation.py::TestValidateMarkdownUnsupported::test_rejects_markdown_features` (bound)

### Official Cucumber Gherkin parser adapter
- Path: `specs/behavior/features/gherkin/official.feature`
- Summary: SpecWeave wraps the official `gherkin-official` parser to validate classic

#### Rule: Parse classic Gherkin with the official parser

- `bdd-official-parse-simple` Official parser extracts feature title, tags, and description -> `tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_parses_simple_feature` (bound)
- `bdd-official-parse-rules` Official parser extracts Rule blocks with tags -> `tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_parses_rule_and_scenario_tags` (bound)
- `bdd-official-parse-no-tags` Official parser handles features without tags -> `tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_empty_feature_tags` (bound)
- `bdd-official-source-path` Official parser stores the source path when provided -> `tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_accepts_source_path` (bound)
- `bdd-official-compile-pickles` Official parser supports pickle compilation mode -> `tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_compile_pickles_smoke` (bound)

#### Rule: Validate classic Gherkin syntax

- `bdd-official-validate-valid` Validation succeeds for valid Gherkin -> `tests/test_gherkin_official.py::TestValidateClassicWithOfficial::test_validates_valid` (bound)
- `bdd-official-validate-invalid` Validation fails for invalid Gherkin -> `tests/test_gherkin_official.py::TestValidateClassicWithOfficial::test_validates_invalid` (bound)

#### Rule: Reject invalid Gherkin on parse

- `bdd-official-reject-invalid` Parser raises ParseError for invalid input -> `tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_rejects_invalid_gherkin` (bound)
- `bdd-official-preserve-description` Parser preserves multi-line descriptions through official parser -> `tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_preserves_description` (bound)

### Gherkin feature file parsing
- Path: `specs/behavior/features/gherkin/parser.feature`
- Summary: The Gherkin parser reads classic feature text and produces

#### Rule: Classic Gherkin parsing extracts structure

- `bdd-parser-classic-feature` Parser extracts feature title and scenarios -> `tests/test_gherkin_parser.py::test_parse_simple_feature` (bound)
- `bdd-parser-classic-rules` Parser extracts Rule blocks -> `tests/test_gherkin_parser.py::test_parse_rule_block` (bound)
- `bdd-parser-classic-tags` Parser preserves tags on features, rules, and scenarios -> `tests/test_gherkin_parser.py::test_parse_no_tags` (bound)
- `bdd-parser-classic-description` Parser preserves feature and scenario descriptions -> `tests/test_gherkin_parser.py::test_parse_feature_description` (bound)
- `bdd-parser-classic-top-level-scenarios` Parser handles top-level scenarios outside rules -> `tests/test_gherkin_parser.py::test_top_level_scenario_before_rule_stays_top_level` (bound)

#### Rule: Parser dispatches by format

- `bdd-parser-rejects-markdown-path` Parser rejects .feature.md files -> `tests/test_gherkin_parser.py::test_classic_parser_rejects_markdown_feature_path` (bound)
- `bdd-parser-dispatch-classic` Parser selects classic parser for .feature files -> `tests/test_gherkin_parser.py::test_parser_dispatch_classic_suffix` (bound)

#### Rule: Parser requires Feature line

- `bdd-parser-requires-feature-line` Parser raises ValueError without Feature line -> `tests/test_gherkin_parser.py::test_parse_missing_feature_raises` (bound)

### Gherkin feature file writing
- Path: `specs/behavior/features/gherkin/writer.feature`
- Summary: The Gherkin writer serializes Feature dataclass instances back to

#### Rule: Writer produces canonical Gherkin output

- `bdd-writer-basic-feature` Writer serializes a feature with scenarios -> `tests/test_gherkin_writer.py::test_writes_tags_feature_scenario_steps` (bound)
- `bdd-writer-rules` Writer serializes Rule blocks -> `tests/test_gherkin_writer.py::test_writes_rule_block` (bound)
- `bdd-writer-tags` Writer preserves tags at all levels -> `tests/test_gherkin_writer.py::test_scenario_without_tags` (bound)
- `bdd-writer-descriptions` Writer preserves descriptions -> `tests/test_gherkin_writer.py::test_feature_description_rendered` (bound)
- `bdd-writer-roundtrip` Parsing then writing produces equivalent output -> `tests/test_gherkin_writer.py::test_rule_round_trips` (bound)

## init

### SpecWeave project initialization
- Path: `specs/behavior/features/init/initialization.feature`
- Summary: specweave init creates the config file and directory layout for a new

#### Rule: Init creates config and directories

- `bdd-init-creates-public-config` Init creates specweave.toml by default -> `tests/test_init_initialization.py::TestInitDefault::test_creates_default_config_and_layout` (bound)
- `bdd-init-creates-dotfile` Init still supports explicit hidden config output -> `tests/test_init_initialization.py::TestInitCompatibility::test_hidden_config_path_still_works_when_explicit` (bound)
- `bdd-init-creates-readme` Init creates a managed README in specs root -> `tests/test_init_initialization.py::TestReadmeIsSpecweaveManaged::test_nonexistent` (bound)
- `bdd-init-creates-gitkeep` Init creates .gitkeep in features directory -> `tests/test_init_initialization.py::TestInitDefault::test_creates_behavior_paths` (bound)

#### Rule: Init is idempotent

- `bdd-init-idempotent` Running init twice does not fail -> `tests/test_init_initialization.py::TestInitIdempotency::test_does_not_overwrite_existing_config` (bound)

#### Rule: Init supports British spelling

- `bdd-init-british-spelling` Init creates behaviour layout with --spelling behaviour -> `tests/test_init_initialization.py::TestInitBritishSpelling::test_creates_behaviour_layout` (bound)

#### Rule: Init supports dry-run mode

- `bdd-init-dry-run` Dry-run reports paths without writing -> `tests/test_init_initialization.py::TestInitDryRun::test_writes_nothing` (bound)

#### Rule: Init refuses to overwrite non-managed README

- `bdd-init-refuses-overwrite-readme` Init skips non-SpecWeave README -> `tests/test_init_initialization.py::TestInitIdempotency::test_does_not_overwrite_non_specweave_readme` (bound)
- `bdd-init-force-overwrites-readme` Init overwrites managed README with --force -> `tests/test_init_initialization.py::TestInitForce::test_force_overwrites_generated_config_only` (bound)

#### Rule: Init warns about existing config

- `bdd-init-warns-existing-config` Init warns when config already exists -> `tests/test_init_initialization.py::TestInitIdempotency::test_reports_existing_directories` (bound)

## integrations

### Archledger integration
- Path: `specs/behavior/features/integrations/archledger.feature`
- Summary: SpecWeave generates Archledger candidate markdown for scenarios that are

#### Rule: Archledger candidate generation

- `bdd-archledger-candidate` archledger command renders candidate markdown -> `tests/test_integrations_archledger.py::test_render_candidate_markdown` (bound)
- `bdd-archledger-unknown-bdd` archledger errors on unknown @bdd-\* id -> `tests/test_integrations_archledger.py::test_unknown_bdd_id_raises` (bound)

#### Rule: Archledger does not write accepted records by default

- `bdd-archledger-candidate-only` archledger produces candidates, not accepted records -> `tests/test_integrations_archledger.py::test_write_candidate_file` (bound)

### Combined cross-tool diagnostics
- Path: `specs/behavior/features/integrations/combi.feature`
- Summary: SpecWeave combi check performs a cross-cutting diagnostic that validates

#### Rule: Combi check identifies missing mappings and evidence

- `bdd-combi-check-gaps` Scenario without pytest mapping or evidence reports gaps -> `tests/test_combi_check.py::test_combi_check_writes_json_and_human_diagnostics` (bound)

#### Rule: Strict mode fails on missing bdd ids

- `bdd-combi-check-strict` Scenario without @bdd-\* tag fails in strict mode -> `tests/test_combi_check.py::test_combi_check_strict_fails_on_missing_bdd_id` (bound)

### Taskledger integration
- Path: `specs/behavior/features/integrations/taskledger.feature`
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
- Path: `specs/behavior/features/planning/create-plan.feature`
- Summary: SpecWeave generates implementation-plan Markdown from a Gherkin feature

#### Rule: Create plan from a feature file

- `bdd-plan-create` Plan includes feature title and implementation TODOs -> `tests/test_plan.py::TestCreatePlan::test_creates_plan_from_feature` (bound)
- `bdd-plan-includes-scenario-steps` Plan includes Given, When, Then steps from the feature -> `tests/test_plan.py::TestCreatePlan::test_plan_includes_scenario_steps` (bound)
- `bdd-plan-validation-commands` Plan includes specweave validation command references -> `tests/test_plan.py::TestCreatePlan::test_plan_includes_validation_commands` (bound)

## python-inspect

### AST-based Python test inspection
- Path: `specs/behavior/features/python-inspect/ast-reader.feature`
- Summary: SpecWeave inspects Python test files via AST (abstract syntax tree) without

#### Rule: Discover test functions via AST

- `bdd-ast-extract-test-functions` AST reader finds test\_\* functions in a Python file -> `tests/test_python_ast_reader.py::test_extract_test_functions` (bound)
- `bdd-ast-ignores-non-test` AST reader ignores helper functions and non-test functions -> `tests/test_python_ast_reader.py::test_extract_ignores_non_test_functions` (bound)

#### Rule: Convert assertions to plain English

- `bdd-ast-assert-equals` Equality assertion becomes "x equals 42" -> `tests/test_python_ast_reader.py::test_describe_assert_equals` (bound)
- `bdd-ast-assert-is-none` Identity assertion becomes "session is None" -> `tests/test_python_ast_reader.py::test_describe_assert_is_none` (bound)
- `bdd-ast-assert-truthy` Truthiness assertion becomes "user is truthy" -> `tests/test_python_ast_reader.py::test_describe_assert_truthy` (bound)
- `bdd-ast-assert-call` Call assertion becomes "func_name succeeds" -> `tests/test_python_ast_reader.py::test_describe_assert_call` (bound)

#### Rule: Discover SpecWeave pytest marker mappings

- `bdd-ast-discover-marker` AST reader extracts @pytest.mark.specweave mappings -> `tests/test_python_ast_reader.py::test_discover_specweave_marker_mapping` (bound)
- `bdd-ast-discover-comment` AST reader extracts # specweave: comment mappings -> `tests/test_python_ast_reader.py::test_discover_specweave_comment_mapping` (bound)
- `bdd-ast-discover-docstring` AST reader extracts docstring-based SpecWeave mappings -> `tests/test_python_ast_reader.py::test_docstring_mapping_accepts_feature_md` (bound)

## reports

### Fail-closed evidence semantics
- Path: `specs/behavior/features/reports/fail-closed.feature`
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
- Path: `specs/behavior/features/reports/mapping.feature`
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
- Path: `specs/behavior/features/reports/normalization.feature`
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
- Path: `specs/behavior/features/reports/parsers.feature`
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
- Path: `specs/behavior/features/review/spec-review.feature`
- Summary: specweave review specs aggregates lint, coverage, and convention findings

#### Rule: Review reports feature and scenario counts

- `bdd-review-counts` Review reports feature and scenario statistics -> `tests/test_review_spec_review.py::TestReviewReportsMissingBindings::test_no_features` (bound)

#### Rule: Review reports missing bindings

- `bdd-review-missing-bindings` Review warns about unbound scenarios -> `tests/test_review_spec_review.py::TestReviewReportsMissingBindings::test_feature_with_no_test` (bound)

#### Rule: Review reports needs-review tags

- `bdd-review-needs-review` Review warns about @needs-review scenarios -> `tests/test_review_spec_review.py::TestReviewReportsNeedsReview::test_needs_review_flagged` (bound)

#### Rule: Review reports deprecated paths

- `bdd-review-deprecated-paths` Review warns about deprecated paths -> `tests/test_review_spec_review.py::TestReviewAggregatesCoverage::test_stale_mapping_causes_failed_review` (bound)

#### Rule: Review reports forbidden pytest-bdd usage

- `bdd-review-forbidden-pytest-bdd` Review errors on pytest-bdd usage -> `tests/test_review_spec_review.py::TestReviewAggregatesCoverage::test_forbidden_pytest_bdd` (bound)

#### Rule: Review aggregates lint findings

- `bdd-review-lint-findings` Review includes lint errors and warnings -> `tests/test_review_spec_review.py::TestReviewAggregatesCoverage::test_lint_findings` (bound)

#### Rule: Review points to detailed coverage

- `bdd-review-coverage-summary-both-directions` Review summary includes pytest reverse coverage counts -> `tests/test_review_spec_review.py::test_review_summary_includes_pytest_reverse_counts` (bound)
- `bdd-review-warning-scenario-once` Review warning prints scenario id once -> `tests/test_review_spec_review.py::test_review_missing_binding_message_does_not_duplicate_scenario_id` (bound)

## runners

### Delegated command runner
- Path: `specs/behavior/features/runners/command.feature`
- Summary: SpecWeave delegates external command execution through a runner that

#### Rule: Run successful commands

- `bdd-runner-success` Successful command writes passed summary -> `tests/test_runner_command.py::test_run_success` (bound)

#### Rule: Run failing commands

- `bdd-runner-failure` Failing command writes failed summary -> `tests/test_runner_command.py::test_run_failure` (bound)

#### Rule: Run command-not-found

- `bdd-runner-not-found` Non-existent command returns error status -> `tests/test_runner_command.py::test_run_not_found` (bound)

#### Rule: Capture stdout and stderr

- `bdd-runner-capture` Stdout and stderr are captured to separate files -> `tests/test_runner_command.py::test_run_captures_stdout_stderr` (bound)

## trace

### End-to-end traceability bundle extraction
- Path: `specs/behavior/features/trace/trace.feature`
- Summary: SpecWeave trace extracts a traceability bundle for a given `@bdd-*` id

#### Rule: Trace by bdd-id reports full mapping chain

- `bdd-trace-by-id` Trace by bdd-id finds feature, ac tags, test references, and gaps -> `tests/test_trace.py::test_trace_by_bdd_id_reports_mapping_and_missing_evidence_gap` (bound)

#### Rule: Trace rejects legacy markdown feature paths

- `bdd-trace-by-path` Trace by .feature.md path fails with a migration message -> `tests/test_trace.py::test_trace_rejects_markdown_feature_path` (bound)

## translation

### Brownfield pytest-to-Gherkin generation
- Path: `specs/behavior/features/translation/pytest-to-gherkin.feature`
- Summary: specweave create gherkin generates draft Gherkin feature files from

#### Rule: Generation discovers tests via AST

- `bdd-translate-discovers-tests` Generation finds test functions in pytest files -> `tests/test_translation_pytest_to_gherkin.py::TestSlug::test_basic` (bound)
- `bdd-translate-group-by-file` Generation groups scenarios by test file -> `tests/test_translation_pytest_to_gherkin.py::TestDeriveArea::test_simple` (bound)

#### Rule: Generation preserves existing features

- `bdd-translate-preserve-manual` Generation does not overwrite manual feature files -> `tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinPreservesExisting::test_skips_manual_file_without_force` (bound)
- `bdd-translate-force-overwrite` Generation overwrites with --force -> `tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinJsonShape::test_force_overwrites_manual` (bound)

#### Rule: Generation marks drafts appropriately

- `bdd-translate-marks-generated` Generated features have @generated tag -> `tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinFromSinglePytestFile::test_marks_needs_review` (bound)

#### Rule: Generation supports dry-run mode

- `bdd-translate-dry-run` Dry-run reports without writing files -> `tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinDryRun::test_writes_nothing` (bound)

### Gherkin-to-test skeleton generation
- Path: `specs/behavior/features/translation/spec-to-code.feature`
- Summary: SpecWeave generates test skeletons from Gherkin features. It produces step

#### Rule: Generate deterministic step function names

- `bdd-spec-to-code-step-name` Step function name derives from keyword and text -> `tests/test_spec_to_code.py::test_step_function_name_basic` (bound)
- `bdd-spec-to-code-dedup` Duplicate step texts get unique suffixes -> `tests/test_spec_to_code.py::test_step_function_name_dedup` (bound)

#### Rule: Draft feature from JSON input

- `bdd-spec-to-code-draft` draft_feature creates a valid feature file from JSON -> `tests/test_spec_to_code.py::test_draft_feature_creates_file` (bound)

#### Rule: Bind feature to a backend step skeleton

- `bdd-spec-to-code-bind-behave` bind_feature creates a behave step skeleton -> `tests/test_spec_to_code.py::test_bind_feature_creates_skeleton` (bound)
- `bdd-spec-to-code-bind-pytest-bdd` bind_feature creates a pytest-bdd step skeleton -> `tests/test_backends_pytest_bdd.py::test_bind_feature_writes_pytest_bdd_file` (bound)
- `bdd-spec-to-code-bind-unsupported` Unsupported backend raises clear error -> `tests/test_spec_to_code.py::test_bind_unsupported_backend_raises` (bound)
