---
id: SPEC-PYTEST
title: Pytest verification map
kind: capability-spec
status: active
version: 1
---

# Pytest verification map

## Intent

This specification keeps pytest-to-requirement coverage closed while product-level behavior specs are being rebound. Each requirement represents one executable pytest contract.

## Requirements

### REQ-TEST-001 — test backends pytest bdd.py test backend registry contents

SpecWeave SHALL preserve the executable contract `tests/test_backends_pytest_bdd.py::test_backend_registry_contents`.

Verification:
- pytest: tests/test_backends_pytest_bdd.py::test_backend_registry_contents

### REQ-TEST-002 — test backends pytest bdd.py test unsupported cucumber backends message

SpecWeave SHALL preserve the executable contract `tests/test_backends_pytest_bdd.py::test_unsupported_cucumber_backends_message`.

Verification:
- pytest: tests/test_backends_pytest_bdd.py::test_unsupported_cucumber_backends_message

### REQ-TEST-003 — test backends pytest bdd.py test pytest bdd skeleton shape

SpecWeave SHALL preserve the executable contract `tests/test_backends_pytest_bdd.py::test_pytest_bdd_skeleton_shape`.

Verification:
- pytest: tests/test_backends_pytest_bdd.py::test_pytest_bdd_skeleton_shape

### REQ-TEST-004 — test backends pytest bdd.py test pytest bdd dedups repeated steps

SpecWeave SHALL preserve the executable contract `tests/test_backends_pytest_bdd.py::test_pytest_bdd_dedups_repeated_steps`.

Verification:
- pytest: tests/test_backends_pytest_bdd.py::test_pytest_bdd_dedups_repeated_steps

### REQ-TEST-005 — test backends pytest bdd.py test pytest bdd collects rule scenarios

SpecWeave SHALL preserve the executable contract `tests/test_backends_pytest_bdd.py::test_pytest_bdd_collects_rule_scenarios`.

Verification:
- pytest: tests/test_backends_pytest_bdd.py::test_pytest_bdd_collects_rule_scenarios

### REQ-TEST-006 — test backends pytest bdd.py test bind feature writes pytest bdd file

SpecWeave SHALL preserve the executable contract `tests/test_backends_pytest_bdd.py::test_bind_feature_writes_pytest_bdd_file`.

Verification:
- pytest: tests/test_backends_pytest_bdd.py::test_bind_feature_writes_pytest_bdd_file

### REQ-TEST-007 — test backends pytest bdd.py test pytest bdd uses source path filename

SpecWeave SHALL preserve the executable contract `tests/test_backends_pytest_bdd.py::test_pytest_bdd_uses_source_path_filename`.

Verification:
- pytest: tests/test_backends_pytest_bdd.py::test_pytest_bdd_uses_source_path_filename

### REQ-TEST-008 — test bdd convert.py test export to target gherkin

SpecWeave SHALL preserve the executable contract `tests/test_bdd_convert.py::test_export_to_target_gherkin`.

Verification:
- pytest: tests/test_bdd_convert.py::test_export_to_target_gherkin

### REQ-TEST-009 — test bdd convert.py test round trip preserves ids

SpecWeave SHALL preserve the executable contract `tests/test_bdd_convert.py::test_round_trip_preserves_ids`.

Verification:
- pytest: tests/test_bdd_convert.py::test_round_trip_preserves_ids

### REQ-TEST-010 — test bdd convert.py test multiple ac tags and extra tags

SpecWeave SHALL preserve the executable contract `tests/test_bdd_convert.py::test_multiple_ac_tags_and_extra_tags`.

Verification:
- pytest: tests/test_bdd_convert.py::test_multiple_ac_tags_and_extra_tags

### REQ-TEST-011 — test bdd convert.py test top level examples become top level scenarios

SpecWeave SHALL preserve the executable contract `tests/test_bdd_convert.py::test_top_level_examples_become_top_level_scenarios`.

Verification:
- pytest: tests/test_bdd_convert.py::test_top_level_examples_become_top_level_scenarios

### REQ-TEST-012 — test bdd convert.py test and but steps group correctly

SpecWeave SHALL preserve the executable contract `tests/test_bdd_convert.py::test_and_but_steps_group_correctly`.

Verification:
- pytest: tests/test_bdd_convert.py::test_and_but_steps_group_correctly

### REQ-TEST-013 — test bdd convert.py test json round trip

SpecWeave SHALL preserve the executable contract `tests/test_bdd_convert.py::test_json_round_trip`.

Verification:
- pytest: tests/test_bdd_convert.py::test_json_round_trip

### REQ-TEST-014 — test bdd convert.py test json to feature to json round trip

SpecWeave SHALL preserve the executable contract `tests/test_bdd_convert.py::test_json_to_feature_to_json_round_trip`.

Verification:
- pytest: tests/test_bdd_convert.py::test_json_to_feature_to_json_round_trip

### REQ-TEST-015 — test behavior autolink.py test autolink generated id top level function

SpecWeave SHALL preserve the executable contract `tests/test_behavior_autolink.py::test_autolink_generated_id_top_level_function`.

Verification:
- pytest: tests/test_behavior_autolink.py::test_autolink_generated_id_top_level_function

### REQ-TEST-016 — test behavior autolink.py test autolink dry run does not write

SpecWeave SHALL preserve the executable contract `tests/test_behavior_autolink.py::test_autolink_dry_run_does_not_write`.

Verification:
- pytest: tests/test_behavior_autolink.py::test_autolink_dry_run_does_not_write

### REQ-TEST-017 — test behavior autolink.py test autolink apply writes mapping comments

SpecWeave SHALL preserve the executable contract `tests/test_behavior_autolink.py::test_autolink_apply_writes_mapping_comments`.

Verification:
- pytest: tests/test_behavior_autolink.py::test_autolink_apply_writes_mapping_comments

### REQ-TEST-018 — test behavior autolink.py test autolink preserves decorators

SpecWeave SHALL preserve the executable contract `tests/test_behavior_autolink.py::test_autolink_preserves_decorators`.

Verification:
- pytest: tests/test_behavior_autolink.py::test_autolink_preserves_decorators

### REQ-TEST-019 — test behavior autolink.py test autolink class method uses method indentation

SpecWeave SHALL preserve the executable contract `tests/test_behavior_autolink.py::test_autolink_class_method_uses_method_indentation`.

Verification:
- pytest: tests/test_behavior_autolink.py::test_autolink_class_method_uses_method_indentation

### REQ-TEST-020 — test behavior autolink.py test autolink skips existing mapping

SpecWeave SHALL preserve the executable contract `tests/test_behavior_autolink.py::test_autolink_skips_existing_mapping`.

Verification:
- pytest: tests/test_behavior_autolink.py::test_autolink_skips_existing_mapping

### REQ-TEST-021 — test behavior autolink.py test autolink reports ambiguous equal score

SpecWeave SHALL preserve the executable contract `tests/test_behavior_autolink.py::test_autolink_reports_ambiguous_equal_score`.

Verification:
- pytest: tests/test_behavior_autolink.py::test_autolink_reports_ambiguous_equal_score

### REQ-TEST-022 — test behavior autolink.py test autolink rewrites duplicate occurrences only when enabled

SpecWeave SHALL preserve the executable contract `tests/test_behavior_autolink.py::test_autolink_rewrites_duplicate_occurrences_only_when_enabled`.

Verification:
- pytest: tests/test_behavior_autolink.py::test_autolink_rewrites_duplicate_occurrences_only_when_enabled

### REQ-TEST-023 — test behavior autolink.py test autolink json shape

SpecWeave SHALL preserve the executable contract `tests/test_behavior_autolink.py::test_autolink_json_shape`.

Verification:
- pytest: tests/test_behavior_autolink.py::test_autolink_json_shape

### REQ-TEST-024 — test behavior autolink.py test autolink uses config paths

SpecWeave SHALL preserve the executable contract `tests/test_behavior_autolink.py::test_autolink_uses_config_paths`.

Verification:
- pytest: tests/test_behavior_autolink.py::test_autolink_uses_config_paths

### REQ-TEST-025 — test behavior coverage.py test behavior coverage feature md bound by comment

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_behavior_coverage_feature_md_bound_by_comment`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_behavior_coverage_feature_md_bound_by_comment

### REQ-TEST-026 — test behavior coverage.py test behavior coverage does not match by title

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_behavior_coverage_does_not_match_by_title`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_behavior_coverage_does_not_match_by_title

### REQ-TEST-027 — test behavior coverage.py test behavior coverage reports stale markdown mapping

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_behavior_coverage_reports_stale_markdown_mapping`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_behavior_coverage_reports_stale_markdown_mapping

### REQ-TEST-028 — test behavior coverage.py test behavior coverage reports forbidden pytest bdd usage

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_behavior_coverage_reports_forbidden_pytest_bdd_usage`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_behavior_coverage_reports_forbidden_pytest_bdd_usage

### REQ-TEST-029 — test behavior coverage.py test behavior coverage ignores pytest bdd text

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_behavior_coverage_ignores_pytest_bdd_text`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_behavior_coverage_ignores_pytest_bdd_text

### REQ-TEST-030 — test behavior coverage.py test coverage missing test file

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_coverage_missing_test_file`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_coverage_missing_test_file

### REQ-TEST-031 — test behavior coverage.py test coverage stale feature binding

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_coverage_stale_feature_binding`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_coverage_stale_feature_binding

### REQ-TEST-032 — test behavior coverage.py test coverage deprecated paths

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_coverage_deprecated_paths`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_coverage_deprecated_paths

### REQ-TEST-033 — test behavior coverage.py test coverage manual scenario skipped

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_coverage_manual_scenario_skipped`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_coverage_manual_scenario_skipped

### REQ-TEST-034 — test behavior coverage.py test coverage lists unmapped pytest tests

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_coverage_lists_unmapped_pytest_tests`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_coverage_lists_unmapped_pytest_tests

### REQ-TEST-035 — test behavior coverage.py test coverage matches mapping on class test method

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_coverage_matches_mapping_on_class_test_method`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_coverage_matches_mapping_on_class_test_method

### REQ-TEST-036 — test behavior coverage.py test coverage marks stale pytest test in reverse inventory

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_coverage_marks_stale_pytest_test_in_reverse_inventory`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_coverage_marks_stale_pytest_test_in_reverse_inventory

### REQ-TEST-037 — test behavior coverage.py test coverage candidate tests are hints not bindings

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_coverage_candidate_tests_are_hints_not_bindings`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_coverage_candidate_tests_are_hints_not_bindings

### REQ-TEST-038 — test behavior coverage.py test render coverage text both directions

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_render_coverage_text_both_directions`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_render_coverage_text_both_directions

### REQ-TEST-039 — test behavior coverage.py test coverage accepts intentional unmapped pytest tests

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_coverage_accepts_intentional_unmapped_pytest_tests`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_coverage_accepts_intentional_unmapped_pytest_tests

### REQ-TEST-040 — test behavior coverage.py test coverage accepts intentional unmapped policy file

SpecWeave SHALL preserve the executable contract `tests/test_behavior_coverage.py::test_coverage_accepts_intentional_unmapped_policy_file`.

Verification:
- pytest: tests/test_behavior_coverage.py::test_coverage_accepts_intentional_unmapped_policy_file

### REQ-TEST-041 — test behavior generation.py test generate single feature

SpecWeave SHALL preserve the executable contract `tests/test_behavior_generation.py::test_generate_single_feature`.

Verification:
- pytest: tests/test_behavior_generation.py::test_generate_single_feature

### REQ-TEST-042 — test behavior generation.py test generate scenario function

SpecWeave SHALL preserve the executable contract `tests/test_behavior_generation.py::test_generate_scenario_function`.

Verification:
- pytest: tests/test_behavior_generation.py::test_generate_scenario_function

### REQ-TEST-043 — test behavior generation.py test generate specweave markers

SpecWeave SHALL preserve the executable contract `tests/test_behavior_generation.py::test_generate_specweave_markers`.

Verification:
- pytest: tests/test_behavior_generation.py::test_generate_specweave_markers

### REQ-TEST-044 — test behavior generation.py test generate docstring

SpecWeave SHALL preserve the executable contract `tests/test_behavior_generation.py::test_generate_docstring`.

Verification:
- pytest: tests/test_behavior_generation.py::test_generate_docstring

### REQ-TEST-045 — test behavior generation.py test generate step comments

SpecWeave SHALL preserve the executable contract `tests/test_behavior_generation.py::test_generate_step_comments`.

Verification:
- pytest: tests/test_behavior_generation.py::test_generate_step_comments

### REQ-TEST-046 — test behavior generation.py test generate canonical path

SpecWeave SHALL preserve the executable contract `tests/test_behavior_generation.py::test_generate_canonical_path`.

Verification:
- pytest: tests/test_behavior_generation.py::test_generate_canonical_path

### REQ-TEST-047 — test behavior generation.py test generate rules

SpecWeave SHALL preserve the executable contract `tests/test_behavior_generation.py::test_generate_rules`.

Verification:
- pytest: tests/test_behavior_generation.py::test_generate_rules

### REQ-TEST-048 — test behavior generation.py test generate avoids long specweave mapping lines

SpecWeave SHALL preserve the executable contract `tests/test_behavior_generation.py::test_generate_avoids_long_specweave_mapping_lines`.

Verification:
- pytest: tests/test_behavior_generation.py::test_generate_avoids_long_specweave_mapping_lines

### REQ-TEST-049 — test behavior generation.py test generate batch

SpecWeave SHALL preserve the executable contract `tests/test_behavior_generation.py::test_generate_batch`.

Verification:
- pytest: tests/test_behavior_generation.py::test_generate_batch

### REQ-TEST-050 — test behavior index.py test index generates markdown

SpecWeave SHALL preserve the executable contract `tests/test_behavior_index.py::test_index_generates_markdown`.

Verification:
- pytest: tests/test_behavior_index.py::test_index_generates_markdown

### REQ-TEST-051 — test behavior index.py test index generates manifest

SpecWeave SHALL preserve the executable contract `tests/test_behavior_index.py::test_index_generates_manifest`.

Verification:
- pytest: tests/test_behavior_index.py::test_index_generates_manifest

### REQ-TEST-052 — test behavior index.py test index scenario entries

SpecWeave SHALL preserve the executable contract `tests/test_behavior_index.py::test_index_scenario_entries`.

Verification:
- pytest: tests/test_behavior_index.py::test_index_scenario_entries

### REQ-TEST-053 — test behavior index.py test index unbound scenario

SpecWeave SHALL preserve the executable contract `tests/test_behavior_index.py::test_index_unbound_scenario`.

Verification:
- pytest: tests/test_behavior_index.py::test_index_unbound_scenario

### REQ-TEST-054 — test behavior index.py test index evidence status

SpecWeave SHALL preserve the executable contract `tests/test_behavior_index.py::test_index_evidence_status`.

Verification:
- pytest: tests/test_behavior_index.py::test_index_evidence_status

### REQ-TEST-055 — test behavior index.py test index rules

SpecWeave SHALL preserve the executable contract `tests/test_behavior_index.py::test_index_rules`.

Verification:
- pytest: tests/test_behavior_index.py::test_index_rules

### REQ-TEST-056 — test behavior reporting.py test import maps by nodeid

SpecWeave SHALL preserve the executable contract `tests/test_behavior_reporting.py::test_import_maps_by_nodeid`.

Verification:
- pytest: tests/test_behavior_reporting.py::test_import_maps_by_nodeid

### REQ-TEST-057 — test behavior reporting.py test import maps by function name

SpecWeave SHALL preserve the executable contract `tests/test_behavior_reporting.py::test_import_maps_by_function_name`.

Verification:
- pytest: tests/test_behavior_reporting.py::test_import_maps_by_function_name

### REQ-TEST-058 — test behavior reporting.py test import maps by manifest

SpecWeave SHALL preserve the executable contract `tests/test_behavior_reporting.py::test_import_maps_by_manifest`.

Verification:
- pytest: tests/test_behavior_reporting.py::test_import_maps_by_manifest

### REQ-TEST-059 — test behavior reporting.py test import unmapped tests

SpecWeave SHALL preserve the executable contract `tests/test_behavior_reporting.py::test_import_unmapped_tests`.

Verification:
- pytest: tests/test_behavior_reporting.py::test_import_unmapped_tests

### REQ-TEST-060 — test behavior reporting.py test import writes evidence

SpecWeave SHALL preserve the executable contract `tests/test_behavior_reporting.py::test_import_writes_evidence`.

Verification:
- pytest: tests/test_behavior_reporting.py::test_import_writes_evidence

### REQ-TEST-061 — test cli cli contract.py test help exits 0

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_help_exits_0`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_help_exits_0

