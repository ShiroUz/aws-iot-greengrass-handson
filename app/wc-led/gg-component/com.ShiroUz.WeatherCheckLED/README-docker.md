# WeatherCheck Docker コンポーネント

このコンポーネントは、AWS IoT Greengrass上でDockerコンテナとして実行され、Raspberry Pi上でGPIOを制御するサンプルアプリケーションです。

## 構成ファイル

- `Dockerfile`: Pythonアプリケーションを実行するためのコンテナイメージを定義
- `docker-compose.yaml`: コンテナの実行環境と必要な権限を設定
- `recipe-docker.yaml`: Greengrassコンポーネントとしての設定
- `main.py`: GPIOを使用するPythonアプリケーション
- `requirements.txt`: 必要なPythonパッケージの一覧

## デプロイ方法

1. コンポーネントをビルドしてS3バケットにアップロード
2. AWS IoT Greengrassコンソールからコンポーネントをデプロイ
3. ターゲットデバイス上でコンポーネントが実行されることを確認

## 必要な権限

このコンポーネントはGPIOを制御するために特権モードで実行されます。
`docker-compose.yaml`ファイルで以下の設定を行っています：

- `privileged: true`: コンテナに特権アクセスを付与
- `/dev/gpiomem`と`/dev/mem`のデバイスマッピング
- `/sys`ディレクトリのマウント

## 注意事項

- このコンポーネントはRaspberry Pi (Buster)上での実行を想定しています
- GPIOピンの設定は必要に応じて`main.py`で変更してください

## requeirement.txtへの出力
$ poetry export -f requirements.txt -o requirements.txt --without-hashes --with rpi