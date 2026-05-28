from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config.loader import load_settings
from orchestration.pipeline import run_pipeline
from storage.duckdb_store import DuckDBStore


app = FastAPI(
    title="AI-Powered Market Analytics Pipeline",
    version="0.1.0",
    description="US equities ingestion, feature engineering, signal analytics, AI summaries, and report delivery.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_store() -> DuckDBStore:
    settings = load_settings()
    return DuckDBStore(settings["storage"]["duckdb_path"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "market-data-pipeline"}


@app.post("/pipeline/run")
def run_pipeline_endpoint(no_ai: bool = False) -> dict:
    result = run_pipeline(use_ai=not no_ai)
    return {"date": result["date"], "paths": result["paths"], "summary": result["report"]["summary"]}


@app.get("/signals/latest")
def latest_signals() -> dict:
    store = get_store()
    try:
        df = store.query(
            """
            select *
            from analysis_results
            qualify row_number() over (partition by ticker order by date desc) = 1
            order by signal_score desc, ticker
            """
        )
    except Exception as exc:
        raise HTTPException(status_code=404, detail="No analysis results available. Run the pipeline first.") from exc
    return {"signals": df.to_dict(orient="records")}


@app.get("/prices/{ticker}")
def prices(ticker: str) -> dict:
    store = get_store()
    df = store.load_prices(ticker)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No prices found for {ticker.upper()}")
    return {"ticker": ticker.upper(), "prices": df.to_dict(orient="records")}
