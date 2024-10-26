from discord.ext import commands, tasks
import discord
from .voice_control import play_voice, change_voice_path, list_available_voices

voice_client = None
current_text_channel = None  # 読み上げる対象のテキストチャンネル

def setup_commands(client):
    @client.command()
    async def join(context):
        global voice_client, current_text_channel

        # ボットが既にボイスチャンネルに接続しているか確認
        if context.voice_client is not None:
            await context.send("I'm already in a voice channel.")
            return

        voice_channel = context.author.voice.channel
        current_text_channel = context.channel  # joinしたテキストチャンネルを記憶
        voice_client = await voice_channel.connect()  # ここでvoice_clientを更新

         # ここで接続状態を確認
        if voice_client.is_connected():
            print(f"Successfully connected to {voice_channel.name}")
            await context.send(f"Joined {voice_channel.name} and will read messages from {current_text_channel.name}")
            check_voice_channel.start()
        else:
            print("Failed to connect to voice channel.")
            await context.send("Failed to join the voice channel.")

    @client.command()
    async def bye(context):
        global voice_client, current_text_channel

        if context.voice_client:
            await context.voice_client.disconnect()
            voice_client = None  # ここでvoice_clientをNoneに設定
            current_text_channel = None
            check_voice_channel.stop()
            await context.send("Disconnected from voice channel.")
        else:
            await context.send("I'm not in a voice channel.")

    @client.command()
    async def list(context):
        voices = list_available_voices()
        await context.send(f"Available voices: {', '.join(voices)}")

    @client.command()
    async def set_voice(context, voice_name: str):
        voices = list_available_voices()
        if voice_name in voices:
            change_voice_path(voice_name)
            await context.send(f"Voice changed to: {voice_name}")
        else:
            await context.send(f"Voice '{voice_name}' not found. Use `flex.list` to see available voices.")

    @client.event
    async def on_message(message):
        global current_text_channel

        # ボット自身のメッセージやコマンド以外のメッセージを無視
        if message.author == client.user or message.content.startswith('flex.'):
            await client.process_commands(message)
            return

        # joinしたテキストチャンネルのメッセージだけを読み上げる
        if message.channel == current_text_channel:
            voice_client = message.guild.voice_client  # ボイスクライアントを取得
            # ボイスクライアントの状態を確認
            if voice_client:
                if voice_client.is_connected():
                    print("Connected to voice channel:", voice_client.channel.name)
                    await play_voice(message.content, voice_client)
                else:
                    print("Voice client exists but is not connected.")
                    await current_text_channel.send("I'm connected to the voice client but not in a voice channel.")
            else:
                print("No voice client found.")
                await current_text_channel.send("I'm not connected to any voice channel.")

    @client.command()
    async def status(context):
        voice_client = context.guild.voice_client
        if voice_client and voice_client.is_connected():
            await context.send(f"I'm connected to {voice_client.channel.name}.")
        else:
            await context.send("I'm not connected to any voice channel.")

    @tasks.loop(seconds=10)
    async def check_voice_channel():
        """ボイスチャンネルの状態を定期的に確認し、誰もいなくなったら自動で退出する"""
        if voice_client and voice_client.channel and len(voice_client.channel.members) == 1:
            # ボイスチャンネルにボットしかいない場合、チャンネルを退出
            await voice_client.disconnect()
            await current_text_channel.send("No users left in the voice channel, so I'm disconnecting.")
            check_voice_channel.stop()
