@area-integrations @feature-taskledger-exchange
Feature: Exchange behavior intent and evidence with Taskledger

  SpecWeave exchanges files with Taskledger while leaving task lifecycle ownership
  in Taskledger.

  Rule: Import Taskledger acceptance exports

    @bdd-taskledger-import-feature
    Example: Import a Taskledger BDD export as a canonical feature
      Given a Taskledger acceptance export contains task id, acceptance criteria, and BDD examples
      When I run specweave behavior import-taskledger export.json --out feature.feature
      Then SpecWeave writes a canonical .feature file
      And task, rule, bdd, and acceptance-criterion ids are preserved as tags

    @bdd-taskledger-import-legacy-shape
    Example: Legacy Taskledger export shapes are accepted when possible
      Given a legacy Taskledger acceptance export contains acceptance criteria
      When SpecWeave imports the export
      Then SpecWeave creates equivalent behavior scenarios

  Rule: Export Task-BDD JSON and draft tasks

    @bdd-taskledger-bdd-round-trip
    Example: Task-BDD JSON round-trips through Gherkin
      Given a Task-BDD JSON file contains rules and examples
      When I run specweave bdd export and then specweave bdd import-feature
      Then task ids, rule ids, bdd ids, ac ids, and custom tags are preserved

    @bdd-taskledger-draft-from-feature
    Example: Create a Taskledger task draft from behavior
      Given a feature contains scenarios tagged with @ac-* acceptance criteria
      When I run specweave create taskledger-task --feature feature.feature
      Then SpecWeave writes a Taskledger draft JSON
      And each @ac-* tag becomes an acceptance criterion reference

  Rule: Write Taskledger-compatible evidence

    @bdd-taskledger-evidence-from-normalized-report
    Example: Normalized BDD evidence can be written for Taskledger
      Given a normalized report contains scenario results and task tags
      When I run specweave report normalize --evidence
      Then SpecWeave writes Taskledger-compatible evidence JSON
