# テスト戦略

## Backend

backend は pytest を使用します。

```sh
make test backend
```

対象:

- unit test
- coverage 90%以上
- 外部 API が絡む場合は marker で unit / e2e を分離

## Frontend

frontend は Vitest と Playwright を使用します。

```sh
make test frontend
```

対象:

- Vitest による unit/component test
- Playwright による E2E
- UI snapshot を除く coverage 90%以上

## 全体検証

```sh
make check
make test
```

## CI

GitHub Actions は `.github/workflows/ci.yml` で定義します。

job:

- `backend`: ruff format, Ruff `ALL` rules, ty, deptry, import-linter, vulture, xenon, pip-audit, pytest
- `frontend`: Biome, TypeScript, pnpm audit, Vitest, Playwright
- `tooling`: Knip, Dependabot config check, OpenAPI freshness check, actionlint, hadolint, Terraform validate, TFLint
- `security`: gitleaks, zizmor
- `filesystem-scan`: Trivy

## TypeScript tooling check

```sh
make check tooling
```

Knip で未使用 dependency や未使用 export を検出します。

`make check tooling` は以下も検証します。

- `.github/dependabot.yml`
- `docs/openapi.json`
- GitHub Actions workflows
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
make check security
```

pre-commit と GitHub Actions でも gitleaks を実行します。

GitHub Actions workflow は zizmor でも検査します。local では以下を実行します。

```sh
make check security
```

## vulnerability scan

```sh
make check backend
make check frontend
```

backend は `pip-audit`、frontend は `pnpm audit --audit-level high` で dependency vulnerability を検出します。

GitHub Actions では Trivy の filesystem scan も実行し、High / Critical の検出結果を SARIF としてアップロードします。
