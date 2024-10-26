from discord.ext import commands
import discord  # discord.Intentsを使用するために必要
from config import DISCORD_SERIAL_KEY
from bot.bot_commands import setup_commands

# Intentsを設定する
intents = discord.Intents.default()
intents.message_content = True  # メッセージの内容にアクセスするためのintent

# ボットの初期化（intentsを指定）
client = commands.Bot(command_prefix='f.', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')

# コマンドの設定
setup_commands(client)

# ボットを起動
client.run(DISCORD_SERIAL_KEY)
