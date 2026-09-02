# Contributing

Thank you for helping improve SharBo Globo.

## Before opening a pull request

1. Open or reference an issue for non-trivial changes.
2. Keep production-specific data and policy outside this repository.
3. Use synthetic or clearly redistributable fixtures.
4. Run `python -m pip install -e .[dev]` and `pytest`.
5. Confirm the example bundle passes `sharbo-validate`.

## Pull request requirements

- describe the contract or behavior being changed;
- include tests for success and fail-closed behavior;
- avoid unrelated formatting or dependency changes;
- do not include secrets, private sources, personal data, or copyrighted articles;
- update documentation and `CHANGELOG.md` when behavior changes.

By contributing, you agree that your contribution is licensed under the repository's current license and may be included in separately licensed commercial distributions by the project maintainer.
