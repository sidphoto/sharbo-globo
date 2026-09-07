from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from dateutil import parser as dtparser

ROOT = Path(__file__).resolve().parents[1]
TZ = ZoneInfo("Asia/Taipei")
SUPPORTED_STRUCTURED_LOCALES = ("zh-TW", "en", "vi-VN")


def parse(value: str | None):
    if not value:
        return None
    dt = dtparser.isoparse(value)
    if dt.tzinfo is None:
        raise ValueError(f"Timestamp lacks timezone: {value}")
    return dt.astimezone(TZ)


def _validate_extensions(report: dict, signal_ids: set[str]) -> None:
    trend_meta = report.get("trend_meta")
    if trend_meta is not None:
        days = int(trend_meta.get("available_history_days", 0))
        full_days = int(trend_meta.get("full_window_days", 7))
        if days < 1 or days > full_days:
            raise SystemExit("trend_meta available_history_days is outside valid range")
        dates = trend_meta.get("history_dates") or []
        if len(dates) != days:
            raise SystemExit("trend_meta history_dates length must match available_history_days")

    for item in report.get("emerging_signals") or []:
        series = item.get("series") or []
        if trend_meta and len(series) != int(trend_meta.get("available_history_days", 0)):
            raise SystemExit(f"Emerging signal series length mismatch: {item.get('id')}")
        if not 0 <= int(item.get("trend_score", 0)) <= 99:
            raise SystemExit(f"Invalid emerging trend_score: {item.get('id')}")
        linked = item.get("signal_ids") or []
        if not linked or any(signal_id not in signal_ids for signal_id in linked):
            raise SystemExit(f"Emerging signal references missing report signal: {item.get('id')}")

    impact_chains = report.get("impact_chains") or []
    chain_ids = set()
    for chain in impact_chains:
        chain_id = chain.get("id")
        if not chain_id or chain_id in chain_ids:
            raise SystemExit("Duplicate or missing impact chain id")
        chain_ids.add(chain_id)
        anchor = chain.get("anchor_signal_id")
        if anchor not in signal_ids:
            raise SystemExit(f"Impact chain anchor references missing signal: {chain_id}")
        confidence = float(chain.get("confidence", 0))
        if not 0 <= confidence <= 1:
            raise SystemExit(f"Impact chain confidence outside 0..1: {chain_id}")
        nodes = chain.get("nodes") or []
        node_ids = {node.get("id") for node in nodes}
        if len(nodes) < 2 or None in node_ids or len(node_ids) != len(nodes):
            raise SystemExit(f"Impact chain has invalid nodes: {chain_id}")
        for edge in chain.get("edges") or []:
            relation = edge.get("relation")
            if relation not in {"SUPPORTED", "POTENTIAL"}:
                raise SystemExit(f"Invalid impact relation: {chain_id}")
            if edge.get("from") not in node_ids or edge.get("to") not in node_ids:
                raise SystemExit(f"Impact edge references missing node: {chain_id}")
            evidence = edge.get("evidence_signal_ids") or []
            if any(signal_id not in signal_ids for signal_id in evidence):
                raise SystemExit(f"Impact edge references missing evidence signal: {chain_id}")
            if relation == "SUPPORTED" and not evidence:
                raise SystemExit(f"SUPPORTED impact edge requires evidence: {chain_id}")
            if relation == "POTENTIAL" and evidence:
                raise SystemExit(f"POTENTIAL impact edge must not masquerade as observed evidence: {chain_id}")

    featured = report.get("featured_impact_chain_id")
    if featured is not None and featured not in chain_ids:
        raise SystemExit("featured_impact_chain_id references missing impact chain")


