# SharBo Globo Public Automation

SharBo Globo now includes a **public-safe daily automation reference** derived from the same operational principles used by the private production system: deterministic daily windows, idempotent execution, fail-closed validation, atomic publication, independent deployment, and an external heartbeat.

The public implementation is intentionally synthetic. It demonstrates the automation mechanics without publishing production sources, queries, ranking policy, live data, credentials, recipients, or private operational records.

## Runnable public pipeline

```text
GitHub schedule or optional precise external trigger
                    ↓
             Idempotency guard
                    ↓
       Build date-shifted synthetic report
                    ↓
       Report / i18n / leak / UI gates
                    ↓
      Commit only validated public data
                    ↓
       Existing GitHub Pages workflow
                    ↓
          Public demo deployment
                    ↓
        Independent heartbeat check
                    ↓
       Issue alert if stale or failed
```

The implementation is split across:

- `.github/workflows/daily-demo.yml` — scheduled synthetic daily build, validation, commit and failure alert;
- `.github/workflows/pages.yml` — independent public validation and GitHub Pages deployment;
- `.github/workflows/heartbeat.yml` — checks whether the live public demo is current;
- `scripts/build_daily_demo.py` — deterministic date rebasing for demo-only fixtures;
- `examples/external-trigger/` — optional Cloudflare Worker dispatch pattern for tighter scheduling;
- `docs/AUTOMATION_PIPELINE.md` — lifecycle, extension points and public/private boundary.

## Fail-closed invariants

The public automation follows the same safety shape as a production pipeline:

1. **Do not overwrite the last-known-good deployment on failure.** A failed build or validation stops before publication.
2. **Run once per report date.** Multiple schedulers may fire, but the idempotency guard prevents duplicate daily writes.
3. **Validate the exact artifact before commit.** Report, multilingual, public-leak and UI-boundary gates all run before new data reaches `main`.
4. **Keep generation and deployment independent.** A validated data commit triggers the existing Pages workflow, which validates again before deployment.
5. **Monitor from outside the generation path.** The heartbeat verifies the live site instead of trusting that an upstream workflow completed.
6. **Never make a public workflow depend on the private production repository.** Public automation must be independently reproducible from public files.

## Daily synthetic demo

Run locally for today in `Asia/Taipei`:

```bash
python scripts/build_daily_demo.py
python scripts/validate_report.py data/latest.json
python scripts/validate_i18n.py
python scripts/validate_public_repo.py
python scripts/validate_public_ui_boundary.py
```

Generate a deterministic fixture for another date:

```bash
python scripts/build_daily_demo.py --date 2030-02-03
```

Check generation without writing files:

```bash
python scripts/build_daily_demo.py --date 2030-02-03 --check
```

The builder refuses non-demo input and preserves `example.invalid` evidence URLs. It shifts timestamps relative to the selected report date, rebuilds the `00:00 → 06:00 Asia/Taipei` window, updates `data/latest.json`, writes a dated synthetic archive entry and maintains a bounded public index.

## Scheduling model

The included GitHub schedule is intentionally **best effort**. GitHub-hosted cron jobs may start late during busy periods. For projects that require tighter dispatch timing, use the optional `examples/external-trigger/` Cloudflare Worker pattern while leaving GitHub cron enabled as backup.

Multiple triggers are safe because the workflow checks whether a valid synthetic report for the target date already exists before rebuilding it.

## Production-style localization handoff

The private product uses an external localization worker and an atomic READY gate. The public repository exposes the **contract pattern**, not a production translator or model credential:

```text
canonical artifact
      ↓
translation request
      ↓
external/local worker
      ↓
re-read persisted locale artifacts
      ↓
full coverage validation
      ↓
READY written last
      ↓
presentation / deployment
```

A fork can implement this boundary with any translator or model. The core requirement is architectural: **READY must be the final write and must only appear after all persisted locale artifacts pass validation**. Do not let individual locale-file writes trigger publication.

## Explicitly excluded

The public repository still does **not** contain or mirror:

- production source/provider registries or real source domains;
- production discovery queries, watchlists or retrieval configuration;
- source weighting, trust mapping, ranking thresholds or private heuristics;
- real daily reports, evidence corpus, raw snapshots or production archives;
- production market-provider configuration;
- private deployment project IDs, API keys, recipient information or operational secrets;
- any automatic private→public synchronization path.

The public project is a source-available reference implementation. Production remains a separate private deployment with independent Git history.
