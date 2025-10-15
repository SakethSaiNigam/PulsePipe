import pandas as pd
from src.validation.schema import EventsSchema

def test_events_schema_passes():
    df = pd.DataFrame({
        "user_id": ["user_00001"],
        "event": ["view"],
        "ts": pd.to_datetime(["2025-01-01"]),
        "latency_ms": [100.0],
        "date": [pd.to_datetime(["2025-01-01"]).date[0]],
        "hour": [12],
    })
    EventsSchema.validate(df)
