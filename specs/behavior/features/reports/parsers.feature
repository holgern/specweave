@area-reports @feature-parsers
Feature: Report format parsers

  SpecWeave parses JUnit XML and Cucumber JSON reports into ScenarioResult

  instances. Each parser extracts scenario name, status, tags, and evidence.

  Rule: JUnit XML parser extracts test cases

    @bdd-junit-parse-cases
    Example: Parser extracts test cases from JUnit XML
      Given a JUnit XML report with test cases
      When specweave parses the JUnit XML
      Then each test case becomes a ScenarioResult
      And each result has name, status, and nodeid

    @bdd-junit-parse-statuses
    Example: Parser maps JUnit statuses correctly
      Given a JUnit XML report with passed, failed, and skipped tests
      When specweave parses the JUnit XML
      Then passed tests have status "passed"
      And failed tests have status "failed"
      And skipped tests have status "skipped"

    @bdd-junit-parse-duration
    Example: Parser extracts test duration
      Given a JUnit XML report with test durations
      When specweave parses the JUnit XML
      Then each result has duration_ms

  Rule: Cucumber JSON parser extracts scenarios

    @bdd-cucumber-parse-scenarios
    Example: Parser extracts scenarios from Cucumber JSON
      Given a Cucumber JSON report with scenario results
      When specweave parses the Cucumber JSON
      Then each scenario becomes a ScenarioResult
      And each result has feature, name, status, and tags

    @bdd-cucumber-parse-tags
    Example: Parser extracts tags from Cucumber scenarios
      Given a Cucumber JSON report with tagged scenarios
      When specweave parses the Cucumber JSON
      Then each result has the scenario tags
