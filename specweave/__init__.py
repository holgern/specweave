"""SpecWeave: translate between Python tests, Gherkin behavior specs,
and BDD execution evidence."""

from __future__ import annotations

try:
    from specweave._version import __version__, __version_tuple__
except Exception:  # pragma: no cover - defensive fallback for unusual source trees
    __version__ = "0+unknown"
    __version_tuple__ = (0, "unknown")

__all__ = ["__version__", "__version_tuple__"]
