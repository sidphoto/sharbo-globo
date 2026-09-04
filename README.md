# 🦐 SharBo Globo｜蝦報。全球情報雷達

> **Verified signals from global noise.**

[![Public Validation Gate](https://github.com/sidphoto/sharbo-globo/actions/workflows/validation.yml/badge.svg)](https://github.com/sidphoto/sharbo-globo/actions/workflows/validation.yml)

**[Public Site](https://sidphoto.github.io/sharbo-globo/)** · **[Interactive Demo](https://sidphoto.github.io/sharbo-globo/demo.html?lang=zh-TW#/today)** · **[Architecture](ARCHITECTURE.md)**

SharBo Globo is a **source-available, multilingual intelligence pipeline** that turns global information noise into verified, ranked and connected signals.

It is built around explicit evidence, cutoff-safe time windows, fail-closed validation and atomic multilingual publishing. It is **not** a generic AI news summarizer: incomplete or inconsistent data is not allowed to reach the presentation layer simply because a model can generate plausible prose.

## What the public preview shows

- **Evidence-first signals** with stable canonical IDs;
- **cutoff-safe contracts** with timezone-aware timestamps;
- **Global Top 5** and source-class validation concepts;
- **Emerging Signals** trend contracts;
- **Impact Chains** with `SUPPORTED` vs `POTENTIAL` relationships;
- **zh-TW / English / Tiếng Việt** overlays with canonical IDs preserved across locales;
- **fail-closed localization validation**;
- **Explain Mode** that makes the public contracts visible inside the demo;
- a responsive intelligence surface modeled after the current SharBo product generation;
- synthetic fixtures only — no production intelligence is published here.

## Public site vs interactive demo

The GitHub Pages root is now the project entry point:

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

## Pipeline

```text
Collector → Normalizer → Deduper → Verifier → Intelligence Scoring
→ Event / Impact Linking → Localization → Validation Gate
→ Presentation → Production
```

The public repository exposes reusable contracts, validators and synthetic examples. Deployment-specific intelligence policy is intentionally excluded.

## Public / private boundary

### Included here

- reusable data and localization contracts;
- validators and tests;
- public UI and reference implementation;
- synthetic demo fixtures;
- architecture, governance and contribution documentation.

### Intentionally excluded

- production source registry and real source domains;
- discovery queries;
- trust strategy and source weighting;
- production ranking/fallback logic;
- production data and archives;
- API keys, credentials, recipients and operational records.

The production system remains in a separate **private repository with independent Git history**. The public UI has no code path that reads from or writes to that private repository.

See [Public Preview v0.2 Redesign Contract](docs/PUBLIC_V0.2_REDESIGN.md) and [Demo / Production Separation](docs/DEMO_AND_PRODUCTION.md).

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

The validation gate fails closed if public contracts, multilingual coverage, demo data or repository-boundary rules are violated.

## Documentation

- [Architecture](ARCHITECTURE.md)
- [Public v0.2 redesign contract](docs/PUBLIC_V0.2_REDESIGN.md)
- [Public data contract](docs/DATA_CONTRACT.md)
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

**蝦報。全球情報雷達**不是把新聞丟給 AI 後產生摘要，而是先用資料契約處理時間窗、證據、來源等級、訊號 ID、趨勢與影響關係，再進行多語呈現與發布驗證。

公開版的目的，是讓開發者可以實際操作 UI、閱讀 contract、研究 validator、Fork 合成資料版本，同時看不到正式環境的來源名單、查詢、權重、真實情報資料與營運設定。

如果這個方向對你有幫助，歡迎 Star、Fork、提 Issue 或送 PR。
