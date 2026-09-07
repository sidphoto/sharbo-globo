from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_report import validate_report_payload


def news_signal(signal_id: str = "demo-news-1") -> dict:
    return {
        "id": signal_id,
        "title": "Synthetic verified signal",
        "observed_at": "2026-01-15T01:00:00+08:00",
        "window_verified": True,
        "sources": [
            {
                "class": "PRIMARY",
                "url": "https://example.invalid/news/1",
                "published_at": "2026-01-15T00:55:00+08:00",
            }
        ],
    }


def base_report() -> dict:
    return {
        "date": "2026-01-15",
        "window": {
            "start": "2026-01-14 00:00",
            "end": "2026-01-15 06:00",
            "timezone": "Asia/Taipei",
        },
        "quality": {"window_verified": True, "mode": "news"},
        "signals": [news_signal()],
        "top5_ids": ["demo-news-1"],
        "emerging_signals": [],
        "impact_chains": [],
        "topic_summary": [],
    }


def structured_block() -> dict:
    return {
        "schema_version": "1.0",
        "counts": {"published": 1},
        "providers": [{"provider": "demo-provider", "status": "ok"}],
        "buckets": {
            "observation": [
                {
                    "id": "demo-observation-1",
                    "observed_at": "2026-01-15T05:30:00+08:00",
                    "updated_at": "2026-01-15T05:35:00+08:00",
                    "text": {
                        "zh-TW": "DEMO：合成觀測資料",
                        "en": "DEMO: synthetic observation",
                        "vi-VN": "DEMO: quan sát tổng hợp",
                    },
                    "source": {
                        "name": "Example Source",
                        "url": "https://example.invalid/observation/1",
                        "type": "official",
                    },
                    "signal": {"score": 70, "band": "candidate", "level": "watch"},
                }
            ]
        },
    }


class ReportModeTests(unittest.TestCase):
    def test_best_effort_one_item_top_projection_passes(self):
        report = base_report()
        self.assertEqual(validate_report_payload(report), (1, 0))

    def test_structured_only_report_passes_with_observation(self):
        report = base_report()
        report["quality"]["mode"] = "structured_only"
        report["signals"] = []
        report["top5_ids"] = []
        report["structured_signals"] = structured_block()
        report["topic_summary"] = [{"id": "science", "count": 1, "structured_count": 1}]
        self.assertEqual(validate_report_payload(report), (0, 1))

    def test_structured_only_without_observation_fails(self):
        report = base_report()
        report["quality"]["mode"] = "structured_only"
        report["signals"] = []
        report["top5_ids"] = []
        with self.assertRaises(SystemExit):
            validate_report_payload(report)

    def test_news_mode_without_news_fails(self):
        report = base_report()
        report["signals"] = []
        report["top5_ids"] = []
        report["structured_signals"] = structured_block()
        with self.assertRaises(SystemExit):
            validate_report_payload(report)

    def test_post_cutoff_structured_update_fails(self):
        report = base_report()
        report["structured_signals"] = structured_block()
        broken = copy.deepcopy(report)
        broken["structured_signals"]["buckets"]["observation"][0]["updated_at"] = "2026-01-15T06:01:00+08:00"
        with self.assertRaises(SystemExit):
            validate_report_payload(broken)

    def test_structured_locales_must_be_complete(self):
        report = base_report()
        report["structured_signals"] = structured_block()
        del report["structured_signals"]["buckets"]["observation"][0]["text"]["vi-VN"]
        with self.assertRaises(SystemExit):
            validate_report_payload(report)

    def test_structured_topic_breakdown_cannot_exceed_total(self):
        report = base_report()
        report["structured_signals"] = structured_block()
        report["topic_summary"] = [{"id": "science", "count": 1, "structured_count": 2}]
        with self.assertRaises(SystemExit):
            validate_report_payload(report)


if __name__ == "__main__":
    unittest.main()
