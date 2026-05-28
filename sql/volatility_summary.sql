-- Latest analytics volatility plus signal context.
-- Source table: analysis_results
select
    ticker,
    date,
    signal,
    signal_score,
    round(volatility_20d * 100, 2) as volatility_20d_pct,
    close,
    change_pct,
    trend_alignment
from analysis_results
where volatility_20d is not null
qualify row_number() over (partition by ticker order by date desc) = 1
order by volatility_20d_pct desc, ticker;

