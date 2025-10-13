# AWS Greengrass Deployment ガイド

このドキュメントでは、AWS Greengrass V2のdeployment.jsonファイルの使用方法とベストプラクティスについて説明します。

## deployment.jsonとは

deployment.jsonは、AWS Greengrass V2でコンポーネントをデプロイする際の設定ファイルです。このファイルには、デプロイするコンポーネントとそのバージョン、設定パラメータ、デプロイメントポリシーなどが定義されています。

## ディレクトリ構造

```
app/gg-poc/
├── deployment-dev.json     # 開発環境用デプロイメント設定
└── gg-component/          # Greengrassコンポーネント
    └── com.ShiroUz.WeatherCheck/
        ├── recipe.yaml
        └── ...
```

## デプロイメント設定のバージョン管理

deployment.jsonファイルはGitなどのバージョン管理システムで管理することを強く推奨します。理由は以下の通りです：

1. **変更履歴の追跡**: デプロイ設定の変更履歴を追跡できます
2. **環境間の一貫性**: 開発、テスト、本番環境で一貫したデプロイ設定を維持できます
3. **チームコラボレーション**: チーム内での協業が容易になります
4. **ロールバック**: 問題発生時に以前の設定に戻すことが簡単です

## 環境別の設定管理

異なる環境（開発、テスト、本番）ごとに別々のdeployment.jsonファイルを用意することをお勧めします：

- `deployment-dev.json`: 開発環境用

## デプロイメントコマンド例

```bash
# 開発環境へのデプロイ
aws greengrassv2 create-deployment --cli-input-json file://deployment-dev.json

# 本番環境へのデプロイ
aws greengrassv2 create-deployment --cli-input-json file://deployment-prod.json
```

## セキュリティのベストプラクティス

1. **機密情報の管理**: 
   - 機密情報（シークレット、認証情報）はdeployment.jsonに直接記述せず、AWS Secrets Managerなどを利用してください
   - 必要に応じてAWS Systems Manager Parameter Storeを使用して設定を管理することも検討してください

2. **最小権限の原則**:
   - コンポーネントには必要最小限のアクセス許可のみを付与してください

## デプロイメント戦略

1. **カナリアデプロイメント**:
   - 重要な変更を行う場合は、まず一部のデバイスにデプロイしてテストすることを検討してください
   - `targetArn`にテスト用のモノグループを指定することで実現できます

2. **ロールバック計画**:
   - デプロイメントに問題が発生した場合のロールバック手順を用意してください
   - `failureHandlingPolicy`を`ROLLBACK`に設定することで、失敗時に自動的にロールバックすることができます

## CI/CDパイプラインへの統合

デプロイメント設定をCI/CDパイプラインに統合することで、自動化されたテストとデプロイメントを実現できます：

1. コードリポジトリへの変更をトリガーにしてテスト環境にデプロイ
2. テストが成功したら、承認ステップを経て本番環境にデプロイ

## 参考リンク

- [AWS Greengrass V2 デプロイメントの作成](https://docs.aws.amazon.com/greengrass/v2/developerguide/create-deployments.html)
- [AWS Greengrass V2 コンポーネントの開発](https://docs.aws.amazon.com/greengrass/v2/developerguide/develop-greengrass-components.html)