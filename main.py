from discord.ext import commands
import discord
from config import DISCORD_SERIAL_KEY
from bot.bot_commands import setup_commands

# Intentsの設定
intents = discord.Intents.default()
intents.message_content = True

# ボットの初期化
client = commands.Bot(command_prefix='f.', intents=intents)

# コマンドとイベントハンドラの設定
setup_commands(client)

# ボットを起動
client.run(DISCORD_SERIAL_KEY)
