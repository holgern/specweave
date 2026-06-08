"""Tag parsing and validation helpers.

Supports both single-tag-per-line and multiple-tags-per-line Gherkin forms::

    @ac-0001
    @bdd-0001 @task-0123 @rule-0001 @ac-0001

``parse_tag`` is retained as a backward-compatible wrapper that returns only the
first tag on a line.
"""

from __future__ import annotations

import re

#: Matches a single ``@token`` (token may include ``:`` for namespaced tags).
TAG_TOKEN_RE = re.compile(r"@(\S+)")


def _tokens(line: str) -> list[str]:
    """Return whitespace-separated tokens of a stripped *line*."""
    return line.strip().split()


def is_tag_line(line: str) -> bool:
    """Return True if *line* is a Gherkin tag line (one or more ``@tags``).

    A tag line is a non-empty line whose every whitespace-separated token starts
    with ``@`` and has at least one character after it::

        @ac-0001                                  -> True
        @bdd-0001 @task-0123 @rule-0001 @ac-0001  -> True
        @taskledger:TL-0042                       -> True
        Scenario: x                               -> False
        @                                         -> False
    """
    tokens = _tokens(line)
    if not tokens:
        return False
    return all(tok.startswith("@") and len(tok) > 1 for tok in tokens)


def parse_tag_line(line: str) -> tuple[str, ...]:
    """Parse all tags from *line*.

    Returns the tag contents (without the leading ``@``) in order of
    appearance. Returns an empty tuple when *line* is not a tag line.
    """
    if not is_tag_line(line):
        return ()
    return tuple(m.group(1) for m in TAG_TOKEN_RE.finditer(line.strip()))


def parse_tag(line: str) -> str | None:
    """Backward-compatible tag parser.

    Returns the first tag content on *line* (without ``@``), or ``None`` when
    the line is not a tag line. Prefer :func:`parse_tag_line` for new code.
    """
    tags = parse_tag_line(line)
    return tags[0] if tags else None


def filter_tags(tags: tuple[str, ...], prefix: str = "") -> tuple[str, ...]:
    """Return tags that start with *prefix*.

    When *prefix* is empty, return all tags unchanged.
    """
    if not prefix:
        return tags
    return tuple(t for t in tags if t.startswith(prefix))
