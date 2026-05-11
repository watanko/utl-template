# infra

このディレクトリはローカル実行と cloud IaC の入口です。

- `local/`: Docker Compose によるローカル統合環境
- `docker/`: backend / frontend のコンテナビルド定義
- `terraform/`: cloud 環境へ展開するための Terraform 雛形

ローカル統合環境を起動します。

```sh
make infra up
```

停止します。

```sh
make infra down
```

cloud deploy は意図的に未実装です。実際の環境、権限、課金設定、secret 管理方針を確認してから追加してください。
