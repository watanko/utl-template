SHELL := /bin/zsh
AREA := $(word 2,$(MAKECMDGOALS))

.PHONY: dev backend frontend check test compl install deploy infra docs security tooling vulnerabilities up down logs ps

dev:
	$(MAKE) -j 2 backend frontend

backend:
ifeq ($(filter check test compl,$(word 1,$(MAKECMDGOALS))),)
	cd backend && uv run uvicorn src.main:create_app --factory --reload --host 127.0.0.1 --port 8000
else
	@:
endif

frontend:
ifeq ($(filter check test,$(word 1,$(MAKECMDGOALS))),)
	cd frontend && corepack pnpm dev --config src/config/vite.config.ts --host 127.0.0.1 --port 5173
else
	@:
endif

install:
	cd backend && uv sync --all-extras --dev
	cd frontend && corepack enable && corepack pnpm install
	cd backend && uv run pre-commit install --config ../ops/precommit/config.yaml

check:
ifeq ($(AREA),backend)
	cd backend && uv run ruff format --check src tests
	cd backend && uv run ruff check src tests
	cd backend && uv run ty check src tests
	cd backend && uv run lint-imports --config importlinter.ini
else ifeq ($(AREA),frontend)
	cd frontend && corepack pnpm exec biome check --config-path biome.json .
	cd frontend && corepack pnpm tsc --noEmit
else ifeq ($(AREA),docs)
	cd frontend && corepack pnpm exec markdownlint-cli2 --config ../.markdownlint-cli2.yaml "../AGENTS.md" "../docs/**/*.md" "../infra/**/*.md" "../ops/**/*.md"
else ifeq ($(AREA),tooling)
	cd frontend && corepack pnpm exec knip --config src/config/knip.json
else ifeq ($(AREA),security)
	gitleaks detect --source . --redact --verbose
else ifeq ($(AREA),vulnerabilities)
	cd backend && uv run pip-audit
	cd frontend && corepack pnpm audit --audit-level high
else
	$(MAKE) check backend
	$(MAKE) check frontend
	$(MAKE) check docs
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

compl:
ifeq ($(AREA),backend)
	cd backend && uv run xenon --max-absolute B --max-modules A --max-average A src tests
else
	$(MAKE) compl backend
endif

infra:
ifeq ($(AREA),up)
	docker compose -f infra/local/compose.yaml up --build
else ifeq ($(AREA),down)
	docker compose -f infra/local/compose.yaml down --remove-orphans
else ifeq ($(AREA),logs)
	docker compose -f infra/local/compose.yaml logs -f
else ifeq ($(AREA),ps)
	docker compose -f infra/local/compose.yaml ps
else
	@echo "usage: make infra [up|down|logs|ps]"
endif

up down logs ps:
	@:

docs:
	@find docs -maxdepth 2 -type f | sort

security tooling vulnerabilities:
	@:

deploy:
	@echo "deploy target は未設定です。環境ごとのコマンドはレビュー後に追加してください。"
