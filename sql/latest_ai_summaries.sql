-- Latest AI summary excerpts from generated JSON report artifacts.
-- The current warehouse schema stores AI summaries in report files rather than a table.
select
    date,
    generated_at,
    market,
    summary.tickers_analyzed as tickers_analyzed,
    summary.bullish as bullish_count,
    summary.neutral as neutral_count,
    summary.bearish as bearish_count,
    left(ai_summary, 280) as ai_summary_excerpt
from read_json_auto('reports/output/daily_market_summary_*.json', union_by_name = true)
order by generated_at desc
limit 5;

