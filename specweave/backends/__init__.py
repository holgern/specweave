"""Step-skeleton backends.

Each backend turns a parsed :class:`~specweave.gherkin.model.Feature` into a
Python step-definition skeleton for a specific BDD framework. The package owns
the framework-specific code generation; ``bind_feature`` selects a backend by
name via :data:`BACKENDS`.

Supported backends:

- ``behave``: behave-style ``@given``/``@when``/``@then`` step decorators.
- ``pytest-bdd``: ``pytest-bdd`` style step decorators using ``parsers``.

Not yet supported (intentionally, per the SpecWeave coding agent guide):

- ``cucumber-js`` and ``cucumber-jvm``: no JavaScript/Java code generation until
  project conventions are known. Requesting them raises a descriptive error.
"""

from __future__ import annotations

from collections.abc import Callable

from specweave.backends._helpers import collect_steps
from specweave.backends.behave import generate_behave
from specweave.backends.pytest_bdd import generate_pytest_bdd
from specweave.gherkin.model import Feature, Step

#: A backend generator renders *feature* into a skeleton source string.
BackendGenerator = Callable[[Feature], str]

#: Registry of supported backend names to generators.
BACKENDS: dict[str, BackendGenerator] = {
    "behave": generate_behave,
    "pytest-bdd": generate_pytest_bdd,
}

#: Backends that exist but are intentionally not implemented yet.
UNSUPPORTED_BACKENDS = ("cucumber-js", "cucumber-jvm")


def get_backend(name: str) -> BackendGenerator:
    """Return the generator for *name*.

    Raises ValueError for unknown backends, with a tailored message for the
    intentionally-not-yet-supported cucumber-* backends.
    """
    if name in BACKENDS:
        return BACKENDS[name]
    if name in UNSUPPORTED_BACKENDS:
        raise ValueError(
            f"Backend {name!r} is not yet supported; "
            "do not generate JS/Java skeletons until project conventions are known."
        )
    raise ValueError(f"Unsupported backend: {name!r}. Supported: {sorted(BACKENDS)}.")


__all__ = [
    "BACKENDS",
    "BackendGenerator",
    "UNSUPPORTED_BACKENDS",
    "collect_steps",
    "get_backend",
]
