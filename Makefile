SHELL := /bin/zsh
AREA := $(word 2,$(MAKECMDGOALS))
.DEFAULT_GOAL := help

.PHONY: help install dev check test sync deploy backend frontend tooling security dto _dev-backend _dev-frontend

help:
	@echo "Usage:"
	@echo "  make <target> [area]"
	@echo ""
	@echo "Targets:"
	@echo "  make install              Install backend/frontend dependencies and pre-commit"
	@echo "  make dev                  Run backend and frontend locally"
	@echo "  make dev backend          Run backend locally"
	@echo "  make dev frontend         Run frontend locally"
	@echo "  make check                Run all checks"
	@echo "  make check backend        Run backend checks, complexity, and dependency audit"
	@echo "  make check frontend       Run frontend checks and dependency audit"
	@echo "  make check tooling        Run TypeScript tooling checks"
	@echo "  make check security       Run secret scan"
	@echo "  make test                 Run all tests"
	@echo "  make test backend         Run backend tests"
	@echo "  make test frontend        Run frontend unit and E2E tests"
	@echo "  make sync dto             Export OpenAPI and regenerate frontend API types"
	@echo "  make deploy               Show deploy placeholder"

install:
	cd backend && uv sync --all-extras --dev
	cd frontend && corepack enable && corepack pnpm install
	cd backend && uv run pre-commit install --config ../pre-commit.yaml

dev:
ifeq ($(AREA),backend)
	cd backend && uv run uvicorn src.main:create_app --factory --reload --host 127.0.0.1 --port 8000
else ifeq ($(AREA),frontend)
	cd frontend && corepack pnpm dev --config src/config/vite.config.ts --host 127.0.0.1 --port 5173
else
	$(MAKE) -j 2 _dev-backend _dev-frontend
endif

_dev-backend:
	cd backend && uv run uvicorn src.main:create_app --factory --reload --host 127.0.0.1 --port 8000

_dev-frontend:
	cd frontend && corepack pnpm dev --config src/config/vite.config.ts --host 127.0.0.1 --port 5173

check:
ifeq ($(AREA),backend)
	cd backend && uv run ruff format --check src tests
	cd backend && uv run ruff check src tests
	cd backend && uv run ty check src tests
	cd backend && uv run lint-imports --config importlinter.ini
	cd backend && uv run vulture
	cd backend && uv run xenon --max-absolute B --max-modules A --max-average A src tests
	cd backend && uv run pip-audit
else ifeq ($(AREA),frontend)
	cd frontend && corepack pnpm exec biome check --config-path biome.json .
	cd frontend && corepack pnpm tsc --noEmit
	cd frontend && corepack pnpm audit --audit-level high
else ifeq ($(AREA),tooling)
	cd frontend && corepack pnpm exec knip --config src/config/knip.json
	cd backend && uv run python ../scripts/check_dependabot.py
	cd backend && uv run python ../scripts/check_openapi.py
else ifeq ($(AREA),security)
	gitleaks detect --source . --redact --verbose
else
	$(MAKE) check backend
	$(MAKE) check frontend
	$(MAKE) check tooling
endif

test:
ifeq ($(AREA),backend)
	cd backend && uv run pytest
else ifeq ($(AREA),frontend)
	cd frontend && corepack pnpm vitest run --config src/config/vite.config.ts --coverage
	cd frontend && corepack pnpm playwright test --config src/config/playwright.config.ts
else
	$(MAKE) test backend
	$(MAKE) test frontend
endif

backend frontend tooling security:
	@if [ "$(word 1,$(MAKECMDGOALS))" = "$@" ]; then $(MAKE) help; fi

sync:
ifeq ($(AREA),dto)
	cd backend && uv run python ../scripts/export_openapi.py
	cd frontend && corepack pnpm run generate:api
else
	@$(MAKE) help
endif

dto:
	@:

deploy:
	@echo "deploy target は未設定です。環境ごとのコマンドはレビュー後に追加してください。"
