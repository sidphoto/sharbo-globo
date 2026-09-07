# Public data contract

The public preview distinguishes machine-readable canonical data from localized presentation text. It now models both verified news signals and a separate structured-observation channel.

## Canonical report

Each synthetic report contains:

- a report date and an explicit `Asia/Taipei` window;
- unique news signal IDs and a stable `top5_ids` projection;
- evidence records with a source class and URL;
- `window_verified` state for cutoff-safe news items;
- optional `structured_signals` for machine-readable observations;
- optional Emerging Signals and Impact Chains that reference existing news signal IDs;
- a Taiwan Radar section;
- an explicit demo marker.

The public validator rejects duplicate IDs, missing references, invalid timestamps, incomplete evidence, invalid report modes, inconsistent structured counts and non-demo URLs.

## News signal narrative fields

The public news narrative contract uses seven fields:

```text
title
what_happened
why_now
why_important
winners_losers
taiwan_impact
what_next
```

The contract describes shape and validation behavior. It does not disclose production ranking values, source weights, thresholds or editorial queries.

## Best-effort Top 5

`top5_ids` is a projection over verified news signals, not a guarantee that five authoritative items always exist.

For a normal news-bearing report:

- at least one verified news signal must exist;
- `top5_ids` contains between 1 and 5 IDs;
- every Top item resolves to a news signal in the report;
- every Top item is window verified;
- every Top item has at least one `PRIMARY` or `CONFIRMED` evidence source.

The public contract therefore demonstrates fail-closed authority without inventing filler simply to reach five items.

## Structured observations

`structured_signals` is a separate reader-facing block. It may contain official or machine-readable observations projected to a generic schema with:

- unique observation IDs;
- timezone-aware observation/update timestamps;
- canonical `metrics`;
- a source URL;
- topic/category metadata;
- reader metadata such as level/band/score;
- optional `text` rendered for `zh-TW`, `en`, and `vi-VN` from the same canonical metrics.

Structured observations do not use the seven news narrative fields and are not included in `top5_ids`.

See [Structured observations — public contract](STRUCTURED_SIGNALS_CONTRACT.md).

## Report modes

A normal report can contain news signals, structured observations, or both.

`quality.mode = "structured_only"` is a special fail-safe mode:

- `signals` must be empty;
- `top5_ids` must be empty;
- at least one structured observation must exist.

A report with neither qualifying news nor structured observations is invalid and fails closed.

## Topic counts

`topic_summary[].count` is the reader-facing total for that topic. If `structured_count` is present, it is a breakdown of the structured contribution already included in `count`.

This distinction matters for idempotent rebuilds: a rerun must replace/recompute the structured contribution rather than increment the existing total again.

## Impact Chain semantics

An edge marked `SUPPORTED` must include evidence news signal IDs. An edge marked `POTENTIAL` is an explicitly labeled transmission scenario and must not include evidence IDs. This prevents a deterministic scenario rule from being presented as observed causality.

## Public/private boundary

The public contract intentionally omits:

- production provider names and allowlists;
- real source domains;
- scoring weights and thresholds;
- domain qualification rules;
- watchlists and provider configuration;
- raw snapshots/evidence corpus;
- production schedules and operational state.

Public fixtures use synthetic provider/source names and `example.invalid` URLs.
