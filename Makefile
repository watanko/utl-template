SHELL := /bin/bash
AREA := $(word 2,$(MAKECMDGOALS))
.DEFAULT_GOAL := help

.PHONY: help install install-tools dev check check-fast test sync deploy backend frontend tooling security changed dto _dev-backend _dev-frontend

help:
	@echo "Usage:"
	@echo "  make <target> [area]"
	@echo ""
	@echo "Targets:"
	@echo "  make install              Install tools, backend/frontend dependencies, and pre-commit"
	@echo "  make install-tools        Install local CLI tools used by checks"
	@echo "  make dev                  Run backend and frontend locally"
	@echo "  make dev backend          Run backend locally"
	@echo "  make dev frontend         Run frontend locally"
	@echo "  make check                Run all checks and available auto-fixes"
	@echo "  make check backend        Run backend auto-fixes, checks, complexity, and dependency audit"
	@echo "  make check frontend       Run frontend auto-fixes, checks, and dependency audit"
	@echo "  make check tooling        Run repository tooling auto-fixes and checks"
	@echo "  make check changed        Run auto-fixes and checks selected from changed files"
	@echo "  make check security       Run security checks"
	@echo "  make check-fast backend   Run fast backend auto-fixes and checks"
	@echo "  make check-fast frontend  Run fast frontend auto-fixes and checks"
	@echo "  make check-fast tooling   Run fast repository tooling checks"
	@echo "  make test                 Run all tests"
	@echo "  make test backend         Run backend tests"
	@echo "  make test frontend        Run frontend unit and E2E tests"
	@echo "  make sync dto             Export OpenAPI and regenerate frontend API types"
	@echo "  make deploy               Show deploy placeholder"

install:
	$(MAKE) install-tools
	cd backend && uv sync --all-extras --dev
	cd frontend && corepack enable && corepack pnpm install
	cd backend && uv run pre-commit install --config ../pre-commit.yaml

install-tools:
	bash scripts/install_tools.sh

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
	cd backend && uv run ruff format src tests
	cd backend && uv run ruff check --fix src tests
	cd backend && uv run ty check src tests
	cd backend && uv run deptry src tests
	cd backend && uv run lint-imports --config importlinter.ini
	cd backend && uv run vulture
	cd backend && uv run xenon --max-absolute B --max-modules A --max-average A src tests
	cd backend && uv run pip-audit
else ifeq ($(AREA),frontend)
	cd frontend && corepack pnpm exec biome check --write --config-path biome.json .
	cd frontend && corepack pnpm tsc --noEmit
	cd frontend && corepack pnpm audit --audit-level high
else ifeq ($(AREA),tooling)
	cd frontend && corepack pnpm exec knip --config src/config/knip.json
	python3 -m json.tool .codex/hooks.json >/dev/null
	bash -n .codex/hooks/post-tool-check.sh .codex/hooks/pre-commit-check.sh scripts/install_tools.sh
	python3 -m py_compile scripts/check_changed.py
	cd backend && uv run python ../scripts/check_dependabot.py
	cd backend && uv run python ../scripts/check_openapi.py
	actionlint
	hadolint docker/backend.Dockerfile docker/frontend.Dockerfile
	terraform -chdir=infra/terraform fmt
	terraform -chdir=infra/terraform init -backend=false
	terraform -chdir=infra/terraform validate
	tflint --chdir=infra/terraform --init
	tflint --chdir=infra/terraform
else ifeq ($(AREA),security)
	gitleaks detect --source . --redact --verbose
	uvx zizmor --offline .
else ifeq ($(AREA),changed)
	python3 scripts/check_changed.py changed
else
	$(MAKE) check backend
	$(MAKE) check frontend
	$(MAKE) check tooling
endif

check-fast:
ifeq ($(AREA),backend)
	cd backend && uv run ruff format src tests
	cd backend && uv run ruff check --fix src tests
	cd backend && uv run ty check src tests
else ifeq ($(AREA),frontend)
	cd frontend && corepack pnpm exec biome check --write --config-path biome.json .
	cd frontend && corepack pnpm tsc --noEmit
else ifeq ($(AREA),tooling)
	python3 -m json.tool .codex/hooks.json >/dev/null
	bash -n .codex/hooks/post-tool-check.sh .codex/hooks/pre-commit-check.sh scripts/install_tools.sh
	python3 -m py_compile scripts/check_changed.py
	actionlint
	terraform -chdir=infra/terraform fmt
else
	$(MAKE) check-fast backend
	$(MAKE) check-fast frontend
	$(MAKE) check-fast tooling
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

backend frontend tooling security changed:
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
