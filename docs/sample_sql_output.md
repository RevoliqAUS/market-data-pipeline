# Sample SQL Runner Output

The SQL example runner prints each query result in a readable table. Exact numbers will vary based on market data and the date the pipeline is run.

```text
$ python scripts/run_sql_examples.py
Database: data/market_pipeline.duckdb
SQL directory: sql

========================================================================================
Latest Signal Ranking
SQL: sql/latest_signal_ranking.sql
----------------------------------------------------------------------------------------
ticker       date  signal  signal_score trend_alignment       volume_price_state                         cost_health  close  change_pct        generated_at
  NVDA 2026-05-28 bullish             2    bullish stack      high-volume advance          majority profitable, trend intact  128.50        1.84 2026-05-28 22:31:04
  MSFT 2026-05-28 neutral             1            mixed             range-bound                       mixed positioning  460.12        0.22 2026-05-28 22:31:04
  AAPL 2026-05-28 neutral             0            mixed       low-volume decline                       mixed positioning  199.75       -0.41 2026-05-28 22:31:04

========================================================================================
Average Volume By Ticker
SQL: sql/average_volume_by_ticker.sql
----------------------------------------------------------------------------------------
ticker  trading_days  avg_volume window_start window_end
  NVDA            21  182340000.0   2026-04-28 2026-05-28
  TSLA            21   94500000.0   2026-04-28 2026-05-28
  AAPL            21   61250000.0   2026-04-28 2026-05-28

========================================================================================
Strongest Momentum Tickers
SQL: sql/strongest_momentum_tickers.sql
----------------------------------------------------------------------------------------
ticker       date  close  close_20_sessions_ago  return_20_session_pct
  NVDA 2026-05-28 128.50                  114.22                  12.50
  AVGO 2026-05-28 220.10                  207.91                   5.86
  MSFT 2026-05-28 460.12                  449.80                   2.29

========================================================================================
Volatility Summary
SQL: sql/volatility_summary.sql
----------------------------------------------------------------------------------------
ticker       date  signal  signal_score  volatility_20d_pct  close  change_pct trend_alignment
  TSLA 2026-05-28 bearish            -2               64.80  321.44       -2.18    bearish stack
  NVDA 2026-05-28 bullish             2               42.10  128.50        1.84    bullish stack

========================================================================================
Latest Ai Summaries
SQL: sql/latest_ai_summaries.sql
----------------------------------------------------------------------------------------
      date         generated_at       market  tickers_analyzed  bullish_count  neutral_count  bearish_count ai_summary_excerpt
2026-05-28 2026-05-28T22:31:04Z  US equities                10              3              5              2 Market leadership remains concentrated...

All SQL examples completed successfully.
```

If the database has not been created yet, the runner prints:

```text
DuckDB database not found: data/market_pipeline.duckdb
Run the pipeline first, for example:
  python scripts/run_pipeline.py --no-ai
```

