`@area-trace` `@feature-trace`

# Feature: End-to-end traceability bundle extraction

SpecWeave trace extracts a traceability bundle for a given `@bdd-*` id
or feature path. It reports the feature metadata, linked acceptance
criteria, mapped pytest test references, and any evidence gaps.

## Rule: Trace by bdd-id reports full mapping chain

`@bdd-trace-by-id`

### Example: Trace by bdd-id finds feature, ac tags, test references, and gaps

- Given a feature with a scenario tagged `@bdd-login-success` and `@ac-0001`
- And a pytest test mapped to that scenario via @pytest.mark.specweave
- And no evidence file references the scenario
- When specweave runs `trace bdd-login-success --format json`
- Then the exit code is zero
- And the JSON trace includes the bdd-id and ac-id
- And the JSON trace includes the test function name
- And the JSON trace includes a "missing_evidence" gap

## Rule: Trace by feature path supports markdown features

`@bdd-trace-by-path`

### Example: Trace by .feature.md path reports feature metadata and bdd-ids

- Given a markdown feature file with a `@bdd-*` tagged scenario
- When specweave runs `trace <path> --format json`
- Then the exit code is zero
- And the JSON trace includes the feature path ending in ".feature.md"
- And the JSON trace includes the bdd-id from the feature
