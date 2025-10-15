from __future__ import annotations
import pandas as pd
from sqlalchemy import create_engine, text
from src.utils.config import settings
from src.utils.logger import get_logger

log = get_logger("load")

def main():
    engine = create_engine(settings.database.uri, echo=False)
    df = pd.read_csv("data/processed/events_enriched.csv", parse_dates=["ts"])
    with engine.begin() as conn:
        conn.exec_driver_sql("""
        CREATE TABLE IF NOT EXISTS events (
            user_id TEXT,
            event TEXT,
            ts TIMESTAMP,
            latency_ms REAL,
            date TEXT,
            hour INTEGER
        );
        """)
        df.to_sql("events", conn, if_exists="replace", index=False)
        # Materialized daily aggregates for fast KPIs
        conn.exec_driver_sql("""
        CREATE TABLE IF NOT EXISTS daily_funnel AS
        SELECT date,
               COUNT(CASE WHEN event='view' THEN 1 END) AS views,
               COUNT(CASE WHEN event='add_to_cart' THEN 1 END) AS adds,
               COUNT(CASE WHEN event='purchase' THEN 1 END) AS purchases,
               AVG(latency_ms) AS avg_latency_ms
        FROM events
        GROUP BY date;
        """)
    log.info("Loaded data into SQLite and built daily_funnel table.")

if __name__ == "__main__":
    main()
