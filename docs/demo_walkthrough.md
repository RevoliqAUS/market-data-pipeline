# Demo Walkthrough Recording Guide

Use this guide to record a short GitHub demo GIF or screen capture. The goal is to show the project as a working data engineering and AI analytics pipeline, not just a code repository.

## Suggested Recording Flow

### 1. Terminal Setup

Show the repository root and dependency setup:

```bash
cd market-data-pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Mention that `OPENAI_API_KEY` is optional. The pipeline can run with `--no-ai` for deterministic analytics only.

### 2. Show Configuration

Open the watchlist:

```bash
sed -n '1,80p' config/watchlist.yaml
```

Point out the configurable US equity tickers and yfinance-compatible symbols.

### 3. Run The Pipeline

Run:

```bash
python scripts/run_pipeline.py --no-ai
```

Show the JSON response with generated report paths.

### 4. Inspect Generated Outputs

List output files:

```bash
ls reports/output
```

Preview the JSON report:

```bash
python -m json.tool reports/output/daily_market_summary_<date>.json | sed -n '1,100p'
```

Preview the CSV signal ranking:

```bash
sed -n '1,20p' reports/output/signal_rankings_<date>.csv
```

### 5. Inspect DuckDB Data

Show the analytical warehouse:

```bash
duckdb data/market_pipeline.duckdb "show tables;"
duckdb data/market_pipeline.duckdb "select ticker, count(*) as rows from prices group by ticker order by ticker;"
duckdb data/market_pipeline.duckdb "select ticker, signal, signal_score, close from analysis_results order by signal_score desc;"
```

### 6. Start The API

Start FastAPI:

```bash
uvicorn dashboard.api:app --reload --port 8000
```

Then show:

- `http://localhost:8000/docs`
- `http://localhost:8000/health`
- `http://localhost:8000/signals/latest`
- `http://localhost:8000/prices/AAPL`

### 7. Show Architecture

Open the README architecture diagram or [docs/architecture.md](architecture.md). Briefly narrate the flow:

Data source to ingestion, DuckDB storage, SQL transformations, analytics engine, AI insight layer, reports and API outputs, with orchestration around the whole pipeline.

## Suggested Demo Length

Keep the final recording between 60 and 120 seconds:

- 15 seconds: repo overview and architecture
- 20 seconds: config and pipeline run
- 20 seconds: generated report and DuckDB queries
- 20 seconds: API docs/endpoints
- 10 seconds: roadmap and disclaimer

