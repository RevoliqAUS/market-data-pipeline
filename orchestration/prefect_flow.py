from __future__ import annotations

from prefect import flow, task

from ai_insights.generator import generate_ai_summary as create_ai_summary
from analytics.signals import analyze_ticker
from config.loader import load_settings, load_watchlist
from ingestion.market_data import fetch_many, fetch_profile
from reports.report_generator import build_report, write_report
from storage.duckdb_store import DuckDBStore
from transformations.features import add_price_features


@task(name="load_config")
def load_config() -> dict:
    settings = load_settings()
    watchlist = load_watchlist()
    return {"settings": settings, "watchlist": watchlist}


@task(name="ingest_market_data", retries=2, retry_delay_seconds=10)
def ingest_market_data(config: dict) -> dict:
    settings = config["settings"]
    watchlist = config["watchlist"]
    tickers = watchlist["tickers"]
    period = watchlist.get("default_period", "1y")
    cache_seconds = int(settings.get("pipeline", {}).get("cache_seconds", 300))
    histories = fetch_many(tickers, period=period, cache_seconds=cache_seconds)
    profiles = {ticker: fetch_profile(ticker) for ticker in tickers}
    return {"histories": histories, "profiles": profiles}


@task(name="persist_to_duckdb")
def persist_to_duckdb(config: dict, market_data: dict) -> str:
    settings = config["settings"]
    store = DuckDBStore(settings["storage"]["duckdb_path"])
    for ticker, df in market_data["histories"].items():
        store.upsert_prices(df)
        store.upsert_profile(market_data["profiles"][ticker])
    return settings["storage"]["duckdb_path"]


@task(name="run_transformations")
def run_transformations(config: dict, _database_path: str):
    settings = config["settings"]
    store = DuckDBStore(settings["storage"]["duckdb_path"])
    prices = store.load_prices()
    return add_price_features(prices)


@task(name="generate_signals")
def generate_signals(config: dict, features) -> list[dict]:
    settings = config["settings"]
    store = DuckDBStore(settings["storage"]["duckdb_path"])
    analyses = [analyze_ticker(frame) for _, frame in features.groupby("ticker")]
    store.upsert_analysis(analyses)
    return analyses


@task(name="generate_ai_summary")
def generate_ai_summary(config: dict, analyses: list[dict], use_ai: bool = True) -> str:
    if not use_ai:
        return ""
    settings = config["settings"]
    date = str(max(item["date"] for item in analyses))
    return create_ai_summary(date, analyses, settings.get("ai", {}).get("model", "gpt-4o-mini"))


@task(name="write_reports")
def write_reports(config: dict, analyses: list[dict], ai_summary: str) -> dict:
    settings = config["settings"]
    date = str(max(item["date"] for item in analyses))
    report = build_report(date, analyses, ai_summary=ai_summary)
    paths = write_report(report, settings.get("reports_dir", "reports/output"))
    return {
        "date": date,
        "paths": {key: str(value) for key, value in paths.items()},
        "summary": report["summary"],
    }


@flow(name="market-data-pipeline")
def market_data_pipeline_flow(use_ai: bool = True) -> dict:
    config = load_config()
    market_data = ingest_market_data(config)
    database_path = persist_to_duckdb(config, market_data)
    features = run_transformations(config, database_path)
    analyses = generate_signals(config, features)
    ai_summary = generate_ai_summary(config, analyses, use_ai=use_ai)
    return write_reports(config, analyses, ai_summary)

