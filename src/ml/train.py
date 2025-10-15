from __future__ import annotations
import pandas as pd
import numpy as np
import joblib, os
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from src.ml.model import build_model
from src.utils.config import settings
from src.utils.logger import get_logger

log = get_logger("train")

def build_training_frame() -> tuple[pd.DataFrame, pd.Series]:
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
        """, conn)
    # Synthetic churn target: users with 0 purchases and >2 views -> churned
    y = ((df["n_purchases"] == 0) & (df["n_views"] >= 2)).astype(int)  # 1 = churn
    X = df.drop(columns=["user_id"])
    return X, y

def main():
    X, y = build_training_frame()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=settings.ml.test_size, random_state=settings.ml.random_state, stratify=y
    )
    model = build_model()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    report = classification_report(y_test, preds, output_dict=False)
    os.makedirs(settings.data_paths.models, exist_ok=True)
    out_path = os.path.join(settings.data_paths.models, "churn_model.joblib")
    joblib.dump(model, out_path)
    log.info(f"Saved model to {out_path}")
    print(report)

if __name__ == "__main__":
    main()
