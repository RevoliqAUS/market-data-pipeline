create or replace view latest_signal_snapshot as
with ranked as (
    select
        *,
        row_number() over (partition by ticker order by date desc) as rn
    from analysis_results
)
select *
from ranked
where rn = 1;

