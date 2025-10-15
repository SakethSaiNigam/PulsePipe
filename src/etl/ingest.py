"""Ingest: Simulate fetching events from a product API and write to raw CSV.

This script generates synthetic product funnel events (view -> add_to_cart -> purchase)
and latency metrics to emulate a near-real-time stream.
"""
from __future__ import annotations
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from src.utils.config import settings
from src.utils.logger import get_logger

log = get_logger("ingest")

def simulate_events(n_users=500, days=3, seed=123):
    rng = np.random.default_rng(seed)
    start = datetime.utcnow() - timedelta(days=days)
    rows = []
    for user in range(n_users):
        uid = f"user_{user:05d}"
        sessions = rng.integers(1, 4)
        last_time = start + timedelta(hours=rng.integers(0, 24*days))
        for s in range(sessions):
            # Page view
            t_view = last_time + timedelta(minutes=rng.integers(0, 240))
            latency_view = np.abs(rng.normal(120, 60))
            rows.append((uid, "view", t_view, latency_view))
            # Add to cart (50-70%)
            if rng.random() < rng.uniform(0.5, 0.7):
                t_cart = t_view + timedelta(minutes=rng.integers(1, 60))
                latency_cart = np.abs(rng.normal(150, 70))
                rows.append((uid, "add_to_cart", t_cart, latency_cart))
                # Purchase (20-50%)
                if rng.random() < rng.uniform(0.2, 0.5):
                    t_purchase = t_cart + timedelta(minutes=rng.integers(1, 60))
                    latency_purchase = np.abs(rng.normal(200, 80))
                    rows.append((uid, "purchase", t_purchase, latency_purchase))
            last_time = t_view
    df = pd.DataFrame(rows, columns=["user_id","event","ts","latency_ms"])
    df["ts"] = pd.to_datetime(df["ts"])
    return df.sort_values("ts").reset_index(drop=True)

def main():
    out_dir = Path(settings.data_paths.raw)
    out_dir.mkdir(parents=True, exist_ok=True)
    df = simulate_events()
    out_file = out_dir / "events.csv"
    df.to_csv(out_file, index=False)
    log.info(f"Wrote raw events: {out_file} rows={len(df)}")

if __name__ == "__main__":
    main()
