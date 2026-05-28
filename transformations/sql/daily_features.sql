create or replace view daily_features as
select
    ticker,
    date,
    open,
    high,
    low,
    close,
    volume,
    close / nullif(lag(close) over (partition by ticker order by date), 0) - 1 as daily_return,
    avg(close) over (partition by ticker order by date rows between 4 preceding and current row) as ma_5,
    avg(close) over (partition by ticker order by date rows between 19 preceding and current row) as ma_20,
    avg(close) over (partition by ticker order by date rows between 59 preceding and current row) as ma_60,
    avg(volume) over (partition by ticker order by date rows between 5 preceding and 1 preceding) as avg_volume_5
from prices;

