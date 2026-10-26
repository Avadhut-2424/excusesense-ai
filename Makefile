.PHONY: help test train api streamlit frontend docker-up docker-down clean

help:
	@echo "ExcuseSense AI - Developer CLI"
	@echo "--------------------------------------------------"
	@echo "  make test        - Run unified test suite with timing and summary"
	@echo "  make train       - Retrain model & regenerate artifacts"
	@echo "  make api         - Start FastAPI backend (uvicorn app.main:app)"
	@echo "  make streamlit   - Run legacy Streamlit dashboard"
	@echo "  make frontend    - Run React + TypeScript workstation"
	@echo "  make docker-up   - Build and start all Docker services"
	@echo "  make docker-down - Stop Docker services"
	@echo "  make clean       - Remove cached bytecode and test runs"

test:
	python run_suite.py

train:
	python -m app.ml.train

api:
	uvicorn app.main:app --reload --port 8000

streamlit:
	streamlit run app.py

frontend:
	cd frontend && npm run dev

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
