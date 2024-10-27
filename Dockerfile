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
FROM python:3.11-slim

# ビルドステージから必要なファイルをすべて一度にコピー
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /app /app
COPY --from=build /usr/bin/ffmpeg /usr/bin/ffmpeg
COPY --from=build /usr/bin/open_jtalk /usr/bin/open_jtalk

# 作業ディレクトリを設定
WORKDIR /app

# ボットを実行
CMD ["python3", "main.py"]
