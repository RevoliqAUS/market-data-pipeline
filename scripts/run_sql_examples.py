#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE = ROOT_DIR / "data" / "market_pipeline.duckdb"
DEFAULT_SQL_DIR = ROOT_DIR / "sql"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run DuckDB SQL analytics examples.")
    parser.add_argument(
        "--database",
        default=os.getenv("DUCKDB_PATH", str(DEFAULT_DATABASE)),
        help="Path to the DuckDB database file. Defaults to DUCKDB_PATH or data/market_pipeline.duckdb.",
    )
    parser.add_argument(
        "--sql-dir",
        default=str(DEFAULT_SQL_DIR),
        help="Directory containing SQL example files.",
    )
    return parser.parse_args()


def resolve_path(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT_DIR / candidate


def print_result(title: str, sql_path: Path, result) -> None:
    print("\n" + "=" * 88)
    print(f"{title}")
    print(f"SQL: {sql_path.relative_to(ROOT_DIR)}")
    print("-" * 88)
    df = result.df()
    if df.empty:
        print("(no rows returned)")
    else:
        print(df.to_string(index=False, max_colwidth=80))


def main() -> int:
    args = parse_args()
    database_path = resolve_path(args.database)
    sql_dir = resolve_path(args.sql_dir)

    if not database_path.exists():
        print(
            f"DuckDB database not found: {database_path}\n"
            "Run the pipeline first, for example:\n"
            "  python scripts/run_pipeline.py --no-ai",
            file=sys.stderr,
        )
        return 1

    if not sql_dir.exists():
        print(f"SQL examples directory not found: {sql_dir}", file=sys.stderr)
        return 1

    try:
        import duckdb
    except ImportError:
        print(
            "The duckdb package is not installed. Install project dependencies first:\n"
            "  pip install -r requirements.txt",
            file=sys.stderr,
        )
        return 1

    sql_files = sorted(sql_dir.glob("*.sql"))
    if not sql_files:
        print(f"No .sql files found in {sql_dir}", file=sys.stderr)
        return 1

    print(f"Database: {database_path.relative_to(ROOT_DIR) if database_path.is_relative_to(ROOT_DIR) else database_path}")
    print(f"SQL directory: {sql_dir.relative_to(ROOT_DIR) if sql_dir.is_relative_to(ROOT_DIR) else sql_dir}")

    failures = 0
    connection = duckdb.connect(str(database_path), read_only=True)
    try:
        for sql_path in sql_files:
            title = sql_path.stem.replace("_", " ").title()
            sql = sql_path.read_text(encoding="utf-8")
            try:
                result = connection.sql(sql)
                print_result(title, sql_path, result)
            except Exception as exc:
                failures += 1
                print("\n" + "=" * 88)
                print(f"{title}")
                print(f"SQL: {sql_path.relative_to(ROOT_DIR)}")
                print("-" * 88)
                print(f"Could not run query: {exc}")
                if "analysis_results" in sql or "prices" in sql:
                    print("Hint: run `python scripts/run_pipeline.py --no-ai` to populate DuckDB tables.")
                if "read_json_auto" in sql:
                    print("Hint: generate reports first so files exist in reports/output/.")
    finally:
        connection.close()

    if failures:
        print(f"\nCompleted with {failures} query warning(s).")
    else:
        print("\nAll SQL examples completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

