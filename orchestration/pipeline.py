from __future__ import annotations

from config.loader import load_settings, load_watchlist
from ingestion.market_data import fetch_many, fetch_profile
from storage.duckdb_store import DuckDBStore
from transformations.features import add_price_features
from analytics.signals import analyze_ticker
from ai_insights.generator import generate_ai_summary
from reports.report_generator import build_report, write_report


def run_pipeline(use_ai: bool = True) -> dict:
    settings = load_settings()
    watchlist = load_watchlist()
    store = DuckDBStore(settings["storage"]["duckdb_path"])
    tickers = watchlist["tickers"]
    period = watchlist.get("default_period", "1y")
    cache_seconds = int(settings.get("pipeline", {}).get("cache_seconds", 300))

    histories = fetch_many(tickers, period=period, cache_seconds=cache_seconds)
    for ticker, df in histories.items():
        store.upsert_prices(df)
        store.upsert_profile(fetch_profile(ticker))

    all_prices = store.load_prices()
    features = add_price_features(all_prices)
    analyses = [analyze_ticker(frame) for _, frame in features.groupby("ticker")]
    store.upsert_analysis(analyses)

    date = str(max(item["date"] for item in analyses))
    ai_summary = generate_ai_summary(date, analyses, settings.get("ai", {}).get("model", "gpt-4o-mini")) if use_ai else ""
    report = build_report(date, analyses, ai_summary=ai_summary)
    paths = write_report(report, settings.get("reports_dir", "reports/output"))

    return {
        "date": date,
        "tickers": tickers,
        "analyses": analyses,
        "report": report,
        "paths": {key: str(value) for key, value in paths.items()},
    }

