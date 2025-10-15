from __future__ import annotations
from fastapi import FastAPI, Query
from sqlalchemy import create_engine, text
import pandas as pd
from src.utils.config import settings
from src.reporting.kpi import compute_kpis
from src.ml.predict import score_users

app = FastAPI(title="PulsePipe API", version="1.0.0")

engine = create_engine(settings.database.uri, echo=False)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/kpis")
def kpis():
    return compute_kpis()

@app.get("/events")
def events(page: int = 1, page_size: int = settings.api.page_size_default):
    offset = (page - 1) * page_size
    with engine.begin() as conn:
        df = pd.read_sql(text("SELECT * FROM events ORDER BY ts DESC LIMIT :limit OFFSET :offset"),
                         conn, params={"limit": page_size, "offset": offset})
    return df.to_dict(orient="records")

@app.get("/scores")
def scores(limit: int = 50):
    df = score_users(limit=limit)
    return df.to_dict(orient="records")
