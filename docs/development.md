# 開発手順

## 初期セットアップ

```sh
make install
```

## ローカル起動

backend と frontend を直接起動します。

```sh
make dev
```

backend だけを起動します。

```sh
make dev backend
```

frontend だけを起動します。

```sh
make dev frontend
```

Docker Compose で統合環境を起動します。

```sh
docker compose -f docker/compose.yaml up --build
```

## 依存追加

backend:

```sh
cd backend
uv add <package>
```

frontend:

```sh
cd frontend
corepack pnpm add <package>
```

## DB migration

Alembic migration を作成します。

```sh
cd backend
uv run alembic revision --autogenerate -m "describe change"
uv run alembic upgrade head
```

## DTO 同期

backend の FastAPI schema から frontend 型を生成します。

```sh
make sync dto
```

生成物:

- `docs/openapi.json`
- `frontend/src/api/generated/schema.ts`

## pre-commit

```sh
cd backend
uv run pre-commit install --config ../pre-commit.yaml
```

Dependabot 設定は pre-commit の `dependabot-check` で YAML 構文と必須 ecosystem を検証します。
