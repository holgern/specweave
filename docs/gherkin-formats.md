# Gherkin Format

SpecWeave uses classic Gherkin `.feature` files as the only canonical behavior
format.

## Canonical shape

```gherkin
@area-auth @feature-password-login
Feature: Password login
  Users authenticate with a password.

  @rule-invalid-password
  Rule: Invalid passwords are rejected

    @bdd-password-login-invalid-password @ac-0001
    Example: Reject invalid password
      Given a registered user exists
      When the user submits an invalid password
      Then login is rejected
```

## Rules

- one `.feature` file per behavior feature
- group features by area under `specs/behavior/features/<area>/`
- use stable `@bdd-*` ids for scenario identity
- use `@ac-*` ids for acceptance-criterion linkage
- use scenario titles for display/debugging only

## Unsupported legacy format

Legacy Markdown `.feature.md` files are no longer supported as canonical specs.
When encountered, SpecWeave returns an explicit migration error instead of
parsing or writing them.
