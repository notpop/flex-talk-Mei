# 第一段階：依存関係のインストールとビルド
FROM python:3.11-slim AS build

# 必要なパッケージのインストール、リポジトリのクローン、依存関係のインストールを1つのRUNで実行
RUN apt-get update && \
    apt-get install -y git ffmpeg open-jtalk curl && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /app && \
    git clone https://github.com/notpop/flex-talk-Mei.git /app && \
    # Python依存パッケージのインストール
    pip install --no-cache-dir -r /app/requirements.txt

# 第二段階：distrolessの最小限のランタイム環境
FROM gcr.io/distroless/python3-debian12

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

# ビルドステージから必要なファイルをすべて一度にコピー
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /app /app
COPY --from=build /usr/bin/ffmpeg /usr/bin/ffmpeg
COPY --from=build /usr/bin/open_jtalk /usr/bin/open_jtalk

# 作業ディレクトリを設定
WORKDIR /app

# ボットを実行
CMD ["main.py"]