def _validate_structured_signals(report: dict, cutoff: datetime) -> int:
    block = report.get("structured_signals")
    if block is None:
        return 0
    if not isinstance(block, dict):
        raise SystemExit("structured_signals must be an object")

    buckets = block.get("buckets") or {}
    if not isinstance(buckets, dict):
        raise SystemExit("structured_signals.buckets must be an object")

    seen: set[str] = set()
    published = 0
    for bucket, records in buckets.items():
        if not isinstance(records, list):
            raise SystemExit(f"structured_signals bucket must be a list: {bucket}")
        for record in records:
            if not isinstance(record, dict):
                raise SystemExit(f"structured_signals record must be an object: {bucket}")
            record_id = record.get("id")
            if not record_id or record_id in seen:
                raise SystemExit(f"Duplicate or missing structured observation id: {record_id}")
            seen.add(record_id)
            published += 1

            observed = parse(record.get("observed_at"))
            updated = parse(record.get("updated_at"))
            if observed and observed > cutoff:
                raise SystemExit(f"Post-cutoff structured observation: {record_id}")
            if updated and updated > cutoff:
                raise SystemExit(f"Post-cutoff structured update: {record_id}")

            source = record.get("source") or {}
            source_url = source.get("url", "")
            if not source_url.startswith(("https://", "http://")):
                raise SystemExit(f"Structured observation lacks valid source URL: {record_id}")

            localized = record.get("text")
            if localized is not None:
                if not isinstance(localized, dict):
                    raise SystemExit(f"Structured observation text must be an object: {record_id}")
                for locale in SUPPORTED_STRUCTURED_LOCALES:
                    if not str(localized.get(locale, "")).strip():
                        raise SystemExit(f"Structured observation missing {locale} text: {record_id}")

            signal_meta = record.get("signal") or {}
            if signal_meta.get("score") is not None:
                score = float(signal_meta["score"])
                if not 0 <= score <= 100:
                    raise SystemExit(f"Structured observation score outside 0..100: {record_id}")

    declared = (block.get("counts") or {}).get("published")
    if declared is not None and int(declared) != published:
        raise SystemExit("structured_signals counts.published does not match bucket records")

    for topic in report.get("topic_summary") or []:
        if "structured_count" not in topic:
            continue
        structured_count = int(topic.get("structured_count") or 0)
        total = int(topic.get("count") or 0)
        if structured_count < 0 or structured_count > total:
            raise SystemExit(f"Invalid structured_count for topic: {topic.get('id')}")

    return published


def validate_report_payload(report: dict) -> tuple[int, int]:
    start = datetime.strptime(report["window"]["start"], "%Y-%m-%d %H:%M").replace(tzinfo=TZ)
    end = datetime.strptime(report["window"]["end"], "%Y-%m-%d %H:%M").replace(tzinfo=TZ)

    signals = report.get("signals", [])
    if not isinstance(signals, list):
        raise SystemExit("signals must be a list")
    if len(signals) > 20:
        raise SystemExit("Report exceeds 20-signal editorial cap")

    ids = set()
    for signal in signals:
        signal_id = signal.get("id")
        if not signal_id or signal_id in ids:
            raise SystemExit(f"Duplicate or missing signal id: {signal_id}")
        ids.add(signal_id)
        observed = parse(signal.get("observed_at"))
        if observed and not (start <= observed <= end):
            raise SystemExit(f"Look-ahead contamination in observed_at: {signal.get('title')}")
        for source in signal.get("sources", []):
            published = parse(source.get("published_at"))
            if published and published > end:
                raise SystemExit(f"Post-cutoff source leaked into report: {signal.get('title')}")
            if not source.get("url", "").startswith(("https://", "http://")):
                raise SystemExit(f"Invalid source URL: {signal.get('title')}")

    structured_count = _validate_structured_signals(report, end)
    mode = (report.get("quality") or {}).get("mode") or "news"
    top5_ids = report.get("top5_ids", [])

    if mode == "structured_only":
        if signals:
            raise SystemExit("structured_only report must not contain news signals")
        if top5_ids:
            raise SystemExit("structured_only report must have empty top5_ids")
        if structured_count < 1:
            raise SystemExit("structured_only report requires at least one structured observation")
    else:
        if len(signals) < 1:
            raise SystemExit("News-bearing report requires at least one verified signal")
        if not 1 <= len(top5_ids) <= 5:
            raise SystemExit("top5_ids must contain between 1 and 5 ids")
        if len(top5_ids) > len(signals):
            raise SystemExit("top5_ids cannot exceed available signals")
        top5 = [s for s in signals if s.get("id") in top5_ids]
        if len(top5) != len(top5_ids):
            raise SystemExit("top5_ids reference missing signals")
        for signal in top5:
            if not signal.get("window_verified"):
                raise SystemExit(f"Top signal is not window verified: {signal.get('title')}")
            if not any(src.get("class") in ("PRIMARY", "CONFIRMED") for src in signal.get("sources", [])):
                raise SystemExit(f"Top signal lacks authoritative source: {signal.get('title')}")

    _validate_extensions(report, ids)
    return len(signals), structured_count


def main(path: str = "data/latest.json") -> int:
    report_path = ROOT / path
    report = json.loads(report_path.read_text(encoding="utf-8"))
    news_count, structured_count = validate_report_payload(report)
    mode = (report.get("quality") or {}).get("mode") or "news"
    print(
        f"OK: {report['date']} / news={news_count} / structured={structured_count} / "
        f"mode={mode} / cutoff {report['window']['end']} Asia/Taipei"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "data/latest.json"))
