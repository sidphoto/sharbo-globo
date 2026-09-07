# Public-safe synchronization policy

`sidphoto/sharbo-globo` is the canonical public SharBo Globo repository. The deployment and intelligence operation remains in a separate private repository. The old `sidphoto/shrimp-intelligence` repository is legacy and must not remain the long-term upstream for new reusable architecture.

The goal is **architecture parity without intelligence leakage**.

## What may move from product development into the public repository

### Public by default

These are reusable product/engineering ideas and should normally be reflected here:

- canonical field shapes and stable-ID rules;
- validation semantics and fail-closed behavior;
- public reader components and interaction patterns;
- multilingual contract behavior;
- Emerging Signal and Impact Chain semantics;
- reader-safe archive digest shapes;
- structured-observation reader contracts;
- generic retry, idempotency and failure-isolation patterns;
- synthetic fixtures and regression tests.

### Public only after sanitization

These need an explicit public projection before publication:

- reader-facing projections of a richer private schema;
- UI changes first developed against production data;
- generic descriptions of a new collector/provider interface;
- scoring *interfaces* without deployment weights or thresholds;
- operational patterns described without schedules, credentials or private paths.

### Private only

These never move into this repository:

- real source registry, domains, discovery queries or watchlists;
- provider allowlists used by production;
- ranking weights, thresholds, relevance policy and editorial heuristics;
- raw provider snapshots or production evidence corpus;
- real daily reports or historical production archives;
- credentials, recipient data, deployment secrets or environment values;
- production schedules, incident records, alert routing and operational state;
- private repository identifiers used as runtime dependencies.

## Promotion workflow

A production improvement is promoted publicly by **reimplementation or sanitization**, never by blindly mirroring the private repository.

```text
Production change
      ↓
Classify: public / sanitize / private-only
      ↓
Public contract or component + synthetic fixture
      ↓
Public leak gate + tests + multilingual validation
      ↓
Immutable public commit
      ↓
Optional: production vendors or re-pins that public commit
```

The public repository has no automation that reads from the private repository. This is intentional: a one-way automatic mirror would turn a classification mistake into a data leak.

## Reader source-of-truth migration

The target state is:

```text
sidphoto/sharbo-globo
  └─ canonical public reader/contracts
          ↓ pinned immutable commit
Private production repository
  └─ vendored production reader + private patches/gates
```

`sidphoto/shrimp-intelligence` may remain temporarily as a pinned compatibility source while existing reader code is reconciled, but **new reusable reader architecture should land in `sharbo-globo` first**. Once the production reader is pinned to an immutable `sharbo-globo` commit and passes its private security gate, the legacy repository should cease to be an upstream.

## Drift review

When production adds a reader-facing field, mode, section or interaction, review whether the public repository needs one of the following:

1. contract update;
2. synthetic fixture update;
3. validator/test update;
4. reference UI update;
5. documentation only;
6. no public change because the feature is deployment-specific.

A difference is acceptable when deliberate and documented. Silent contract drift is not.

## Licensing and project wording

SharBo Globo remains **source-available, not OSI Open Source**. The public/private engineering boundary and the software license are separate concerns: publishing a reusable contract or reference implementation does not disclose the private intelligence operation, and the PolyForm Noncommercial / commercial-license model continues to apply.
