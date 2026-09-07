# Architecture

SharBo Globo separates canonical intelligence, structured observations, localization, presentation, and deployment. Each boundary has an explicit contract and fails closed.

This public document describes reusable architecture only. Deployment-specific sources, provider configuration, thresholds, weights, queries, watchlists, credentials and operational state remain private.

## Input plane: independent channels

SharBo can ingest two different classes of information without coupling their failure modes.

```text
News / event channel                  Structured observation channel
        │                                         │
        ▼                                         ▼
   Collector(s)                              Provider adapters
        │                                         │
   Normalizer                                   Normalizer
        │                                         │
     Deduper                                Domain qualification
        │                                         │
    Verifier                                     │
        │                                         │
Intelligence scoring                       Reader-safe projection
        │                                         │
        └──────────────┐             ┌─────────────┘
                       ▼             ▼
                         Daily report
                  signals + structured_signals
```

The channels are deliberately independent:

- a news retrieval failure must not erase valid structured observations;
- a structured-provider failure must not invalidate otherwise valid news intelligence;
- failure in one channel is surfaced as degraded state rather than silently changing the semantics of the other;
- structured observations are not a promotion path for news that failed verification.

## Canonical report plane

The daily report keeps the channels separate:

- `signals`: verified news/event intelligence used by `top5_ids`, narrative fields, Emerging Signals and Impact Chains;
- `structured_signals`: reader-safe observations with canonical metrics, evidence links and optional multilingual rendered text;
- `topic_summary`: counts may include both channels, with `structured_count` used only as a breakdown of an already-included total.

A normal report can contain both channels. If no qualifying news exists but structured observations do, `quality.mode = "structured_only"` allows the report to publish with an empty `signals` / `top5_ids` pair. If neither channel has publishable information, the system still fails closed.

## Processing stages

1. **News Collection** discovers candidate information inside the configured window.
2. **News Normalization / Deduplication** converts candidates into canonical, timezone-aware event records and groups duplicate claims.
3. **Verification** attaches evidence and rejects unsupported news claims.
4. **News Intelligence Scoring** ranks verified news using deployment-specific policy.
5. **Structured Collection** independently obtains machine-readable observations through provider adapters.
6. **Structured Qualification** determines whether an observation is meaningful before ranking; the deployment policy for doing so is private.
7. **Reader-safe Projection** strips private scoring internals and projects allowed observation fields into `structured_signals`.
8. **Event / Impact Linking** creates Emerging Signals and Impact Chains from eligible canonical news signals.
9. **Localization** localizes narrative text while preserving canonical IDs. Metric-bearing structured observations may render locale text from the same canonical metrics so numbers cannot diverge by language.
10. **Validation Gate** enforces coverage, references, time safety, report-mode invariants and public/private boundaries.
11. **Presentation** re-applies any idempotent report projections needed for the report being rebuilt, then creates reader assets only from validated state.
12. **Deployment** validates bundle integrity and retains the last known-good release on failure.

## Idempotency and schedule independence

Independent collectors can finish in different orders. Presentation must therefore not depend on a particular cron winning a race.

Reusable rule:

```text
rebuild(report_date)
  → read current canonical report
  → re-project current structured observation set for that report date
  → recompute derived counts from base + current contribution
  → validate
  → render
```

Derived counts are recomputed rather than blindly incremented. Re-running the same build must produce the same result, and a shrinking observation set must shrink the derived reader state.

## Localization invariants

- Canonical news signal IDs and ordering are identical across locales.
- Every localized news signal contains the seven required narrative fields.
- Structured observation metrics remain canonical across locales.
- If structured observations expose rendered `text`, `zh-TW`, `en`, and `vi-VN` are generated from the same underlying metrics rather than translated independently.
- READY is written only after re-reading and validating the final persisted localization state.
- Presentation never triggers from individual locale-file writes.

## Emerging Signal and Impact Chain invariants

- Emerging Signal references resolve to canonical news signal IDs.
- Impact Chain anchors and `SUPPORTED` evidence IDs resolve to canonical news signal IDs.
- `SUPPORTED` edges require evidence IDs.
- `POTENTIAL` edges are explicit scenarios and must not masquerade as observed causality.

## Reader-safe archive

Historical presentation should use a reduced digest rather than exposing the full current-day drill-down contract. A reader-safe archive may retain summary, topic distribution, selected headline metadata, Taiwan relevance, market snapshot and featured-chain title while omitting private evidence and detailed production-only fields.

## Repository boundary

`sidphoto/sharbo-globo` owns the canonical public contracts, validators, reference UI, synthetic fixtures and reusable architecture. Deployments own collectors, source/provider registries, trust policies, ranking heuristics, thresholds, live data, raw snapshots, credentials, publishing configuration and operational records.

No mechanism in this repository reads from or writes to the private production repository.

See also:

- [Public data contract](docs/DATA_CONTRACT.md)
- [Structured observations contract](docs/STRUCTURED_SIGNALS_CONTRACT.md)
- [Public-safe synchronization policy](docs/PUBLIC_SYNC_POLICY.md)
- [Demo / production separation](docs/DEMO_AND_PRODUCTION.md)