### REQ-TEST-062 — test cli cli contract.py test review golden reports agent outputs

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_review_golden_reports_agent_outputs`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_review_golden_reports_agent_outputs

### REQ-TEST-063 — test cli cli contract.py test version exits 0

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_version_exits_0`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_version_exits_0

### REQ-TEST-064 — test cli cli contract.py test bdd export and import round trip

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_bdd_export_and_import_round_trip`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_bdd_export_and_import_round_trip

### REQ-TEST-065 — test cli cli contract.py test report normalize writes json and exits nonzero on failure

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_report_normalize_writes_json_and_exits_nonzero_on_failure`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_report_normalize_writes_json_and_exits_nonzero_on_failure

### REQ-TEST-066 — test cli cli contract.py test report normalize passing exits 0

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_report_normalize_passing_exits_0`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_report_normalize_passing_exits_0

### REQ-TEST-067 — test cli cli contract.py test report inspect prints summary

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_report_inspect_prints_summary`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_report_inspect_prints_summary

### REQ-TEST-068 — test cli cli contract.py test archledger candidate command

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_archledger_candidate_command`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_archledger_candidate_command

### REQ-TEST-069 — test cli cli contract.py test bind pytest bdd backend

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_bind_pytest_bdd_backend`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_bind_pytest_bdd_backend

### REQ-TEST-070 — test cli cli contract.py test behavior check accepts canonical feature

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_behavior_check_accepts_canonical_feature`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_behavior_check_accepts_canonical_feature

### REQ-TEST-071 — test cli cli contract.py test behavior check warns on deprecated specs bdd path

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_behavior_check_warns_on_deprecated_specs_bdd_path`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_behavior_check_warns_on_deprecated_specs_bdd_path

### REQ-TEST-072 — test cli cli contract.py test behavior generate tests creates plain pytest

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_behavior_generate_tests_creates_plain_pytest`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_behavior_generate_tests_creates_plain_pytest

### REQ-TEST-073 — test cli cli contract.py test behavior index writes markdown and manifest

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_behavior_index_writes_markdown_and_manifest`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_behavior_index_writes_markdown_and_manifest

### REQ-TEST-074 — test cli cli contract.py test behavior index accepts tests alias

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_behavior_index_accepts_tests_alias`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_behavior_index_accepts_tests_alias

### REQ-TEST-075 — test cli cli contract.py test behavior commands use configured default paths

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_behavior_commands_use_configured_default_paths`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_behavior_commands_use_configured_default_paths

### REQ-TEST-076 — test cli cli contract.py test behavior coverage reports bound scenarios

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_behavior_coverage_reports_bound_scenarios`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_behavior_coverage_reports_bound_scenarios

### REQ-TEST-077 — test cli cli contract.py test behavior coverage text shows missing

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_behavior_coverage_text_shows_missing`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_behavior_coverage_text_shows_missing

### REQ-TEST-078 — test cli cli contract.py test behavior coverage feature filter

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_behavior_coverage_feature_filter`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_behavior_coverage_feature_filter

### REQ-TEST-079 — test cli cli contract.py test review coverage both directions text

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_review_coverage_both_directions_text`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_review_coverage_both_directions_text

### REQ-TEST-080 — test cli cli contract.py test behavior coverage view test json

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_behavior_coverage_view_test_json`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_behavior_coverage_view_test_json

### REQ-TEST-081 — test cli cli contract.py test review specs prints scenario only once

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_review_specs_prints_scenario_only_once`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_review_specs_prints_scenario_only_once

### REQ-TEST-082 — test cli cli contract.py test behavior mappings lists comment and marker sources

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_behavior_mappings_lists_comment_and_marker_sources`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_behavior_mappings_lists_comment_and_marker_sources

### REQ-TEST-083 — test cli cli contract.py test behavior import report maps pytest nodeid

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_behavior_import_report_maps_pytest_nodeid`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_behavior_import_report_maps_pytest_nodeid

### REQ-TEST-084 — test cli cli contract.py test config option

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_config_option`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_config_option

### REQ-TEST-085 — test cli cli contract.py test init respects explicit hidden config

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_init_respects_explicit_hidden_config`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_init_respects_explicit_hidden_config

### REQ-TEST-086 — test cli cli contract.py test json output

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_json_output`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_json_output

### REQ-TEST-087 — test cli cli contract.py test json init

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_json_init`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_json_init

### REQ-TEST-088 — test cli cli contract.py test bdd check alias

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_bdd_check_alias`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_bdd_check_alias

### REQ-TEST-089 — test cli cli contract.py test bdd index alias

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_bdd_index_alias`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_bdd_index_alias

### REQ-TEST-090 — test cli cli contract.py test create feature

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_create_feature`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_create_feature

### REQ-TEST-091 — test cli cli contract.py test create gherkin

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_create_gherkin`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_create_gherkin

### REQ-TEST-092 — test cli cli contract.py test create plan

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_create_plan`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_create_plan

### REQ-TEST-093 — test cli cli contract.py test exit doctor failed

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_exit_doctor_failed`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_exit_doctor_failed

### REQ-TEST-094 — test cli cli contract.py test exit check errors

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_exit_check_errors`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_exit_check_errors

### REQ-TEST-095 — test cli cli contract.py test specifications index writes markdown and manifest

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_specifications_index_writes_markdown_and_manifest`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_specifications_index_writes_markdown_and_manifest

### REQ-TEST-096 — test cli cli contract.py test sdd index alias

SpecWeave SHALL preserve the executable contract `tests/test_cli_cli_contract.py::test_sdd_index_alias`.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_sdd_index_alias

### REQ-TEST-097 — test cli json.py TestRootJson test json version

SpecWeave SHALL preserve the executable contract `tests/test_cli_json.py::TestRootJson::test_json_version`.

Verification:
- pytest: tests/test_cli_json.py::TestRootJson::test_json_version

### REQ-TEST-098 — test cli json.py TestRootJson test human version

SpecWeave SHALL preserve the executable contract `tests/test_cli_json.py::TestRootJson::test_human_version`.

Verification:
- pytest: tests/test_cli_json.py::TestRootJson::test_human_version

### REQ-TEST-099 — test cli json.py TestRootJson test json init dry run

SpecWeave SHALL preserve the executable contract `tests/test_cli_json.py::TestRootJson::test_json_init_dry_run`.

Verification:
- pytest: tests/test_cli_json.py::TestRootJson::test_json_init_dry_run

### REQ-TEST-100 — test cli json.py TestRootJson test human init

SpecWeave SHALL preserve the executable contract `tests/test_cli_json.py::TestRootJson::test_human_init`.

Verification:
- pytest: tests/test_cli_json.py::TestRootJson::test_human_init

### REQ-TEST-101 — test cli json.py TestRootJson test json init british

SpecWeave SHALL preserve the executable contract `tests/test_cli_json.py::TestRootJson::test_json_init_british`.

Verification:
- pytest: tests/test_cli_json.py::TestRootJson::test_json_init_british

### REQ-TEST-102 — test cli json.py TestRootJson test json doctor

SpecWeave SHALL preserve the executable contract `tests/test_cli_json.py::TestRootJson::test_json_doctor`.

Verification:
- pytest: tests/test_cli_json.py::TestRootJson::test_json_doctor

### REQ-TEST-103 — test cli json.py TestRootJson test json review specs

SpecWeave SHALL preserve the executable contract `tests/test_cli_json.py::TestRootJson::test_json_review_specs`.

Verification:
- pytest: tests/test_cli_json.py::TestRootJson::test_json_review_specs

### REQ-TEST-104 — test cli json.py TestRootJson test config option

SpecWeave SHALL preserve the executable contract `tests/test_cli_json.py::TestRootJson::test_config_option`.

Verification:
- pytest: tests/test_cli_json.py::TestRootJson::test_config_option

### REQ-TEST-105 — test cli json.py TestInitIdempotency test init twice no force

SpecWeave SHALL preserve the executable contract `tests/test_cli_json.py::TestInitIdempotency::test_init_twice_no_force`.

Verification:
- pytest: tests/test_cli_json.py::TestInitIdempotency::test_init_twice_no_force

### REQ-TEST-106 — test combi check.py test combi check writes json and human diagnostics

SpecWeave SHALL preserve the executable contract `tests/test_combi_check.py::test_combi_check_writes_json_and_human_diagnostics`.

Verification:
- pytest: tests/test_combi_check.py::test_combi_check_writes_json_and_human_diagnostics

### REQ-TEST-107 — test combi check.py test combi check strict fails on missing bdd id

SpecWeave SHALL preserve the executable contract `tests/test_combi_check.py::test_combi_check_strict_fails_on_missing_bdd_id`.

Verification:
- pytest: tests/test_combi_check.py::test_combi_check_strict_fails_on_missing_bdd_id

### REQ-TEST-108 — test combi check.py test combi check includes specification requirements

SpecWeave SHALL preserve the executable contract `tests/test_combi_check.py::test_combi_check_includes_specification_requirements`.

Verification:
- pytest: tests/test_combi_check.py::test_combi_check_includes_specification_requirements

### REQ-TEST-109 — test common behavior helpers.py TestFeatureStem test feature md

SpecWeave SHALL preserve the executable contract `tests/test_common_behavior_helpers.py::TestFeatureStem::test_feature_md`.

Verification:
- pytest: tests/test_common_behavior_helpers.py::TestFeatureStem::test_feature_md

### REQ-TEST-110 — test common behavior helpers.py TestFeatureStem test classic feature

SpecWeave SHALL preserve the executable contract `tests/test_common_behavior_helpers.py::TestFeatureStem::test_classic_feature`.

Verification:
- pytest: tests/test_common_behavior_helpers.py::TestFeatureStem::test_classic_feature

### REQ-TEST-111 — test common behavior helpers.py TestFeatureStem test deep path

SpecWeave SHALL preserve the executable contract `tests/test_common_behavior_helpers.py::TestFeatureStem::test_deep_path`.

Verification:
- pytest: tests/test_common_behavior_helpers.py::TestFeatureStem::test_deep_path

### REQ-TEST-112 — test common behavior helpers.py TestFeatureStem test other extension

SpecWeave SHALL preserve the executable contract `tests/test_common_behavior_helpers.py::TestFeatureStem::test_other_extension`.

Verification:
- pytest: tests/test_common_behavior_helpers.py::TestFeatureStem::test_other_extension

### REQ-TEST-113 — test common behavior helpers.py TestSlugify test basic

SpecWeave SHALL preserve the executable contract `tests/test_common_behavior_helpers.py::TestSlugify::test_basic`.

Verification:
- pytest: tests/test_common_behavior_helpers.py::TestSlugify::test_basic

### REQ-TEST-114 — test common behavior helpers.py TestSlugify test special chars

SpecWeave SHALL preserve the executable contract `tests/test_common_behavior_helpers.py::TestSlugify::test_special_chars`.

Verification:
- pytest: tests/test_common_behavior_helpers.py::TestSlugify::test_special_chars

### REQ-TEST-115 — test common behavior helpers.py TestSlugify test empty

