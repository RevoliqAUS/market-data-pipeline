# Lightweight Dashboard UI

The dashboard UI is a small React + Vite + TypeScript frontend located in `dashboard/web/`. It is designed for GitHub portfolio demos and local exploration of the existing FastAPI dashboard API.

It is intentionally lightweight:

- no authentication
- no SaaS-style account model
- no backend replacement
- no heavy charting dependency
- sample data fallback when the API or DuckDB data is unavailable

## What It Shows

- KPI cards for tracked tickers, latest pipeline run time, signal counts, and database status.
- Signal ranking table with ticker, latest price, signal, momentum score, volatility score, and update time.
- CSS-based charts for signal distribution and momentum ranking.
- AI insight panel explaining the optional AI summary layer.
- API/demo status showing whether data came from the live API or local sample data.

## Startup

Start the backend:

```bash
python -m uvicorn dashboard.api:app --reload
```

Start the frontend:

```bash
cd dashboard/web
npm install
npm run dev
```

Then open the Vite URL, usually `http://localhost:5173`.

## API Base URL

The frontend reads `VITE_API_BASE_URL` from `dashboard/web/.env`.

```bash
cp dashboard/web/.env.example dashboard/web/.env
```

Default:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Live Data And Sample Fallback

The dashboard requests:

- `GET /health`
- `GET /signals/latest`

If the API is unavailable, the database has not been populated, or `/signals/latest` returns no rows, the UI falls back to `dashboard/web/src/sampleData.ts`.

## Screenshot Placeholder

The README uses [docs/assets/dashboard-ui.svg](assets/dashboard-ui.svg) as a placeholder. To replace it with a real screenshot:

1. Start the backend and frontend.
2. Run the pipeline so DuckDB has current data.
3. Open the dashboard in a browser.
4. Capture a screenshot.
5. Save it as `docs/assets/dashboard-ui.png`.
6. Update the README image link.

