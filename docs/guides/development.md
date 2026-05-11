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

Docker Compose で統合環境を起動します。

```sh
make infra up
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
uv run pre-commit install --config ../ops/precommit/config.yaml
```
