# Codex hooks

このディレクトリには、Codex の project-local hooks から呼び出す script を置きます。

hook 定義は `.codex/hooks.json` にあります。Codex の `/hooks` で project hook が `Trusted` かつ `Active` になっていることを確認してください。

## 発火条件

| Codex event | Matcher | Script | 発火タイミング | 主な処理 |
| --- | --- | --- | --- | --- |
| `PostToolUse` | `Edit\|Write\|apply_patch` | `.codex/hooks/post-tool-check.sh` | Codex がファイル編集 tool を実行した直後 | 編集対象ファイルを `scripts/check_changed.py post-tool` に渡し、必要な `make check ...` だけを自動実行します。 |
| `PreToolUse` | `Bash` | `.codex/hooks/pre-commit-check.sh` | Codex が shell command を実行する直前 | `git commit ...` の場合だけ staged files を `scripts/check_changed.py pre-commit` で検査します。それ以外の shell command は素通しします。 |

## 変更ファイルと check の対応

`scripts/check_changed.py` は変更ファイルの path から実行する check を選びます。

| 変更 path | 実行される check |
| --- | --- |
| `backend/**` | `make check backend` |
| `frontend/**` | `make check frontend` |
| `Makefile`, `pre-commit.yaml`, `.codex/**`, `.github/**`, `docker/**`, `infra/terraform/**`, `scripts/**` | `make check tooling` |
| `.github/workflows/**`, `pre-commit.yaml` | `make check security` |

## 失敗時の挙動

- `PostToolUse` で check が失敗した場合は、hook が `decision: "block"` と失敗理由を返します。
- `PreToolUse` で `git commit ...` 前の check が失敗した場合は、hook が `permissionDecision: "deny"` を返します。
- 出力が長い場合、失敗理由は末尾 6000 文字に丸めます。

## 手動確認

hook と同じ dispatcher は手動でも実行できます。

```sh
make check changed
```

個別 hook script の構文確認は `make check tooling` に含まれています。
