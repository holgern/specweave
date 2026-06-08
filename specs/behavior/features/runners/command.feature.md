`@area-runners` `@feature-command`

# Feature: Delegated command runner

SpecWeave delegates external command execution through a runner that
captures exit codes, stdout, stderr, and writes a normalized summary
JSON artifact. It handles success, failure, and command-not-found cases.

## Rule: Run successful commands

`@bdd-runner-success`

### Example: Successful command writes passed summary

- Given a command that prints to stdout and exits zero
- When specweave runs the command
- Then the exit code is zero
- And a summary.json file is created in the report directory
- And the summary status is "passed"
- And the summary exit_code is 0
- And the summary runner is "command"

## Rule: Run failing commands

`@bdd-runner-failure`

### Example: Failing command writes failed summary

- Given a command that exits with code 1
- When specweave runs the command
- Then the exit code is 1
- And the summary status is "failed"
- And the summary exit_code is 1

## Rule: Run command-not-found

`@bdd-runner-not-found`

### Example: Non-existent command returns error status

- Given a command name that does not exist on the system
- When specweave runs the command
- Then the exit code is -1
- And the summary status is "error"

## Rule: Capture stdout and stderr

`@bdd-runner-capture`

### Example: Stdout and stderr are captured to separate files

- Given a command that writes to stdout and stderr
- When specweave runs the command
- Then stdout.txt exists in the report directory
- And stderr.txt exists in the report directory
- And stdout.txt contains the expected stdout output
- And stderr.txt contains the expected stderr output
