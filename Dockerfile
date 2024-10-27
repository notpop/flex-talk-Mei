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
