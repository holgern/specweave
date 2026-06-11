# Integrations

## Taskledger

Taskledger exchange is file-based. SpecWeave reads acceptance exports and writes
canonical `.feature` files or normalized evidence JSON.

Default behaviour mapping location:

```text
specs/behaviour/mappings/taskledger/
```

## Archledger

SpecWeave can render draft candidate markdown for Archledger. It does not
create accepted architecture records by default. Behaviour scenarios and
specification requirements can both be rendered as candidate records.

## External runners

SpecWeave delegates execution. Native reports such as JUnit XML or Cucumber
JSON are the evidence inputs; stdout and exit code alone are not sufficient.
