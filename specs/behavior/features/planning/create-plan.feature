@area-planning @feature-create-plan
Feature: Implementation plan generation from features

  SpecWeave generates implementation-plan Markdown from a Gherkin feature
  file. The plan includes the feature title, scenario steps, implementation
  TODOs, and validation command references.

  Rule: Create plan from a feature file

    @bdd-plan-create
    Example: Plan includes feature title and implementation TODOs
      Given a feature file with a Feature title, Rule, and Scenario
      When specweave creates a plan from the feature
      Then the output plan file exists
      And the plan contains the Feature title
      And the plan contains an "Implementation TODOs" section
      And the plan contains a "Validation" section

    @bdd-plan-includes-scenario-steps
    Example: Plan includes Given, When, Then steps from the feature
      Given a feature file with a Scenario containing specific steps
      When specweave creates a plan from the feature
      Then the plan includes the Given step text
      And the plan includes the When step text
      And the plan includes the Then step text

    @bdd-plan-validation-commands
    Example: Plan includes specweave validation command references
      Given a feature file in the features directory
      When specweave creates a plan from the feature
      Then the plan includes "specweave doctor"
      And the plan includes "specweave review specs"
