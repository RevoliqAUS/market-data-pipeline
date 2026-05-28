from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd

from config.loader import project_path


SCHEMA_SQL = """
create table if not exists prices (
    ticker varchar,
    date date,
    open double,
    high double,
    low double,
    close double,
    volume bigint,
    primary key (ticker, date)
);

create table if not exists instrument_profiles (
    ticker varchar primary key,
    name varchar,
    sector varchar,
    industry varchar,
    market_cap double,
    shares_outstanding double,
    trailing_pe double,
    forward_pe double,
    price_to_book double,
    updated_at timestamp
);

create table if not exists analysis_results (
    ticker varchar,
    date date,
    signal varchar,
    signal_score integer,
    trend_alignment varchar,
    volume_price_state varchar,
    cost_health varchar,
    volatility_20d double,
    close double,
    change_pct double,
    generated_at timestamp,
    primary key (ticker, date)
);
"""


class DuckDBStore:
    def __init__(self, path: str | Path):
        self.path = project_path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = duckdb.connect(str(self.path))
        self.initialize()

    def initialize(self) -> None:
        self.connection.execute(SCHEMA_SQL)

    def upsert_prices(self, df: pd.DataFrame) -> None:
        if df.empty:
            return
        self.connection.register("incoming_prices", df)
        self.connection.execute(
            """
            insert or replace into prices
            select ticker, date, open, high, low, close, volume
            from incoming_prices
            """
        )
        self.connection.unregister("incoming_prices")

    def upsert_profile(self, profile: dict) -> None:
        self.connection.execute(
            """
            insert or replace into instrument_profiles
            values (?, ?, ?, ?, ?, ?, ?, ?, ?, current_timestamp)
            """,
            [
                profile.get("ticker"),
                profile.get("name"),
                profile.get("sector"),
                profile.get("industry"),
                profile.get("market_cap"),
                profile.get("shares_outstanding"),
                profile.get("trailing_pe"),
                profile.get("forward_pe"),
                profile.get("price_to_book"),
            ],
        )

    def upsert_analysis(self, rows: list[dict]) -> None:
        if not rows:
            return
        df = pd.DataFrame(rows)
        self.connection.register("incoming_analysis", df)
        self.connection.execute(
            """
            insert or replace into analysis_results
            select
                ticker, date, signal, signal_score, trend_alignment,
                volume_price_state, cost_health, volatility_20d, close,
                change_pct, current_timestamp
            from incoming_analysis
            """
        )
        self.connection.unregister("incoming_analysis")

    def load_prices(self, ticker: str | None = None) -> pd.DataFrame:
        if ticker:
            return self.connection.execute(
                "select * from prices where ticker = ? order by date",
                [ticker.upper()],
            ).df()
        return self.connection.execute("select * from prices order by ticker, date").df()

    def query(self, sql: str) -> pd.DataFrame:
        return self.connection.execute(sql).df()

    def run_sql_file(self, path: str | Path) -> None:
        sql_path = project_path(path)
        self.connection.execute(sql_path.read_text(encoding="utf-8"))

