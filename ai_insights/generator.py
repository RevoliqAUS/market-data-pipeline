from __future__ import annotations

import os
from typing import Any

from openai import OpenAI


def build_market_prompt(date: str, analyses: list[dict[str, Any]]) -> str:
    rows = []
    for item in analyses:
        rows.append(
            "- {ticker}: close={close}, change={change_pct}%, signal={signal} "
            "(score={signal_score}), trend={trend_alignment}, volume={volume_price_state}, "
            "cost={cost_health}, vol20d={volatility_20d}".format(**item)
        )
    return f"""You are an AI market analytics assistant for a research pipeline.

Generate a concise US equities market summary for {date}.

Use only the supplied analytics. Do not give financial advice. Explain signal drivers, risk clusters, and what to monitor next.

Analytics:
{chr(10).join(rows)}

Return:
1. Market regime snapshot
2. Top bullish/constructive signals
3. Top risk or caution signals
4. Volatility and trend commentary
5. Watchlist for the next session
"""


def generate_ai_summary(date: str, analyses: list[dict[str, Any]], model: str = "gpt-4o-mini") -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return "AI summary skipped because OPENAI_API_KEY is not configured."

    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": build_market_prompt(date, analyses)}],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""

