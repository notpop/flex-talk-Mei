# ベースイメージとしてPython 3.11を使用
FROM python:3.11-slim

# 必要なパッケージのインストール
RUN apt-get update && \
    apt-get install -y git ffmpeg open-jtalk curl && \
    rm -rf /var/lib/apt/lists/*

# go-taskのインストール
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d

# Taskをシステム全体で使えるように /usr/local/bin に移動
RUN mv ./bin/task /usr/local/bin/task

# 作業ディレクトリを作成
WORKDIR /app

# リポジトリをクローン
RUN git clone https://github.com/notpop/flex-talk-Mei.git /app

# Docker用のセットアップを実行
RUN task docker-setup

# ボットを実行
CMD ["task", "run"]
