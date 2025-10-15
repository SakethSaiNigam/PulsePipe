from __future__ import annotations
import pandas as pd
from sqlalchemy import create_engine
from src.validation.schema import EventsSchema, DailyFunnelSchema
from src.utils.config import settings
from src.utils.logger import get_logger

log = get_logger("validate")

def main():
    # Validate processed events
    df = pd.read_csv("data/processed/events_enriched.csv", parse_dates=["ts"])
    EventsSchema.validate(df, lazy=True)
    log.info("Processed events passed schema validation.")
    # Validate KPI aggregates and business rules
    engine = create_engine(settings.database.uri, echo=False)
    with engine.begin() as conn:
        df_kpi = pd.read_sql("SELECT * FROM daily_funnel", conn)
    DailyFunnelSchema.validate(df_kpi, lazy=True)
    # Business rule checks
    conv_rate = (df_kpi["purchases"].sum() / max(df_kpi["views"].sum(), 1))
    latency_p95_approx = df["latency_ms"].quantile(0.95)
    thr = settings.kpi_thresholds
    assert thr.conversion_rate_min <= conv_rate <= thr.conversion_rate_max,         f"Conversion rate {conv_rate:.3f} outside [{thr.conversion_rate_min}, {thr.conversion_rate_max}]"
    assert latency_p95_approx <= thr.latency_ms_p95_max,         f"P95 latency {latency_p95_approx:.0f} ms exceeds {thr.latency_ms_p95_max} ms"
    log.info(f"KPIs OK. conv_rate={conv_rate:.3f}, p95_latency={latency_p95_approx:.0f}ms")

if __name__ == "__main__":
    main()
