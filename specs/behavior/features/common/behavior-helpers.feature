@area-common @feature-behavior-helpers
Feature: Behavior helper functions
  The behavior.common module provides shared helpers for slugification,
  feature identity extraction, canonical test path derivation, and
  scenario iteration.

  Rule: Slugification produces stable lowercase slugs

    @bdd-slugify-basic
    Example: Slugify converts text to lowercase slug
      Given a text value to slugify
      When specweave slugifies "My Feature Title"
      When specweave slugifies "My Feature Title"
      Then the result is "my-feature-title"

    @bdd-slugify-special-chars
    Example: Slugify replaces special characters with hyphens
      Given a text value with special characters
      When specweave slugifies "feature@name!"
      When specweave slugifies "feature@name!"
      Then the result is "feature-name"

    @bdd-slugify-empty
    Example: Slugify returns "behavior" for empty input
      Given an empty text value
      When specweave slugifies ""
      When specweave slugifies ""
      Then the result is "behavior"

  Rule: Feature identity extracts area and slug

    @bdd-feature-identity-from-path
    Example: Feature identity derives area from parent directory
      Given a feature path "specs/behavior/features/auth/login.feature"
      When specweave extracts the feature identity
      Then the area is "auth"
      And the feature_slug is "login"

    @bdd-feature-identity-no-area
    Example: Feature identity uses "behavior" when no area directory
      Given a feature path "specs/behavior/features/login.feature"
      When specweave extracts the feature identity
      Then the area is "behavior"
      And the feature_slug is "login"

    @bdd-feature-stem-markdown
    Example: feature_stem handles .feature.md suffix
      Given a feature path with .feature.md suffix
      When specweave extracts the stem from "auth/login.feature.md"
      When specweave extracts the stem from "auth/login.feature.md"
      Then the stem is "login"

    @bdd-feature-stem-classic
    Example: feature_stem handles .feature suffix
      Given a feature path with .feature suffix
      When specweave extracts the stem from "auth/login.feature"
      When specweave extracts the stem from "auth/login.feature"
      Then the stem is "login"

  Rule: Canonical test path derivation

    @bdd-canonical-test-path
    Example: Test path is derived from feature path
      Given a feature path "specs/behavior/features/auth/login.feature"
      When specweave derives the canonical test path
      Then the test path is "tests/test_auth_login.py"

  Rule: Scenario iteration yields all scenarios

    @bdd-iter-scenarios-top-level
    Example: Iterator yields top-level scenarios
      Given a Feature with top-level scenarios
      When specweave iterates the feature scenarios
      Then the top-level scenarios are yielded with rule=None

    @bdd-iter-scenarios-in-rules
    Example: Iterator yields scenarios from rules
      Given a Feature with rules containing scenarios
      When specweave iterates the feature scenarios
      Then the rule scenarios are yielded with their rule

  Rule: Scenario ID extraction

    @bdd-scenario-id-value
    Example: scenario_id_value returns first @bdd-* tag
      Given a scenario tagged @bdd-example @ac-0001
      When specweave extracts the scenario id
      Then the id is "bdd-example"

    @bdd-scenario-id-missing
    Example: scenario_id_value returns empty string when no @bdd-* tag
      Given a scenario without @bdd-* tags
      When specweave extracts the scenario id
      Then the id is ""
