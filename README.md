# flex-talk-mei
このプロジェクトは、Discordサーバーでのメッセージを音声として読み上げるボットです。Open JTalk または VOICEBOX API を使用して、テキストを音声に変換します。

## 前提条件
サーバー上でこのボットを動作させるためには、以下のソフトウェアおよびツールが必要です。

- Python 3.8 以降
- FFmpeg: 音声再生のため
- Open JTalk: 音声合成エンジン（VOICEBOX も選択可能）
- Discord API トークン
- （オプション）VOICEBOX API キー: VOICEBOX API を使用する場合
## セットアップ手順
1. taskのinstall
```bash
$ brew install go-task/tap/go-task
```
2. リポジトリのクローン
まず、プロジェクトをクローンしてディレクトリに移動します。
```bash
$ git clone https://github.com/notpop/flex-talk-Mei.git
$ cd flex-talk-Mei
```
3. Python 仮想環境の作成 (推奨)
Python の仮想環境を作成し、プロジェクトで必要な依存関係を隔離します。

```bash
$ python3 -m venv venv
$ source venv/bin/activate  # Windowsの場合は venv\Scripts\activate
```
4. 必要なパッケージのインストール
requirements.txt に記載されている依存パッケージをインストールします。

```bash
$ pip install -r requirements.txt
```
5. FFmpeg と Open JTalk のインストール
Ubuntuでのインストール方法
```bash
$ sudo apt update
$ sudo apt install ffmpeg
$ sudo apt install open-jtalk
$ sudo apt install open-jtalk-mecab-naist-jdic
```
macOSでのインストール方法
```bash
$ brew install ffmpeg
$ brew install open-jtalk
$ brew install open-jtalk-mecab-naist-jdic
```
6. 環境変数の設定
環境変数を管理するための `.env` ファイルをプロジェクトルートに作成します。以下の内容を記述してください。

`.env` ファイルの内容
```ini
DISCORD_SERIAL_KEY=YOUR_DISCORD_BOT_KEY
VOICEBOX_API_KEY=YOUR_VOICEBOX_API_KEY  # VOICEBOXを使用しない場合は設定不要
VOICE_DIRECTORY=/path/to/voices  # サーバー上に配置したOpen JTalkの音声ファイルのパス
```
- DISCORD_SERIAL_KEY: Discord API のボットトークンです。Discordの開発者ポータルで取得できます。
- VOICEBOX_API_KEY: VOICEBOX API を使用する場合に必要です。VOICEBOX APIを使わない場合は、この項目を削除または空欄にしておいても問題ありません。
- VOICE_DIRECTORY: Open JTalkの .htsvoice ファイルを格納しているディレクトリへのパスを指定します。
7. 音声ファイルの配置
サーバー上に Open JTalk 用の .htsvoice ファイルを用意し、VOICE_DIRECTORY で指定したディレクトリに配置します。プロジェクトにはいくつかの音声ファイルがデフォルトで含まれているので、それらを使用することもできます。

8. ボットの起動
設定が完了したら、以下のコマンドでボットを起動します。

```bash
$ python main.py
```
ボットが正常に起動すると、Discord サーバー上でメッセージを読み上げるためのコマンドが利用できるようになります。

## コマンド一覧
### ボイスチャンネル関連
- `flex.join`
ユーザーが参加しているボイスチャンネルにボットを接続します。

- `flex.bye`
ボットをボイスチャンネルから切断します。

### 音声設定関連
- `flex.list`
使用可能な音声ファイルのリストを表示します。リストにはOpen JTalkの音声ファイルと`voicebox`が含まれます。

- `flex.set_voice <voice_name>`
`flex.list`で表示された音声の中から、使用する音声ファイルを選択します。`voicebox`を指定すると、VOICEBOX API を使用した音声生成が有効になります。

### 自動読み上げ
ボイスチャンネルにボットが接続されている間、サーバー内のテキストメッセージは自動的に音声に変換され、ボイスチャンネル内で再生されます。カスタム絵文字やURLは除外されます。

## 注意事項
- VOICEBOX APIを使用する場合
`flex.set_voice voicebox`コマンドで VOICEBOX API を使用できます。この際、`.env`に VOICEBOX API キーを設定してください。

- Open JTalkの音声ファイル
Open JTalk 用の音声ファイル（`.htsvoice`）は自由に追加できます。サーバー上に保存して、`VOICE_DIRECTORY`にそのパスを指定してください。

## ライセンス
このプロジェクトはMITライセンスのもとで公開されています。
