# OctoCAT Supply API - Python Backend Makefile
# Mirrors the npm scripts from api-nodejs/package.json

PYTHON := python3
VENV := .venv
VENV_BIN := $(VENV)/bin
SRC_DIR := src

# Use venv Python/pip if available
ifeq ($(wildcard $(VENV_BIN)/python),)
	PY := $(PYTHON)
	PIP := pip3
	UVICORN := uvicorn
	PYTEST := pytest
	RUFF := ruff
else
	PY := $(VENV_BIN)/python
	PIP := $(VENV_BIN)/pip
	UVICORN := $(VENV_BIN)/uvicorn
	PYTEST := $(VENV_BIN)/pytest
	RUFF := $(VENV_BIN)/ruff
endif

.DEFAULT_GOAL := help

.PHONY: help
help: ## Display available commands
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

.PHONY: venv
venv: ## Create virtual environment
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install -e ".[dev]"

.PHONY: build
build: ## Build/install the package (equivalent to npm run build)
	$(PIP) install -e .

.PHONY: start
start: start-install ## Start the production server

.PHONY: start-install
start-install: ## Initialize DB with seed data and start server
	$(PY) -m $(SRC_DIR).init_db
	$(PY) -m $(SRC_DIR).seed_data
	$(UVICORN) $(SRC_DIR).main:app --host 0.0.0.0 --port 3000

.PHONY: dev
dev: ## Start the development server with hot reload
	$(UVICORN) $(SRC_DIR).main:app --reload --host 0.0.0.0 --port 3000

.PHONY: test
test: ## Run tests
	$(PYTEST)

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	$(PYTEST) --cov

.PHONY: lint
lint: ## Lint code with ruff
	$(RUFF) check .

.PHONY: lint-fix
lint-fix: ## Lint and auto-fix issues with ruff
	$(RUFF) check --fix .

.PHONY: format
format: ## Format code with ruff
	$(RUFF) format .

.PHONY: db-init
db-init: ## Initialize database schema
	$(PY) -m $(SRC_DIR).init_db

.PHONY: db-seed
db-seed: ## Initialize and seed database with sample data
	$(PY) -m $(SRC_DIR).init_db
	$(PY) -m $(SRC_DIR).seed_data

.PHONY: db-migrate
db-migrate: ## Run database migrations (alias for db-init)
	$(PY) -m $(SRC_DIR).init_db
