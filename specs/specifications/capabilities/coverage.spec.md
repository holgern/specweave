---
id: SPEC-COV
title: Coverage and reverse coverage
kind: capability-spec
status: active
version: 2
---

# Coverage and reverse coverage

## Intent

SpecWeave reports traceability gaps in both directions for behavior scenarios, specification requirements, and pytest tests.

## Requirements

### REQ-COV-001 — Bidirectional coverage

SpecWeave SHALL make bidirectional coverage the documented default for both behavior scenarios and specification requirements.

Verification:
- pytest: tests/test_behavior_coverage.py::test_render_coverage_text_both_directions

### REQ-COV-002 — Intentional unmapped policy

SpecWeave SHALL allow explicit waivers for intentionally unmapped pytest tests while keeping unwaived gaps visible.

Verification:
- pytest: tests/test_behavior_coverage.py::test_coverage_accepts_intentional_unmapped_pytest_tests

