from __future__ import annotations

import csv
import json
import math
from datetime import date, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]


def project_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT_DIR / candidate


def build_report(date: str, analyses: list[dict[str, Any]], ai_summary: str | None = None) -> dict[str, Any]:
    ranked = sorted(analyses, key=lambda item: item["signal_score"], reverse=True)
    return {
        "date": date,
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "market": "US equities",
        "pipeline": "AI-Powered Market Analytics Pipeline",
        "summary": {
            "tickers_analyzed": len(analyses),
            "bullish": sum(1 for item in analyses if item["signal"] == "bullish"),
            "neutral": sum(1 for item in analyses if item["signal"] == "neutral"),
            "bearish": sum(1 for item in analyses if item["signal"] == "bearish"),
        },
        "rankings": ranked,
        "ai_summary": ai_summary or "",
        "disclaimer": "This project is for research and analytics purposes only and does not constitute financial advice.",
    }


def make_json_safe(value: Any) -> Any:
    """Convert pandas/numpy/datetime values into JSON-safe Python values."""
    if value is None:
        return None
    if value is pd.NaT:
        return None
    if isinstance(value, (pd.Timestamp, datetime, date)):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        value = float(value)
        return None if math.isnan(value) or math.isinf(value) else value
    if isinstance(value, float):
        return None if math.isnan(value) or math.isinf(value) else value
    if isinstance(value, dict):
        return {key: make_json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [make_json_safe(item) for item in value]
    if pd.isna(value) if not isinstance(value, (str, bytes, bool, int)) else False:
        return None
    return value


def write_report(report: dict[str, Any], reports_dir: str | Path) -> dict[str, Path]:
    output_dir = project_path(reports_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    date = report["date"]
    json_path = output_dir / f"daily_market_summary_{date}.json"
    csv_path = output_dir / f"signal_rankings_{date}.csv"

    json_path.write_text(json.dumps(make_json_safe(report), indent=2), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "ticker",
                "date",
                "signal",
                "signal_score",
                "trend_alignment",
                "volume_price_state",
                "cost_health",
                "volatility_20d",
                "close",
                "change_pct",
                "volume_ratio",
            ],
        )
        writer.writeheader()
        for item in report["rankings"]:
            writer.writerow({key: item.get(key) for key in writer.fieldnames})

    return {"json": json_path, "csv": csv_path}
