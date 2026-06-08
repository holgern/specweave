"""Convert between classic Gherkin and Markdown-with-Gherkin files."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

from specweave.config import SpecWeaveConfig
from specweave.gherkin.lint import collect_feature_files
from specweave.gherkin.markdown import markdown_to_classic
from specweave.gherkin.parser import parse_feature
from specweave.gherkin.writer import write_feature

_SUPPORTED_FORMATS = frozenset({"classic", "markdown"})


def infer_document_format(path: Path, text: str | None = None) -> str:
    """Infer the SpecWeave Gherkin document format from *path* and optionally text."""
    path_text = path.as_posix()
    if path_text.endswith(".feature.md"):
        return "markdown"
    if path.suffix == ".feature":
        return "classic"

    if text is not None:
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("# Feature:"):
                return "markdown"
            if stripped.startswith("Feature:") or stripped.startswith("@"):
                return "classic"

    return "classic"


def default_output_path(source_path: Path, target_format: str) -> Path:
    """Return the default output path for a conversion target format."""
    if target_format == "markdown":
        if source_path.as_posix().endswith(".feature.md"):
            return source_path
        if source_path.suffix == ".feature":
            return source_path.with_name(f"{source_path.name}.md")
        return source_path.with_suffix(f"{source_path.suffix}.feature.md")

    if source_path.as_posix().endswith(".feature.md"):
        return source_path.with_name(source_path.name[: -len(".md")])
    if source_path.suffix == ".feature":
        return source_path
    return source_path.with_suffix(".feature")


def _validate_format(name: str, value: str) -> None:
    if value not in _SUPPORTED_FORMATS:
        expected = ", ".join(sorted(_SUPPORTED_FORMATS))
        raise ValueError(f"Unsupported {name}: {value}; expected one of: {expected}")


def _is_feature_file(path: Path) -> bool:
    text = path.as_posix()
    return text.endswith(".feature") or text.endswith(".feature.md")


def collect_conversion_sources(paths: Iterable[Path]) -> list[Path]:
    """Return unique feature files from explicit files and directories."""

    sources: list[Path] = []
    directory_roots: list[Path] = []
    for path in paths:
        if path.is_file():
            if _is_feature_file(path):
                sources.append(path)
            continue
        directory_roots.append(path)

    sources.extend(collect_feature_files(directory_roots))

    seen: set[Path] = set()
    unique: list[Path] = []
    for source in sources:
        if source in seen:
            continue
        seen.add(source)
        unique.append(source)
    return unique


def _validate_with_official(
    text: str,
    *,
    source_path: Path,
    document_format: str,
) -> None:
    """Validate *text* through gherkin-official's classic parser.

    The Python gherkin-official parser validates classic Gherkin. For Markdown-
    with-Gherkin, SpecWeave first renders the Markdown document to classic
    Gherkin and validates that equivalent classic form.
    """
    from specweave.gherkin.official import validate_classic_with_official

    if document_format == "markdown":
        text = markdown_to_classic(text)
    validate_classic_with_official(text, source_path=source_path)


def convert_feature_file(
    *,
    source_path: Path,
    out_path: Path | None = None,
    target_format: str | None = None,
    source_format: str = "auto",
    force: bool = False,
    dry_run: bool = False,
    validate: bool = True,
    config: SpecWeaveConfig | None = None,
) -> dict:
    """Convert one feature file and return a JSON-serialisable result dict."""
    if config is None:
        config = SpecWeaveConfig()

    source_text = source_path.read_text(encoding="utf-8")
    if source_format == "auto":
        resolved_source_format = infer_document_format(source_path, source_text)
    else:
        resolved_source_format = source_format
    _validate_format("source format", resolved_source_format)

    resolved_target_format = target_format or config.gherkin.document_format
    _validate_format("target format", resolved_target_format)

    target_path = out_path or default_output_path(source_path, resolved_target_format)

    if validate and config.gherkin.official_parser:
        _validate_with_official(
            source_text,
            source_path=source_path,
            document_format=resolved_source_format,
        )

    feature = parse_feature(
        source_text,
        source_path=source_path,
        document_format=resolved_source_format,
        use_official=(
            validate
            and config.gherkin.official_parser
            and resolved_source_format == "classic"
        ),
        compile_pickles=config.gherkin.compile_pickles,
    )
    converted_text = write_feature(feature, document_format=resolved_target_format)

    if validate and config.gherkin.official_parser:
        _validate_with_official(
            converted_text,
            source_path=target_path,
            document_format=resolved_target_format,
        )

    warnings: list[str] = []
    should_write = True
    status = "created"
    if target_path == source_path and resolved_source_format == resolved_target_format:
        if source_text == converted_text:
            status = "unchanged"
            should_write = False
        elif not force:
            status = "unchanged"
            should_write = False
            warnings.append("already_target_format")
        else:
            status = "updated"
    elif target_path.exists():
        existing = target_path.read_text(encoding="utf-8")
        if existing == converted_text:
            status = "unchanged"
            should_write = False
        elif not force:
            raise ValueError(f"{target_path} already exists. Use --force to overwrite.")
        else:
            status = "updated"

    if dry_run:
        write_status = "dry-run"
    else:
        write_status = status
        if should_write:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(converted_text, encoding="utf-8")

    return {
        "schema_version": 1,
        "command": "convert",
        "status": write_status,
        "planned_status": status,
        "source_path": str(source_path),
        "output_path": str(target_path),
        "source_format": resolved_source_format,
        "target_format": resolved_target_format,
        "validated": bool(validate and config.gherkin.official_parser),
        "warnings": warnings,
    }


def _deletable_source(result: dict[str, Any], *, replace_source: bool) -> bool:
    return (
        replace_source
        and result["source_format"] == "classic"
        and result["target_format"] == "markdown"
        and result["source_path"] != result["output_path"]
    )


def convert_feature_files(
    *,
    paths: Iterable[Path],
    out_dir: Path | None = None,
    target_format: str | None = None,
    source_format: str = "auto",
    force: bool = False,
    dry_run: bool = False,
    validate: bool = True,
    replace_source: bool = False,
    config: SpecWeaveConfig | None = None,
) -> dict[str, Any]:
    """Convert multiple feature files and return a batch result dict."""

    if config is None:
        config = SpecWeaveConfig()
    if out_dir is not None:
        raise ValueError("Batch conversion does not support --out yet.")

    resolved_target_format = target_format or config.gherkin.document_format
    _validate_format("target format", resolved_target_format)

    sources = collect_conversion_sources(paths)
    if not sources:
        raise ValueError("No feature files found to convert.")

    write_targets: dict[Path, list[Path]] = {}
    for source_path in sources:
        output_path = default_output_path(source_path, resolved_target_format)
        if output_path != source_path:
            write_targets.setdefault(output_path, []).append(source_path)
    collision_sources = {
        source
        for mapped_sources in write_targets.values()
        if len(mapped_sources) > 1
        for source in mapped_sources
    }
    collision_messages = {
        source: (
            f"{default_output_path(source, resolved_target_format)} would be produced "
            "by multiple batch inputs."
        )
        for source in collision_sources
    }

    items: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    summary = {
        "created": 0,
        "updated": 0,
        "unchanged": 0,
        "skipped": 0,
        "errors": 0,
        "deleted_sources": 0,
    }

    for source_path in sources:
        if source_path in collision_sources:
            output_path = default_output_path(source_path, resolved_target_format)
            error_message = collision_messages[source_path]
            items.append(
                {
                    "status": "error",
                    "source_path": str(source_path),
                    "output_path": str(output_path),
                    "source_format": source_format,
                    "target_format": resolved_target_format,
                    "validated": False,
                    "deleted_source": False,
                    "warnings": [],
                    "error": error_message,
                }
            )
            errors.append(
                {
                    "source_path": str(source_path),
                    "output_path": str(output_path),
                    "error": error_message,
                }
            )
            summary["errors"] += 1
            continue

        try:
            result = convert_feature_file(
                source_path=source_path,
                target_format=resolved_target_format,
                source_format=source_format,
                force=force,
                dry_run=dry_run,
                validate=validate,
                config=config,
            )
        except ValueError as exc:
            output_path = default_output_path(source_path, resolved_target_format)
            items.append(
                {
                    "status": "error",
                    "source_path": str(source_path),
                    "output_path": str(output_path),
                    "source_format": source_format,
                    "target_format": resolved_target_format,
                    "validated": False,
                    "deleted_source": False,
                    "warnings": [],
                    "error": str(exc),
                }
            )
            errors.append(
                {
                    "source_path": str(source_path),
                    "output_path": str(output_path),
                    "error": str(exc),
                }
            )
            summary["errors"] += 1
            continue

        item = dict(result)
        item["deleted_source"] = False
        if dry_run and _deletable_source(item, replace_source=replace_source):
            item["would_delete_source"] = True
        elif _deletable_source(item, replace_source=replace_source):
            Path(item["source_path"]).unlink()
            item["deleted_source"] = True
            summary["deleted_sources"] += 1

        planned_status = str(item["planned_status"])
        summary[planned_status] += 1
        items.append(item)

    return {
        "schema_version": 1,
        "command": "convert",
        "mode": "batch",
        "status": "failed" if errors else ("dry-run" if dry_run else "passed"),
        "source_count": len(sources),
        "summary": summary,
        "target_format": resolved_target_format,
        "validated": bool(validate and config.gherkin.official_parser),
        "items": items,
        "errors": errors,
    }
