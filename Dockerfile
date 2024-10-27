# 第一段階：依存関係のインストールとビルド
FROM python:3.11-slim AS build

# 必要なパッケージのインストール、リポジトリのクローン、依存関係のインストールを1つのRUNで実行
RUN apt-get update && \
    apt-get install -y git ffmpeg open-jtalk curl && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /app && cd /app && \
    git clone https://github.com/notpop/flex-talk-Mei.git . && \
    # Python依存パッケージのインストール
    pip install --no-cache-dir -r requirements.txt

# 第二段階：最小限のランタイム環境
FROM python:3.11-slim

# ビルド時に渡す環境変数を指定（Railwayから提供される）
ARG DISCORD_SERIAL_KEY
ARG DISCORD_APPLICATION_ID
ARG VOICEBOX_API_KEY
ARG VOICE_DIRECTORY

# これらの環境変数をランタイムで使用できるように設定
ENV DISCORD_SERIAL_KEY=$DISCORD_SERIAL_KEY \
    DISCORD_APPLICATION_ID=$DISCORD_APPLICATION_ID \
    VOICEBOX_API_KEY=$VOICEBOX_API_KEY \
    VOICE_DIRECTORY=$VOICE_DIRECTORY

# 必要なパッケージのインストールを実行
RUN apt-get update && \
    apt-get install -y ffmpeg open-jtalk && \
    rm -rf /var/lib/apt/lists/*

# ビルドステージからPythonパッケージを含むディレクトリをコピー
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /app /app

# 作業ディレクトリを設定
WORKDIR /app

# ボットを実行
CMD ["python3", "main.py"]
