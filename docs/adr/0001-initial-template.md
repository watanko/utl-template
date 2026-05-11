# ADR 0001: 初期テンプレート構成

## Status

Accepted

## Context

backend, frontend, infra, docs を一つの repository で管理し、初期段階から品質チェックとレイヤ制約を自動化したい。

## Decision

- backend は FastAPI と `backend/src` package root を採用する
- backend は core / adapters / api の依存方向を import-linter で検証する
- frontend は React + Vite を採用する
- local infra は Docker Compose で提供する
- cloud IaC は Terraform の provider 非依存雛形から開始する
- docs は root 直下の `docs/` に集約する

## Consequences

- 初期から `make check`, `make test`, `make compl backend` を実行できる
- cloud provider を決めるまでは deploy target を未実装に保つ
- root 直下は `infra/` と `docs/` を置くため、直下要素数ルールの例外とする
