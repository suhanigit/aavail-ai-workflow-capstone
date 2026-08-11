.PHONY: install train eda test run monitor docker-build docker-run

install:
	python -m pip install -r requirements.txt

train:
	python -m src.train --data data/monthly_revenue.csv --model-dir artifacts/models --metrics-dir artifacts/metrics

eda:
	python -m src.eda --data data/monthly_revenue.csv --metrics-dir artifacts/metrics --figure-dir artifacts/figures

test:
	python run_tests.py

run:
	uvicorn src.api:app --host 0.0.0.0 --port 8000

monitor:
	python -m src.monitor --metrics-dir artifacts/metrics --output runtime/monitoring/performance.jsonl

docker-build:
	docker build -t aavail-capstone .

docker-run:
	docker run --rm -p 8000:8000 aavail-capstone
