.PHONY: setup run-api run-dashboard train etl validate kpi test fmt lint docker

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

run-api:
	uvicorn src.app.api:app --reload --port 8000

run-dashboard:
	streamlit run src/reporting/serve_dashboard.py

etl:
	python -m src.etl.ingest && python -m src.etl.transform && python -m src.etl.load

validate:
	python -m src.validation.validate

kpi:
	python -m src.reporting.kpi

train:
	python -m src.ml.train

test:
	pytest -q

fmt:
	python -m black src tests

lint:
	python -m flake8 src tests

docker:
	docker build -t pulsepipe:latest .
