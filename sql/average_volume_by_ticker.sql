-- Average volume over the latest 30 calendar days available in the warehouse.
-- Source table: prices
with max_available_date as (
    select max(date) as max_date
    from prices
)
select
    p.ticker,
    count(*) as trading_days,
    round(avg(p.volume), 0) as avg_volume,
    min(p.date) as window_start,
    max(p.date) as window_end
from prices p
cross join max_available_date m
where p.date >= m.max_date - interval 30 day
group by p.ticker
order by avg_volume desc;

