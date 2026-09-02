# Release process

SharBo Globo uses semantic version tags and maintainer-led releases.

## Before a release

1. Keep the change on `main` and update `CHANGELOG.md`.
2. Run the full validation gate locally:
   - `python -m unittest discover -s tests -v`
   - `python scripts/validate_public_repo.py`
   - `python scripts/validate_i18n.py`
   - `python scripts/validate_report.py data/latest.json`
   - the JavaScript syntax and regression checks in `.github/workflows/validation.yml`
3. Confirm the public/private boundary and synthetic-data policy.
4. Confirm the exact commit has a successful GitHub Actions validation run.

## Publishing

1. Create a tag in the form `vMAJOR.MINOR.PATCH` from the validated commit.
2. Create the matching GitHub Release with a concise summary and migration notes.
3. Mark preview releases as pre-releases until the public interfaces are stable.
4. Link the release from the changelog and keep the release body free of production data.

The `v0.1.0` release is the current Public Preview baseline.

## Safety rules

- Never release production source registries, real daily intelligence, credentials, private operations documents, or proprietary source-selection strategy.
- Every release must pass the public leak gate and contract validators.
- A failed or incomplete validation blocks publication.
- Production deployments remain separate from this repository and its release artifacts.
