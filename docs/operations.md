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

`make deploy` は未設定です。cloud への deploy は、対象環境、権限、secret 管理、課金影響を確認してから実装します。

## secret 管理

`.env` と `.tfvars` は git 管理しません。共有が必要な値は `.env.example` や `*.tfvars.example` に安全な例だけを書きます。

## dependency update

Dependabot は `.github/dependabot.yml` で設定します。

対象:

- backend uv dependencies
- frontend npm dependencies
- GitHub Actions
- Docker images
- Terraform providers/modules

更新 PR は月曜 09:00 Asia/Tokyo に週次で作成します。