SpecWeave SHALL preserve the executable contract `tests/test_common_behavior_helpers.py::TestSlugify::test_empty`.

Verification:
- pytest: tests/test_common_behavior_helpers.py::TestSlugify::test_empty

### REQ-TEST-116 — test common behavior helpers.py TestFeatureIdentity test from path

SpecWeave SHALL preserve the executable contract `tests/test_common_behavior_helpers.py::TestFeatureIdentity::test_from_path`.

Verification:
- pytest: tests/test_common_behavior_helpers.py::TestFeatureIdentity::test_from_path

### REQ-TEST-117 — test common behavior helpers.py TestFeatureIdentity test no area

SpecWeave SHALL preserve the executable contract `tests/test_common_behavior_helpers.py::TestFeatureIdentity::test_no_area`.

Verification:
- pytest: tests/test_common_behavior_helpers.py::TestFeatureIdentity::test_no_area

### REQ-TEST-118 — test common behavior helpers.py TestCanonicalTestPath test derives path

SpecWeave SHALL preserve the executable contract `tests/test_common_behavior_helpers.py::TestCanonicalTestPath::test_derives_path`.

Verification:
- pytest: tests/test_common_behavior_helpers.py::TestCanonicalTestPath::test_derives_path

### REQ-TEST-119 — test common behavior helpers.py TestIterFeatureScenarios test yields top level

SpecWeave SHALL preserve the executable contract `tests/test_common_behavior_helpers.py::TestIterFeatureScenarios::test_yields_top_level`.

Verification:
- pytest: tests/test_common_behavior_helpers.py::TestIterFeatureScenarios::test_yields_top_level

### REQ-TEST-120 — test common behavior helpers.py TestIterFeatureScenarios test yields from rules

SpecWeave SHALL preserve the executable contract `tests/test_common_behavior_helpers.py::TestIterFeatureScenarios::test_yields_from_rules`.

Verification:
- pytest: tests/test_common_behavior_helpers.py::TestIterFeatureScenarios::test_yields_from_rules

### REQ-TEST-121 — test common behavior helpers.py TestScenarioIdValue test returns first bdd tag

SpecWeave SHALL preserve the executable contract `tests/test_common_behavior_helpers.py::TestScenarioIdValue::test_returns_first_bdd_tag`.

Verification:
- pytest: tests/test_common_behavior_helpers.py::TestScenarioIdValue::test_returns_first_bdd_tag

### REQ-TEST-122 — test common behavior helpers.py TestScenarioIdValue test returns empty when no bdd

SpecWeave SHALL preserve the executable contract `tests/test_common_behavior_helpers.py::TestScenarioIdValue::test_returns_empty_when_no_bdd`.

Verification:
- pytest: tests/test_common_behavior_helpers.py::TestScenarioIdValue::test_returns_empty_when_no_bdd

### REQ-TEST-123 — test config configuration.py TestFindConfig test prefers explicit

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestFindConfig::test_prefers_explicit`.

Verification:
- pytest: tests/test_config_configuration.py::TestFindConfig::test_prefers_explicit

### REQ-TEST-124 — test config configuration.py TestFindConfig test prefers public over dotfile

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestFindConfig::test_prefers_public_over_dotfile`.

Verification:
- pytest: tests/test_config_configuration.py::TestFindConfig::test_prefers_public_over_dotfile

### REQ-TEST-125 — test config configuration.py TestFindConfig test returns none when missing

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestFindConfig::test_returns_none_when_missing`.

Verification:
- pytest: tests/test_config_configuration.py::TestFindConfig::test_returns_none_when_missing

### REQ-TEST-126 — test config configuration.py TestFindConfig test finds hidden config

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestFindConfig::test_finds_hidden_config`.

Verification:
- pytest: tests/test_config_configuration.py::TestFindConfig::test_finds_hidden_config

### REQ-TEST-127 — test config configuration.py TestFindConfig test walks up directories

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestFindConfig::test_walks_up_directories`.

Verification:
- pytest: tests/test_config_configuration.py::TestFindConfig::test_walks_up_directories

### REQ-TEST-128 — test config configuration.py TestLoadConfig test defaults when missing

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestLoadConfig::test_defaults_when_missing`.

Verification:
- pytest: tests/test_config_configuration.py::TestLoadConfig::test_defaults_when_missing

### REQ-TEST-129 — test config configuration.py TestLoadConfig test rejects unsupported schema

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestLoadConfig::test_rejects_unsupported_schema`.

Verification:
- pytest: tests/test_config_configuration.py::TestLoadConfig::test_rejects_unsupported_schema

### REQ-TEST-130 — test config configuration.py TestLoadConfig test normalizes nested behaviour paths

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestLoadConfig::test_normalizes_nested_behaviour_paths`.

Verification:
- pytest: tests/test_config_configuration.py::TestLoadConfig::test_normalizes_nested_behaviour_paths

### REQ-TEST-131 — test config configuration.py TestLoadConfig test preserves flat behavior path fields

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestLoadConfig::test_preserves_flat_behavior_path_fields`.

Verification:
- pytest: tests/test_config_configuration.py::TestLoadConfig::test_preserves_flat_behavior_path_fields

### REQ-TEST-132 — test config configuration.py TestLoadConfig test loads all sections

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestLoadConfig::test_loads_all_sections`.

Verification:
- pytest: tests/test_config_configuration.py::TestLoadConfig::test_loads_all_sections

### REQ-TEST-133 — test config configuration.py TestLoadConfig test loads specifications paths

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestLoadConfig::test_loads_specifications_paths`.

Verification:
- pytest: tests/test_config_configuration.py::TestLoadConfig::test_loads_specifications_paths

### REQ-TEST-134 — test config configuration.py TestLoadConfig test resolves paths from config project root

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestLoadConfig::test_resolves_paths_from_config_project_root`.

Verification:
- pytest: tests/test_config_configuration.py::TestLoadConfig::test_resolves_paths_from_config_project_root

### REQ-TEST-135 — test config configuration.py TestLoadConfig test rejects unsupported group by

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestLoadConfig::test_rejects_unsupported_group_by`.

Verification:
- pytest: tests/test_config_configuration.py::TestLoadConfig::test_rejects_unsupported_group_by

### REQ-TEST-136 — test config configuration.py TestLoadConfig test gherkin fields preserved

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestLoadConfig::test_gherkin_fields_preserved`.

Verification:
- pytest: tests/test_config_configuration.py::TestLoadConfig::test_gherkin_fields_preserved

### REQ-TEST-137 — test config configuration.py TestRenderDefaultConfig test renders behavior

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestRenderDefaultConfig::test_renders_behavior`.

Verification:
- pytest: tests/test_config_configuration.py::TestRenderDefaultConfig::test_renders_behavior

### REQ-TEST-138 — test config configuration.py TestRenderDefaultConfig test renders behaviour

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestRenderDefaultConfig::test_renders_behaviour`.

Verification:
- pytest: tests/test_config_configuration.py::TestRenderDefaultConfig::test_renders_behaviour

### REQ-TEST-139 — test config configuration.py TestRenderDefaultConfig test renders both modes

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestRenderDefaultConfig::test_renders_both_modes`.

Verification:
- pytest: tests/test_config_configuration.py::TestRenderDefaultConfig::test_renders_both_modes

### REQ-TEST-140 — test config configuration.py TestRenderDefaultConfig test is valid toml

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestRenderDefaultConfig::test_is_valid_toml`.

Verification:
- pytest: tests/test_config_configuration.py::TestRenderDefaultConfig::test_is_valid_toml

### REQ-TEST-141 — test config configuration.py TestRenderDefaultConfig test roundtrip

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestRenderDefaultConfig::test_roundtrip`.

Verification:
- pytest: tests/test_config_configuration.py::TestRenderDefaultConfig::test_roundtrip

### REQ-TEST-142 — test config configuration.py TestRenderDefaultConfig test renders classic only defaults

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestRenderDefaultConfig::test_renders_classic_only_defaults`.

Verification:
- pytest: tests/test_config_configuration.py::TestRenderDefaultConfig::test_renders_classic_only_defaults

### REQ-TEST-143 — test config configuration.py TestSpecWeavePaths test defaults

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestSpecWeavePaths::test_defaults`.

Verification:
- pytest: tests/test_config_configuration.py::TestSpecWeavePaths::test_defaults

### REQ-TEST-144 — test config configuration.py TestSpecWeavePaths test frozen

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestSpecWeavePaths::test_frozen`.

Verification:
- pytest: tests/test_config_configuration.py::TestSpecWeavePaths::test_frozen

### REQ-TEST-145 — test config configuration.py TestSpecWeaveConfig test defaults

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestSpecWeaveConfig::test_defaults`.

Verification:
- pytest: tests/test_config_configuration.py::TestSpecWeaveConfig::test_defaults

### REQ-TEST-146 — test config configuration.py TestSpecWeaveConfig test frozen

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestSpecWeaveConfig::test_frozen`.

Verification:
- pytest: tests/test_config_configuration.py::TestSpecWeaveConfig::test_frozen

### REQ-TEST-147 — test config configuration.py test specweave skill uses canonical report paths

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::test_specweave_skill_uses_canonical_report_paths`.

Verification:
- pytest: tests/test_config_configuration.py::test_specweave_skill_uses_canonical_report_paths

### REQ-TEST-148 — test config configuration.py TestSpecWeaveGherkin test default official parser is false

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestSpecWeaveGherkin::test_default_official_parser_is_false`.

Verification:
- pytest: tests/test_config_configuration.py::TestSpecWeaveGherkin::test_default_official_parser_is_false

### REQ-TEST-149 — test config configuration.py TestSpecWeaveGherkin test default keyword is example

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestSpecWeaveGherkin::test_default_keyword_is_example`.

Verification:
- pytest: tests/test_config_configuration.py::TestSpecWeaveGherkin::test_default_keyword_is_example

### REQ-TEST-150 — test config configuration.py TestSpecWeaveGherkin test compile pickles without official raises

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestSpecWeaveGherkin::test_compile_pickles_without_official_raises`.

Verification:
- pytest: tests/test_config_configuration.py::TestSpecWeaveGherkin::test_compile_pickles_without_official_raises

### REQ-TEST-151 — test config configuration.py TestSpecWeaveGherkin test compile pickles with official ok

SpecWeave SHALL preserve the executable contract `tests/test_config_configuration.py::TestSpecWeaveGherkin::test_compile_pickles_with_official_ok`.

Verification:
- pytest: tests/test_config_configuration.py::TestSpecWeaveGherkin::test_compile_pickles_with_official_ok

### REQ-TEST-152 — test create feature json.py TestParseFeatureDraft test parses title and tags

SpecWeave SHALL preserve the executable contract `tests/test_create_feature_json.py::TestParseFeatureDraft::test_parses_title_and_tags`.

Verification:
- pytest: tests/test_create_feature_json.py::TestParseFeatureDraft::test_parses_title_and_tags

### REQ-TEST-153 — test create feature json.py TestParseFeatureDraft test parses rules and scenarios

SpecWeave SHALL preserve the executable contract `tests/test_create_feature_json.py::TestParseFeatureDraft::test_parses_rules_and_scenarios`.

Verification:
- pytest: tests/test_create_feature_json.py::TestParseFeatureDraft::test_parses_rules_and_scenarios

### REQ-TEST-154 — test create feature json.py TestParseFeatureDraft test parses steps

SpecWeave SHALL preserve the executable contract `tests/test_create_feature_json.py::TestParseFeatureDraft::test_parses_steps`.

Verification:
- pytest: tests/test_create_feature_json.py::TestParseFeatureDraft::test_parses_steps

### REQ-TEST-155 — test create feature json.py TestParseFeatureDraft test load from file

SpecWeave SHALL preserve the executable contract `tests/test_create_feature_json.py::TestParseFeatureDraft::test_load_from_file`.

Verification:
- pytest: tests/test_create_feature_json.py::TestParseFeatureDraft::test_load_from_file

### REQ-TEST-156 — test create feature json.py TestWriteDraftFeature test writes classic feature

SpecWeave SHALL preserve the executable contract `tests/test_create_feature_json.py::TestWriteDraftFeature::test_writes_classic_feature`.

Verification:
- pytest: tests/test_create_feature_json.py::TestWriteDraftFeature::test_writes_classic_feature

### REQ-TEST-157 — test create feature json.py TestCreateFeatureFromJson test cli from json

SpecWeave SHALL preserve the executable contract `tests/test_create_feature_json.py::TestCreateFeatureFromJson::test_cli_from_json`.

Verification:
- pytest: tests/test_create_feature_json.py::TestCreateFeatureFromJson::test_cli_from_json

### REQ-TEST-158 — test create feature json.py TestCreateFeatureFromJson test cli from json dry run

SpecWeave SHALL preserve the executable contract `tests/test_create_feature_json.py::TestCreateFeatureFromJson::test_cli_from_json_dry_run`.

Verification:
- pytest: tests/test_create_feature_json.py::TestCreateFeatureFromJson::test_cli_from_json_dry_run

### REQ-TEST-159 — test create feature json.py TestCreateFeatureFromJson test cli from json refuses existing

SpecWeave SHALL preserve the executable contract `tests/test_create_feature_json.py::TestCreateFeatureFromJson::test_cli_from_json_refuses_existing`.

Verification:
- pytest: tests/test_create_feature_json.py::TestCreateFeatureFromJson::test_cli_from_json_refuses_existing

### REQ-TEST-160 — test create feature json.py TestCreateFeatureFromJson test cli from json force overwrites

SpecWeave SHALL preserve the executable contract `tests/test_create_feature_json.py::TestCreateFeatureFromJson::test_cli_from_json_force_overwrites`.

Verification:
- pytest: tests/test_create_feature_json.py::TestCreateFeatureFromJson::test_cli_from_json_force_overwrites

