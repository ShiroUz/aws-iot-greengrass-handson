## Github Repositoryに必要な設定
### デバイスのProvisioningで利用するパラメータ
設定方法は以下を参考
https://docs.github.com/ja/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets

#### - Secrets
- `IMAGES_RELEASE_ROLE_ARN`: Github Actionsで利用するImageをS3に配置するためのRole
  - `arn:aws:iam::${account_name}:role/aws-gg-handson-images-release-gha-role`
- `GG_COMPONENT_RELEASE_ROLE_ARN`: Github ActionsでGreengrass コンポーネントをリリースするためのRole
  - `arn:aws:iam::${account_name}:role/aws-gg-handson-gg-component-release-gha-role`
- `GG_COMPONENT_DEPLOY_ROLE_ARN`: Github ActionsでGreengrass コンポーネントをデプロイするためのRole
  - `arn:aws:iam::${account_name}:role/aws-gg-handson-gg-component-deploy-gha-role`
- `IOT_DATA_ENDPOINT`: IoT Dataエンドポイント
  - 確認方法は `IOT_DATA_ENDPOINT確認方法`を参照
- `IOT_CRED_ENDPOINT`: IoT認証情報エンドポイント
  - 確認方法は `IOT_CRED_ENDPOINT確認方法`を参照
- `IMAGES_PUT_S3_BUCKET_NAME`: S3バケット名（イメージ保存用）

### IOT_DATA_ENDPOINT確認方法

AWS CLIを使用してIoT Dataエンドポイントを確認します：

```bash
aws iot describe-endpoint --endpoint-type iot:Data-ATS --region ap-northeast-1
```

結果の`endpointAddress`の値を`IOT_DATA_ENDPOINT`として設定してください。

### IOT_CRED_ENDPOINT確認方法

AWS CLIを使用してIoT認証情報エンドポイントを確認します：

```bash
aws iot describe-endpoint --endpoint-type iot:CredentialProvider --region ap-northeast-1
```

結果の`endpointAddress`の値を`IOT_CRED_ENDPOINT`として設定してください。

### OpenID Connectの作成
以下を参考に、作成してください。
https://docs.github.com/ja/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws