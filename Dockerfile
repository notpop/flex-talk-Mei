# 第一段階：依存関係のインストールとビルド
FROM python:3.11-slim AS build

# 必要なパッケージのインストール、リポジトリのクローン、依存関係のインストールを1つのRUNで実行
RUN apt-get update && \
    apt-get install -y git ffmpeg open-jtalk curl && \
    rm -rf /var/lib/apt/lists/* && \
    # 作業ディレクトリを作成しリポジトリをクローン
    mkdir /app && cd /app && \
    git clone https://github.com/notpop/flex-talk-Mei.git . && \
    # Python依存パッケージのインストール
    pip install --no-cache-dir -r requirements.txt

# 第二段階：最小限のランタイム環境
FROM python:3.11-slim

# 必要なパッケージのインストール、第一段階から必要なファイルのコピー、不要ファイルの削除を1つのRUNで実行
RUN apt-get update && \
    apt-get install -y ffmpeg open-jtalk && \
    rm -rf /var/lib/apt/lists/* && \
    # 第一段階から必要なファイルをコピー
    COPY --from=build /app /app && \
    # 不要なキャッシュファイルを削除
    find /usr/local/lib/python3.11/site-packages -name '__pycache__' -exec rm -rf {} + || true

# 作業ディレクトリを設定
WORKDIR /app

# ボットを実行
CMD ["python3", "main.py"]