### REQ-TEST-161 — test create feature json.py TestCreateFeatureFromJson test cli legacy path still works

SpecWeave SHALL preserve the executable contract `tests/test_create_feature_json.py::TestCreateFeatureFromJson::test_cli_legacy_path_still_works`.

Verification:
- pytest: tests/test_create_feature_json.py::TestCreateFeatureFromJson::test_cli_legacy_path_still_works

### REQ-TEST-162 — test create feature json.py TestCreateFeatureFromJson test cli legacy dry run writes nothing

SpecWeave SHALL preserve the executable contract `tests/test_create_feature_json.py::TestCreateFeatureFromJson::test_cli_legacy_dry_run_writes_nothing`.

Verification:
- pytest: tests/test_create_feature_json.py::TestCreateFeatureFromJson::test_cli_legacy_dry_run_writes_nothing

### REQ-TEST-163 — test create feature json.py TestCreateFeatureFromJson test cli legacy rejects empty area

SpecWeave SHALL preserve the executable contract `tests/test_create_feature_json.py::TestCreateFeatureFromJson::test_cli_legacy_rejects_empty_area`.

Verification:
- pytest: tests/test_create_feature_json.py::TestCreateFeatureFromJson::test_cli_legacy_rejects_empty_area

### REQ-TEST-164 — test doctor diagnostics.py TestDoctorPasses test passes initialized project

SpecWeave SHALL preserve the executable contract `tests/test_doctor_diagnostics.py::TestDoctorPasses::test_passes_initialized_project`.

Verification:
- pytest: tests/test_doctor_diagnostics.py::TestDoctorPasses::test_passes_initialized_project

### REQ-TEST-165 — test doctor diagnostics.py TestDoctorPasses test explicit config uses resolved paths without relative warnings

SpecWeave SHALL preserve the executable contract `tests/test_doctor_diagnostics.py::TestDoctorPasses::test_explicit_config_uses_resolved_paths_without_relative_warnings`.

Verification:
- pytest: tests/test_doctor_diagnostics.py::TestDoctorPasses::test_explicit_config_uses_resolved_paths_without_relative_warnings

### REQ-TEST-166 — test doctor diagnostics.py TestDoctorReportsMissing test reports missing features dir

SpecWeave SHALL preserve the executable contract `tests/test_doctor_diagnostics.py::TestDoctorReportsMissing::test_reports_missing_features_dir`.

Verification:
- pytest: tests/test_doctor_diagnostics.py::TestDoctorReportsMissing::test_reports_missing_features_dir

### REQ-TEST-167 — test doctor diagnostics.py TestDoctorReportsMissing test reports missing tests dir

SpecWeave SHALL preserve the executable contract `tests/test_doctor_diagnostics.py::TestDoctorReportsMissing::test_reports_missing_tests_dir`.

Verification:
- pytest: tests/test_doctor_diagnostics.py::TestDoctorReportsMissing::test_reports_missing_tests_dir

### REQ-TEST-168 — test doctor diagnostics.py TestDoctorReportsMissing test no config warning

SpecWeave SHALL preserve the executable contract `tests/test_doctor_diagnostics.py::TestDoctorReportsMissing::test_no_config_warning`.

Verification:
- pytest: tests/test_doctor_diagnostics.py::TestDoctorReportsMissing::test_no_config_warning

### REQ-TEST-169 — test doctor diagnostics.py TestDoctorReportsDuplicateBddTags test detects duplicates

SpecWeave SHALL preserve the executable contract `tests/test_doctor_diagnostics.py::TestDoctorReportsDuplicateBddTags::test_detects_duplicates`.

Verification:
- pytest: tests/test_doctor_diagnostics.py::TestDoctorReportsDuplicateBddTags::test_detects_duplicates

### REQ-TEST-170 — test doctor diagnostics.py TestDoctorReportsDeprecatedPaths test detects deprecated

SpecWeave SHALL preserve the executable contract `tests/test_doctor_diagnostics.py::TestDoctorReportsDeprecatedPaths::test_detects_deprecated`.

Verification:
- pytest: tests/test_doctor_diagnostics.py::TestDoctorReportsDeprecatedPaths::test_detects_deprecated

### REQ-TEST-171 — test doctor diagnostics.py TestDoctorReportsDeprecatedPaths test warns for deprecated specs behavior layout

SpecWeave SHALL preserve the executable contract `tests/test_doctor_diagnostics.py::TestDoctorReportsDeprecatedPaths::test_warns_for_deprecated_specs_behavior_layout`.

Verification:
- pytest: tests/test_doctor_diagnostics.py::TestDoctorReportsDeprecatedPaths::test_warns_for_deprecated_specs_behavior_layout

### REQ-TEST-172 — test doctor diagnostics.py TestDoctorSpecifications test reports missing specifications directories

SpecWeave SHALL preserve the executable contract `tests/test_doctor_diagnostics.py::TestDoctorSpecifications::test_reports_missing_specifications_directories`.

Verification:
- pytest: tests/test_doctor_diagnostics.py::TestDoctorSpecifications::test_reports_missing_specifications_directories

### REQ-TEST-173 — test doctor diagnostics.py TestDoctorFix test fix creates missing dirs

SpecWeave SHALL preserve the executable contract `tests/test_doctor_diagnostics.py::TestDoctorFix::test_fix_creates_missing_dirs`.

Verification:
- pytest: tests/test_doctor_diagnostics.py::TestDoctorFix::test_fix_creates_missing_dirs

### REQ-TEST-174 — test doctor diagnostics.py TestDoctorFix test unsupported schema

SpecWeave SHALL preserve the executable contract `tests/test_doctor_diagnostics.py::TestDoctorFix::test_unsupported_schema`.

Verification:
- pytest: tests/test_doctor_diagnostics.py::TestDoctorFix::test_unsupported_schema

### REQ-TEST-175 — test exchange schemas.py test exchange schemas are json schema documents

SpecWeave SHALL preserve the executable contract `tests/test_exchange_schemas.py::test_exchange_schemas_are_json_schema_documents`.

Verification:
- pytest: tests/test_exchange_schemas.py::test_exchange_schemas_are_json_schema_documents

### REQ-TEST-176 — test exchange schemas.py test trace schema representative payload contract

SpecWeave SHALL preserve the executable contract `tests/test_exchange_schemas.py::test_trace_schema_representative_payload_contract`.

Verification:
- pytest: tests/test_exchange_schemas.py::test_trace_schema_representative_payload_contract

### REQ-TEST-177 — test exchange schemas.py test taskledger schema representative payload contract

SpecWeave SHALL preserve the executable contract `tests/test_exchange_schemas.py::test_taskledger_schema_representative_payload_contract`.

Verification:
- pytest: tests/test_exchange_schemas.py::test_taskledger_schema_representative_payload_contract

### REQ-TEST-178 — test exchange schemas.py test evidence schema representative payload contract

SpecWeave SHALL preserve the executable contract `tests/test_exchange_schemas.py::test_evidence_schema_representative_payload_contract`.

Verification:
- pytest: tests/test_exchange_schemas.py::test_evidence_schema_representative_payload_contract

### REQ-TEST-179 — test exchange schemas.py test archledger schema representative payload contract

SpecWeave SHALL preserve the executable contract `tests/test_exchange_schemas.py::test_archledger_schema_representative_payload_contract`.

Verification:
- pytest: tests/test_exchange_schemas.py::test_archledger_schema_representative_payload_contract

### REQ-TEST-180 — test gherkin lint.py test lint multiple feature lines

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_lint.py::test_lint_multiple_feature_lines`.

Verification:
- pytest: tests/test_gherkin_lint.py::test_lint_multiple_feature_lines

### REQ-TEST-181 — test gherkin lint.py test lint empty feature title

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_lint.py::test_lint_empty_feature_title`.

Verification:
- pytest: tests/test_gherkin_lint.py::test_lint_empty_feature_title

### REQ-TEST-182 — test gherkin lint.py test lint empty scenario title

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_lint.py::test_lint_empty_scenario_title`.

Verification:
- pytest: tests/test_gherkin_lint.py::test_lint_empty_scenario_title

### REQ-TEST-183 — test gherkin lint.py test lint missing given when then

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_lint.py::test_lint_missing_given_when_then`.

Verification:
- pytest: tests/test_gherkin_lint.py::test_lint_missing_given_when_then

### REQ-TEST-184 — test gherkin lint.py test lint empty rule

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_lint.py::test_lint_empty_rule`.

Verification:
- pytest: tests/test_gherkin_lint.py::test_lint_empty_rule

### REQ-TEST-185 — test gherkin lint.py test lint duplicate bdd tags

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_lint.py::test_lint_duplicate_bdd_tags`.

Verification:
- pytest: tests/test_gherkin_lint.py::test_lint_duplicate_bdd_tags

### REQ-TEST-186 — test gherkin lint.py test lint missing bdd tag

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_lint.py::test_lint_missing_bdd_tag`.

Verification:
- pytest: tests/test_gherkin_lint.py::test_lint_missing_bdd_tag

### REQ-TEST-187 — test gherkin lint.py test lint task tags discouraged

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_lint.py::test_lint_task_tags_discouraged`.

Verification:
- pytest: tests/test_gherkin_lint.py::test_lint_task_tags_discouraged

### REQ-TEST-188 — test gherkin lint.py test lint canonical path

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_lint.py::test_lint_canonical_path`.

Verification:
- pytest: tests/test_gherkin_lint.py::test_lint_canonical_path

### REQ-TEST-189 — test gherkin lint.py test lint area subdirectory

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_lint.py::test_lint_area_subdirectory`.

Verification:
- pytest: tests/test_gherkin_lint.py::test_lint_area_subdirectory

### REQ-TEST-190 — test gherkin lint.py test lint deprecated path

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_lint.py::test_lint_deprecated_path`.

Verification:
- pytest: tests/test_gherkin_lint.py::test_lint_deprecated_path

### REQ-TEST-191 — test gherkin lint.py test lint strict unsupported

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_lint.py::test_lint_strict_unsupported`.

Verification:
- pytest: tests/test_gherkin_lint.py::test_lint_strict_unsupported

### REQ-TEST-192 — test gherkin lint.py test lint rejects markdown feature file

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_lint.py::test_lint_rejects_markdown_feature_file`.

Verification:
- pytest: tests/test_gherkin_lint.py::test_lint_rejects_markdown_feature_file

### REQ-TEST-193 — test gherkin official.py TestParseClassicWithOfficial test parses simple feature

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_parses_simple_feature`.

Verification:
- pytest: tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_parses_simple_feature

### REQ-TEST-194 — test gherkin official.py TestParseClassicWithOfficial test parses rule and scenario tags

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_parses_rule_and_scenario_tags`.

Verification:
- pytest: tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_parses_rule_and_scenario_tags

### REQ-TEST-195 — test gherkin official.py TestParseClassicWithOfficial test rejects invalid gherkin

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_rejects_invalid_gherkin`.

Verification:
- pytest: tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_rejects_invalid_gherkin

### REQ-TEST-196 — test gherkin official.py TestParseClassicWithOfficial test accepts source path

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_accepts_source_path`.

Verification:
- pytest: tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_accepts_source_path

### REQ-TEST-197 — test gherkin official.py TestParseClassicWithOfficial test compile pickles smoke

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_compile_pickles_smoke`.

Verification:
- pytest: tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_compile_pickles_smoke

### REQ-TEST-198 — test gherkin official.py TestParseClassicWithOfficial test empty feature tags

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_empty_feature_tags`.

Verification:
- pytest: tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_empty_feature_tags

### REQ-TEST-199 — test gherkin official.py TestParseClassicWithOfficial test preserves description

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_preserves_description`.

Verification:
- pytest: tests/test_gherkin_official.py::TestParseClassicWithOfficial::test_preserves_description

### REQ-TEST-200 — test gherkin official.py TestValidateClassicWithOfficial test validates valid

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_official.py::TestValidateClassicWithOfficial::test_validates_valid`.

Verification:
- pytest: tests/test_gherkin_official.py::TestValidateClassicWithOfficial::test_validates_valid

### REQ-TEST-201 — test gherkin official.py TestValidateClassicWithOfficial test validates invalid

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_official.py::TestValidateClassicWithOfficial::test_validates_invalid`.

Verification:
- pytest: tests/test_gherkin_official.py::TestValidateClassicWithOfficial::test_validates_invalid

### REQ-TEST-202 — test gherkin official.py TestMissingOfficialDependency test import error message mentions extra

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_official.py::TestMissingOfficialDependency::test_import_error_message_mentions_extra`.

Verification:
- pytest: tests/test_gherkin_official.py::TestMissingOfficialDependency::test_import_error_message_mentions_extra

### REQ-TEST-203 — test gherkin parser.py test parse simple feature

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_parse_simple_feature`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parse_simple_feature

### REQ-TEST-204 — test gherkin parser.py test parse ignores comments and blanks

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_parse_ignores_comments_and_blanks`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parse_ignores_comments_and_blanks

### REQ-TEST-205 — test gherkin parser.py test parse no tags

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_parse_no_tags`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parse_no_tags

### REQ-TEST-206 — test gherkin parser.py test parse missing feature raises

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_parse_missing_feature_raises`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parse_missing_feature_raises

### REQ-TEST-207 — test gherkin parser.py test parse multiple scenarios

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_parse_multiple_scenarios`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parse_multiple_scenarios

### REQ-TEST-208 — test gherkin parser.py test parse and but keywords

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_parse_and_but_keywords`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parse_and_but_keywords

### REQ-TEST-209 — test gherkin parser.py test parse multi tag line

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_parse_multi_tag_line`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parse_multi_tag_line

### REQ-TEST-210 — test gherkin parser.py test parse mixed tag styles

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_parse_mixed_tag_styles`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parse_mixed_tag_styles

### REQ-TEST-211 — test gherkin parser.py test parse rule block

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_parse_rule_block`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parse_rule_block

