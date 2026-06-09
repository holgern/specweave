---
schema_version: 2
id: al_content_0007
type: section
section: deployment_view
title: Deployment View
order: 70
status: accepted
date: "2026-06-08"
body_format: markdown
created_at: "2026-06-08T12:58:35Z"
updated_at: "2026-06-08T18:30:00Z"
---

## Deployment model

SpecWeave is a single Python package deployed to a developer's environment via
`pip install specweave`. It has no server component.

```text
┌──────────────────────────────────────────┐
│          Developer Workstation            │
│                                          │
│  ┌──────────────┐   ┌────────────────┐  │
│  │ specweave CLI │   │ Python ≥3.10   │  │
│  │ (pip install) │   │ (venv/system)  │  │
│  └──────┬───────┘   └────────────────┘  │
│         │ invokes                        │
│  ┌──────▼───────┐                        │
│  │    pytest     │ (external, already     │
│  │              │  installed in venv)     │
│  └──────────────┘                        │
│                                          │
│  Project checkout:                       │
│    .specweave.toml                       │
│    specs/behavior/features/              │
│    tests/                                │
│    specs/behavior/reports/                     │
│    .specweave/                           │
└──────────────────────────────────────────┘
```

## Artifact layout

```text
.specweave.toml              # config (hidden, preferred)
specweave.toml               # config (public alternative)
specs/behavior/
  README.md                  # generated index
  features/<area>/*.feature
  manifest.json              # generated manifest
tests/test_<area>_<feature>.py
specs/behavior/reports/*.xml       # native runner output
.specweave/
  evidence/*.json            # normalized evidence
  reports/*.json             # report state
  mappings/taskledger/*.json # Taskledger exchange
skills/specweave/SKILL.md    # agent skill (not packaged)
```

## CI integration

SpecWeave runs in CI as a CLI step after `pytest --junitxml=...`:

```bash
pytest --junitxml=specs/behavior/reports/pytest-junit.xml
specweave behavior import-report specs/behavior/reports/pytest-junit.xml --format junit-xml
```

No special CI plugin, Docker image, or hosted service is required.
