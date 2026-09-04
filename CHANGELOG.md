# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

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
