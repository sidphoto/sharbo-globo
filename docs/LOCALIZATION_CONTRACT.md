# Localization contract

Supported public locales are:

```text
zh-TW
en
vi-VN
```

## Invariants

- canonical signal IDs and order do not change by locale;
- every locale has a non-empty `world_summary`;
- every localized signal contains all seven narrative fields;
- Taiwan Radar has the same count and canonical order in every locale;
- English and Vietnamese structural files cover all Emerging Signal and Impact Chain references;
- a locale cannot mutate canonical machine fields through an overlay;
- a failed locale blocks the READY marker and presentation build.

The public validator reads the final persisted bundle before a deployment may claim readiness. Individual translation writes are not publication triggers.
