# 開発手順

## 初期セットアップ

Task CLI が未導入の場合は、初回だけ直接 tool installer を実行します。

```sh
bash scripts/install_tools.sh
```

```sh
task install
```

## ローカル起動

backend と frontend を直接起動します。

```sh
task dev
```

backend だけを起動します。

```sh
task dev:backend
```

frontend だけを起動します。

```sh
task dev:frontend
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
task sync:dto
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

## Codex hooks

Codex は `.codex/hooks.json` の project-local hook を読み込みます。project-local hook は、その project の `.codex/` layer が trusted の場合に有効です。

- `PostToolUse`: `Edit`, `Write`, `apply_patch` の直後に `.codex/hooks/post-tool-check.sh` を自動実行します。
- `PreToolUse`: `Bash` 実行直前に `.codex/hooks/pre-commit-check.sh` を自動実行します。script 側で `git commit` 以外は通します。

hook は `scripts/check_changed.py` で変更ファイルを分類します。`PostToolUse` では反復速度を優先して必要な `task check:fast:...` だけを実行し、`git commit ...` 前の `PreToolUse` では `task check:backend`, `task check:frontend`, `task check:tooling`, `task check:security` の full check を実行します。Ruff, Biome, Terraform fmt など修正可能なものは自動修正します。`git commit ...` 前の hook では自動修正後に対象 files を再 stage します。自動修正できない検査で失敗した場合は hook が agent に block 理由を返します。hook は変更を自動ロールバックしません。

## 外部 CLI

`task install` は macOS と Ubuntu の両方で、`task check:tooling` と `task check:security` が使う外部 CLI も導入します。

- macOS: `Brewfile` 経由で Homebrew package を導入します。
- Ubuntu: `scripts/install_tools.sh` 経由で apt, HashiCorp apt repository, Go install, release binary を組み合わせて導入します。

CI では workflow 内で setup します。

- `actionlint`
- `gitleaks`
- `hadolint`
- `terraform`
- `tflint`
- `uvx zizmor`
