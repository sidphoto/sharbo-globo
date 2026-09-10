# Optional precise scheduler

GitHub Actions `schedule:` is best-effort and may start late. SharBo's public reference therefore keeps GitHub cron as a backup and provides this optional Cloudflare Worker pattern when a tighter dispatch time matters.

This example is generic. It contains no SharBo production repository name, source configuration, query, credential, or operational endpoint.

## Setup

1. Copy `wrangler.toml.example` to `wrangler.toml` and set the repository variables for your fork.
2. Create a fine-grained GitHub token limited to the target repository with **Actions: read and write**.
3. Store it as a Worker secret: `npx wrangler secret put GITHUB_TOKEN`.
4. Optionally store `TRIGGER_KEY` if you want the authenticated manual test endpoint.
5. Deploy with `npx wrangler deploy`.

The scheduled handler dispatches `.github/workflows/daily-demo.yml`. The GitHub-native schedules remain enabled as fallback triggers, while the workflow's idempotency guard prevents duplicate daily publication.

## Security model

- No token is committed to Git.
- The manual HTTP endpoint is disabled unless `TRIGGER_KEY` exists.
- Invalid manual requests return `404`.
- The GitHub token should be scoped to one repository and only the Actions permission required to dispatch the workflow.
