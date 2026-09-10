from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_daily_demo import rebase_report, update_index
from scripts.validate_report import validate_report_payload


def test_rebase_report_preserves_public_contract() -> None:
    template = json.loads((ROOT / "data" / "latest.json").read_text(encoding="utf-8"))
    target = date(2030, 2, 3)
    report = rebase_report(template, target)

    assert report["demo"] is True
    assert report["date"] == "2030-02-03"
    assert report["window"] == {
        "start": "2030-02-02 00:00",
        "end": "2030-02-03 06:00",
        "timezone": "Asia/Taipei",
    }
    news_count, structured_count = validate_report_payload(report)
    assert news_count == len(report.get("signals", []))
    assert structured_count >= 0

    for signal in report.get("signals", []):
        for source in signal.get("sources", []):
            assert urlparse(source["url"]).hostname == "example.invalid"
    for market in report.get("market", []):
        assert urlparse(market["source_url"]).hostname == "example.invalid"


def test_update_index_is_idempotent_and_bounded() -> None:
    report = {"date": "2030-02-03", "signals": [{"id": "demo"}]}
    initial = {
        "reports": [
            {"date": "2030-02-03", "signals": 99, "summary": "Synthetic stale row"},
            {"date": "2030-02-02", "signals": 1, "summary": "Synthetic older row"},
        ]
    }
    first = update_index(initial, report)
    second = update_index(first, report)

    assert first == second
    assert first["reports"][0]["date"] == "2030-02-03"
    assert first["reports"][0]["signals"] == 1
    assert len(first["reports"]) <= 30
