import os

# 環境変数を取得する関数
def get_env_variable(name, default_value=None):
    return os.getenv(name, default_value)

# 音声ファイルが格納されているディレクトリとデフォルトの音声ファイル
VOICE_DIRECTORY = get_env_variable('VOICE_DIRECTORY', './voices')
DEFAULT_VOICE_PATH = os.path.join(VOICE_DIRECTORY, 'mei_sad.htsvoice')

# VOICEBOX APIキー
VOICEBOX_API_KEY = get_env_variable('VOICEBOX_API_KEY')

# Discord APIキー
DISCORD_SERIAL_KEY = get_env_variable('DISCORD_SERIAL_KEY')
