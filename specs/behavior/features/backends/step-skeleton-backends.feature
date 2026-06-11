@area-backends @feature-step-skeleton-backends
Feature: Generate optional step skeletons for BDD backends

  SpecWeave can scaffold step definitions for teams that also use behave or
  pytest-bdd, but plain pytest mapping remains the default SpecWeave path.

  Rule: Select supported backends

    @bdd-backend-registry
    Example: Supported backends are registered
      Given a feature file contains scenario steps
      When I request a step skeleton backend
      Then SpecWeave accepts behave and pytest-bdd
      And SpecWeave rejects unsupported Cucumber backends with a clear message

    @bdd-backend-behave-skeleton
    Example: Behave skeleton contains step functions
      Given a feature contains repeated Given When Then step texts
      When I run specweave bind --backend behave
      Then SpecWeave writes Python step definitions
      And repeated step texts appear once

    @bdd-backend-pytest-bdd-skeleton
    Example: pytest-bdd skeleton contains scenarios and step decorators
      Given a feature contains scenarios and steps
      When I run specweave bind --backend pytest-bdd
      Then SpecWeave writes pytest-bdd imports, scenarios calls, and step decorators

    @bdd-backend-rule-scenarios-included
    Example: Rule scenarios are included in backend skeletons
      Given a feature contains scenarios inside Rule blocks
      When SpecWeave generates backend skeletons
      Then those scenarios and steps are included in the skeleton
