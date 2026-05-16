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

## pre-commit

```sh
cd backend
uv run pre-commit install --config ../pre-commit.yaml
```

Dependabot 設定は pre-commit の `dependabot-check` で YAML 構文と必須 ecosystem を検証します。
