from __future__ import annotations
from sqlalchemy import create_engine
import pandas as pd
from src.utils.config import settings
from src.utils.logger import get_logger

log = get_logger("kpi")

def compute_kpis() -> dict:
    engine = create_engine(settings.database.uri, echo=False)
    with engine.begin() as conn:
        df = pd.read_sql("SELECT * FROM daily_funnel", conn)
    views = int(df["views"].sum())
    adds = int(df["adds"].sum())
    purchases = int(df["purchases"].sum())
    conv_rate = purchases / max(views, 1)
    latency_avg = float(df["avg_latency_ms"].mean())
    return {
        "views": views,
        "adds": adds,
        "purchases": purchases,
        "conversion_rate": round(conv_rate, 4),
        "avg_latency_ms": round(latency_avg, 1),
    }

def main():
    print(compute_kpis())

if __name__ == "__main__":
    main()
