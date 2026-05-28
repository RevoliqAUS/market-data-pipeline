# Orchestration

Orchestration turns a data pipeline from a script into a repeatable workflow with named steps, retries, logs, and a path toward scheduling. This project keeps orchestration lightweight: the original CLI runner remains the simplest production-shaped entry point, and Prefect is added as an optional demo layer.

## Current Runner

The existing runner remains:

```bash
python scripts/run_pipeline.py --no-ai
```

It executes the end-to-end pipeline in one Python process:

1. Load settings and watchlist.
2. Fetch market data.
3. Persist prices and profiles to DuckDB.
4. Build features.
5. Generate and persist signals.
6. Optionally generate AI commentary.
7. Write JSON and CSV reports.

## Optional Prefect Flow

The Prefect flow is defined in `orchestration/prefect_flow.py` and can be run locally:

```bash
python scripts/run_prefect_flow.py --no-ai
```

Prefect is included for portfolio and demo purposes. It gives each stage a clear task boundary without replacing the existing pipeline.

```mermaid
flowchart LR
    S["Scheduled Flow"] --> I["Ingestion Task"]
    I --> D["Storage Task"]
    D --> T["Transformation Task"]
    T --> A["Analytics Task"]
    A --> AI["AI Summary Task"]
    AI --> R["Report Task"]
```

## Flow Structure

Tasks:

- `load_config`: reads settings and watchlist files.
- `ingest_market_data`: fetches OHLCV history and instrument profiles.
- `persist_to_duckdb`: upserts market data into DuckDB.
- `run_transformations`: builds analytical features.
- `generate_signals`: produces and persists signal rankings.
- `generate_ai_summary`: optionally creates natural-language market commentary.
- `write_reports`: writes JSON and CSV output artifacts.

## Production Evolution

The current shape can evolve into:

- Prefect deployments with scheduled runs and retries.
- Airflow DAGs for teams already standardized on Airflow.
- GitHub Actions scheduled workflows for lightweight automation.
- AWS EventBridge plus ECS/Fargate for containerized scheduled execution.
- Managed workflow platforms for alerting, observability, and backfills.

The important design point is that orchestration wraps the pipeline; it does not own the business logic. Core ingestion, storage, transformation, analytics, and report functions remain reusable from CLI, API, tests, and schedulers.
