# 運用手順

## ローカル統合環境

起動:

```sh
make infra up
```

状態確認:

```sh
make infra ps
```

ログ:

```sh
make infra logs
```

停止:

```sh
make infra down
```

## deploy

`make deploy` は未設定です。cloud への deploy は、対象環境、権限、secret 管理、課金影響を確認してから実装します。

## secret 管理

`.env` と `.tfvars` は git 管理しません。共有が必要な値は `.env.example` や `*.tfvars.example` に安全な例だけを書きます。
