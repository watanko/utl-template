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
make compl backend
```

## CI

GitHub Actions は `.github/workflows/ci.yml` で定義します。

job:

- `backend`: ruff, ty, import-linter, pytest, xenon
- `frontend`: Biome, TypeScript, Vitest, Playwright
- `docs`: markdownlint-cli2, Knip
- `security`: gitleaks
- `vulnerabilities`: pip-audit, pnpm audit, Trivy

## ドキュメント lint

```sh
make check docs
```

## TypeScript tooling check

```sh
make check tooling
```

Knip で未使用 dependency や未使用 export を検出します。

## secret scan

ローカルに `gitleaks` がある場合は以下で実行できます。

```sh
make check security
```

pre-commit と GitHub Actions でも gitleaks を実行します。

## vulnerability scan

```sh
make check vulnerabilities
```

backend は `pip-audit`、frontend は `pnpm audit --audit-level high` で dependency vulnerability を検出します。

GitHub Actions では Trivy の filesystem scan も実行し、High / Critical の検出結果を SARIF としてアップロードします。
