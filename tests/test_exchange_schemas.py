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
        "subject": {"type": "bdd_scenario", "id": "bdd-0001"},
        "task_ids": [],
        "ac_ids": [],
        "bdd_ids": ["bdd-0001"],
        "archledger_refs": [],
        "source_refs": [],
        "test_refs": [],
        "evidence_refs": [],
        "status": {},
        "gaps": [],
    }
    assert set(schema["required"]) <= set(good_payload)
    bad_payload = dict(good_payload)
    bad_payload.pop("subject")
    assert not set(schema["required"]) <= set(bad_payload)
