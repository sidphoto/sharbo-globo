# Demo and production separation

The optional GitHub Pages site built from this repository is a synthetic demonstration. The Pages workflow is manual-only and intentionally independent from the production data plane; the public repository does not automatically publish a site on every commit.

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
