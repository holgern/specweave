---
id: SPEC-CLI
title: CLI interface
kind: interface-spec
status: active
version: 2
---

# CLI interface

## Requirements

### IF-CLI-001 — Expose scriptable CLI workflows

SpecWeave SHALL expose CLI commands with human-readable output, JSON output where intended, meaningful exit codes, and compatibility aliases.

Verification:
- pytest: tests/test_cli_cli_contract.py::test_help_exits_0

