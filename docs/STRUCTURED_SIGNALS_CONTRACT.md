# Structured observations — public contract

SharBo may combine two reader-facing channels in one daily report:

- `signals`: verified news/event intelligence;
- `structured_signals`: official or machine-readable observations projected into a reader-safe shape.

This public contract describes the **shape and invariants only**. It intentionally does not publish production providers, provider configuration, source allowlists, watchlists, scoring weights, thresholds or raw snapshots.

## Why a separate block

`top5_ids` indexes the news `signals` array, and news signals carry narrative fields such as `why_important` and `what_next`. Structured observations are facts with different semantics, so they remain under a separate `structured_signals` block instead of being mixed into the news array.

## Reader-safe shape

A public/synthetic structured block may use this shape:

```json
{
  "structured_signals": {
    "schema_version": "1.0",
    "generated_at": "2026-01-15T05:40:00+08:00",
    "providers": [
      {"provider": "demo-provider", "status": "ok"}
    ],
    "counts": {"published": 1},
    "buckets": {
      "observation": [
        {
          "id": "demo-observation-001",
          "text": {
            "zh-TW": "DEMO：合成觀測資料",
            "en": "DEMO: synthetic observation",
            "vi-VN": "DEMO: quan sát tổng hợp"
          },
          "provider": "demo-provider",
          "category": "demo_observation",
          "topic": "science",
          "topic_slug": "science",
          "subtype": "synthetic",
          "title": "Synthetic observation",
          "observed_at": "2026-01-15T05:30:00+08:00",
          "updated_at": "2026-01-15T05:30:00+08:00",
          "geography": {"label": "Demo Region"},
          "metrics": {"value": 1},
          "source": {
            "name": "Example Source",
            "url": "https://example.invalid/observation/001",
            "type": "official"
          },
          "signal": {
            "level": "watch",
            "band": "candidate",
            "score": 70,
            "reasons": ["Synthetic fixture"]
          }
        }
      ]
    }
  }
}
```

## Invariants

- observation IDs are unique inside the structured block;
- all timestamps are timezone-aware;
- reader-facing observations cannot use timestamps after the report cutoff;
- every published observation has a source URL;
- metric-bearing text is rendered for `zh-TW`, `en`, and `vi-VN` from the same canonical metrics so numbers cannot drift by locale;
- score, level and band may be exposed as reader metadata, but the policy that produced them is deployment-specific;
- public fixtures use synthetic provider names and `example.invalid` URLs only;
- `topic_summary[].structured_count`, when present, is a breakdown of observations already included in the topic's total count and must never be additively accumulated across reruns.

## `structured_only` mode

A report may be marked `quality.mode = "structured_only"` when there are no qualifying news signals but there are valid structured observations.

For this mode:

- `signals` is empty;
- `top5_ids` is empty;
- `structured_signals` contains at least one published observation;
- the report still passes validation and may be presented;
- a day with neither qualifying news nor structured observations still fails closed.

This fallback does not weaken the news evidence bar. Structured observations are a separate channel, not a promotion path for news that failed verification.

## Idempotent merge

Structured observations can arrive on a schedule independent from the news pipeline. Rebuilding presentation must therefore be safe to re-run:

- the structured block is replaced/projected from the current observation set;
- topic counts remove the previous structured contribution before applying the new one;
- reruns cannot inflate counts;
- a shrinking observation set must shrink the reader-facing block as well;
- the merge resolves the report date from the report being rebuilt, not only from the wall clock.
