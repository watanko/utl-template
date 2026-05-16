# 環境変数

環境変数の source of truth は `backend/src/config.py` の `Settings` です。新しい環境変数を追加する場合は、`Settings` に型、default、`description` を追加し、必要に応じて `backend/.env.example` とこの文書を更新します。

公開してよい設定値は `str`, `bool`, `list[str]` などで定義します。secret は `SecretStr` などの secret 型で定義し、`.env.example` には local 起動用のダミー値だけを書きます。

## Backend

| 変数名 | 型 | 概要 | 必須 | デフォルト値 | local 注入元 | cloud 注入元 |
| --- | --- | --- | --- | --- | --- | --- |
| `APP_NAME` | `str` | logs と API metadata に使う公開 service name | No | `utl-template` | `backend/.env` または `docker/compose.yaml` | deployment manifest / Terraform variables |
| `APP_ENV` | `local \| test \| staging \| production` | runtime environment name | No | `local` | `backend/.env` または `docker/compose.yaml` | deployment manifest / Terraform variables |
| `DATABASE_URL` | `str` | SQLAlchemy database URL | No | `sqlite:///./local.db` | `backend/.env` または `docker/compose.yaml` | cloud secret manager / GitHub Actions secrets |
| `JWT_SECRET` | `SecretStr` | JWT signing secret | No | `replace-me-local-only` | `backend/.env` の local dummy value | cloud secret manager / GitHub Actions secrets |
| `LOG_LEVEL` | `str` | process log level | No | `INFO` | `backend/.env` または `docker/compose.yaml` | deployment manifest / Terraform variables |

## Docker Compose

| 変数名 | 概要 | 必須 | デフォルト値 | local 注入元 | cloud 注入元 |
| --- | --- | --- | --- | --- | --- |
| `POSTGRES_DB` | local PostgreSQL database name | Yes | なし | `docker/compose.yaml` | cloud では原則使わず managed database 側で管理 |
| `POSTGRES_USER` | local PostgreSQL user | Yes | なし | `docker/compose.yaml` | cloud では原則使わず managed database 側で管理 |
| `POSTGRES_PASSWORD` | local PostgreSQL password | Yes | なし | `docker/compose.yaml` の local dummy value | cloud secret manager / GitHub Actions secrets |

## Frontend

| 変数名 | 型 | 概要 | 必須 | デフォルト値 | local 注入元 | cloud 注入元 |
| --- | --- | --- | --- | --- | --- | --- |
| `VITE_API_BASE_URL` | `str` | frontend から参照する API base URL | No | なし | `docker/compose.yaml` または Vite env file | hosting provider environment variables |
