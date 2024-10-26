import os
import discord
import subprocess
import requests
from config import VOICE_DIRECTORY, DEFAULT_VOICE_PATH, VOICEBOX_API_KEY
from utils.text_processing import remove_custom_emoji, urlAbb

voice_path = DEFAULT_VOICE_PATH
use_voicebox = False

def change_voice_path(voice_name):
    global voice_path, use_voicebox
    if voice_name == 'voicebox':
        use_voicebox = True
    else:
        use_voicebox = False
        voice_path = os.path.join(VOICE_DIRECTORY, f'{voice_name}.htsvoice')

def list_available_voices():
    voices = [f.replace('.htsvoice', '') for f in os.listdir(VOICE_DIRECTORY) if f.endswith('.htsvoice')]
    voices.append('voicebox')  # VOICEBOXもリストに追加
    return voices

async def play_voice(text, voice_client):
    print(f"Starting play_voice with text: {text}")

    if not voice_client:
        print("Voice client is None")
        raise ValueError("Voice client is not provided")

    if not voice_client.is_connected():
        print("Voice client is not connected")
        raise discord.ClientException("Voice client is not connected")

    try:
        print("Creating WAV file...")
        input_text = urlAbb(remove_custom_emoji(text))
        create_WAV(input_text)

        print("Checking if output.wav exists...")
        if not os.path.exists("output.wav"):
            raise FileNotFoundError("output.wav was not created")

        print("Creating audio source...")
        audio_source = discord.FFmpegPCMAudio(
            "output.wav",
            # FFmpegのオプションを追加
            options={
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }
        )

        print("Playing audio...")
        voice_client.play(
            audio_source,
            after=lambda e: print(f'Finished playing: {e}' if e else 'Finished playing successfully')
        )
        print(f"Playing voice: {text}")

    except Exception as e:
        print(f"Error in play_voice: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise

def create_WAV(input_text):
    try:
        dictionary_path = '/usr/share/open_jtalk/dic'
        voice_speed = '0.9'
        output_file_name = 'output.wav'

        with open('input.txt', 'w', encoding='utf-8') as file:
            file.write(input_text)

        command = f'open_jtalk -x {dictionary_path} -m {voice_path} -r {voice_speed} -ow {output_file_name} input.txt'
        subprocess.run(command, shell=True, check=True)

    except Exception as e:
        print(f"Error in create_WAV: {e}")
        raise

async def play_voice_with_voicebox(text, voice_client):
    url = "https://api.voicebox.com/v1/synthesize"
    headers = {"Authorization": f"Bearer {VOICEBOX_API_KEY}"}
    data = {"text": text, "voice": "default_voice"}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        with open('output.wav', 'wb') as f:
            f.write(response.content)
        audio_source = discord.FFmpegPCMAudio("output.wav")
        voice_client.play(audio_source)
    else:
        print(f"VOICEBOX API error: {response.status_code}")
