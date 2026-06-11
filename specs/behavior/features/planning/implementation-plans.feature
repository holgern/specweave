@area-planning @feature-implementation-plans
Feature: Create implementation plans from behavior features

  SpecWeave can turn accepted behavior into a deterministic implementation plan
  for a coding agent without mutating source code.

  Rule: Plan from a feature file

    @bdd-plan-includes-feature-context
    Example: Plan includes feature and scenario context
      Given a feature contains a title, rules, scenarios, and steps
      When I run specweave create plan --feature feature.feature
      Then SpecWeave writes a plan markdown file
      And the plan includes the feature title
      And the plan includes scenario titles and steps

    @bdd-plan-includes-test-targets
    Example: Plan proposes pytest implementation targets
      Given a behavior feature has scenarios
      When SpecWeave creates a plan
      Then the plan includes expected pytest file names
      And the plan includes TODOs for implementing the scenarios

    @bdd-plan-includes-validation-commands
    Example: Plan includes SpecWeave validation commands
      Given a feature file is used to create a plan
      When SpecWeave writes the plan
      Then the plan includes behavior check, coverage, and pytest validation commands
