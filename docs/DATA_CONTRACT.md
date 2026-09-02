# Public data contract

The public preview distinguishes machine-readable canonical data from localized presentation text.

## Canonical report

Each synthetic report contains:

- a report date and an explicit `Asia/Taipei` window;
- unique signal IDs and a stable `top5_ids` projection;
- evidence records with a source class and URL;
- `window_verified` state for cutoff-safe items;
- optional Emerging Signals and Impact Chains that reference existing signal IDs;
- a Taiwan Radar section;
- an explicit demo marker.

The public validator rejects duplicate IDs, missing references, invalid cutoff timestamps, incomplete evidence, and non-demo URLs.

## Signal narrative fields

The public narrative contract uses seven fields:

```text
title
what_happened
why_now
why_important
winners_losers
taiwan_impact
what_next
```

The contract describes shape and validation behavior. It does not disclose production ranking values, source weights, or editorial queries.

## Impact Chain semantics

An edge marked `SUPPORTED` must include evidence signal IDs. An edge marked `POTENTIAL` is an explicitly labeled transmission scenario and must not include evidence IDs. This prevents a deterministic scenario rule from being presented as observed causality.
