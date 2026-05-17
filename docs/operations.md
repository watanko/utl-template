# 運用手順

## ローカル統合環境

起動:

```sh
docker compose -f docker/compose.yaml up --build
```

状態確認:

```sh
docker compose -f docker/compose.yaml ps
```

ログ:

```sh
docker compose -f docker/compose.yaml logs -f
```

停止:

```sh
docker compose -f docker/compose.yaml down --remove-orphans
```

## deploy

`task deploy` は未設定です。cloud への deploy は、対象環境、権限、secret 管理、課金影響を確認してから実装します。

## secret 管理

`.env` と `.tfvars` は git 管理しません。共有が必要な値は `.env.example` や `*.tfvars.example` に安全な例だけを書きます。

環境変数と secret の一覧は `docs/env.md` にまとめます。source of truth は `backend/src/config.py` の `Settings` です。`Settings` は Pydantic Settings の schema として扱い、各 field には型、default、`description` を書きます。公開してよい設定値は `str`, `bool`, `list[str]` などで定義し、secret は `SecretStr` などの secret 型を使います。

`SettingsConfigDict(extra="forbid")` を使い、未定義の環境変数を設定 schema に混ぜない方針です。新しい環境変数を追加する場合は、`Settings` と `backend/.env.example` を同時に更新します。

`.env.example` に置く secret は local 起動用のダミー値だけにします。production / staging では GitHub Actions secrets、cloud secret manager、または Terraform remote state に secret を直接残さない仕組みを使います。

## dependency update

Dependabot は `.github/dependabot.yml` で設定します。

対象:

- backend uv dependencies
- frontend npm dependencies
- GitHub Actions
- Docker images
- Terraform providers/modules

更新 PR は月曜 09:00 Asia/Tokyo に週次で作成します。
