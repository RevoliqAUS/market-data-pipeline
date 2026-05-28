from __future__ import annotations

import time
from dataclasses import dataclass

import pandas as pd
import yfinance as yf


_CACHE: dict[str, tuple[float, pd.DataFrame, yf.Ticker]] = {}


@dataclass(frozen=True)
class MarketInstrument:
    ticker: str
    name: str | None = None
    asset_class: str = "equity"
    market: str = "US"


def normalize_ticker(ticker: str) -> str:
    cleaned = ticker.strip().upper()
    if not cleaned:
        raise ValueError("Ticker cannot be empty")
    return cleaned


def fetch_price_history(ticker: str, period: str = "1y", cache_seconds: int = 300) -> tuple[pd.DataFrame, yf.Ticker]:
    ticker = normalize_ticker(ticker)
    cache_key = f"{ticker}:{period}"
    now = time.time()
    cached = _CACHE.get(cache_key)
    if cached and cache_seconds > 0 and now - cached[0] < cache_seconds:
        return cached[1].copy(), cached[2]

    instrument = yf.Ticker(ticker)
    df = instrument.history(period=period, timeout=20)
    if df is None or df.empty:
        raise ValueError(f"No market data returned for {ticker}")

    df = df.reset_index()
    if "Date" not in df.columns:
        df = df.rename(columns={df.columns[0]: "Date"})
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df["Ticker"] = ticker
    df = df[["Ticker", "Date", "Open", "High", "Low", "Close", "Volume"]]
    df = df[df["Volume"].fillna(0) > 0].copy()
    df.columns = [column.lower() for column in df.columns]
    _CACHE[cache_key] = (now, df.copy(), instrument)
    return df, instrument


def fetch_many(tickers: list[str], period: str = "1y", cache_seconds: int = 300) -> dict[str, pd.DataFrame]:
    histories = {}
    for ticker in tickers:
        df, _ = fetch_price_history(ticker, period=period, cache_seconds=cache_seconds)
        histories[normalize_ticker(ticker)] = df
    return histories


def fetch_profile(ticker: str) -> dict:
    instrument = yf.Ticker(normalize_ticker(ticker))
    try:
        info = instrument.info or {}
    except Exception:
        info = {}
    return {
        "ticker": normalize_ticker(ticker),
        "name": info.get("longName") or info.get("shortName") or normalize_ticker(ticker),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "market_cap": info.get("marketCap"),
        "shares_outstanding": info.get("sharesOutstanding") or info.get("floatShares"),
        "trailing_pe": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "price_to_book": info.get("priceToBook"),
    }