### REQ-TEST-212 — test gherkin parser.py test parse multiple rules and scenarios

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_parse_multiple_rules_and_scenarios`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parse_multiple_rules_and_scenarios

### REQ-TEST-213 — test gherkin parser.py test scenario after rule belongs to rule

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_scenario_after_rule_belongs_to_rule`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_scenario_after_rule_belongs_to_rule

### REQ-TEST-214 — test gherkin parser.py test top level scenario before rule stays top level

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_top_level_scenario_before_rule_stays_top_level`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_top_level_scenario_before_rule_stays_top_level

### REQ-TEST-215 — test gherkin parser.py test parse feature description

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_parse_feature_description`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parse_feature_description

### REQ-TEST-216 — test gherkin parser.py test parse target example round trip

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_parse_target_example_round_trip`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parse_target_example_round_trip

### REQ-TEST-217 — test gherkin parser.py test parse example keyword and line numbers

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_parse_example_keyword_and_line_numbers`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parse_example_keyword_and_line_numbers

### REQ-TEST-218 — test gherkin parser.py test parser dispatch classic suffix

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_parser_dispatch_classic_suffix`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parser_dispatch_classic_suffix

### REQ-TEST-219 — test gherkin parser.py test parser rejects markdown feature path

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_parser_rejects_markdown_feature_path`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parser_rejects_markdown_feature_path

### REQ-TEST-220 — test gherkin parser.py test classic parser rejects markdown feature path

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_parser.py::test_classic_parser_rejects_markdown_feature_path`.

Verification:
- pytest: tests/test_gherkin_parser.py::test_classic_parser_rejects_markdown_feature_path

### REQ-TEST-221 — test gherkin validation.py TestValidateClassicValid test valid simple feature

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicValid::test_valid_simple_feature`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicValid::test_valid_simple_feature

### REQ-TEST-222 — test gherkin validation.py TestValidateClassicValid test valid with rule

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicValid::test_valid_with_rule`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicValid::test_valid_with_rule

### REQ-TEST-223 — test gherkin validation.py TestValidateClassicValid test valid with tags

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicValid::test_valid_with_tags`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicValid::test_valid_with_tags

### REQ-TEST-224 — test gherkin validation.py TestValidateClassicValid test valid with description

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicValid::test_valid_with_description`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicValid::test_valid_with_description

### REQ-TEST-225 — test gherkin validation.py TestValidateClassicValid test valid with and but

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicValid::test_valid_with_and_but`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicValid::test_valid_with_and_but

### REQ-TEST-226 — test gherkin validation.py TestValidateClassicValid test valid with example keyword

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicValid::test_valid_with_example_keyword`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicValid::test_valid_with_example_keyword

### REQ-TEST-227 — test gherkin validation.py TestValidateClassicValid test valid with comments

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicValid::test_valid_with_comments`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicValid::test_valid_with_comments

### REQ-TEST-228 — test gherkin validation.py TestValidateClassicUnsupported test rejects background

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_background`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_background

### REQ-TEST-229 — test gherkin validation.py TestValidateClassicUnsupported test rejects scenario outline

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_scenario_outline`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_scenario_outline

### REQ-TEST-230 — test gherkin validation.py TestValidateClassicUnsupported test rejects scenario template

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_scenario_template`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_scenario_template

### REQ-TEST-231 — test gherkin validation.py TestValidateClassicUnsupported test rejects examples keyword

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_examples_keyword`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_examples_keyword

### REQ-TEST-232 — test gherkin validation.py TestValidateClassicUnsupported test rejects data table

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_data_table`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_data_table

### REQ-TEST-233 — test gherkin validation.py TestValidateClassicUnsupported test rejects doc string

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_doc_string`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_doc_string

### REQ-TEST-234 — test gherkin validation.py TestValidateClassicUnsupported test rejects wildcard step

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_wildcard_step`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_wildcard_step

### REQ-TEST-235 — test gherkin validation.py TestValidateClassicUnsupported test rejects junk line in scenario after steps

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_junk_line_in_scenario_after_steps`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_junk_line_in_scenario_after_steps

### REQ-TEST-236 — test gherkin validation.py TestValidateClassicUnsupported test rejects multiple features

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_multiple_features`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_multiple_features

### REQ-TEST-237 — test gherkin validation.py TestValidateClassicUnsupported test rejects missing feature

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_missing_feature`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_rejects_missing_feature

### REQ-TEST-238 — test gherkin validation.py TestValidateClassicUnsupported test includes source path in error

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_includes_source_path_in_error`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateClassicUnsupported::test_includes_source_path_in_error

### REQ-TEST-239 — test gherkin validation.py TestValidateMarkdownUnsupported test rejects markdown features

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_validation.py::TestValidateMarkdownUnsupported::test_rejects_markdown_features`.

Verification:
- pytest: tests/test_gherkin_validation.py::TestValidateMarkdownUnsupported::test_rejects_markdown_features

### REQ-TEST-240 — test gherkin writer.py test writes tags feature scenario steps

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_writer.py::test_writes_tags_feature_scenario_steps`.

Verification:
- pytest: tests/test_gherkin_writer.py::test_writes_tags_feature_scenario_steps

### REQ-TEST-241 — test gherkin writer.py test scenario without tags

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_writer.py::test_scenario_without_tags`.

Verification:
- pytest: tests/test_gherkin_writer.py::test_scenario_without_tags

### REQ-TEST-242 — test gherkin writer.py test multiple scenarios

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_writer.py::test_multiple_scenarios`.

Verification:
- pytest: tests/test_gherkin_writer.py::test_multiple_scenarios

### REQ-TEST-243 — test gherkin writer.py test multi tag scenario on one line

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_writer.py::test_multi_tag_scenario_on_one_line`.

Verification:
- pytest: tests/test_gherkin_writer.py::test_multi_tag_scenario_on_one_line

### REQ-TEST-244 — test gherkin writer.py test writes rule block

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_writer.py::test_writes_rule_block`.

Verification:
- pytest: tests/test_gherkin_writer.py::test_writes_rule_block

### REQ-TEST-245 — test gherkin writer.py test rule round trips

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_writer.py::test_rule_round_trips`.

Verification:
- pytest: tests/test_gherkin_writer.py::test_rule_round_trips

### REQ-TEST-246 — test gherkin writer.py test feature description rendered

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_writer.py::test_feature_description_rendered`.

Verification:
- pytest: tests/test_gherkin_writer.py::test_feature_description_rendered

### REQ-TEST-247 — test gherkin writer.py TestWriterRejectsUnsupportedKeywords test rejects scenario outline in classic

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_writer.py::TestWriterRejectsUnsupportedKeywords::test_rejects_scenario_outline_in_classic`.

Verification:
- pytest: tests/test_gherkin_writer.py::TestWriterRejectsUnsupportedKeywords::test_rejects_scenario_outline_in_classic

### REQ-TEST-248 — test gherkin writer.py TestWriterRejectsUnsupportedKeywords test rejects scenario template in classic

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_writer.py::TestWriterRejectsUnsupportedKeywords::test_rejects_scenario_template_in_classic`.

Verification:
- pytest: tests/test_gherkin_writer.py::TestWriterRejectsUnsupportedKeywords::test_rejects_scenario_template_in_classic

### REQ-TEST-249 — test gherkin writer.py TestWriterRejectsUnsupportedKeywords test accepts example keyword

SpecWeave SHALL preserve the executable contract `tests/test_gherkin_writer.py::TestWriterRejectsUnsupportedKeywords::test_accepts_example_keyword`.

Verification:
- pytest: tests/test_gherkin_writer.py::TestWriterRejectsUnsupportedKeywords::test_accepts_example_keyword

### REQ-TEST-250 — test init initialization.py TestInitDefault test creates default config and layout

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestInitDefault::test_creates_default_config_and_layout`.

Verification:
- pytest: tests/test_init_initialization.py::TestInitDefault::test_creates_default_config_and_layout

### REQ-TEST-251 — test init initialization.py TestInitDefault test creates behaviour paths

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestInitDefault::test_creates_behaviour_paths`.

Verification:
- pytest: tests/test_init_initialization.py::TestInitDefault::test_creates_behaviour_paths

### REQ-TEST-252 — test init initialization.py TestInitBritishSpelling test creates behaviour layout

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestInitBritishSpelling::test_creates_behaviour_layout`.

Verification:
- pytest: tests/test_init_initialization.py::TestInitBritishSpelling::test_creates_behaviour_layout

### REQ-TEST-253 — test init initialization.py TestInitBritishSpelling test creates legacy behavior layout when explicit

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestInitBritishSpelling::test_creates_legacy_behavior_layout_when_explicit`.

Verification:
- pytest: tests/test_init_initialization.py::TestInitBritishSpelling::test_creates_legacy_behavior_layout_when_explicit

### REQ-TEST-254 — test init initialization.py TestInitModes test mode specifications creates specifications layout

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestInitModes::test_mode_specifications_creates_specifications_layout`.

Verification:
- pytest: tests/test_init_initialization.py::TestInitModes::test_mode_specifications_creates_specifications_layout

### REQ-TEST-255 — test init initialization.py TestInitModes test mode both creates both layouts

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestInitModes::test_mode_both_creates_both_layouts`.

Verification:
- pytest: tests/test_init_initialization.py::TestInitModes::test_mode_both_creates_both_layouts

### REQ-TEST-256 — test init initialization.py TestInitModes test upgrade layout migrates only when explicit

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestInitModes::test_upgrade_layout_migrates_only_when_explicit`.

Verification:
- pytest: tests/test_init_initialization.py::TestInitModes::test_upgrade_layout_migrates_only_when_explicit

### REQ-TEST-257 — test init initialization.py TestInitCompatibility test hidden config path still works when explicit

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestInitCompatibility::test_hidden_config_path_still_works_when_explicit`.

Verification:
- pytest: tests/test_init_initialization.py::TestInitCompatibility::test_hidden_config_path_still_works_when_explicit

### REQ-TEST-258 — test init initialization.py TestInitIdempotency test does not overwrite existing config

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestInitIdempotency::test_does_not_overwrite_existing_config`.

Verification:
- pytest: tests/test_init_initialization.py::TestInitIdempotency::test_does_not_overwrite_existing_config

### REQ-TEST-259 — test init initialization.py TestInitIdempotency test does not overwrite non specweave readme

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestInitIdempotency::test_does_not_overwrite_non_specweave_readme`.

Verification:
- pytest: tests/test_init_initialization.py::TestInitIdempotency::test_does_not_overwrite_non_specweave_readme

### REQ-TEST-260 — test init initialization.py TestInitIdempotency test reports existing directories

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestInitIdempotency::test_reports_existing_directories`.

Verification:
- pytest: tests/test_init_initialization.py::TestInitIdempotency::test_reports_existing_directories

### REQ-TEST-261 — test init initialization.py TestInitForce test force overwrites generated config only

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestInitForce::test_force_overwrites_generated_config_only`.

Verification:
- pytest: tests/test_init_initialization.py::TestInitForce::test_force_overwrites_generated_config_only

### REQ-TEST-262 — test init initialization.py TestInitDryRun test writes nothing

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestInitDryRun::test_writes_nothing`.

Verification:
- pytest: tests/test_init_initialization.py::TestInitDryRun::test_writes_nothing

### REQ-TEST-263 — test init initialization.py TestInitJsonShape test json shape

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestInitJsonShape::test_json_shape`.

Verification:
- pytest: tests/test_init_initialization.py::TestInitJsonShape::test_json_shape

### REQ-TEST-264 — test init initialization.py TestReadmeIsSpecweaveManaged test nonexistent

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestReadmeIsSpecweaveManaged::test_nonexistent`.

Verification:
- pytest: tests/test_init_initialization.py::TestReadmeIsSpecweaveManaged::test_nonexistent

