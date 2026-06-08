"""SpecWeave configuration."""

from __future__ import annotations

from pathlib import Path

REPORT_DIR = Path(".specweave/reports")
"""Default directory for runner summary reports."""

BEHAVIOR_FEATURES_DIR = Path("specs/behavior/features")
BEHAVIOR_INDEX_PATH = Path("specs/behavior/README.md")
BEHAVIOR_MANIFEST_PATH = Path("specs/behavior/manifest.json")
PYTEST_TESTS_DIR = Path("tests")
BEHAVIOR_REPORTS_DIR = Path("reports/behavior")
SPECWEAVE_REPORTS_DIR = REPORT_DIR
SPECWEAVE_EVIDENCE_DIR = Path(".specweave/evidence")
SPECWEAVE_MAPPING_DIR = Path(".specweave/mappings")

# Compatibility aliases retained for older code paths.
FEATURES_DIR = BEHAVIOR_FEATURES_DIR
BDD_INDEX_PATH = BEHAVIOR_INDEX_PATH
BDD_MANIFEST_PATH = BEHAVIOR_MANIFEST_PATH
BDD_TESTS_DIR = PYTEST_TESTS_DIR
BDD_REPORTS_DIR = BEHAVIOR_REPORTS_DIR
