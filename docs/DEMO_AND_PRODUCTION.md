# Demo and production separation

The GitHub Pages site built from this repository is a synthetic demonstration. It is intentionally independent from the production data plane.

```text
Public demo repository
  ├─ synthetic reports
  ├─ public contracts
  ├─ deterministic validators
  └─ GitHub Pages presentation

Private production repository
  ├─ live source registry
  ├─ retrieval and verification configuration
  ├─ canonical and localized production data
  ├─ private operational workflows
  └─ production deployment secrets
```

The public code does not need access to the private repository. Operators who build a private deployment are responsible for maintaining this boundary.
