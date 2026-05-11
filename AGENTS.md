## 1. 一般事項

- ユーザーは日本語話者です。思考は英語で、最終回答は日本語で行います。
- ファイル内コメントは英語で端的に書きます。
- 質問には回答を返し、実装指示が明確でない限り勝手に実行しません。
- `git push` や cloud deploy は必ず許可を取ってから実行します。

## 2. コーディング規約

- すべてのコードに型アノテーションを追加します。
- `Any` は使用しません。内部処理と外部入出力のどちらにもモデルを定義します。
- 1ファイルは1000行未満に保ちます。
- 1ディレクトリ直下の要素が7つ以上になる場合は、サブディレクトリへ分割します。
- クラス・関数には docstring を追加し、必要に応じて Args, Attributes, Returns, Raises を充実させます。
- エラーは正しい境界で発生させます。`None` や空リストで失敗を隠しません。
- ハードコードは避け、設定ファイルや環境変数で外部化します。
- `try` は async fan-out や外部 API など Errorable な境界でのみ使用します。
- 修正はアドホックにせず、拡張可能性を考えて実装します。
- 振る舞いを定義する抽象と実装クラスを分けます。
- 型変換や解析の重複を取り除く場合を除き、ヘルパー関数を過剰に増やしません。
- コメントは処理内容ではなく、why / why not を説明します。
- テストコメントは "A should", "A should not", "A must", "A must not" の形式で書きます。

## 3. ツール

- pre-commit でテスト・lint・format を自動化します。
- よく使う操作は Makefile target に集約します。
  - `make dev`
  - `make test backend`
  - `make test frontend`
  - `make check backend`
  - `make check frontend`
  - `make compl backend`
  - `make deploy`

## 4. バックエンド

- 独立したコアレイヤパターンを使用します。
- 依存方向は `core -> adapters -> api` とし、逆方向 import は禁止します。
- パッケージ管理は `uv` を使用し、`pip` は使用しません。
- 依存追加は `uv add <package>` で行います。
- FastAPI, SQLAlchemy, structlog, pytest, ruff, ty, import-linter, xenon を使用します。
- LLM 呼び出しでは structured output を使用します。
- 外部 API にはレート制限、指数バックオフ、リクエスト数・コスト logging を入れます。
- 外部 API 境界では Result 型を使用します。

## 5. フロントエンド

- React + Vite を使用します。
- バックエンド風のレイヤリングより、人間にとっての可読性を優先します。
- validation を超える業務ロジックはフロントエンドへ置きません。
- パッケージ管理は pnpm を使用します。
- `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes` を有効化します。
- `any` は使用しません。`unknown` は parse 直後の境界だけで許可し、すぐに絞り込みます。
- バックエンド DTO とフロントエンドモデルを手動同期しません。
- Biome, Vitest, Playwright を使用します。
