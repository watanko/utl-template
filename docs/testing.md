# テスト戦略

## Backend

backend は pytest を使用します。

```sh
task test:backend
```

対象:

- unit test
- coverage 90%以上
- 外部 API が絡む場合は marker で unit / e2e を分離

## Frontend

frontend は Vitest と Playwright を使用します。

```sh
task test:frontend
```

対象:

- Vitest による unit/component test
- Playwright による E2E
- UI snapshot を除く coverage 90%以上

## 全体検証

```sh
task check
task test
```

## CI

GitHub Actions は無効化済みです。workflow template は `.github/workflows/ci.yml.disabled` として保持します。

再有効化する場合は `.github/workflows/ci.yml` に戻してください。想定 job は以下です。

job:

- `backend`: ruff format/write, Ruff `ALL` rules with auto-fix, ty, deptry, import-linter, vulture, xenon, pip-audit, pytest
- `frontend`: Biome write/check, TypeScript, pnpm audit, Vitest, Playwright
- `tooling`: Knip, Codex hook config check, Dependabot config check, OpenAPI freshness check, actionlint, hadolint, Terraform fmt/validate, TFLint
- `security`: gitleaks, zizmor
- `filesystem-scan`: Trivy

`task check:fast:...` は Codex の `PostToolUse` hook 用です。編集直後は Ruff/Biome/TypeScript/ty/actionlint/Terraform fmt など短時間で終わる検査だけを実行し、依存監査や複雑度など重い検査は commit 前または CI で実行します。

## TypeScript tooling check

```sh
task check:tooling
```

Knip で未使用 dependency や未使用 export を検出します。

`task check:tooling` は以下も検証します。

- `.github/dependabot.yml`
- `.codex/hooks.json`
- `.codex/hooks/*.sh`
- `scripts/check_changed.py`
- `docs/openapi.json`
- 有効な GitHub Actions workflows
- Dockerfiles
- Terraform files

## Python unused code check

```sh
cd backend
uv run vulture
```

vulture は confidence 60%以上の未使用コード候補を検出します。テンプレートの拡張ポイントとして先置きしているクラスや設定名は `backend/pyproject.toml` の `[tool.vulture]` で除外します。

## secret scan

ローカルに `gitleaks` がある場合は以下で実行できます。

```sh
task check:security
```

pre-commit で gitleaks を実行します。GitHub Actions を再有効化する場合は CI でも実行します。

GitHub Actions workflow を再有効化する場合は zizmor でも検査します。local では以下を実行します。

```sh
task check:security
```

## vulnerability scan

```sh
task check:backend
task check:frontend
```

backend は `pip-audit`、frontend は `pnpm audit --audit-level high` で dependency vulnerability を検出します。

GitHub Actions を再有効化する場合は Trivy の filesystem scan も実行し、High / Critical の検出結果を SARIF としてアップロードします。
