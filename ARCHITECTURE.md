# Architecture

SharBo Globo separates canonical intelligence, localization, presentation, and production deployment. Each boundary has an explicit contract and fails closed.

## Stages

1. **Collector** discovers candidate information inside a configured time window.
2. **Normalizer** converts candidates into deterministic canonical fields and timezone-aware timestamps.
3. **Deduper** groups substantially identical event claims.
4. **Verifier** attaches evidence and rejects unsupported claims.
5. **Intelligence Scoring** ranks verified signals using deployment-specific policy.
6. **Event / Impact Linking** creates Emerging Signals and Impact Chains with stable IDs.
7. **Localization** produces locale-specific renderable fields without changing canonical IDs.
8. **Validation Gate** enforces full coverage, order, required fields, and structure references.
9. **Presentation** builds reader assets only after an atomic READY marker exists.
10. **Production** validates bundle integrity and retains the last known-good release on failure.

## Invariants

- All timestamps entering cutoff evaluation include an explicit timezone.
- Items outside the canonical window are rejected, not guessed into the window.
- Canonical signal IDs and ordering are identical across locales.
- Every localized signal contains all seven required narrative fields.
- Taiwan Radar coverage equals canonical signal coverage and preserves order.
- Emerging Signal and Impact Chain references resolve to canonical IDs.
- READY is written only after re-reading and validating the final persisted localization bundle.
- Presentation never triggers from individual locale-file writes.

## Repository boundary

The public package owns generic contracts and validators. Deployments own collectors, source registries, trust policies, ranking heuristics, live data, credentials, publishing configuration, and operational records.

No mechanism in this repository reads from or writes to the private production repository.
