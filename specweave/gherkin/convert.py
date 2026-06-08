"""Convert between classic Gherkin and Markdown-with-Gherkin files."""

from __future__ import annotations

from pathlib import Path

from specweave.config import SpecWeaveConfig
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

    status = "created"
    if target_path.exists():
        existing = target_path.read_text(encoding="utf-8")
        if existing == converted_text:
            status = "unchanged"
        elif not force:
            raise ValueError(f"{target_path} already exists. Use --force to overwrite.")
        else:
            status = "updated"

    if dry_run:
        write_status = "dry-run"
    else:
        write_status = status
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(converted_text, encoding="utf-8")

    return {
        "schema_version": 1,
        "command": "convert",
        "status": write_status,
        "source_path": str(source_path),
        "output_path": str(target_path),
        "source_format": resolved_source_format,
        "target_format": resolved_target_format,
        "validated": bool(validate and config.gherkin.official_parser),
        "warnings": [],
    }
