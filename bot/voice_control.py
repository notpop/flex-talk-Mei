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
    if use_voicebox:
        await play_voice_with_voicebox(text, voice_client)
    else:
        input_text = urlAbb(remove_custom_emoji(text))
        create_WAV(input_text)
        audio_source = discord.FFmpegPCMAudio("output.wav")

        if not voice_client.is_playing():
            voice_client.play(audio_source)

def create_WAV(input_text):
    dictionary_path = '/usr/share/open_jtalk/dic'
    voice_speed = '0.9'
    output_file_name = 'output.wav'

    command = f'open_jtalk -x {dictionary_path} -m {voice_path} -r {voice_speed} -ow {output_file_name} input.txt'

    with open('input.txt', 'w', encoding='utf-8') as file:
        file.write(input_text)

    subprocess.run(command, shell=True)

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
