from __future__ import annotations

import numpy as np
import pandas as pd


def volume_price_state(change_pct: float, volume_ratio: float | None) -> str:
    ratio = volume_ratio if volume_ratio is not None and not np.isnan(volume_ratio) else 0
    if ratio > 3:
        return "unusual volume expansion"
    if change_pct > 0.5 and ratio < 0.8:
        return "low-volume advance"
    if change_pct > 0.5 and ratio >= 0.8:
        return "high-volume advance"
    if change_pct < -0.5 and ratio < 0.8:
        return "low-volume decline"
    if change_pct < -0.5 and ratio >= 0.8:
        return "high-volume decline"
    return "range-bound"


def moving_average_alignment(row: pd.Series) -> str:
    values = [row.get(column) for column in ["ma_5", "ma_10", "ma_20", "ma_60"]]
    values = [float(value) for value in values if pd.notna(value)]
    if len(values) < 3:
        return "insufficient history"
    if all(values[i] >= values[i + 1] for i in range(len(values) - 1)):
        return "bullish stack"
    if all(values[i] <= values[i + 1] for i in range(len(values) - 1)):
        return "bearish stack"
    return "mixed"


def estimate_cost_distribution(df: pd.DataFrame, window: int = 250) -> dict | None:
    if df is None or len(df) < 20:
        return None
    data = df.tail(window).copy()
    price_min = data["low"].min() * 0.95
    price_max = data["high"].max() * 1.05
    if price_max <= price_min:
        return None
    step = max(round((price_max - price_min) / 600, 2), 0.01)
    bins = np.arange(price_min, price_max + step, step)
    if len(bins) < 2:
        return None

    bin_centers = (bins[:-1] + bins[1:]) / 2
    chips = np.zeros(len(bin_centers))
    for _, row in data.iterrows():
        low, high, volume, close = row["low"], row["high"], row["volume"], row["close"]
        decay = 0.985
        if volume <= 0 or high <= low:
            chips *= decay
            continue
        mask = (bin_centers >= low) & (bin_centers <= high)
        matched = bin_centers[mask]
        if len(matched) == 0:
            chips *= decay
            continue
        distance = np.abs(matched - close)
        max_distance = max(high - close, close - low, 0.01)
        weights = np.maximum(0, 1 - distance / max_distance)
        if weights.sum() > 0:
            chips[mask] += weights / weights.sum() * volume
        chips *= decay

    total = chips.sum()
    if total <= 0:
        return None
    current_price = data.iloc[-1]["close"]
    profit_ratio = chips[bin_centers <= current_price].sum() / total * 100
    avg_cost = np.average(bin_centers, weights=chips)
    cumsum = np.cumsum(chips) / total
    low_idx = min(np.searchsorted(cumsum, 0.05), len(bin_centers) - 1)
    high_idx = min(np.searchsorted(cumsum, 0.95), len(bin_centers) - 1)
    range_low = bin_centers[low_idx]
    range_high = bin_centers[high_idx]
    concentration = (range_high - range_low) / avg_cost * 100 if avg_cost > 0 else 0
    return {
        "profit_ratio": round(float(profit_ratio), 2),
        "avg_cost": round(float(avg_cost), 2),
        "range_low": round(float(range_low), 2),
        "range_high": round(float(range_high), 2),
        "concentration": round(float(concentration), 2),
    }


def cost_health(cost: dict | None, close: float) -> str:
    if not cost:
        return "insufficient data"
    profit = cost["profit_ratio"]
    price_vs_cost = close / cost["avg_cost"] if cost["avg_cost"] else 0
    concentration = cost["concentration"]
    if profit > 95 and price_vs_cost > 1.5 and concentration > 20:
        return "elevated profit-taking risk"
    if profit > 95 and price_vs_cost < 1.15 and concentration < 12:
        return "tight cost base, breakout watch"
    if profit < 30:
        return "broad holder losses, base-building area"
    if profit > 70:
        return "majority profitable, trend intact"
    return "mixed positioning"


def analyze_ticker(feature_df: pd.DataFrame) -> dict:
    data = feature_df.sort_values("date")
    latest = data.iloc[-1]
    prev_close = data.iloc[-2]["close"] if len(data) >= 2 else latest["close"]
    change_pct = round((latest["close"] - prev_close) / prev_close * 100, 2) if prev_close else 0
    alignment = moving_average_alignment(latest)
    vp_state = volume_price_state(change_pct, latest.get("volume_ratio"))
    cost = estimate_cost_distribution(data)
    health = cost_health(cost, latest["close"])

    score = 0
    if alignment == "bullish stack":
        score += 1
    elif alignment == "bearish stack":
        score -= 1
    if vp_state in {"low-volume advance", "high-volume advance"}:
        score += 1
    elif vp_state in {"low-volume decline", "high-volume decline"}:
        score -= 1
    if cost and cost["profit_ratio"] < 30:
        score += 1
    elif cost and cost["profit_ratio"] > 90:
        score -= 1
    if pd.notna(latest.get("volatility_20d")) and latest["volatility_20d"] > 0.55:
        score -= 1

    signal = "bullish" if score >= 2 else "bearish" if score <= -2 else "neutral"
    return {
        "ticker": latest["ticker"],
        "date": latest["date"],
        "signal": signal,
        "signal_score": int(score),
        "trend_alignment": alignment,
        "volume_price_state": vp_state,
        "cost_distribution": cost,
        "cost_health": health,
        "volatility_20d": None if pd.isna(latest.get("volatility_20d")) else round(float(latest["volatility_20d"]), 4),
        "close": round(float(latest["close"]), 2),
        "change_pct": change_pct,
        "volume_ratio": None if pd.isna(latest.get("volume_ratio")) else round(float(latest["volume_ratio"]), 2),
    }

