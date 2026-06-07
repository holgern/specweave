"""Step definitions for Password login feature."""

from __future__ import annotations

from behave import given, then, when  # type: ignore[import-untyped]


@given("a registered user exists")
def step_given_a_registered_user_exists(context) -> None:
    """Set up a registered user."""
    raise NotImplementedError("Bind this step to project setup code.")


@when("the user submits an invalid password")
def step_when_the_user_submits_an_invalid_password(context) -> None:
    """Simulate login with bad credentials."""
    raise NotImplementedError("Bind this step to action code.")


@then("login is rejected")
def step_then_login_is_rejected(context) -> None:
    """Assert login was denied."""
    raise NotImplementedError("Bind this step to assertion code.")


@then("no authenticated session is created")
def step_then_no_authenticated_session_is_created(context) -> None:
    """Assert no session exists."""
    raise NotImplementedError("Bind this step to assertion code.")
