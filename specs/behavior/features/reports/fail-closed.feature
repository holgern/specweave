@area-reports @feature-fail-closed
Feature: Fail-closed evidence semantics
  SpecWeave enforces fail-closed semantics for acceptance criteria. A
  criterion is passed only when every linked scenario passed. Skipped,
  pending, undefined, ambiguous, errored, or failed scenarios block
  the criterion.

  Rule: Blocking statuses fail linked criteria

    @bdd-fail-closed-failed-scenario
    Example: Failed scenario fails the linked criterion
      Given a scenario tagged @ac-0001 with status "failed"
      When specweave evaluates the criterion
      Then the criterion status is "failed"

    @bdd-fail-closed-skipped-scenario
    Example: Skipped scenario fails the criterion by default
      Given a scenario tagged @ac-0001 with status "skipped"
      When specweave evaluates the criterion
      Then the criterion status is "failed"

    @bdd-fail-closed-undefined-scenario
      Example: Undefined scenario fails the criterion
      Given a scenario tagged @ac-0001 with status "undefined"
      When specweave evaluates the criterion
      Then the criterion status is "failed"

    @bdd-fail-closed-pending-scenario
      Example: Pending scenario fails the criterion
      Given a scenario tagged @ac-0001 with status "pending"
      When specweave evaluates the criterion
      Then the criterion status is "failed"

    @bdd-fail-closed-ambiguous-scenario
      Example: Ambiguous scenario fails the criterion
      Given a scenario tagged @ac-0001 with status "ambiguous"
      When specweave evaluates the criterion
      Then the criterion status is "failed"

  Rule: Only passing scenarios satisfy criteria

    @bdd-fail-closed-passed-scenario
    Example: Passed scenario satisfies the criterion
      Given a scenario tagged @ac-0001 with status "passed"
      When specweave evaluates the criterion
      Then the criterion status is "passed"

  Rule: Unlinked scenarios do not affect criteria

    @bdd-fail-closed-unlinked-scenario
    Example: Unlinked scenario does not satisfy any criterion
      Given a scenario without @ac-* tags with status "passed"
      When specweave evaluates criteria
      Then the scenario does not appear in any criterion

  Rule: Multiple scenarios for one criterion

    @bdd-fail-closed-multiple-scenarios
    Example: One failed scenario fails the whole criterion
      Given two scenarios tagged @ac-0001, one passed and one failed
      When specweave evaluates the criterion
      Then the criterion status is "failed"

  Rule: Exit code alone is not sufficient evidence

    @bdd-fail-closed-exit-code-not-evidence
    Example: Passing exit code does not override failed scenarios
      Given a report with a failed scenario
      When specweave normalizes the report
      Then the overall status is "failed"
      And the exit code is not used as acceptance evidence
