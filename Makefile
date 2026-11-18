.PHONY: setup seed api simulate web test lint

PY := backend/.venv/bin/python

setup: ## Install backend and frontend dependencies
	cd backend && python3.12 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
	cd backend && [ -f .env ] || cp .env.example .env
	cd frontend && npm install && ([ -f .env ] || cp .env.example .env)
	cd backend && .venv/bin/python manage.py migrate

seed: ## Reset the database with 6h of demo history (includes the attack)
	cd backend && .venv/bin/python manage.py seed_demo

api: ## Run the API on :8000
	cd backend && .venv/bin/python manage.py runserver

simulate: ## Generate live readings every 5s
	cd backend && .venv/bin/python manage.py simulate

web: ## Run the dashboard on :5173
	cd frontend && npm run dev

test: ## Backend + frontend tests
	cd backend && .venv/bin/pytest
	cd frontend && npm test

lint: ## Backend + frontend linters
	cd backend && .venv/bin/ruff check . && .venv/bin/black --check .
	cd frontend && npm run lint && npm run format:check && npm run typecheck
