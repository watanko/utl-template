# Terraform

cloud 環境へ展開するための雛形です。現時点では provider を固定せず、環境・権限・課金・secret 管理方針を決めたあとに provider module を追加する前提にしています。

基本方針:

- state backend は本番利用前に remote backend へ切り替える
- secret は `.tfvars` に書かず、cloud secret manager または CI の secret store から注入する
- `local`, `staging`, `production` を workspace またはディレクトリで分離する
- deploy は Taskfile に直書きせず、レビュー済みの手順として追加する

初期化例:

```sh
cd infra/terraform
terraform init
terraform validate
```
