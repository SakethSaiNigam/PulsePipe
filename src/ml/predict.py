from __future__ import annotations
import pandas as pd
import joblib, os
from sqlalchemy import create_engine
from src.utils.config import settings

def score_users(limit: int = 50) -> pd.DataFrame:
    engine = create_engine(settings.database.uri, echo=False)
    with engine.begin() as conn:
        df = pd.read_sql("""
            SELECT user_id,
                   SUM(CASE WHEN event='view' THEN 1 ELSE 0 END) AS n_views,
                   SUM(CASE WHEN event='add_to_cart' THEN 1 ELSE 0 END) AS n_adds,
                   SUM(CASE WHEN event='purchase' THEN 1 ELSE 0 END) AS n_purchases,
                   AVG(latency_ms) AS avg_latency_ms
            FROM events
            GROUP BY user_id
            LIMIT :limit
        """, conn, params={"limit": limit})
    model = joblib.load(os.path.join(settings.data_paths.models, "churn_model.joblib"))
    X = df.drop(columns=["user_id"])
    df["churn_prob"] = model.predict_proba(X)[:,1]
    return df

if __name__ == "__main__":
    print(score_users().head())
