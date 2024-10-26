import os
import discord
import subprocess
import shutil  # ディレクトリ削除用
from config import VOICE_DIRECTORY, DEFAULT_VOICE_PATH, VOICEBOX_API_KEY
from utils.text_processing import remove_custom_emoji, urlAbb

voice_path = DEFAULT_VOICE_PATH
temp_dir = "./temp"  # 一時ファイルを保存するディレクトリ

# 一時ファイルディレクトリを作成
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

def change_voice_path(voice_name):
    """音声ファイルのパスを変更"""
    global voice_path
    voice_path = os.path.join(VOICE_DIRECTORY, f'{voice_name}.htsvoice') if voice_name != 'voicebox' else None

def list_available_voices():
    """利用可能な音声ファイルをリストアップ"""
    voices = [f.replace('.htsvoice', '') for f in os.listdir(VOICE_DIRECTORY) if f.endswith('.htsvoice')]
    voices.append('voicebox')
    return voices

async def play_voice(text, voice_client):
    """音声を再生"""
    try:
        if not voice_client or not voice_client.is_connected():
            raise discord.ClientException("ボイスチャンネルに接続されていません。")

        input_text = urlAbb(remove_custom_emoji(text))
        wav_file_path = create_WAV(input_text)

        if not os.path.exists(wav_file_path):
            raise FileNotFoundError(f"{wav_file_path}が作成されませんでした。")

        audio_source = discord.FFmpegPCMAudio(wav_file_path, options={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'})
        voice_client.play(audio_source, after=lambda e: cleanup_temp_files())  # 再生後にクリーンアップ

    except Exception as e:
        print(f"音声再生中にエラーが発生しました: {e}")
        raise

def create_WAV(input_text):
    """WAVファイルを作成"""
    try:
        dictionary_path = './dic'
        voice_speed = '0.9'
        output_file_name = os.path.join(temp_dir, 'output.wav')

        input_file_name = os.path.join(temp_dir, 'input.txt')
        with open(input_file_name, 'w', encoding='utf-8') as file:
            file.write(input_text)

        command = f'open_jtalk -x {dictionary_path} -m {voice_path} -r {voice_speed} -ow {output_file_name} {input_file_name}'
        subprocess.run(command, shell=True, check=True)

        return output_file_name

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"WAVファイルの作成に失敗しました: {e}")

def cleanup_temp_files():
    """一時ファイルを削除"""
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
        print("一時ファイルをクリーンアップしました。")
    except Exception as e:
        print(f"一時ファイルの削除中にエラーが発生しました: {e}")
