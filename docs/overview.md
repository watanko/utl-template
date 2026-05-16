# 概要

このテンプレートは FastAPI backend と React frontend を持つ full-stack プロジェクトの出発点です。

目的:

- backend は core / adapters / api の依存方向を守る
- frontend は React + Vite で可読性を優先する
- format, lint, type-check, test, complexity check を Makefile から実行できる
- ローカル統合環境を Docker Compose で起動できる
- cloud IaC は Terraform 雛形から安全に拡張できる

主要コマンド:

```sh
make install
make check
make test
make dev
```
