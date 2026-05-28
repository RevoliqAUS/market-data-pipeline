from __future__ import annotations

import numpy as np
import pandas as pd


def add_price_features(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    data = df.sort_values(["ticker", "date"]).copy()
    grouped = data.groupby("ticker", group_keys=False)
    data["daily_return"] = grouped["close"].pct_change()
    data["ma_5"] = grouped["close"].transform(lambda series: series.rolling(5).mean())
    data["ma_10"] = grouped["close"].transform(lambda series: series.rolling(10).mean())
    data["ma_20"] = grouped["close"].transform(lambda series: series.rolling(20).mean())
    data["ma_60"] = grouped["close"].transform(lambda series: series.rolling(60).mean())
    data["ma_120"] = grouped["close"].transform(lambda series: series.rolling(120).mean())
    data["avg_volume_5"] = grouped["volume"].transform(lambda series: series.shift(1).rolling(5).mean())
    data["volume_ratio"] = data["volume"] / data["avg_volume_5"].replace(0, np.nan)
    previous_close = grouped["close"].shift(1)
    data["amplitude_pct"] = (data["high"] - data["low"]) / previous_close * 100
    data["volatility_20d"] = grouped["daily_return"].transform(lambda series: series.rolling(20).std() * np.sqrt(252))
    return data


def latest_by_ticker(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    return df.sort_values(["ticker", "date"]).groupby("ticker", as_index=False).tail(1)
