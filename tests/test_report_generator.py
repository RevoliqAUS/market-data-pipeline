from __future__ import annotations

import json
from datetime import date, datetime

import numpy as np
import pandas as pd

from reports.report_generator import write_report


def test_write_report_serializes_pandas_numpy_and_missing_values(tmp_path) -> None:
    report = {
        "date": pd.Timestamp("2026-05-28"),
        "generated_at": datetime(2026, 5, 28, 10, 30),
        "market": "US equities",
        "summary": {
            "tickers_analyzed": np.int64(1),
            "bullish": 1,
            "neutral": 0,
            "bearish": 0,
        },
        "rankings": [
            {
                "ticker": "AAPL",
                "date": date(2026, 5, 28),
                "signal": "bullish",
                "signal_score": np.int64(2),
                "trend_alignment": "bullish stack",
                "volume_price_state": "range-bound",
                "cost_health": "mixed positioning",
                "volatility_20d": np.float64(0.25),
                "close": np.float64(199.75),
                "change_pct": float("nan"),
                "volume_ratio": pd.NaT,
            }
        ],
        "ai_summary": "sample",
    }

    paths = write_report(report, tmp_path)
    payload = json.loads(paths["json"].read_text(encoding="utf-8"))

    assert payload["date"] == "2026-05-28T00:00:00"
    assert payload["summary"]["tickers_analyzed"] == 1
    assert payload["rankings"][0]["signal_score"] == 2
    assert payload["rankings"][0]["volatility_20d"] == 0.25
    assert payload["rankings"][0]["change_pct"] is None
    assert payload["rankings"][0]["volume_ratio"] is None
