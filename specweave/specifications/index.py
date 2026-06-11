"""Specification manifest and Markdown index generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from specweave.specifications.parser import (
    collect_specification_files,
    parse_specification,
)


def _project_root_for(root: Path) -> Path:
    if root.name == "specifications" and root.parent.name == "specs":
        return root.parent.parent
    return root.parent


def _display_path(path: Path, *, project_root: Path | None = None) -> str:
    if project_root is not None:
        try:
            return path.resolve().relative_to(project_root.resolve()).as_posix()
        except ValueError:
            pass
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def build_specification_index(
    *,
    root: Path,
) -> tuple[dict[str, Any], str]:
    """Build the specifications manifest payload and Markdown index."""
    project_root = _project_root_for(root)
    spec_files = collect_specification_files([root])
    documents: list[dict[str, Any]] = []
    requirements: list[dict[str, Any]] = []
    markdown_lines = [
        "# Specifications index",
        "",
        f"Generated from `{_display_path(root, project_root=project_root)}`.",
        "",
    ]

    for spec_path in spec_files:
        document = parse_specification(spec_path)
        document_ref = _display_path(spec_path, project_root=project_root)
        document_entry: dict[str, Any] = {
            "id": document.spec_id,
            "path": document_ref,
            "title": document.title,
            "kind": document.kind,
            "status": document.status,
            "requirements": [requirement.id for requirement in document.requirements],
        }
        documents.append(document_entry)

        markdown_lines.extend(
            [
                f"## {document.title}",
                "",
                f"- Path: `{document_ref}`",
                f"- Id: `{document.spec_id}`",
                f"- Kind: `{document.kind}`",
                f"- Status: `{document.status}`",
                "",
            ]
        )
        for requirement in document.requirements:
            requirements.append(
                {
                    "id": requirement.id,
                    "document_id": document.spec_id,
                    "path": document_ref,
                    "line": requirement.line,
                    "title": requirement.title,
                    "kind": requirement.kind,
                    "status": requirement.status,
                    "verification": [
                        {"kind": ref.kind, "target": ref.target}
                        for ref in requirement.verification_refs
                    ],
                    "links": list(requirement.links),
                    "evidence_status": "missing",
                }
            )
            markdown_lines.append(
                f"- `{requirement.id}` {requirement.title} ({requirement.status})"
            )
        markdown_lines.append("")

    product_spec = next(
        (
            _display_path(spec_path, project_root=project_root)
            for spec_path in spec_files
            if spec_path.name == "product.spec.md"
        ),
        _display_path(root / "product.spec.md", project_root=project_root),
    )
    manifest = {
        "schema": "specweave.specifications-manifest.v1",
        "mode": "specifications",
        "root": _display_path(root, project_root=project_root),
        "product_spec": product_spec,
        "documents": documents,
        "requirements": requirements,
        "mappings": [],
    }
    markdown = "\n".join(markdown_lines).rstrip() + "\n"
    return manifest, markdown


def write_specification_index(
    *,
    root: Path,
    out: Path,
    manifest_path: Path,
) -> tuple[Path, Path]:
    """Write the specifications Markdown index and manifest JSON."""
    manifest, markdown = build_specification_index(root=root)
    out.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown, encoding="utf-8")
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return out, manifest_path
