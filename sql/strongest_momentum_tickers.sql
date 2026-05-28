-- 20-session momentum ranking using persisted OHLCV history.
-- Source table: prices
with momentum as (
    select
        ticker,
        date,
        close,
        lag(close, 20) over (partition by ticker order by date) as close_20_sessions_ago
    from prices
)
select
    ticker,
    date,
    close,
    close_20_sessions_ago,
    round((close / nullif(close_20_sessions_ago, 0) - 1) * 100, 2) as return_20_session_pct
from momentum
where close_20_sessions_ago is not null
qualify row_number() over (partition by ticker order by date desc) = 1
order by return_20_session_pct desc, ticker;

