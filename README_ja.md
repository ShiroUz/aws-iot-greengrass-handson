## aws-iot-greengrass-handson

<table>
	<thead>
    	<tr>
      		<th style="text-align:center"><a href="README.md">English</th>
      		<th style="text-align:center">日本語</a></th>
    	</tr>
  	</thead>
</table>

## 概要
このリポジトリは、Raspberry PiをIoTデバイスとして利用し、AWS IoT Greengrassを活用したエッジコンピューティングシステムを構築するためのハンズオン教材です。

詳細は[TECH BOOK By KINTO Technologies Vol.01](https://techbookfest.org/product/qCPrJpWLmKnLt7eWVd9zJ6)の`第13章 AWS IoT Greengrassをサンプルアプリを使ってハンズオンしてみよう`
で詳しく解説されています。無料でダウンロードして読めるので、ご確認ください。

### 主な機能
このプロジェクトには、2つのアプリケーション例が含まれています：

#### 1. Weather Check LED (wc-led)
- 天気情報をチェックしてLEDで通知するアプリケーション
- AWS Lambda、Amazon Polly、Amazon Bedrockを活用した音声合成機能
- IoT Coreを経由したデバイス制御

#### 2. AI Driving Partner (ai-dp)
- AI駆動のパートナーアプリケーション
- AWS Lambda、Amazon Polly、Amazon Bedrockによる対話型機能
- IoT Core経由でのリアルタイム通信

### アーキテクチャ構成
- **デバイス層**: Raspberry Pi上でAWS IoT Greengrass V2を実行
- **エッジ層**: Dockerコンテナ化されたGreengrassコンポーネント
- **クラウド層**: AWS Lambda、IoT Core、S3、DynamoDB、Bedrockなどのマネージドサービス
- **IaC**: Terraformによるインフラ管理（infra/配下）
- **CI/CD**: GitHub ActionsによるDockerイメージのビルド・デプロイ自動化

### 技術スタック
- **デバイスプロビジョニング**: Ansible、systemdサービス
- **コンテナ化**: Docker、Docker Compose
- **インフラストラクチャ**: Terraform
- **言語**: Python 3.13
- **CI/CD**: GitHub Actions（OIDC認証）
- **AWS サービス**: IoT Greengrass V2、IoT Core、Lambda、Bedrock、Polly、S3、DynamoDB

## fork後にGithub Repositoryに必要な設定
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