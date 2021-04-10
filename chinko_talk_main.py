import discord
from discord.ext import commands
import asyncio
import os
import subprocess
import ffmpeg
from manko_generator import create_WAV
import configparser
# import math
# import random

# send_message = [
#     'change_contextさんの事、好きかもしれない///',
#     'change_contextさん好いとーよ///',
#     'change_contextさんの馬鹿！！',
#     '「僕は……change_contextちゃん大好きなのに…change_contextちゃんは僕のこと嫌いなのぉ…？',
#     '嘘はよくないよ!!僕…嘘つくchange_contextちゃん嫌いだよ？',
#     'べ、別に僕…change_contextに会いたいなんか思ってなからねッ!!//',
#     'change_contextちゃあん、オバケ恐いから…一緒に寝よ？',
#     'こ、子供扱いしないでよ、もう…っ',
#     'お手々ぎゅーってして寝よ？',
#     'change_contextちゃんがなでなでしてくれたら…イイ子にするけど…//'
# ]

config = configparser.ConfigParser()
config.read('config.ini', encoding='shift-jis')

client = commands.Bot(command_prefix='flex.')
voice_client = None

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')

@client.command()
async def join(context):
    print('#voicechannelを取得')
    voice_channel = context.author.voice.channel
    print('#voicechannelに接続')
    await voice_channel.connect()

@client.command()
async def bye(context):
    #誤字じゃないよ！！！！
    print('#セツナトリップ')
    await context.voice_client.disconnect()

# @client.command()
# async def talk(context):
#     target_number = math.floor(random.random() * 10) + 1
#     print('#show talk')
#     target_name = context.author.name
#     selected_message = send_message[target_number]
#     await context.send(selected_message.translate(str.maketrans('change_context', target_name)))

@client.event
async def on_message(message):
    message_client = message.guild.voice_client
    if message.content.startswith('flex.'):
        pass
    else:
        if message.guild.voice_client:
            print(message_client)
            create_WAV(message.content)
            audio_source = discord.FFmpegPCMAudio("output.wav")
            message.guild.voice_client.play(audio_source)
        else:
            pass
    await client.process_commands(message)

client.run(config['DISCORD']['serial_key'])