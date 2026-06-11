@area-execution @feature-delegated-runner
Feature: Run delegated validation commands

  SpecWeave can execute an external command and capture its outputs, but it does
  not replace pytest, Cucumber, behave, or a project-specific test runner.

  Rule: Capture command execution

    @bdd-runner-success-summary
    Example: Successful delegated command writes a passed summary
      Given a delegated command exits with status 0
      When I run specweave run -- that command
      Then SpecWeave records a passed runner summary
      And stdout and stderr are captured separately

    @bdd-runner-failure-summary
    Example: Failing delegated command writes a failed summary
      Given a delegated command exits with a non-zero status
      When I run specweave run -- that command
      Then SpecWeave records a failed runner summary
      And the command exits with failure

    @bdd-runner-command-not-found
    Example: Missing commands are reported as runner errors
      Given the delegated command cannot be found
      When I run specweave run -- missing-command
      Then SpecWeave records an error summary
      And the command exits with failure
