"""Tag parsing and validation helpers."""

from __future__ import annotations

import re

TAG_RE = re.compile(r"^@(\S+)$")


def parse_tag(line: str) -> str | None:
    """Parse a Gherkin tag from a line.

    Returns the tag content (without ``@``) or ``None``.
    """
    m = TAG_RE.match(line.strip())
    return m.group(1) if m else None


def is_tag(line: str) -> bool:
    """Return True if the line is a Gherkin tag."""
    return bool(TAG_RE.match(line.strip()))


def filter_tags(tags: tuple[str, ...], prefix: str = "") -> tuple[str, ...]:
    """Return tags that start with *prefix*.

    When *prefix* is empty, return all tags unchanged.
    """
    if not prefix:
        return tags
    return tuple(t for t in tags if t.startswith(prefix))
