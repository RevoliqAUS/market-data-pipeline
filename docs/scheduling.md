# Scheduling

The simplest production-like schedule is cron:

```cron
30 18 * * 1-5 cd /path/to/market-data-pipeline && .venv/bin/python scripts/run_pipeline.py >> logs/pipeline.log 2>&1
```

For orchestrators:

- Airflow can call `orchestration.pipeline.run_pipeline` from a PythonOperator.
- Prefect can wrap `run_pipeline` in a flow with retry policies.
- GitHub Actions can run the script on a scheduled workflow and upload report artifacts.

The pipeline is idempotent at the table level because price and analysis rows are upserted by ticker/date.

