from __future__ import annotations

import json
from pathlib import Path

SCHEMA_DIR = Path("specweave/schemas")


def _load(name: str) -> dict[str, object]:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def test_exchange_schemas_are_json_schema_documents() -> None:
    for name in (
        "combi.trace.v1.schema.json",
        "specweave.taskledger-bdd-export.v1.schema.json",
        "specweave.behavior-evidence.v1.schema.json",
        "specweave.archledger-candidate.v1.schema.json",
    ):
        schema = _load(name)
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema["type"] == "object"
        assert schema["required"]


def test_trace_schema_representative_payload_contract() -> None:
    schema = _load("combi.trace.v1.schema.json")
    good_payload = {
        "schema": "combi.trace.v1",
        "producer": "specweave",
        "target": "bdd-0001",
        "traces": [],
        "gaps": [],
    }
    assert set(schema["required"]) <= set(good_payload)
    bad_payload = dict(good_payload)
    bad_payload.pop("target")
    assert not set(schema["required"]) <= set(bad_payload)


def test_exchange_schema_required_fields_match_current_payloads() -> None:
    payloads = {
        "specweave.taskledger-bdd-export.v1.schema.json": {
            "task_id": "task-0001",
            "feature": "Login",
            "rules": [],
            "examples": [],
        },
        "specweave.behavior-evidence.v1.schema.json": {
            "schema_version": 2,
            "generated_by": "specweave",
            "task_id": "task-0001",
            "source_report": "report.xml",
            "status": "passed",
            "criteria": [],
            "scenarios": [],
        },
        "specweave.archledger-candidate.v1.schema.json": {
            "schema": "specweave.archledger-candidate.v1",
            "producer": "specweave",
            "candidate": {
                "title": "Login",
                "source_refs": ["login.feature.md"],
                "bdd_ids": ["bdd-login"],
                "status": "draft",
            },
        },
    }
    for name, payload in payloads.items():
        schema = _load(name)
        assert set(schema["required"]) <= set(payload)
