#!/usr/bin/env python3
"""Fail closed when public UI assets contain production-only identifiers.

This is intentionally narrow and complements validate_public_repo.py. It protects the
presentation layer added for the public preview from accidentally copying private
repository, deployment, credential, or source-registry identifiers.
"""
from __future__ import annotations

import re
from pathlib import Path

PUBLIC_UI_FILES = (
    Path("index.html"),
    Path("demo.html"),
    Path("landing.css"),
    Path("public-v02.css"),
    Path("public-v02.js"),
    Path("README.md"),
)

FORBIDDEN = {
    "private repository slug": re.compile(r"sharbo-globo-production", re.I),
    "private source registry path": re.compile(r"source_registry(?:\.json)?", re.I),
    "Vercel production API credential": re.compile(r"VERCEL_(?:API_KEY|TOKEN)", re.I),
    "Tavily production credential": re.compile(r"TAVILY_API_KEY", re.I),
    "Vercel REST deployment endpoint": re.compile(r"api\.vercel\.com", re.I),
    "production Vercel hostname": re.compile(r"sharbo-globo-production[^\s\"']*\.vercel\.app", re.I),
}


def main() -> int:
    failures: list[str] = []
    for path in PUBLIC_UI_FILES:
        if not path.exists():
            failures.append(f"missing required public UI file: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN.items():
            if pattern.search(text):
                failures.append(f"{path}: contains {label}")

    if failures:
        print("PUBLIC UI BOUNDARY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PUBLIC UI BOUNDARY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
