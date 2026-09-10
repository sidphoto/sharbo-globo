# Daily automation pipeline

This document describes the **public-safe automation architecture** for SharBo Globo. It captures reusable operational patterns from the live system without copying production source intelligence, provider policy, credentials, data, or private deployment configuration.

## 1. Two layers: reusable core vs deployment policy

SharBo separates automation mechanics from deployment-specific intelligence policy.

### Reusable public core

- report-date and timezone handling;
- cutoff-safe data contracts;
- idempotency;
- deterministic validators;
- multilingual coverage rules;
- atomic publication gates;
- last-known-good behavior;
- presentation/deployment separation;
- external heartbeat monitoring;
- alert-on-failure patterns;
- optional precise external workflow dispatch.

### Deployment-owned policy

- source/provider registries;
- discovery queries and watchlists;
- trust and weighting strategy;
- ranking thresholds and fallback rules;
- raw evidence and live daily data;
- translator/model credentials;
- hosting account/project identifiers;
- recipient and private operations data.

The second category must stay outside this repository.

## 2. Reference lifecycle

A production-grade deployment can compose the public contracts into this state machine:

```text
PRE-CUTOFF
   │
   ├─ optional independent structured observations
   │
CUTOFF CLOSED
   ↓
TRIGGER
   ↓
IDEMPOTENCY GUARD ── already complete ──→ STOP OK
   ↓
COLLECT / NORMALIZE / DEDUPE / VERIFY / RANK
   ↓
CANONICAL VALIDATION ── fail ──→ KEEP LAST-KNOWN-GOOD + ALERT
   ↓
CANONICAL COMMIT
   ↓
LOCALIZATION REQUEST
   ↓
EXTERNAL LOCALIZER
   ↓
RE-READ PERSISTED LOCALES
   ↓
LOCALIZATION GATE ── fail ──→ NO READY
   ↓
READY (FINAL WRITE)
   ↓
PRESENTATION BUILD + PUBLIC-SAFETY GATE
   ↓
DEPLOY
   ↓
EXACT-ASSET SMOKE TEST
   ↓
LIVE
   ↓
INDEPENDENT HEARTBEAT
```

The public repository runs a smaller but executable synthetic version of this lifecycle in `daily-demo.yml`.

## 3. Why idempotency is mandatory

Reliable scheduling often uses more than one trigger: an external scheduler for punctuality and one or more GitHub cron entries as backup. Without an idempotency guard, backup triggers can produce duplicate reports or overlapping deployments.

The public workflow resolves the target report date in `Asia/Taipei`, reads `data/latest.json`, and stops successfully when that date is already represented by a valid `demo=true` artifact.

## 4. Why publication is atomic

Localization and multi-file presentation are not atomic by default. If publication listens to each file write independently, readers can observe a mixed-generation state.

Use an explicit state marker such as READY only after:

1. every expected locale exists;
2. all canonical IDs are represented;
3. required narrative fields are non-empty;
4. structural references resolve;
5. the final persisted files are re-read and validated.

Then write READY **last**. Presentation should trigger from READY, not from individual locale files.

## 5. Failure isolation

Each stage should have one failure domain and a clear consequence:

| Stage | Failure behavior |
| --- | --- |
| trigger | backup scheduler may still run |
| generation | no canonical publication |
| validation | reject new artifact |
| localization | no READY marker |
| presentation | no deployment |
| deployment | last-known-good site remains live |
| heartbeat | open/update an issue; do not mutate production |

A model or provider outage therefore does not automatically become a broken public site.

## 6. Public executable reference

The canonical public repo intentionally uses synthetic data only:

```text
.github/workflows/daily-demo.yml
        ↓
scripts/build_daily_demo.py
        ↓
validate_report.py
validate_i18n.py
validate_public_repo.py
validate_public_ui_boundary.py
        ↓
commit exact synthetic files
        ↓
.github/workflows/pages.yml
        ↓
GitHub Pages
        ↓
.github/workflows/heartbeat.yml
```

The daily builder reuses the checked-in synthetic fixture, shifts all date-bearing timestamps by the report-date delta, and preserves demo-only source URLs. This makes the automation testable every day without simulating access to production intelligence.

## 7. Adapting the public core to a real deployment

For a real installation, keep the public contracts/validators but put deployment policy in a private repository or private configuration layer.

A safe extension typically replaces only the input side:

```text
private provider adapter(s)
      ↓
public canonical contract
      ↓
public validators
      ↓
private localization/deployment configuration
```

Do not add real source registries, provider credentials, private queries, production data, or hosting secrets to this public repository just to make a fork operational.

## 8. Precise scheduling

`examples/external-trigger/` contains a generic Cloudflare Worker that dispatches a GitHub Actions workflow. It is optional: GitHub cron remains the fallback.

The Worker requires only a narrowly scoped GitHub token stored as a Worker secret. Repository owner/name/workflow/ref are configuration values. The example does not contain SharBo production identifiers.

## 9. Observability

A successful workflow run is not proof that the public site is current. The independent heartbeat fetches the live `data/latest.json`, verifies `demo=true` and checks the live report date against the current `Asia/Taipei` date. A mismatch opens or updates a GitHub issue.

This closes the loop:

```text
expected state → build → deploy → observe actual live state
```

## 10. Security boundary

Public automation is subject to the same repository leak gate as all other contributions. In particular:

- public JSON source URLs remain `example.invalid`;
- private production directories are rejected;
- production-only workflow tokens are rejected;
- the public workflow commits an explicit allowlist of synthetic output files rather than an entire data directory;
- secrets exist only in the runtime secret store of whichever deployment an adopter owns.
