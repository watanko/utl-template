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
