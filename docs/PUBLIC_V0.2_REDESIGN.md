# SharBo Globo Public Preview v0.2 — Redesign Contract

This document defines the public presentation redesign. It is a product-experience update, not a production-intelligence export.

## Goal

Bring the public repository to the same product-generation as the live SharBo reader while preserving a strict boundary between reusable public architecture and private production intelligence.

The public surface should answer two questions clearly:

1. What does SharBo feel like to use?
2. Why can the pipeline fail closed instead of publishing incomplete intelligence?

## Public surfaces

### Project landing

`index.html` is the public flagship entry point. It explains:

- evidence-first intelligence;
- cutoff-safe contracts;
- fail-closed validation;
- atomic multilingual publication;
- signal, trend and impact relationships;
- the public/private repository boundary.

### Interactive demo

`demo.html` loads only checked-in synthetic fixtures and keeps the existing static GitHub Pages architecture.

The v0.2 presentation layer adds:

- production-generation navigation icons;
- a stronger Today hierarchy;
- a list-oriented Global Radar on desktop;
- Public Contract Inspector on signal detail;
- Explain Mode for Top 5, Emerging Signals, Impact Chain, Radar and Signal Detail;
- explicit synthetic/public boundary messaging;
- responsive desktop/tablet/mobile behavior.

## Information hierarchy

The Today page is organized as:

```text
Global Intelligence Hero
→ Global Top 5
→ Emerging Signals + Impact Chain
→ Taiwan context + Market context
→ Focus Story
→ My Radar
→ Topics
```

This hierarchy is intentionally reader-first. Public features are not presented as an equal-weight widget wall.

## Explain Mode

Explain Mode is specific to the public repository. It exposes architecture concepts without exposing production policy.

It may explain:

- that public Top 5 uses synthetic authoritative-class fixtures and cutoff-safe contracts;
- that Emerging Signals demonstrate persistence/maturity concepts using synthetic series;
- that `SUPPORTED` impact relationships require evidence signal IDs;
- that `POTENTIAL` relationships remain explicitly possible;
- canonical IDs and required localization/narrative structure.

It must not expose:

- real source names or domains;
- source weights;
- production ranking thresholds;
- discovery queries;
- production fallback logic;
- production archives;
- credentials or deployment secrets.

## Public/Private boundary

### Allowed to flow from product learning into Public

- interaction patterns;
- information architecture;
- design tokens and component language;
- generic contracts;
- validators;
- synthetic examples;
- accessibility and responsive improvements.

### Never allowed to flow into Public

- production source registry;
- real source corpus;
- discovery queries;
- trust strategy and source weighting;
- deployment-specific ranking heuristics;
- production data or archive;
- credentials;
- recipient or operations information.

## Validation

`validate_public_repo.py` remains the broad repository leak gate.

`validate_public_ui_boundary.py` adds a narrow presentation-layer check so UI modernization cannot accidentally copy private repository, credential, deployment or source-registry identifiers.

A public redesign is complete only when all existing contract, i18n, report, package and leak validations continue to pass.
