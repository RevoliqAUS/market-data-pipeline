-- Latest signal snapshot ranked by model score.
-- Source table: analysis_results
select
    ticker,
    date,
    signal,
    signal_score,
    trend_alignment,
    volume_price_state,
    cost_health,
    close,
    change_pct,
    generated_at
from analysis_results
qualify row_number() over (partition by ticker order by date desc) = 1
order by signal_score desc, ticker;

