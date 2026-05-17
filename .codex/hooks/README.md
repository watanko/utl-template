# Codex hooks

このディレクトリには、Codex の project-local hooks から呼び出す script を置きます。

hook 定義は `.codex/hooks.json` にあります。Codex の `/hooks` で project hook が `Trusted` かつ `Active` になっていることを確認してください。

## 発火条件

| Codex event | Matcher | Script | 発火タイミング | 主な処理 |
| --- | --- | --- | --- | --- |
| `PostToolUse` | `Edit\|Write\|apply_patch` | `.codex/hooks/post-tool-check.sh` | Codex がファイル編集 tool を実行した直後 | 編集対象ファイルを `scripts/check_changed.py post-tool` に渡し、必要な `task check:fast:...` だけを自動実行します。Ruff, Biome, Terraform fmt など修正可能なものは自動修正します。 |
| `PreToolUse` | `Bash` | `.codex/hooks/pre-commit-check.sh` | Codex が shell command を実行する直前 | `git commit ...` の場合だけ staged files を `scripts/check_changed.py pre-commit` で full check します。修正可能なものは commit 前に自動修正し、対象 files を再 stage します。それ以外の shell command は素通しします。 |

## 変更ファイルと check の対応

`scripts/check_changed.py` は変更ファイルの path から実行する check を選びます。

| 変更 path | `PostToolUse` の fast check | `git commit ...` 前の full check |
| --- | --- | --- |
| `backend/**` | `task check:fast:backend` | `task check:backend` |
| `frontend/**` | `task check:fast:frontend` | `task check:frontend` |
| `Taskfile.yml`, `pre-commit.yaml`, `.codex/**`, `.github/**`, `docker/**`, `infra/terraform/**`, `scripts/**` | `task check:fast:tooling` | `task check:tooling` |
| `.github/workflows/**`, `pre-commit.yaml` | `task check:security` | `task check:security` |

## 自動修正と失敗時の挙動

- `task check:backend` は `ruff format` と `ruff check --fix` を実行します。
- `task check:frontend` は `biome check --write` を実行します。
- `task check:tooling` は `terraform fmt` を実行します。
- `task check:fast:backend` は Ruff format/fix と ty だけを実行します。
- `task check:fast:frontend` は Biome write/check と TypeScript check だけを実行します。
- `task check:fast:tooling` は hook config 構文、`actionlint`, `terraform fmt` だけを実行します。
- `PreToolUse` の `git commit ...` では、自動修正後に対象 staged files を `git add -A` で再 stage します。
- 自動修正できない検査で失敗した場合、`PostToolUse` は `decision: "block"` と失敗理由を返します。
- 自動修正後も `git commit ...` 前の検査が失敗した場合、`PreToolUse` は `permissionDecision: "deny"` を返します。
- hook は自動修正後の差分を残します。変更を自動ロールバックしません。
- 出力が長い場合、失敗理由は末尾 6000 文字に丸めます。

## 手動確認

hook と同じ dispatcher は手動でも実行できます。

```sh
task check:changed
```

個別 hook script の構文確認は `task check:tooling` に含まれています。
