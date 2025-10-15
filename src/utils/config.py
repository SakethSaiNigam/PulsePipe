from pydantic import BaseModel
from typing import Optional
import yaml, os

class DBConfig(BaseModel):
    uri: str

class DataPaths(BaseModel):
    raw: str
    processed: str
    models: str

class KPIThresholds(BaseModel):
    conversion_rate_min: float
    conversion_rate_max: float
    latency_ms_p95_max: int

class MLConfig(BaseModel):
    target: str
    test_size: float
    random_state: int

class APIConfig(BaseModel):
    page_size_default: int

class Settings(BaseModel):
    environment: str
    database: DBConfig
    data_paths: DataPaths
    kpi_thresholds: KPIThresholds
    ml: MLConfig
    api: APIConfig

def load_settings(path: str = "configs/settings.yaml") -> Settings:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)
    return Settings(**raw)

settings = load_settings()
