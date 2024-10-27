# ベースイメージとしてPython 3.11を使用
FROM python:3.11-slim

# 必要なパッケージのインストール
RUN apt-get update && \
    apt-get install -y ffmpeg open-jtalk && \
    rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを作成
WORKDIR /app

# リポジトリをクローン
RUN apt-get install -y git
RUN git clone https://github.com/notpop/flex-talk-Mei.git /app

# Pythonの依存パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# 環境セットアップ
RUN task setup

# ボットを実行
CMD ["task", "run"]
