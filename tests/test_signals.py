from __future__ import annotations

import pandas as pd

from analytics.signals import analyze_ticker, volume_price_state
from transformations.features import add_price_features


def test_volume_price_state_classifies_advance() -> None:
    assert volume_price_state(1.2, 0.7) == "low-volume advance"
    assert volume_price_state(-1.2, 1.5) == "high-volume decline"


def test_analyze_ticker_returns_signal_payload() -> None:
    rows = []
    for idx in range(80):
        close = 100 + idx * 0.5
        rows.append(
            {
                "ticker": "AAPL",
                "date": pd.Timestamp("2026-01-01") + pd.Timedelta(days=idx),
                "open": close - 0.2,
                "high": close + 1,
                "low": close - 1,
                "close": close,
                "volume": 1_000_000 + idx * 1_000,
            }
        )
    features = add_price_features(pd.DataFrame(rows))
    result = analyze_ticker(features)
    assert result["ticker"] == "AAPL"
    assert result["signal"] in {"bullish", "neutral", "bearish"}
    assert "trend_alignment" in result

