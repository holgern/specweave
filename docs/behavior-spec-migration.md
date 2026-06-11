# Behavior spec migration note

The product-level Gherkin suite in `specweave_fit_gherkin.zip` was used as the target behavior layer. The current implementation was not blindly replaced. Low-level contracts remain enforced by the existing pytest unit tests unless they describe public CLI or file-format behavior.

## Retained as product behavior

These workflows are now primary under `specs/behavior/features`:

- project initialization and configuration resolution
- canonical feature authoring and supported Gherkin subset
- pytest-to-Gherkin brownfield discovery
- plain pytest skeleton generation
- explicit mappings, autolink, and bidirectional coverage
- evidence normalization with fail-closed semantics
- project health review and golden review workflow
- behavior index and manifest generation
- implementation plan creation
- delegated runner summaries
- Taskledger, Archledger, and combi read-only exchange/audit behavior
- scriptable CLI JSON and compatibility aliases

## Rewritten or moved

Former module-shaped feature files were consolidated into product workflow files:

- `behavior/coverage.feature`, `behavior/autolink.feature`, and `reports/mapping.feature` became `review/static-coverage-review.feature` and `traceability/mapping-and-autolink.feature`.
- `gherkin/parser.feature`, `gherkin/writer.feature`, `gherkin/lint.feature`, `gherkin/official.feature`, and `gherkin/markdown.feature` became `authoring/canonical-feature-authoring.feature` and `authoring/gherkin-subset.feature`.
- `reports/normalization.feature`, `reports/parsers.feature`, and `reports/fail-closed.feature` became `evidence/report-normalization.feature`.
- `init/initialization.feature` and `config/configuration.feature` became `setup/project-initialization.feature` and `configuration/configuration-resolution.feature`.
- `review/spec-review.feature`, `doctor/diagnostics.feature`, and behavior refresh coverage became `review/project-health-review.feature` plus `review/static-coverage-review.feature`.

## Demoted to unit-test-only coverage

The following old Gherkin areas described implementation internals rather than product workflows and are no longer first-class behavior specs:

- `common/behavior-helpers.feature`
- `python-inspect/ast-reader.feature`
- parser tokenization and writer round-trip micro-contracts that are not externally visible
- helper-level slug, title, and path derivation rules except where exposed through CLI output or file formats

Existing pytest tests continue to protect these contracts. Their SpecWeave mappings should be removed or waived as internal helper coverage during follow-up binding cleanup.

## New golden review command

Use this command as the coding-agent default review path:

```bash
specweave review golden
```

It aggregates doctor, behavior check, bidirectional coverage, mapping inventory, and spec review. It writes:

- `specs/behavior/reports/specweave/coverage-gaps.md`
- `specs/behavior/reports/specweave/mappings.json`
- `specs/behavior/reports/specweave/review.json`

Bidirectional coverage is the documented default. Plain pytest remains the enforcement path. pytest-bdd is optional skeleton output only.
