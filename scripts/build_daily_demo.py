from __future__ import annotations

import argparse
import copy
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
LATEST = DATA_DIR / "latest.json"
INDEX = DATA_DIR / "index.json"
TZ = ZoneInfo("Asia/Taipei")
MAX_INDEX_REPORTS = 30

TIMESTAMP_KEYS = {
    "generated_at",
    "observed_at",
    "published_at",
    "as_of",
    "captured_at",
    "updated_at",
}


def _shift_iso_timestamp(value: str, delta: timedelta) -> str:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp lacks timezone: {value}")
    return (parsed + delta).isoformat()


def _shift_dates(value, *, delta: timedelta, key: str | None = None):
    if isinstance(value, dict):
        return {k: _shift_dates(v, delta=delta, key=k) for k, v in value.items()}
    if isinstance(value, list):
        return [_shift_dates(item, delta=delta, key=key) for item in value]
    if isinstance(value, str) and key in TIMESTAMP_KEYS:
        return _shift_iso_timestamp(value, delta)
    return value


def rebase_report(template: dict, report_date: date) -> dict:
    if template.get("demo") is not True:
        raise ValueError("public daily automation only accepts demo=true fixtures")

    template_date = date.fromisoformat(str(template["date"]))
    delta = report_date - template_date
    report = _shift_dates(copy.deepcopy(template), delta=delta)

    report["date"] = report_date.isoformat()
    report["generated_at"] = datetime(
        report_date.year, report_date.month, report_date.day, 6, 5, tzinfo=TZ
    ).isoformat()
    report["window"] = {
        "start": f"{report_date - timedelta(days=1)} 00:00",
        "end": f"{report_date} 06:00",
        "timezone": "Asia/Taipei",
    }

    trend_meta = report.get("trend_meta")
    if isinstance(trend_meta, dict):
        history = trend_meta.get("history_dates") or []
        shifted: list[str] = []
        for item in history:
            shifted.append((date.fromisoformat(item) + delta).isoformat())
        trend_meta["history_dates"] = shifted

    # Public automation must remain unmistakably synthetic after every run.
    report["demo"] = True
    report.setdefault("quality", {})["grade"] = "DEMO"
    notes = report["quality"].setdefault("notes", [])
    if "Synthetic fixture only." not in notes:
        notes.append("Synthetic fixture only.")
    return report


def update_index(index: dict, report: dict) -> dict:
    row = {
        "date": report["date"],
        "signals": len(report.get("signals", [])),
        "summary": "Synthetic public demo fixture. No production source metadata is included.",
    }
    reports = [item for item in index.get("reports", []) if item.get("date") != report["date"]]
    reports.append(row)
    reports.sort(key=lambda item: item.get("date", ""), reverse=True)
    return {"reports": reports[:MAX_INDEX_REPORTS]}


def resolve_date(raw: str | None) -> date:
    if raw:
        return date.fromisoformat(raw)
    return datetime.now(TZ).date()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a date-shifted synthetic SharBo public demo report.")
    parser.add_argument("--date", help="Asia/Taipei report date (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--check", action="store_true", help="Validate generation in memory without writing files.")
    args = parser.parse_args()

    report_date = resolve_date(args.date)
    template = json.loads(LATEST.read_text(encoding="utf-8"))
    report = rebase_report(template, report_date)
    index = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else {"reports": []}
    next_index = update_index(index, report)

    if args.check:
        print(f"public daily demo check PASS: date={report['date']} signals={len(report.get('signals', []))}")
        return 0

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(report, ensure_ascii=False, separators=(",", ":")) + "\n"
    (DATA_DIR / f"{report_date}.json").write_text(rendered, encoding="utf-8")
    LATEST.write_text(rendered, encoding="utf-8")
    INDEX.write_text(json.dumps(next_index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"public daily demo built: date={report['date']} signals={len(report.get('signals', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
