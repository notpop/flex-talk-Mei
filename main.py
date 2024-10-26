from discord.ext import commands
from config import DISCORD_SERIAL_KEY
from bot.bot_commands import setup_commands

client = commands.Bot(command_prefix='f.')

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')

setup_commands(client)

client.run(DISCORD_SERIAL_KEY)
