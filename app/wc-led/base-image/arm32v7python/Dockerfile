FROM arm32v7/python:3.12.10-slim-bookworm AS builder

# 必要なパッケージのインストール
RUN apt update && apt install -y \
    build-essential \
    cmake \
    git \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-gpiozero \
    vim \
    wget \
    alsa-utils \
    mpg321 \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの設定
WORKDIR /app

# 必要なファイルをコピー
COPY requirements.txt .

# COPY src/ ./src/

# 依存関係のインストール
RUN pip install --no-cache-dir --verbose -r requirements.txt