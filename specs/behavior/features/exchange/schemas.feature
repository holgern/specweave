@area-exchange @feature-schemas
Feature: Exchange schema contracts

  SpecWeave defines JSON Schema documents for its file-based exchange
  formats. These schemas enforce the contract for combi traces, Taskledger
  BDD exports, behavior evidence, and Archledger candidates.

  Rule: Schema files are valid JSON Schema documents

    @bdd-exchange-schema-valid
    Example: Each exchange schema is a valid JSON Schema
      Given the schema directory contains exchange schema files
      When specweave loads a schema
      Then the $schema field points to JSON Schema draft 2020-12
      And the type is "object"
      And the schema declares required fields

  Rule: Representative payloads satisfy schema requirements

    @bdd-exchange-combi-trace-schema
    Example: Combi trace representative payload satisfies required fields
      Given a representative combi trace payload with producer, target, traces, and gaps
      When checked against the trace schema required fields
      Then all required fields are present in the payload
      And removing a required field causes the check to fail

    @bdd-exchange-taskledger-schema
    Example: Taskledger BDD export representative payload satisfies schema
      Given a representative Taskledger BDD export payload
      When checked against the export schema required fields
      Then all required fields including task_id, feature, rules, and examples are present

    @bdd-exchange-evidence-schema
    Example: Behavior evidence representative payload satisfies schema
      Given a representative behavior evidence payload
      When checked against the evidence schema required fields
      Then all required fields including schema_version, task_id, status, criteria, and scenarios are present

    @bdd-exchange-archledger-schema
    Example: Archledger candidate representative payload satisfies schema
      Given a representative Archledger candidate payload
      When checked against the candidate schema required fields
      Then all required fields including schema, producer, and candidate are present
