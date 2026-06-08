`@area-behavior` `@feature-index`

# Feature: Behavior index and manifest generation

specweave behavior index generates a Markdown index and JSON manifest

from canonical behavior feature files. The manifest maps scenarios to

their test bindings and evidence status.

## Rule: Index generation scans feature files

`@bdd-index-generates-markdown`

### Example: Index generates Markdown with feature listing

- Given canonical behavior feature files exist
- When specweave generates the behavior index
- Then a Markdown file is written
- And the Markdown contains feature titles grouped by area

`@bdd-index-generates-manifest`

### Example: Index generates JSON manifest with scenario mappings

- Given canonical behavior feature files exist
- When specweave generates the behavior index
- Then a JSON manifest file is written
- And the manifest has schema_version 1
- And each feature entry has path, area, feature_slug, and title

`@bdd-index-scenario-entries`

### Example: Manifest includes scenario entries with automation status

- Given a feature file with a scenario bound to a pytest test
- When specweave generates the behavior index
- Then the manifest scenario entry has automation status "bound"
- And the entry includes the test_file and nodeid

`@bdd-index-unbound-scenario`

### Example: Manifest marks unbound scenarios as missing

- Given a feature file with a scenario not bound to any test
- When specweave generates the behavior index
- Then the manifest scenario entry has automation status "missing"

## Rule: Index reflects evidence status

`@bdd-index-evidence-status`

### Example: Manifest includes latest evidence status when available

- Given a feature file with evidence in .specweave/evidence
- When specweave generates the behavior index
- Then the manifest scenario entry has latest_evidence_status

## Rule: Index supports rule blocks

`@bdd-index-rules`

### Example: Manifest preserves Rule structure

- Given a feature file with Rule blocks containing scenarios
- When specweave generates the behavior index
- Then the manifest feature entry has a rules array
- And each rule has id, title, tags, and scenarios
