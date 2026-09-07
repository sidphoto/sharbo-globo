# 🦐 SharBo Globo｜蝦報。全球情報雷達

> **Verified signals from global noise.**

[![Public Validation Gate](https://github.com/sidphoto/sharbo-globo/actions/workflows/validation.yml/badge.svg)](https://github.com/sidphoto/sharbo-globo/actions/workflows/validation.yml)

**[Public Site](https://sidphoto.github.io/sharbo-globo/)** · **[Interactive Demo](https://sidphoto.github.io/sharbo-globo/demo.html?lang=zh-TW#/today)** · **[Architecture](ARCHITECTURE.md)**

SharBo Globo is a **source-available, multilingual intelligence pipeline** that turns global information noise and structured observations into verified, ranked and connected reader-facing signals.

It is built around explicit evidence, cutoff-safe time windows, independent failure domains, fail-closed validation and atomic multilingual publishing. It is **not** a generic AI news summarizer: incomplete or inconsistent data is not allowed to reach the presentation layer simply because a model can generate plausible prose.

## What the public preview shows

- **Evidence-first news signals** with stable canonical IDs;
- **cutoff-safe contracts** with timezone-aware timestamps;
- **best-effort Top 5** semantics: authoritative 1–5, never filler just to reach five;
- a separate **structured observations** contract for machine-readable facts;
- a fail-safe **`structured_only`** report mode when valid observations exist but no news clears the news bar;
- **Emerging Signals** trend contracts;
- **Impact Chains** with `SUPPORTED` vs `POTENTIAL` relationships;
- **zh-TW / English / Tiếng Việt** overlays with canonical IDs preserved across locales;
- metric-bearing observation text rendered from the same canonical values across all three languages;
- **fail-closed localization validation**;
- **Explain Mode** that makes the public contracts visible inside the demo;
- reader-safe archive concepts rather than full historical production disclosure;
- a responsive intelligence surface modeled after the current SharBo product generation;
- synthetic fixtures only — no production intelligence is published here.

## Public site vs interactive demo

The GitHub Pages root is the project entry point:

```text
/
└─ Project landing
   ├─ product idea
   ├─ public/private boundary
   ├─ architecture
   └─ Open Demo

/demo.html?lang=zh-TW#/today
└─ Interactive synthetic intelligence surface
   ├─ Today
   ├─ Global Radar
   ├─ Emerging Signals
   ├─ Business
   ├─ My Radar
   ├─ Archive
   └─ Signal Detail + Public Contract Inspector
```

The public demo uses the same class of information hierarchy and interaction language as the live product, while keeping the production intelligence boundary intact.

## Architecture

SharBo now models two independent input channels:

```text
News / event channel                     Structured observation channel
Collector → Normalize → Dedupe           Provider adapter → Normalize
        → Verify → Rank                          → Qualify → Project
                 │                                  │
                 └──────────────┬───────────────────┘
                                ▼
                Daily canonical reader contract
                 signals + structured_signals
                                ↓
               Trends / Impact + Localization
                                ↓
                     Validation Gate
                                ↓
                       Presentation
```

The public repository exposes the reusable contracts, validators and synthetic examples behind this architecture. Deployment-specific source/provider policy is intentionally excluded.

See [Architecture](ARCHITECTURE.md) and [Structured observations contract](docs/STRUCTURED_SIGNALS_CONTRACT.md).

## Public / private boundary

### Included here

- reusable data and localization contracts;
- best-effort / structured-only report-mode semantics;
- generic structured-observation shape and validation rules;
- validators and tests;
- public UI and reference implementation;
- synthetic demo fixtures;
- architecture, governance and contribution documentation.

### Intentionally excluded

- production source/provider registry and real source domains;
- discovery queries and watchlists;
- trust strategy, source weighting and ranking thresholds;
- production relevance/fallback heuristics;
- provider configuration and raw snapshots;
- production data and archives;
- API keys, credentials, recipients, schedules and operational records.

The production system remains in a separate **private repository with independent Git history**. The public UI has no code path that reads from or writes to that private repository.

Architecture updates are promoted through a sanitization/classification process rather than an automatic private→public mirror. See [Public-safe synchronization policy](docs/PUBLIC_SYNC_POLICY.md).

## Repository roles

```text
sidphoto/sharbo-globo
  Canonical public project / contracts / reference UI

Private production repository
  Deployment and intelligence operation

sidphoto/shrimp-intelligence
  Legacy compatibility history — not the target upstream for new architecture
```

Reusable reader work should converge on `sharbo-globo`; production should consume immutable, validated public commits where appropriate rather than letting the legacy repository remain the long-term source of truth.

## Quick start

Requires Python 3.11 or later.

```bash
python -m pip install -e '.[dev]'
python -m sharbo_globo.validator examples/data/localization-bundle.json
python -m pytest
```

Run the static public site locally:

```bash
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080/
http://localhost:8080/demo.html?lang=zh-TW#/today
```

The demo needs no API key. Public evidence fixtures use `example.invalid` and are intentionally synthetic.

## Validation

```bash
python -m unittest discover -s tests -v
pytest
python scripts/validate_public_repo.py
python scripts/validate_public_ui_boundary.py
python scripts/validate_i18n.py
python scripts/validate_report.py data/latest.json
node --check app.js
node --check public-v02.js
```

The validation gate fails closed if public contracts, multilingual coverage, report-mode invariants, demo data or repository-boundary rules are violated.

## Documentation

- [Architecture](ARCHITECTURE.md)
- [Public-safe synchronization policy](docs/PUBLIC_SYNC_POLICY.md)
- [Public data contract](docs/DATA_CONTRACT.md)
- [Structured observations contract](docs/STRUCTURED_SIGNALS_CONTRACT.md)
- [Public v0.2 redesign contract](docs/PUBLIC_V0.2_REDESIGN.md)
- [Localization contract](docs/LOCALIZATION_CONTRACT.md)
- [Demo / production separation](docs/DEMO_AND_PRODUCTION.md)
- [Data policy](DATA_POLICY.md)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)
- [Disclaimer](DISCLAIMER.md)
- [Roadmap](docs/ROADMAP.md)

## License

SharBo Globo is **source-available, not OSI Open Source**.

Personal, educational, research and other qualifying noncommercial uses are licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE). Commercial SaaS, hosted services, enterprise deployment, OEM / white-label, paid data products and other commercial use require a separate license; see [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md).

`SharBo Globo`、`蝦報全球` 與相關品牌識別不隨 software license 授權，詳見 [TRADEMARKS.md](TRADEMARKS.md)。

---

## 中文說明

**蝦報。全球情報雷達**不是把新聞丟給 AI 後產生摘要，而是把新聞事件與結構化觀測分成不同資料通道，再用資料契約處理時間窗、證據、訊號 ID、趨勢、影響關係、多語呈現與發布驗證。

公開版會持續跟進正式產品中**可重用、可安全公開**的架構，例如 report contract、reader UI、validator、idempotency 與 failure isolation；但正式環境的來源名單、provider 設定、queries、watchlist、權重、閾值、raw data、真實情報資料與營運設定不會同步出去。

如果這個方向對你有幫助，歡迎 Star、Fork、提 Issue 或送 PR。
