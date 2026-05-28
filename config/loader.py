from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]


def _resolve(path: str | os.PathLike[str]) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT_DIR / candidate


def load_yaml(path: str | os.PathLike[str]) -> dict[str, Any]:
    resolved = _resolve(path)
    with resolved.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_settings() -> dict[str, Any]:
    load_dotenv(ROOT_DIR / ".env")
    path = os.getenv("MARKET_PIPELINE_CONFIG", "config/settings.yaml")
    settings = load_yaml(path)
    duckdb_path = os.getenv("DUCKDB_PATH")
    reports_dir = os.getenv("REPORTS_DIR")
    ai_model = os.getenv("AI_MODEL")
    if duckdb_path:
        settings.setdefault("storage", {})["duckdb_path"] = duckdb_path
    if reports_dir:
        settings["reports_dir"] = reports_dir
    if ai_model:
        settings.setdefault("ai", {})["model"] = ai_model
    return settings


def load_watchlist() -> dict[str, Any]:
    path = os.getenv("MARKET_PIPELINE_WATCHLIST", "config/watchlist.yaml")
    data = load_yaml(path)
    data.setdefault("tickers", [])
    data["tickers"] = [str(ticker).strip().upper() for ticker in data["tickers"] if str(ticker).strip()]
    data.setdefault("benchmarks", {"SPY": "S&P 500 ETF", "QQQ": "Nasdaq 100 ETF"})
    return data


def project_path(path: str | os.PathLike[str]) -> Path:
    return _resolve(path)

