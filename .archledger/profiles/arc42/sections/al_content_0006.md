---
schema_version: 2
id: al_content_0006
type: section
section: runtime_view
title: Runtime View
order: 60
status: accepted
date: "2026-06-08"
body_format: markdown
created_at: "2026-06-08T12:58:35Z"
updated_at: "2026-06-08T18:30:00Z"
---

## Brownfield workflow (tests → specs → evidence)

```text
Developer          SpecWeave CLI              Filesystem
   │                     │                        │
   │ specweave init      │                        │
   │────────────────────►│ create .specweave.toml │
   │                     │───────────────────────►│
   │                     │                        │
   │ specweave create    │                        │
   │   gherkin           │                        │
   │   --from-tests      │ AST-read tests/*.py    │
   │────────────────────►│───────────────────────►│
   │                     │ generate .feature.md   │
   │                     │───────────────────────►│
   │                     │                        │
   │ specweave behavior  │                        │
   │   check             │ lint .feature.md files │
   │────────────────────►│───────────────────────►│
   │                     │                        │
   │ specweave behavior  │                        │
   │   index             │ write README + manifest│
   │────────────────────►│───────────────────────►│
   │                     │                        │
   │ specweave behavior  │                        │
   │   generate-tests    │ write test_*.py files  │
   │────────────────────►│───────────────────────►│
   │                     │                        │
   │ pytest              │                        │
   │─────────────────────────────────────────────►│
   │                     │                        │
   │ specweave behavior  │                        │
   │   import-report     │ read JUnit XML         │
   │────────────────────►│───────────────────────►│
   │                     │ write evidence JSON    │
   │                     │───────────────────────►│
```

## New-feature workflow (spec-first)

```text
Developer          SpecWeave CLI              Filesystem
   │                     │                        │
   │ specweave create    │                        │
   │   feature           │                        │
   │   --area --title    │ generate .feature.md   │
   │────────────────────►│───────────────────────►│
   │                     │                        │
   │ specweave behavior  │                        │
   │   generate-tests    │ write test_*.py        │
   │────────────────────►│───────────────────────►│
   │                     │                        │
   │ (implement tests)   │                        │
   │─────────────────────────────────────────────►│
```

## Report normalization flow

1. External runner (pytest with `--junitxml`) writes native XML to
   `reports/behavior/`.
2. `specweave report normalize` parses the XML via
   `specweave/reports/junit_xml.py`, maps scenario results to `@bdd-*` tags,
   rolls up acceptance criteria via `@ac-*`.
3. Non-passed scenarios fail the report. Missing expected `@ac-*` coverage
   fails the report.
4. Output: normalized JSON or Taskledger evidence JSON to
   `.specweave/evidence/`.
