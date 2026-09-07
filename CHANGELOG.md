# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

### Public architecture sync v0.3

- Added a public-safe synchronization policy defining what may be promoted from product development, what requires sanitization, and what remains private-only.
- Updated the public architecture from a single collector pipeline to independent news/event and structured-observation channels with explicit failure isolation.
- Added the public `structured_signals` reader contract without production provider names, thresholds, watchlists, source allowlists or scoring weights.
- Updated report semantics to support best-effort authoritative Top items (`1..5`) instead of requiring filler to reach exactly five.
- Added `structured_only` mode: no news + at least one valid structured observation can publish; no news + no observations still fails closed.
- Added validation for structured observation IDs, timestamps, three-language rendered text, source URLs, published counts and topic `structured_count` consistency.
- Added regression tests for best-effort and structured-only report modes.
- Documented idempotent structured-observation merge semantics so presentation rebuilds do not depend on collector schedule order.
- Declared `sidphoto/sharbo-globo` the target canonical public upstream for reusable reader architecture; `sidphoto/shrimp-intelligence` is legacy compatibility only.

### Public Preview v0.2 redesign

- Split the GitHub Pages root into a public flagship project landing and a dedicated interactive `demo.html` surface.
- Reworked the public demo presentation to the current SharBo product generation while keeping synthetic fixtures only.
- Added production-generation SVG navigation icons and stronger desktop/mobile information hierarchy.
- Reordered Today into reader-first sections: Hero → Top 5 → Emerging / Impact → Taiwan / Market → Focus → My Radar → Topics.
- Changed Global Radar toward a list-oriented intelligence explorer on desktop.
- Added Public Contract Inspector to Signal Detail.
- Added Explain Mode for Top 5, Emerging Signals, Impact Chain, Radar and Signal Detail.
- Added explicit public / production boundary messaging inside the demo.
- Added `scripts/validate_public_ui_boundary.py` so presentation changes fail closed on private repository, credential, deployment or source-registry identifiers.
- Updated the app manifest to launch the interactive public demo.
- Repositioned README as the canonical public project entry point.

### Repository maintenance

- Added feature-request and issue-routing templates for public contributors.
- Added support and release-process documentation for the source-available edition.
- Added weekly Dependabot checks for Python dependencies and GitHub Actions.

## [0.1.0] - 2026-09-02

### Added

- Public Preview architecture and repository-boundary documentation.
- PolyForm Noncommercial 1.0.0 and separate commercial-license notice.
- Public localization contract constants.
- Fail-closed multilingual bundle validator.
- Fully synthetic `zh-TW`, `en`, and `vi-VN` fixture.
- Tests for locale completeness, required fields, canonical ordering, and READY state.
- Unified CI validation on every branch push and pull request, including the public leak gate.
- Shared HTML escaping and icon allowlisting for JSON-driven rendering.
- Static CSP metadata and least-privilege Pages deployment permissions.
