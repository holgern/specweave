"""SpecWeave error types."""

from __future__ import annotations


class SpecWeaveError(Exception):
    """Base error for all SpecWeave exceptions."""


class ParseError(SpecWeaveError):
    """Raised when Gherkin parsing fails."""


class BackendError(SpecWeaveError):
    """Raised when an unsupported backend is requested."""


class RunnerError(SpecWeaveError):
    """Raised when delegated command execution fails."""
