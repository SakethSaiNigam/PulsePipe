from __future__ import annotations
import pandas as pd
from pathlib import Path
from src.utils.config import settings
from src.utils.logger import get_logger

log = get_logger("transform")

def add_session_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = df["ts"].dt.date
    df["hour"] = df["ts"].dt.hour
    return df

def main():
    raw = Path(settings.data_paths.raw) / "events.csv"
    df = pd.read_csv(raw, parse_dates=["ts"])
    df = add_session_features(df)
    out = Path(settings.data_paths.processed) / "events_enriched.csv"
    Path(settings.data_paths.processed).mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    log.info(f"Wrote processed events: {out} rows={len(df)}")

if __name__ == "__main__":
    main()