### REQ-TEST-265 — test init initialization.py TestReadmeIsSpecweaveManaged test non managed content

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestReadmeIsSpecweaveManaged::test_non_managed_content`.

Verification:
- pytest: tests/test_init_initialization.py::TestReadmeIsSpecweaveManaged::test_non_managed_content

### REQ-TEST-266 — test init initialization.py TestReadmeIsSpecweaveManaged test managed content

SpecWeave SHALL preserve the executable contract `tests/test_init_initialization.py::TestReadmeIsSpecweaveManaged::test_managed_content`.

Verification:
- pytest: tests/test_init_initialization.py::TestReadmeIsSpecweaveManaged::test_managed_content

### REQ-TEST-267 — test integrations archledger.py test render candidate markdown

SpecWeave SHALL preserve the executable contract `tests/test_integrations_archledger.py::test_render_candidate_markdown`.

Verification:
- pytest: tests/test_integrations_archledger.py::test_render_candidate_markdown

### REQ-TEST-268 — test integrations archledger.py test render candidate from parsed feature

SpecWeave SHALL preserve the executable contract `tests/test_integrations_archledger.py::test_render_candidate_from_parsed_feature`.

Verification:
- pytest: tests/test_integrations_archledger.py::test_render_candidate_from_parsed_feature

### REQ-TEST-269 — test integrations archledger.py test unknown bdd id raises

SpecWeave SHALL preserve the executable contract `tests/test_integrations_archledger.py::test_unknown_bdd_id_raises`.

Verification:
- pytest: tests/test_integrations_archledger.py::test_unknown_bdd_id_raises

### REQ-TEST-270 — test integrations archledger.py test write candidate file

SpecWeave SHALL preserve the executable contract `tests/test_integrations_archledger.py::test_write_candidate_file`.

Verification:
- pytest: tests/test_integrations_archledger.py::test_write_candidate_file

### REQ-TEST-271 — test integrations archledger.py test render requirement candidate markdown

SpecWeave SHALL preserve the executable contract `tests/test_integrations_archledger.py::test_render_requirement_candidate_markdown`.

Verification:
- pytest: tests/test_integrations_archledger.py::test_render_requirement_candidate_markdown

### REQ-TEST-272 — test integrations taskledger.py test load rich shape

SpecWeave SHALL preserve the executable contract `tests/test_integrations_taskledger.py::test_load_rich_shape`.

Verification:
- pytest: tests/test_integrations_taskledger.py::test_load_rich_shape

### REQ-TEST-273 — test integrations taskledger.py test load legacy mvp shape

SpecWeave SHALL preserve the executable contract `tests/test_integrations_taskledger.py::test_load_legacy_mvp_shape`.

Verification:
- pytest: tests/test_integrations_taskledger.py::test_load_legacy_mvp_shape

### REQ-TEST-274 — test integrations taskledger.py test task id from report

SpecWeave SHALL preserve the executable contract `tests/test_integrations_taskledger.py::test_task_id_from_report`.

Verification:
- pytest: tests/test_integrations_taskledger.py::test_task_id_from_report

### REQ-TEST-275 — test integrations taskledger.py test task id from report missing is empty

SpecWeave SHALL preserve the executable contract `tests/test_integrations_taskledger.py::test_task_id_from_report_missing_is_empty`.

Verification:
- pytest: tests/test_integrations_taskledger.py::test_task_id_from_report_missing_is_empty

### REQ-TEST-276 — test integrations taskledger.py test write evidence round trip

SpecWeave SHALL preserve the executable contract `tests/test_integrations_taskledger.py::test_write_evidence_round_trip`.

Verification:
- pytest: tests/test_integrations_taskledger.py::test_write_evidence_round_trip

### REQ-TEST-277 — test integrations taskledger.py test write evidence explicit task id

SpecWeave SHALL preserve the executable contract `tests/test_integrations_taskledger.py::test_write_evidence_explicit_task_id`.

Verification:
- pytest: tests/test_integrations_taskledger.py::test_write_evidence_explicit_task_id

### REQ-TEST-278 — test integrations taskledger.py test no taskledger import required

SpecWeave SHALL preserve the executable contract `tests/test_integrations_taskledger.py::test_no_taskledger_import_required`.

Verification:
- pytest: tests/test_integrations_taskledger.py::test_no_taskledger_import_required

### REQ-TEST-279 — test integrations taskledger.py test import taskledger to canonical behavior feature

SpecWeave SHALL preserve the executable contract `tests/test_integrations_taskledger.py::test_import_taskledger_to_canonical_behavior_feature`.

Verification:
- pytest: tests/test_integrations_taskledger.py::test_import_taskledger_to_canonical_behavior_feature

### REQ-TEST-280 — test integrations taskledger.py test import taskledger writes classic feature

SpecWeave SHALL preserve the executable contract `tests/test_integrations_taskledger.py::test_import_taskledger_writes_classic_feature`.

Verification:
- pytest: tests/test_integrations_taskledger.py::test_import_taskledger_writes_classic_feature

### REQ-TEST-281 — test integrations taskledger.py test taskledger draft ac mapping

SpecWeave SHALL preserve the executable contract `tests/test_integrations_taskledger.py::test_taskledger_draft_ac_mapping`.

Verification:
- pytest: tests/test_integrations_taskledger.py::test_taskledger_draft_ac_mapping

### REQ-TEST-282 — test plan.py TestCreatePlan test creates plan from feature

SpecWeave SHALL preserve the executable contract `tests/test_plan.py::TestCreatePlan::test_creates_plan_from_feature`.

Verification:
- pytest: tests/test_plan.py::TestCreatePlan::test_creates_plan_from_feature

### REQ-TEST-283 — test plan.py TestCreatePlan test plan includes scenario steps

SpecWeave SHALL preserve the executable contract `tests/test_plan.py::TestCreatePlan::test_plan_includes_scenario_steps`.

Verification:
- pytest: tests/test_plan.py::TestCreatePlan::test_plan_includes_scenario_steps

### REQ-TEST-284 — test plan.py TestCreatePlan test plan includes validation commands

SpecWeave SHALL preserve the executable contract `tests/test_plan.py::TestCreatePlan::test_plan_includes_validation_commands`.

Verification:
- pytest: tests/test_plan.py::TestCreatePlan::test_plan_includes_validation_commands

### REQ-TEST-285 — test python ast reader.py test extract test functions

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_extract_test_functions`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_extract_test_functions

### REQ-TEST-286 — test python ast reader.py test extract ignores non test functions

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_extract_ignores_non_test_functions`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_extract_ignores_non_test_functions

### REQ-TEST-287 — test python ast reader.py test describe assert equals

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_describe_assert_equals`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_describe_assert_equals

### REQ-TEST-288 — test python ast reader.py test describe assert is none

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_describe_assert_is_none`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_describe_assert_is_none

### REQ-TEST-289 — test python ast reader.py test describe assert truthy

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_describe_assert_truthy`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_describe_assert_truthy

### REQ-TEST-290 — test python ast reader.py test describe assert call

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_describe_assert_call`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_describe_assert_call

### REQ-TEST-291 — test python ast reader.py test discover specweave marker mapping

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_discover_specweave_marker_mapping`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_discover_specweave_marker_mapping

### REQ-TEST-292 — test python ast reader.py test discover specweave comment mapping

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_discover_specweave_comment_mapping`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_discover_specweave_comment_mapping

### REQ-TEST-293 — test python ast reader.py test discover specweave short comment mapping

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_discover_specweave_short_comment_mapping`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_discover_specweave_short_comment_mapping

### REQ-TEST-294 — test python ast reader.py test discover specweave block comment mapping

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_discover_specweave_block_comment_mapping`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_discover_specweave_block_comment_mapping

### REQ-TEST-295 — test python ast reader.py test discover specweave requirement comment mapping

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_discover_specweave_requirement_comment_mapping`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_discover_specweave_requirement_comment_mapping

### REQ-TEST-296 — test python ast reader.py test discover specweave marker requirement mapping

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_discover_specweave_marker_requirement_mapping`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_discover_specweave_marker_requirement_mapping

### REQ-TEST-297 — test python ast reader.py test one test can map to bdd and sdd

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_one_test_can_map_to_bdd_and_sdd`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_one_test_can_map_to_bdd_and_sdd

### REQ-TEST-298 — test python ast reader.py test docstring mapping accepts feature md

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_docstring_mapping_accepts_feature_md`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_docstring_mapping_accepts_feature_md

### REQ-TEST-299 — test python ast reader.py test discover pytest tests lists all test functions

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_discover_pytest_tests_lists_all_test_functions`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_discover_pytest_tests_lists_all_test_functions

### REQ-TEST-300 — test python ast reader.py test collect pytest tests keeps unmapped tests

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_collect_pytest_tests_keeps_unmapped_tests`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_collect_pytest_tests_keeps_unmapped_tests

### REQ-TEST-301 — test python ast reader.py test discover specweave tests qualifies class mapping nodeids

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_discover_specweave_tests_qualifies_class_mapping_nodeids`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_discover_specweave_tests_qualifies_class_mapping_nodeids

