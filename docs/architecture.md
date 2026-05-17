# アーキテクチャ

## Backend

backend は `backend/src` を Python package root とします。

依存方向:

```text
core -> adapters -> api
```

`core` は業務ルールとユースケースを持ち、`adapters` と `api` を import しません。依存方向は import-linter で検証します。

```sh
task check:backend
```

DB schema migration は Alembic で管理します。migration script は `backend/src/adapters/db/migrations` に配置します。

## Frontend

frontend は `frontend/src` 配下に UI、API client、test、E2E、設定を配置します。backend のような厳密なレイヤリングは行わず、読みやすさを優先します。

外部入力は Zod で検証し、`unknown` は parse 境界だけで扱います。

backend / frontend DTO は OpenAPI を経由して同期します。backend の schema を `docs/openapi.json` に export し、`openapi-typescript` で `frontend/src/api/generated/schema.ts` を生成します。

```sh
task sync:dto
```

## Infra

`docker/` は Dockerfile と Docker Compose によるローカル統合環境です。`infra/terraform` は cloud provider を選定したあとに拡張する IaC の入口です。
