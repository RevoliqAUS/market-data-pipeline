# Architecture

The platform follows a layered pipeline design:

```mermaid
flowchart LR
    DS["Data Sources<br/>yfinance"] --> IN["Ingestion Layer<br/>OHLCV + profiles"]
    IN --> DB["DuckDB Storage<br/>prices, profiles, analysis_results"]
    DB --> SQL["SQL Views + Transformations<br/>daily_features, latest snapshots"]
    SQL --> FE["Feature Engineering<br/>returns, MA, volume ratios, volatility"]
    FE --> AN["Analytics Engine<br/>trend, volume/price, cost distribution"]
    AN --> AI["AI Insight Layer<br/>OpenAI market summaries"]
    AN --> OUT["Reports + API Outputs<br/>JSON, CSV, FastAPI"]
    AI --> OUT
    ORCH["Orchestration<br/>CLI, cron, Docker-ready"] -.-> IN
    ORCH -.-> AN
    ORCH -.-> OUT
```

## Component Responsibilities

- `ingestion/`: external market data access and ticker normalization.
- `storage/`: warehouse schema, table creation, upserts, and SQL query helpers.
- `transformations/`: Python and SQL feature engineering.
- `analytics/`: deterministic signal generation and ranking logic.
- `ai_insights/`: prompt construction and OpenAI summary generation.
- `reports/`: JSON/CSV output generation.
- `dashboard/`: FastAPI service layer.
- `orchestration/`: composable pipeline entry point for local, cron, CI, or Airflow/Prefect execution.

## Runtime Flow

```mermaid
sequenceDiagram
    participant User
    participant Runner as Pipeline Runner
    participant YF as yfinance
    participant DB as DuckDB
    participant Engine as Analytics Engine
    participant AI as AI Insight Layer
    participant Output as Reports/API

    User->>Runner: python scripts/run_pipeline.py
    Runner->>YF: Fetch ticker history and profiles
    Runner->>DB: Upsert prices and profiles
    Runner->>DB: Load historical prices
    Runner->>Engine: Build features and signals
    Engine->>DB: Persist analysis_results
    Engine->>AI: Send compact signal context
    AI->>Output: Return market summary
    Runner->>Output: Write JSON and CSV reports
```
