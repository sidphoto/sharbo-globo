# Public / private boundary

| Capability or asset | Public repository | Private production repository |
|---|---:|---:|
| Generic data contracts | Yes | May consume |
| Fail-closed validators | Yes | May consume |
| Architecture documentation | Yes | Operational extensions |
| Synthetic fixtures | Yes | No |
| Production source registry | No | Yes |
| Domain allowlists and RSS inventory | No | Yes |
| Discovery queries and fallback logic | No | Yes |
| Trust weights and full ranking heuristics | No | Yes |
| Daily canonical and localized data | No | Yes |
| Credentials, recipients, and delivery logs | No | Yes |
| Private operations contracts | No | Yes |

The repositories must not share Git history. Public extraction is performed by explicit, reviewed copying into a clean repository, followed by source and secret audits.
