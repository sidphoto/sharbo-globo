# Data policy

## Included

- synthetic event and localization examples;
- generic schemas and validation rules;
- fixtures created solely to demonstrate expected contracts;
- documentation describing public architectural behavior.

## Excluded

- production source registries and domain allowlists;
- complete RSS lists and discovery queries;
- source weights, trust strategy, and fallback logic;
- raw or canonical daily production intelligence;
- recipient information, personal email addresses, and delivery logs;
- private operations documents and production configuration;
- API keys, tokens, secrets, deployment identifiers, and private endpoints;
- complete proprietary ranking heuristics.

## Contributions

Contributors must not submit copyrighted news articles, private datasets, credentials, personal data, or source lists copied from non-public deployments. Test data must be synthetic, public-domain, or clearly licensed for redistribution.

## Removal

If prohibited or sensitive data is found, report it privately according to `SECURITY.md`. Maintainers may remove it from the current tree and rewrite affected Git history before publication.
