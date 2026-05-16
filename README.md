# utl-template

FastAPI backend と React frontend を持つ full-stack project template です。

## 技術スタック

### Runtime / Framework

| 領域 | 技術 | 用途 |
| --- | --- | --- |
| Backend | Python 3.12 | backend 実装言語 |
| Backend | FastAPI | HTTP API 実装 |
| Backend | SQLAlchemy | DB access と ORM |
| Backend | Alembic | DB migration 管理 |
| Backend | Pydantic Settings | 環境変数と設定読み込み |
| Backend | structlog | structured logging |
| Frontend | TypeScript | frontend 実装言語 |
| Frontend | React | UI 実装 |
| Frontend | Vite | frontend dev server と build |
| Frontend | Zod | API response など外部入力の validation |
| Frontend | openapi-typescript | backend OpenAPI から frontend API 型を生成 |
| Infrastructure | Docker | backend / frontend container image |
| Infrastructure | Docker Compose | local integration environment |
| Infrastructure | Terraform | cloud infrastructure as code |

### Dependency Management

| 領域 | 技術 | 用途 |
| --- | --- | --- |
| Backend | uv | Python dependency と lock 管理 |
| Frontend | pnpm | Node dependency と lock 管理 |

### Test

| 領域 | 技術 | 用途 |
| --- | --- | --- |
| Backend | pytest | backend unit / integration test |
| Frontend | Vitest | frontend unit / component test |
| Frontend | Playwright | browser E2E test |

### Lint / Type / Quality

| 領域 | 技術 | 用途 |
| --- | --- | --- |
| Backend | ruff | Python format と lint |
| Backend | ty | Python type check |
| Backend | import-linter | layer 依存方向の検証 |
| Backend | vulture | 未使用コード検出 |
| Backend | xenon | code complexity check |
| Frontend | Biome | TypeScript format と lint |
| Frontend | Knip | unused dependency / export check |

### Automation / CI

| 領域 | 技術 | 用途 |
| --- | --- | --- |
| Automation | GitHub Actions | CI |
| Automation | Dependabot | dependency update PR |
| Automation | pre-commit | commit 前の local checks |

### Security

| 領域 | 技術 | 用途 |
| --- | --- | --- |
| Backend | pip-audit | Python dependency vulnerability scan |
| Security | gitleaks | secret scan |
| Security | Trivy | filesystem vulnerability scan |

## 主要コマンド

```sh
make install
make dev
make check
make test
```

backend DTO 変更後に frontend 型を同期する場合:

```sh
make sync dto
```

backend / frontend を個別に起動する場合:

```sh
make dev backend
make dev frontend
```

ローカル統合環境:

```sh
docker compose -f docker/compose.yaml up --build
```

環境変数と secret の一覧は [docs/env.md](docs/env.md) にあります。
