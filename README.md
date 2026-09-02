# 蝦報。全球情報雷達 / SharBo Globo

> Verified signals from global noise.

SharBo Globo is a source-available, multilingual intelligence pipeline that turns global information noise into verified, ranked, and connected signals.

It is designed around deterministic time windows, explicit evidence, fail-closed validation, and atomic multilingual publishing. It is not a generic AI news summarizer and it does not require an LLM to decide whether incomplete data may reach production.

## What this public preview demonstrates

- deterministic collection cutoff with timezone-aware timestamps;
- canonical signal contracts and stable IDs;
- complete multilingual field coverage;
- fail-closed localization validation;
- Emerging Signals and Impact Chains contracts;
- atomic READY publication only after all locales pass;
- synthetic examples with no production sources, queries, weights, or data.

## Pipeline

```text
Collector → Normalizer → Deduper → Verifier → Intelligence Scoring
→ Event / Impact Linking → Localization → Validation Gate
→ Presentation → Production
```

## Quick start

Requires Python 3.11 or later.

```bash
python -m pip install -e '.[dev]'
python -m sharbo_globo.validator examples/data/localization-bundle.json
python -m pytest
```

The included dataset is synthetic. A successful validation prints `PASS` and exits with status `0`; incomplete or inconsistent bundles fail closed with a non-zero status.

## Run the public demo

```bash
python3 -m http.server 8080
```

Open `http://localhost:8080/?lang=zh-TW#/today`. The demo needs no API key and uses only the checked-in synthetic fixture.

## Public and private boundary

This repository contains reusable contracts, validators, documentation, and synthetic examples. It intentionally excludes the production source registry, domain allowlists, discovery queries, trust strategy, source weighting, fallback logic, API keys, recipient information, operational intelligence, daily data, and private operations documents.

The production system remains in a separate private repository with independent Git history.

## License

SharBo Globo is **source-available**, not OSI Open Source. Personal, educational, research, and other qualifying noncommercial uses are licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE). Commercial use requires a separate license; see [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md).

## Project status

`v0.1.0` is a Public Preview of the intelligence and localization contracts. Interfaces may change before `v1.0`.

## Documentation

- [Architecture](ARCHITECTURE.md)
- [Public data contract](docs/DATA_CONTRACT.md)
- [Localization contract](docs/LOCALIZATION_CONTRACT.md)
- [Demo / production separation](docs/DEMO_AND_PRODUCTION.md)
- [Data policy](DATA_POLICY.md)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)
- [Disclaimer](DISCLAIMER.md)

---

## 中文說明

蝦報。全球情報雷達是一套將全球資訊轉成「已驗證、已排序、可連結、多語發布」訊號的情報產線。公開版著重資料契約、驗證器、合成範例與架構文件；正式來源、真實資料、私有策略及部署憑證不在本 Repository 中。

本專案採 source-available 模式。個人、教育、研究與符合授權條件的非商業使用，可依 PolyForm Noncommercial 1.0.0 使用；商業使用需另行取得授權。
