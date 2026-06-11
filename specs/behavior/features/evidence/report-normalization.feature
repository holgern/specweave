@area-evidence @feature-report-normalization
Feature: Normalize runner reports into behavior evidence

  SpecWeave converts runner-native reports into stable evidence and fails closed
  when the evidence is missing, incomplete, or not passing.

  Rule: Normalize supported report formats

    @bdd-report-normalize-junit
    Example: Normalize pytest JUnit XML
      Given pytest has produced a JUnit XML report
      When I run specweave report normalize --format junit-xml
      Then SpecWeave emits normalized scenario results
      And the command fails when any normalized result is not passed

    @bdd-report-normalize-cucumber
    Example: Normalize Cucumber JSON
      Given a BDD runner has produced a Cucumber JSON report
      When I run specweave report normalize --format cucumber-json
      Then SpecWeave emits normalized scenario results with tags and statuses

    @bdd-report-normalize-rejects-unknown-format
    Example: Unsupported report formats are rejected
      Given a report format is not junit-xml or cucumber-json
      When I run specweave report normalize with that format
      Then SpecWeave reports the unsupported format
      And the command exits with failure

  Rule: Fail closed on acceptance evidence

    @bdd-report-fail-closed-failed
    Example: Failed scenarios block acceptance
      Given a report contains a failed scenario linked to @ac-login
      When SpecWeave summarizes acceptance criteria
      Then @ac-login is failed

    @bdd-report-fail-closed-skipped
    Example: Skipped scenarios block acceptance by default
      Given a report contains a skipped scenario linked to @ac-login
      When SpecWeave normalizes the report
      Then the report status is failed

    @bdd-report-expect-ac
    Example: Expected acceptance criteria must have passing evidence
      Given I require @ac-login with --expect-ac
      And the report has no passing scenario linked to @ac-login
      When I run specweave report normalize
      Then SpecWeave fails the command because expected coverage is missing

  Rule: Import pytest evidence for behavior mappings

    @bdd-behavior-import-report-maps-tests
    Example: Import pytest JUnit evidence through behavior mappings
      Given a behavior manifest maps pytest nodeids to @bdd-* scenarios
      And pytest has produced a JUnit XML report
      When I run specweave behavior import-report
      Then SpecWeave writes pytest behavior evidence JSON
      And each mapped test result references the behavior scenario

    @bdd-behavior-import-report-unmapped-fails
    Example: Unmapped pytest results fail behavior evidence import
      Given a pytest JUnit report contains a test without SpecWeave mapping
      When I run specweave behavior import-report
      Then the evidence includes the unmapped test
      And the command exits with failure
