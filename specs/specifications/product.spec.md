---
id: SPEC-PRODUCT
title: SpecWeave product specification
kind: product-spec
status: active
version: 2
---

# SpecWeave product specification

## Intent

SpecWeave keeps product behavior, specification requirements, pytest verification, and validation evidence traceable. The product workflow is source-first: write or discover readable behavior, map it to plain pytest, review coverage in both directions, and import evidence fail-closed.

## Requirements

### REQ-SETUP-001 — Initialize and diagnose projects

SpecWeave SHALL initialize, load, and diagnose configured project layouts for behavior and specification modes.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parse_target_example_round_trip

### REQ-AUTHOR-001 — Author canonical feature files

SpecWeave SHALL author, parse, write, and lint classic `.feature` files using the supported readable Gherkin subset.

Verification:
- pytest: tests/test_create_feature_json.py::TestCreateFeatureFromJson::test_cli_from_json

### REQ-BROWN-001 — Discover behavior from existing pytest

SpecWeave SHALL discover candidate behavior specs from existing pytest tests without overwriting manual feature files by default.

Verification:
- pytest: tests/test_gherkin_parser.py::test_parse_target_example_round_trip

### REQ-ENFORCE-001 — Generate plain pytest enforcement

SpecWeave SHALL generate plain pytest skeletons with explicit SpecWeave mappings from behavior scenarios.

Verification:
- pytest: tests/test_behavior_generation.py::test_generate_single_feature

### REQ-TRACE-001 — Review bidirectional behavior coverage

SpecWeave SHALL report feature to pytest and pytest to feature coverage, including missing, stale, duplicate, waived, and unmapped items.

Verification:
- pytest: tests/test_behavior_coverage.py::test_render_coverage_text_both_directions

### REQ-EVID-001 — Normalize evidence fail closed

SpecWeave SHALL normalize runner reports into evidence and treat failed, skipped, missing, or unmapped evidence as not accepted by default.

Verification:
- pytest: tests/test_exchange_schemas.py::test_evidence_schema_representative_payload_contract

### REQ-NAV-001 — Generate navigation artifacts

SpecWeave SHALL generate Markdown indexes and machine-readable manifests for behavior and specification assets.

Verification:
- pytest: tests/test_behavior_index.py::test_index_generates_markdown

### REQ-PLAN-001 — Create implementation plans and optional backend skeletons

SpecWeave SHALL create implementation plans and optional BDD backend skeletons without making pytest-bdd mandatory.

Verification:
- pytest: tests/test_plan.py::TestCreatePlan::test_creates_plan_from_feature

### REQ-INT-001 — Exchange integration data without owning external tools

SpecWeave SHALL exchange Taskledger, Archledger, trace, schema, and combi audit data through files without mutating external ledgers.

Verification:
- pytest: tests/test_combi_check.py::test_combi_check_writes_json_and_human_diagnostics

### REQ-SPEC-001 — Manage specification documents and coverage

SpecWeave SHALL lint, index, review, and report bidirectional coverage for specification Markdown requirements.

Verification:
- pytest: tests/test_spec_to_code.py::test_step_function_name_dedup

### REQ-IMPL-001 — Preserve internal implementation contracts

SpecWeave SHALL preserve low-level parser, helper, and inspection contracts with pytest unit tests when those details are not promoted to product-level Gherkin.

Verification:
- pytest: tests/test_common_behavior_helpers.py::TestSlugify::test_basic