### REQ-TEST-302 — test python ast reader.py test pytest discovery ignores non collectible class nesting

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_pytest_discovery_ignores_non_collectible_class_nesting`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_pytest_discovery_ignores_non_collectible_class_nesting

### REQ-TEST-303 — test python ast reader.py test discover pytest tests preserves intentional unmapped waiver

SpecWeave SHALL preserve the executable contract `tests/test_python_ast_reader.py::test_discover_pytest_tests_preserves_intentional_unmapped_waiver`.

Verification:
- pytest: tests/test_python_ast_reader.py::test_discover_pytest_tests_preserves_intentional_unmapped_waiver

### REQ-TEST-304 — test reports fail closed.py test criterion requires passing native result

SpecWeave SHALL preserve the executable contract `tests/test_reports_fail_closed.py::test_criterion_requires_passing_native_result`.

Verification:
- pytest: tests/test_reports_fail_closed.py::test_criterion_requires_passing_native_result

### REQ-TEST-305 — test reports fail closed.py test criterion fails when sibling undefined

SpecWeave SHALL preserve the executable contract `tests/test_reports_fail_closed.py::test_criterion_fails_when_sibling_undefined`.

Verification:
- pytest: tests/test_reports_fail_closed.py::test_criterion_fails_when_sibling_undefined

### REQ-TEST-306 — test reports fail closed.py test missing expected coverage fails

SpecWeave SHALL preserve the executable contract `tests/test_reports_fail_closed.py::test_missing_expected_coverage_fails`.

Verification:
- pytest: tests/test_reports_fail_closed.py::test_missing_expected_coverage_fails

### REQ-TEST-307 — test reports fail closed.py test scenario without bdd tag is unlinked

SpecWeave SHALL preserve the executable contract `tests/test_reports_fail_closed.py::test_scenario_without_bdd_tag_is_unlinked`.

Verification:
- pytest: tests/test_reports_fail_closed.py::test_scenario_without_bdd_tag_is_unlinked

### REQ-TEST-308 — test reports fail closed.py test title only never drives matching

SpecWeave SHALL preserve the executable contract `tests/test_reports_fail_closed.py::test_title_only_never_drives_matching`.

Verification:
- pytest: tests/test_reports_fail_closed.py::test_title_only_never_drives_matching

### REQ-TEST-309 — test reports fail closed.py test evidence records command source and paths

SpecWeave SHALL preserve the executable contract `tests/test_reports_fail_closed.py::test_evidence_records_command_source_and_paths`.

Verification:
- pytest: tests/test_reports_fail_closed.py::test_evidence_records_command_source_and_paths

### REQ-TEST-310 — test reports fail closed.py test passing report only when all gates pass

SpecWeave SHALL preserve the executable contract `tests/test_reports_fail_closed.py::test_passing_report_only_when_all_gates_pass`.

Verification:
- pytest: tests/test_reports_fail_closed.py::test_passing_report_only_when_all_gates_pass

### REQ-TEST-311 — test reports fail closed.py test failed scenario fails criterion

SpecWeave SHALL preserve the executable contract `tests/test_reports_fail_closed.py::test_failed_scenario_fails_criterion`.

Verification:
- pytest: tests/test_reports_fail_closed.py::test_failed_scenario_fails_criterion

### REQ-TEST-312 — test reports fail closed.py test skipped scenario fails criterion

SpecWeave SHALL preserve the executable contract `tests/test_reports_fail_closed.py::test_skipped_scenario_fails_criterion`.

Verification:
- pytest: tests/test_reports_fail_closed.py::test_skipped_scenario_fails_criterion

### REQ-TEST-313 — test reports fail closed.py test pending scenario fails criterion

SpecWeave SHALL preserve the executable contract `tests/test_reports_fail_closed.py::test_pending_scenario_fails_criterion`.

Verification:
- pytest: tests/test_reports_fail_closed.py::test_pending_scenario_fails_criterion

### REQ-TEST-314 — test reports fail closed.py test ambiguous scenario fails criterion

SpecWeave SHALL preserve the executable contract `tests/test_reports_fail_closed.py::test_ambiguous_scenario_fails_criterion`.

Verification:
- pytest: tests/test_reports_fail_closed.py::test_ambiguous_scenario_fails_criterion

### REQ-TEST-315 — test reports fail closed.py test exit code not used as evidence

SpecWeave SHALL preserve the executable contract `tests/test_reports_fail_closed.py::test_exit_code_not_used_as_evidence`.

Verification:
- pytest: tests/test_reports_fail_closed.py::test_exit_code_not_used_as_evidence

### REQ-TEST-316 — test reports mapping.py test extract ids partitions by prefix

SpecWeave SHALL preserve the executable contract `tests/test_reports_mapping.py::test_extract_ids_partitions_by_prefix`.

Verification:
- pytest: tests/test_reports_mapping.py::test_extract_ids_partitions_by_prefix

### REQ-TEST-317 — test reports mapping.py test summarize passes when linked scenario passed

SpecWeave SHALL preserve the executable contract `tests/test_reports_mapping.py::test_summarize_passes_when_linked_scenario_passed`.

Verification:
- pytest: tests/test_reports_mapping.py::test_summarize_passes_when_linked_scenario_passed

### REQ-TEST-318 — test reports mapping.py test summarize fails when linked scenario failed

SpecWeave SHALL preserve the executable contract `tests/test_reports_mapping.py::test_summarize_fails_when_linked_scenario_failed`.

Verification:
- pytest: tests/test_reports_mapping.py::test_summarize_fails_when_linked_scenario_failed

### REQ-TEST-319 — test reports mapping.py test summarize fails on skipped unless allowed

SpecWeave SHALL preserve the executable contract `tests/test_reports_mapping.py::test_summarize_fails_on_skipped_unless_allowed`.

Verification:
- pytest: tests/test_reports_mapping.py::test_summarize_fails_on_skipped_unless_allowed

### REQ-TEST-320 — test reports mapping.py test summarize fails on undefined and pending

SpecWeave SHALL preserve the executable contract `tests/test_reports_mapping.py::test_summarize_fails_on_undefined_and_pending`.

Verification:
- pytest: tests/test_reports_mapping.py::test_summarize_fails_on_undefined_and_pending

### REQ-TEST-321 — test reports mapping.py test unlinked scenarios are ignored

SpecWeave SHALL preserve the executable contract `tests/test_reports_mapping.py::test_unlinked_scenarios_are_ignored`.

Verification:
- pytest: tests/test_reports_mapping.py::test_unlinked_scenarios_are_ignored

### REQ-TEST-322 — test reports mapping.py test matching never uses title

SpecWeave SHALL preserve the executable contract `tests/test_reports_mapping.py::test_matching_never_uses_title`.

Verification:
- pytest: tests/test_reports_mapping.py::test_matching_never_uses_title

### REQ-TEST-323 — test reports mapping.py test require expected coverage missing fails

SpecWeave SHALL preserve the executable contract `tests/test_reports_mapping.py::test_require_expected_coverage_missing_fails`.

Verification:
- pytest: tests/test_reports_mapping.py::test_require_expected_coverage_missing_fails

### REQ-TEST-324 — test reports mapping.py test require expected coverage all present passes

SpecWeave SHALL preserve the executable contract `tests/test_reports_mapping.py::test_require_expected_coverage_all_present_passes`.

Verification:
- pytest: tests/test_reports_mapping.py::test_require_expected_coverage_all_present_passes

### REQ-TEST-325 — test reports mapping.py test require expected coverage only failing counts as missing

SpecWeave SHALL preserve the executable contract `tests/test_reports_mapping.py::test_require_expected_coverage_only_failing_counts_as_missing`.

Verification:
- pytest: tests/test_reports_mapping.py::test_require_expected_coverage_only_failing_counts_as_missing

### REQ-TEST-326 — test reports mapping.py test empty expected is passing

SpecWeave SHALL preserve the executable contract `tests/test_reports_mapping.py::test_empty_expected_is_passing`.

Verification:
- pytest: tests/test_reports_mapping.py::test_empty_expected_is_passing

### REQ-TEST-327 — test reports mapping.py test fail closed no passing scenario

SpecWeave SHALL preserve the executable contract `tests/test_reports_mapping.py::test_fail_closed_no_passing_scenario`.

Verification:
- pytest: tests/test_reports_mapping.py::test_fail_closed_no_passing_scenario

### REQ-TEST-328 — test reports mapping.py test extract ac ids from tags

SpecWeave SHALL preserve the executable contract `tests/test_reports_mapping.py::test_extract_ac_ids_from_tags`.

Verification:
- pytest: tests/test_reports_mapping.py::test_extract_ac_ids_from_tags

### REQ-TEST-329 — test reports normalization.py test normalize junit xml

SpecWeave SHALL preserve the executable contract `tests/test_reports_normalization.py::test_normalize_junit_xml`.

Verification:
- pytest: tests/test_reports_normalization.py::test_normalize_junit_xml

### REQ-TEST-330 — test reports normalization.py test normalize cucumber json

SpecWeave SHALL preserve the executable contract `tests/test_reports_normalization.py::test_normalize_cucumber_json`.

Verification:
- pytest: tests/test_reports_normalization.py::test_normalize_cucumber_json

### REQ-TEST-331 — test reports normalization.py test normalize unsupported format

SpecWeave SHALL preserve the executable contract `tests/test_reports_normalization.py::test_normalize_unsupported_format`.

Verification:
- pytest: tests/test_reports_normalization.py::test_normalize_unsupported_format

### REQ-TEST-332 — test reports normalization.py test normalize all passed

SpecWeave SHALL preserve the executable contract `tests/test_reports_normalization.py::test_normalize_all_passed`.

Verification:
- pytest: tests/test_reports_normalization.py::test_normalize_all_passed

### REQ-TEST-333 — test reports normalization.py test normalize any failed

SpecWeave SHALL preserve the executable contract `tests/test_reports_normalization.py::test_normalize_any_failed`.

Verification:
- pytest: tests/test_reports_normalization.py::test_normalize_any_failed

### REQ-TEST-334 — test reports normalization.py test normalize skipped fails by default

SpecWeave SHALL preserve the executable contract `tests/test_reports_normalization.py::test_normalize_skipped_fails_by_default`.

Verification:
- pytest: tests/test_reports_normalization.py::test_normalize_skipped_fails_by_default

### REQ-TEST-335 — test reports normalization.py test normalize allow skipped

SpecWeave SHALL preserve the executable contract `tests/test_reports_normalization.py::test_normalize_allow_skipped`.

Verification:
- pytest: tests/test_reports_normalization.py::test_normalize_allow_skipped

### REQ-TEST-336 — test reports normalization.py test normalize missing ac coverage

SpecWeave SHALL preserve the executable contract `tests/test_reports_normalization.py::test_normalize_missing_ac_coverage`.

Verification:
- pytest: tests/test_reports_normalization.py::test_normalize_missing_ac_coverage

### REQ-TEST-337 — test reports normalization.py test normalize ac covered

SpecWeave SHALL preserve the executable contract `tests/test_reports_normalization.py::test_normalize_ac_covered`.

Verification:
- pytest: tests/test_reports_normalization.py::test_normalize_ac_covered

### REQ-TEST-338 — test reports normalization.py test normalize evidence json

SpecWeave SHALL preserve the executable contract `tests/test_reports_normalization.py::test_normalize_evidence_json`.

Verification:
- pytest: tests/test_reports_normalization.py::test_normalize_evidence_json

### REQ-TEST-339 — test reports parsers.py test parse junit pass fail skip

SpecWeave SHALL preserve the executable contract `tests/test_reports_parsers.py::test_parse_junit_pass_fail_skip`.

Verification:
- pytest: tests/test_reports_parsers.py::test_parse_junit_pass_fail_skip

### REQ-TEST-340 — test reports parsers.py test junit error counts as failed

SpecWeave SHALL preserve the executable contract `tests/test_reports_parsers.py::test_junit_error_counts_as_failed`.

Verification:
- pytest: tests/test_reports_parsers.py::test_junit_error_counts_as_failed

### REQ-TEST-341 — test reports parsers.py test junit tags from properties

SpecWeave SHALL preserve the executable contract `tests/test_reports_parsers.py::test_junit_tags_from_properties`.

Verification:
- pytest: tests/test_reports_parsers.py::test_junit_tags_from_properties

### REQ-TEST-342 — test reports parsers.py test normalize junit skipped fails closed

SpecWeave SHALL preserve the executable contract `tests/test_reports_parsers.py::test_normalize_junit_skipped_fails_closed`.

Verification:
- pytest: tests/test_reports_parsers.py::test_normalize_junit_skipped_fails_closed

### REQ-TEST-343 — test reports parsers.py test normalize junit all passed

SpecWeave SHALL preserve the executable contract `tests/test_reports_parsers.py::test_normalize_junit_all_passed`.

Verification:
- pytest: tests/test_reports_parsers.py::test_normalize_junit_all_passed

### REQ-TEST-344 — test reports parsers.py test parse pytest junit case nodeid and file

SpecWeave SHALL preserve the executable contract `tests/test_reports_parsers.py::test_parse_pytest_junit_case_nodeid_and_file`.

Verification:
- pytest: tests/test_reports_parsers.py::test_parse_pytest_junit_case_nodeid_and_file

### REQ-TEST-345 — test reports parsers.py test parse junit preserves nodeid and test file

SpecWeave SHALL preserve the executable contract `tests/test_reports_parsers.py::test_parse_junit_preserves_nodeid_and_test_file`.

Verification:
- pytest: tests/test_reports_parsers.py::test_parse_junit_preserves_nodeid_and_test_file

### REQ-TEST-346 — test reports parsers.py test cucumber json passing scenario

SpecWeave SHALL preserve the executable contract `tests/test_reports_parsers.py::test_cucumber_json_passing_scenario`.

Verification:
- pytest: tests/test_reports_parsers.py::test_cucumber_json_passing_scenario

### REQ-TEST-347 — test reports parsers.py test skipped fails closed by default

SpecWeave SHALL preserve the executable contract `tests/test_reports_parsers.py::test_skipped_fails_closed_by_default`.

Verification:
- pytest: tests/test_reports_parsers.py::test_skipped_fails_closed_by_default

### REQ-TEST-348 — test reports parsers.py test allow skipped does not fail

SpecWeave SHALL preserve the executable contract `tests/test_reports_parsers.py::test_allow_skipped_does_not_fail`.

Verification:
- pytest: tests/test_reports_parsers.py::test_allow_skipped_does_not_fail

### REQ-TEST-349 — test reports parsers.py test failed step fails scenario and report

SpecWeave SHALL preserve the executable contract `tests/test_reports_parsers.py::test_failed_step_fails_scenario_and_report`.

Verification:
- pytest: tests/test_reports_parsers.py::test_failed_step_fails_scenario_and_report

### REQ-TEST-350 — test reports parsers.py test behear string tags and inline status

SpecWeave SHALL preserve the executable contract `tests/test_reports_parsers.py::test_behear_string_tags_and_inline_status`.

Verification:
- pytest: tests/test_reports_parsers.py::test_behear_string_tags_and_inline_status

### REQ-TEST-351 — test reports parsers.py test normalized dict shape

SpecWeave SHALL preserve the executable contract `tests/test_reports_parsers.py::test_normalized_dict_shape`.

Verification:
- pytest: tests/test_reports_parsers.py::test_normalized_dict_shape

### REQ-TEST-352 — test reports parsers.py test unsupported format raises

SpecWeave SHALL preserve the executable contract `tests/test_reports_parsers.py::test_unsupported_format_raises`.

Verification:
- pytest: tests/test_reports_parsers.py::test_unsupported_format_raises

### REQ-TEST-353 — test reports parsers.py test junit parse duration

SpecWeave SHALL preserve the executable contract `tests/test_reports_parsers.py::test_junit_parse_duration`.

Verification:
- pytest: tests/test_reports_parsers.py::test_junit_parse_duration

### REQ-TEST-354 — test review spec review.py TestReviewReportsMissingBindings test no features

SpecWeave SHALL preserve the executable contract `tests/test_review_spec_review.py::TestReviewReportsMissingBindings::test_no_features`.

Verification:
- pytest: tests/test_review_spec_review.py::TestReviewReportsMissingBindings::test_no_features

### REQ-TEST-355 — test review spec review.py TestReviewReportsMissingBindings test feature with no test

SpecWeave SHALL preserve the executable contract `tests/test_review_spec_review.py::TestReviewReportsMissingBindings::test_feature_with_no_test`.

Verification:
- pytest: tests/test_review_spec_review.py::TestReviewReportsMissingBindings::test_feature_with_no_test

### REQ-TEST-356 — test review spec review.py TestReviewReportsNeedsReview test needs review flagged

SpecWeave SHALL preserve the executable contract `tests/test_review_spec_review.py::TestReviewReportsNeedsReview::test_needs_review_flagged`.

Verification:
- pytest: tests/test_review_spec_review.py::TestReviewReportsNeedsReview::test_needs_review_flagged

### REQ-TEST-357 — test review spec review.py TestReviewJsonShape test json shape

SpecWeave SHALL preserve the executable contract `tests/test_review_spec_review.py::TestReviewJsonShape::test_json_shape`.

Verification:
- pytest: tests/test_review_spec_review.py::TestReviewJsonShape::test_json_shape

### REQ-TEST-358 — test review spec review.py TestReviewAggregatesCoverage test stale mapping causes failed review

SpecWeave SHALL preserve the executable contract `tests/test_review_spec_review.py::TestReviewAggregatesCoverage::test_stale_mapping_causes_failed_review`.

Verification:
- pytest: tests/test_review_spec_review.py::TestReviewAggregatesCoverage::test_stale_mapping_causes_failed_review

### REQ-TEST-359 — test review spec review.py TestReviewAggregatesCoverage test forbidden pytest bdd

SpecWeave SHALL preserve the executable contract `tests/test_review_spec_review.py::TestReviewAggregatesCoverage::test_forbidden_pytest_bdd`.

Verification:
- pytest: tests/test_review_spec_review.py::TestReviewAggregatesCoverage::test_forbidden_pytest_bdd

### REQ-TEST-360 — test review spec review.py TestReviewAggregatesCoverage test lint findings

SpecWeave SHALL preserve the executable contract `tests/test_review_spec_review.py::TestReviewAggregatesCoverage::test_lint_findings`.

Verification:
- pytest: tests/test_review_spec_review.py::TestReviewAggregatesCoverage::test_lint_findings

### REQ-TEST-361 — test review spec review.py test review summary includes pytest reverse counts

SpecWeave SHALL preserve the executable contract `tests/test_review_spec_review.py::test_review_summary_includes_pytest_reverse_counts`.

Verification:
- pytest: tests/test_review_spec_review.py::test_review_summary_includes_pytest_reverse_counts

### REQ-TEST-362 — test review spec review.py test review missing binding message does not duplicate scenario id

SpecWeave SHALL preserve the executable contract `tests/test_review_spec_review.py::test_review_missing_binding_message_does_not_duplicate_scenario_id`.

Verification:
- pytest: tests/test_review_spec_review.py::test_review_missing_binding_message_does_not_duplicate_scenario_id

### REQ-TEST-363 — test runner command.py test run success

SpecWeave SHALL preserve the executable contract `tests/test_runner_command.py::test_run_success`.

Verification:
- pytest: tests/test_runner_command.py::test_run_success

### REQ-TEST-364 — test runner command.py test run failure

SpecWeave SHALL preserve the executable contract `tests/test_runner_command.py::test_run_failure`.

Verification:
- pytest: tests/test_runner_command.py::test_run_failure

### REQ-TEST-365 — test runner command.py test run not found

SpecWeave SHALL preserve the executable contract `tests/test_runner_command.py::test_run_not_found`.

Verification:
- pytest: tests/test_runner_command.py::test_run_not_found

### REQ-TEST-366 — test runner command.py test run captures stdout stderr

SpecWeave SHALL preserve the executable contract `tests/test_runner_command.py::test_run_captures_stdout_stderr`.

Verification:
- pytest: tests/test_runner_command.py::test_run_captures_stdout_stderr

### REQ-TEST-367 — test spec to code.py test step function name basic

SpecWeave SHALL preserve the executable contract `tests/test_spec_to_code.py::test_step_function_name_basic`.

Verification:
- pytest: tests/test_spec_to_code.py::test_step_function_name_basic

### REQ-TEST-368 — test spec to code.py test step function name dedup

SpecWeave SHALL preserve the executable contract `tests/test_spec_to_code.py::test_step_function_name_dedup`.

Verification:
- pytest: tests/test_spec_to_code.py::test_step_function_name_dedup

### REQ-TEST-369 — test spec to code.py test draft feature creates file

SpecWeave SHALL preserve the executable contract `tests/test_spec_to_code.py::test_draft_feature_creates_file`.

Verification:
- pytest: tests/test_spec_to_code.py::test_draft_feature_creates_file

### REQ-TEST-370 — test spec to code.py test bind feature creates skeleton

SpecWeave SHALL preserve the executable contract `tests/test_spec_to_code.py::test_bind_feature_creates_skeleton`.

Verification:
- pytest: tests/test_spec_to_code.py::test_bind_feature_creates_skeleton

### REQ-TEST-371 — test spec to code.py test bind unsupported backend raises

SpecWeave SHALL preserve the executable contract `tests/test_spec_to_code.py::test_bind_unsupported_backend_raises`.

Verification:
- pytest: tests/test_spec_to_code.py::test_bind_unsupported_backend_raises

### REQ-TEST-372 — test specifications coverage.py test requirement bound by pytest mapping passes coverage

SpecWeave SHALL preserve the executable contract `tests/test_specifications_coverage.py::test_requirement_bound_by_pytest_mapping_passes_coverage`.

Verification:
- pytest: tests/test_specifications_coverage.py::test_requirement_bound_by_pytest_mapping_passes_coverage

### REQ-TEST-373 — test specifications coverage.py test missing pytest mapping fails coverage

SpecWeave SHALL preserve the executable contract `tests/test_specifications_coverage.py::test_missing_pytest_mapping_fails_coverage`.

Verification:
- pytest: tests/test_specifications_coverage.py::test_missing_pytest_mapping_fails_coverage

### REQ-TEST-374 — test specifications coverage.py test stale pytest nodeid fails coverage

SpecWeave SHALL preserve the executable contract `tests/test_specifications_coverage.py::test_stale_pytest_nodeid_fails_coverage`.

Verification:
- pytest: tests/test_specifications_coverage.py::test_stale_pytest_nodeid_fails_coverage

### REQ-TEST-375 — test specifications coverage.py test reverse coverage lists unmapped pytest tests

SpecWeave SHALL preserve the executable contract `tests/test_specifications_coverage.py::test_reverse_coverage_lists_unmapped_pytest_tests`.

Verification:
- pytest: tests/test_specifications_coverage.py::test_reverse_coverage_lists_unmapped_pytest_tests

### REQ-TEST-376 — test specifications coverage.py test intentional unmapped policy waives reverse gap

SpecWeave SHALL preserve the executable contract `tests/test_specifications_coverage.py::test_intentional_unmapped_policy_waives_reverse_gap`.

Verification:
- pytest: tests/test_specifications_coverage.py::test_intentional_unmapped_policy_waives_reverse_gap

### REQ-TEST-377 — test specifications index.py test writes manifest

SpecWeave SHALL preserve the executable contract `tests/test_specifications_index.py::test_writes_manifest`.

Verification:
- pytest: tests/test_specifications_index.py::test_writes_manifest

### REQ-TEST-378 — test specifications index.py test includes product spec capabilities interfaces and integrations

SpecWeave SHALL preserve the executable contract `tests/test_specifications_index.py::test_includes_product_spec_capabilities_interfaces_and_integrations`.

Verification:
- pytest: tests/test_specifications_index.py::test_includes_product_spec_capabilities_interfaces_and_integrations

### REQ-TEST-379 — test specifications index.py test includes verification refs

SpecWeave SHALL preserve the executable contract `tests/test_specifications_index.py::test_includes_verification_refs`.

Verification:
- pytest: tests/test_specifications_index.py::test_includes_verification_refs

### REQ-TEST-380 — test specifications lint.py test duplicate document ids fail

SpecWeave SHALL preserve the executable contract `tests/test_specifications_lint.py::test_duplicate_document_ids_fail`.

Verification:
- pytest: tests/test_specifications_lint.py::test_duplicate_document_ids_fail

### REQ-TEST-381 — test specifications lint.py test duplicate requirement ids fail

SpecWeave SHALL preserve the executable contract `tests/test_specifications_lint.py::test_duplicate_requirement_ids_fail`.

Verification:
- pytest: tests/test_specifications_lint.py::test_duplicate_requirement_ids_fail

### REQ-TEST-382 — test specifications lint.py test missing verification fails when required

SpecWeave SHALL preserve the executable contract `tests/test_specifications_lint.py::test_missing_verification_fails_when_required`.

Verification:
- pytest: tests/test_specifications_lint.py::test_missing_verification_fails_when_required

### REQ-TEST-383 — test specifications lint.py test weak normative language warns

SpecWeave SHALL preserve the executable contract `tests/test_specifications_lint.py::test_weak_normative_language_warns`.

Verification:
- pytest: tests/test_specifications_lint.py::test_weak_normative_language_warns

### REQ-TEST-384 — test specifications lint.py test unsupported id prefix fails

SpecWeave SHALL preserve the executable contract `tests/test_specifications_lint.py::test_unsupported_id_prefix_fails`.

Verification:
- pytest: tests/test_specifications_lint.py::test_unsupported_id_prefix_fails

### REQ-TEST-385 — test specifications parser.py test parses front matter

SpecWeave SHALL preserve the executable contract `tests/test_specifications_parser.py::test_parses_front_matter`.

Verification:
- pytest: tests/test_specifications_parser.py::test_parses_front_matter

### REQ-TEST-386 — test specifications parser.py test parses product spec

SpecWeave SHALL preserve the executable contract `tests/test_specifications_parser.py::test_parses_product_spec`.

Verification:
- pytest: tests/test_specifications_parser.py::test_parses_product_spec

### REQ-TEST-387 — test specifications parser.py test parses requirement headings

SpecWeave SHALL preserve the executable contract `tests/test_specifications_parser.py::test_parses_requirement_headings`.

Verification:
- pytest: tests/test_specifications_parser.py::test_parses_requirement_headings

### REQ-TEST-388 — test specifications parser.py test parses verification lists

SpecWeave SHALL preserve the executable contract `tests/test_specifications_parser.py::test_parses_verification_lists`.

Verification:
- pytest: tests/test_specifications_parser.py::test_parses_verification_lists

### REQ-TEST-389 — test specifications parser.py test preserves line numbers

SpecWeave SHALL preserve the executable contract `tests/test_specifications_parser.py::test_preserves_line_numbers`.

Verification:
- pytest: tests/test_specifications_parser.py::test_preserves_line_numbers

### REQ-TEST-390 — test specifications reporting.py test imports junit xml to requirement evidence

SpecWeave SHALL preserve the executable contract `tests/test_specifications_reporting.py::test_imports_junit_xml_to_requirement_evidence`.

Verification:
- pytest: tests/test_specifications_reporting.py::test_imports_junit_xml_to_requirement_evidence

### REQ-TEST-391 — test specifications reporting.py test fail closed status blocks requirement

SpecWeave SHALL preserve the executable contract `tests/test_specifications_reporting.py::test_fail_closed_status_blocks_requirement`.

Verification:
- pytest: tests/test_specifications_reporting.py::test_fail_closed_status_blocks_requirement

### REQ-TEST-392 — test specifications reporting.py test passing mapped pytest test verifies requirement

SpecWeave SHALL preserve the executable contract `tests/test_specifications_reporting.py::test_passing_mapped_pytest_test_verifies_requirement`.

Verification:
- pytest: tests/test_specifications_reporting.py::test_passing_mapped_pytest_test_verifies_requirement

### REQ-TEST-393 — test specifications review.py test review specifications aggregates lint and coverage

SpecWeave SHALL preserve the executable contract `tests/test_specifications_review.py::test_review_specifications_aggregates_lint_and_coverage`.

Verification:
- pytest: tests/test_specifications_review.py::test_review_specifications_aggregates_lint_and_coverage

### REQ-TEST-394 — test specifications review.py test review specs includes both modes

SpecWeave SHALL preserve the executable contract `tests/test_specifications_review.py::test_review_specs_includes_both_modes`.

Verification:
- pytest: tests/test_specifications_review.py::test_review_specs_includes_both_modes

### REQ-TEST-395 — test taskledger draft.py TestTaskledgerDraft test creates draft from feature

SpecWeave SHALL preserve the executable contract `tests/test_taskledger_draft.py::TestTaskledgerDraft::test_creates_draft_from_feature`.

Verification:
- pytest: tests/test_taskledger_draft.py::TestTaskledgerDraft::test_creates_draft_from_feature

### REQ-TEST-396 — test taskledger draft.py TestTaskledgerDraft test draft does not require taskledger import

SpecWeave SHALL preserve the executable contract `tests/test_taskledger_draft.py::TestTaskledgerDraft::test_draft_does_not_require_taskledger_import`.

Verification:
- pytest: tests/test_taskledger_draft.py::TestTaskledgerDraft::test_draft_does_not_require_taskledger_import

### REQ-TEST-397 — test taskledger draft.py TestTaskledgerDraft test draft json is valid

SpecWeave SHALL preserve the executable contract `tests/test_taskledger_draft.py::TestTaskledgerDraft::test_draft_json_is_valid`.

Verification:
- pytest: tests/test_taskledger_draft.py::TestTaskledgerDraft::test_draft_json_is_valid

### REQ-TEST-398 — test trace.py test trace by bdd id reports mapping and missing evidence gap

SpecWeave SHALL preserve the executable contract `tests/test_trace.py::test_trace_by_bdd_id_reports_mapping_and_missing_evidence_gap`.

Verification:
- pytest: tests/test_trace.py::test_trace_by_bdd_id_reports_mapping_and_missing_evidence_gap

### REQ-TEST-399 — test trace.py test trace rejects markdown feature path

SpecWeave SHALL preserve the executable contract `tests/test_trace.py::test_trace_rejects_markdown_feature_path`.

Verification:
- pytest: tests/test_trace.py::test_trace_rejects_markdown_feature_path

### REQ-TEST-400 — test trace.py test trace by requirement id reports mapping and missing evidence gap

SpecWeave SHALL preserve the executable contract `tests/test_trace.py::test_trace_by_requirement_id_reports_mapping_and_missing_evidence_gap`.

Verification:
- pytest: tests/test_trace.py::test_trace_by_requirement_id_reports_mapping_and_missing_evidence_gap

### REQ-TEST-401 — test translation pytest to gherkin.py TestSlug test basic

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestSlug::test_basic`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestSlug::test_basic

