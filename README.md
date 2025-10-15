# PulsePipe — Real‑Time KPI Validation & ML Reporting

An end‑to‑end, production‑style project built by an **AI & Data Engineering Intern** to showcase:
- **Automated ETL** with Python APIs
- **Data validation** pipelines for quality gates
- **ML‑based KPI reporting** (simple churn propensity)
- **FastAPI** service exposing KPIs and model scores
- **Streamlit** dashboard for real‑time visibility
- **SQLite + SQLAlchemy** for a self‑contained warehouse
- **Docker** & Makefile for easy, fast deployment

> ⚡️ Designed for quick setup and repeatable deployment. The structure mirrors
patterns you'd use with bigger infra (Airflow/DBT/Kafka) but remains lightweight.

## Project Structure

```
pulsepipe-ml-kpi-pipeline/
├── configs/
│   └── settings.yaml
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── src/
│   ├── app/                # FastAPI
│   ├── etl/                # Ingest → Transform → Load
│   ├── ml/                 # Train / Predict
│   ├── reporting/          # KPI compute + Streamlit dashboard
│   ├── validation/         # pandera schemas and checks
│   └── utils/              # config, logging
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── Makefile
└── README.md
```

## Quickstart

### 1) Install & generate data
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run ETL (simulated API -> CSV -> SQLite)
make etl
```

### 2) Validate data quality
```bash
make validate
```

### 3) Train ML model (churn propensity)
```bash
make train
```

### 4) Serve API & dashboard
```bash
# API
make run-api  # http://localhost:8000/docs

# Dashboard (in another terminal)
make run-dashboard  # http://localhost:8501
```

Or use Docker:
```bash
docker compose up --build
```

## What it demonstrates (mapped to resume bullets)

- **Developed and automated data validation pipelines**  
  - `pandera` schemas for row/field constraints  
  - Business‑rule checks on conversion rates & latency (`src/validation/validate.py`)

- **Integrated Python APIs for ETL automation**  
  - Simulated external API ingestion (`src/etl/ingest.py`) and automated ETL (`Makefile`, `docker-compose`)

- **Collaborated with product engineers to streamline dataset preparation**  
  - Clear transforms and materialized aggregates (`src/etl/transform.py`, `src/etl/load.py`)

- **Supported deployment and testing of AI prototypes**  
  - Reproducible training & scoring (`src/ml/train.py`, `src/ml/predict.py`)  
  - FastAPI for serving KPIs & scores (`src/app/api.py`)  
  - Streamlit monitoring UI (`src/reporting/serve_dashboard.py`)  
  - Dockerfile + Makefile enable quick deploys (time savings)

## Endpoints

- `GET /health` — service health
- `GET /kpis` — current KPIs (views, adds, purchases, conversion, latency)
- `GET /events?page=1&page_size=50` — paginated events
- `GET /scores?limit=50` — churn propensities by user

Interactive docs: `http://localhost:8000/docs`

## Notes

- The pipeline uses **SQLite** for portability. Swap `configs/settings.yaml` to point
  at Postgres/MySQL in real deployments.
- The dataset is synthetic but realistic enough for KPI/ML demos.
- If you want stricter CI/CD, add GH Actions to run `make etl validate test` on PRs.

## Example workflow

```bash
make etl          # generate + load data
make validate     # run data quality gates
make train        # train churn model
make run-api      # serve KPIs and scores
make run-dashboard
```

## Testing

```bash
pytest -q
```

## License

MIT