### REQ-TEST-402 — test translation pytest to gherkin.py TestSlug test special chars

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestSlug::test_special_chars`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestSlug::test_special_chars

### REQ-TEST-403 — test translation pytest to gherkin.py TestDeriveArea test simple

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestDeriveArea::test_simple`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestDeriveArea::test_simple

### REQ-TEST-404 — test translation pytest to gherkin.py TestDeriveArea test nested

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestDeriveArea::test_nested`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestDeriveArea::test_nested

### REQ-TEST-405 — test translation pytest to gherkin.py TestDeriveFeatureTitle test test prefix

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestDeriveFeatureTitle::test_test_prefix`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestDeriveFeatureTitle::test_test_prefix

### REQ-TEST-406 — test translation pytest to gherkin.py TestDeriveFeatureTitle test test suffix

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestDeriveFeatureTitle::test_test_suffix`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestDeriveFeatureTitle::test_test_suffix

### REQ-TEST-407 — test translation pytest to gherkin.py TestCreateGherkinFromSinglePytestFile test creates feature

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinFromSinglePytestFile::test_creates_feature`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinFromSinglePytestFile::test_creates_feature

### REQ-TEST-408 — test translation pytest to gherkin.py TestCreateGherkinFromSinglePytestFile test marks needs review

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinFromSinglePytestFile::test_marks_needs_review`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinFromSinglePytestFile::test_marks_needs_review

### REQ-TEST-409 — test translation pytest to gherkin.py TestCreateGherkinFromSinglePytestFile test includes bdd id

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinFromSinglePytestFile::test_includes_bdd_id`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinFromSinglePytestFile::test_includes_bdd_id

### REQ-TEST-410 — test translation pytest to gherkin.py TestCreateGherkinGroupsByArea test groups by file

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinGroupsByArea::test_groups_by_file`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinGroupsByArea::test_groups_by_file

### REQ-TEST-411 — test translation pytest to gherkin.py TestCreateGherkinGroupsByArea test rejects unsupported grouping

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinGroupsByArea::test_rejects_unsupported_grouping`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinGroupsByArea::test_rejects_unsupported_grouping

### REQ-TEST-412 — test translation pytest to gherkin.py TestCreateGherkinGroupsByArea test duplicate ids are deterministic

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinGroupsByArea::test_duplicate_ids_are_deterministic`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinGroupsByArea::test_duplicate_ids_are_deterministic

### REQ-TEST-413 — test translation pytest to gherkin.py TestCreateGherkinPreservesExisting test skips manual file without force

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinPreservesExisting::test_skips_manual_file_without_force`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinPreservesExisting::test_skips_manual_file_without_force

### REQ-TEST-414 — test translation pytest to gherkin.py TestCreateGherkinPreservesExisting test preserves existing bdd id

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinPreservesExisting::test_preserves_existing_bdd_id`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinPreservesExisting::test_preserves_existing_bdd_id

### REQ-TEST-415 — test translation pytest to gherkin.py TestCreateGherkinDryRun test writes nothing

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinDryRun::test_writes_nothing`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinDryRun::test_writes_nothing

### REQ-TEST-416 — test translation pytest to gherkin.py TestCreateGherkinJsonShape test json shape

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinJsonShape::test_json_shape`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinJsonShape::test_json_shape

### REQ-TEST-417 — test translation pytest to gherkin.py TestCreateGherkinJsonShape test force overwrites manual

SpecWeave SHALL preserve the executable contract `tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinJsonShape::test_force_overwrites_manual`.

Verification:
- pytest: tests/test_translation_pytest_to_gherkin.py::TestCreateGherkinJsonShape::test_force_overwrites_manual

