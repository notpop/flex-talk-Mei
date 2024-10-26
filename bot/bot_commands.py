from discord.ext import commands, tasks
import discord
import asyncio
from .voice_control import play_voice, change_voice_path, list_available_voices

class VoiceState:
    """ボイスチャンネルに関する状態を管理"""
    def __init__(self):
        self.voice_client = None
        self.current_channel = None
        self.text_channel = None

voice_state = VoiceState()

# 定期的にボイスチャンネルの状態を確認するタスク
@tasks.loop(seconds=10)
async def check_voice_channel(client):
    """定期的にボイスチャンネルの状態を確認する"""
    for guild in client.guilds:
        voice_client = guild.voice_client
        if not voice_client or not voice_client.is_connected():
            continue

        # ボイスチャンネル内に他のメンバーがいるか確認
        human_count = sum(1 for m in voice_client.channel.members if not m.bot)
        if human_count == 0:
            await voice_client.disconnect()
            if voice_state.text_channel:  # 最初にjoinを実行したテキストチャンネルにメッセージを送る
                await voice_state.text_channel.send(f"{voice_client.channel.name}に誰もいなくなったため、切断しました。")

def setup_commands(client):
    """ボットにコマンドとイベントハンドラをセットアップする"""

    @client.event
    async def on_ready():
        """ボットが起動した際のイベント"""
        print(f'Logged in as {client.user.name} ({client.user.id})')
        check_voice_channel.start(client)  # on_readyでタスクをスタート

    @client.event
    async def on_message(message):
        """メッセージ受信時のイベント"""
        # コマンドを処理
        await client.process_commands(message)

        # ボット自身のメッセージは無視
        if message.author == client.user:
            return

        # メッセージがコマンドでない場合、音声を再生
        if message.content.startswith('f.'):
            return

        voice_client = message.guild.voice_client
        if voice_client and voice_client.is_connected():
            try:
                if voice_client.is_playing():
                    voice_client.stop()
                await play_voice(message.content, voice_client)
            except Exception as e:
                await message.channel.send("音声の再生中にエラーが発生しました。")
                print(f"Error playing voice: {e}")
        else:
            await message.channel.send("ボイスチャンネルに接続されていません。")

    @client.command()
    async def check_environment(context):
        """音声機能の環境をチェックする"""
        import subprocess
        permissions = context.guild.me.guild_permissions
        ffmpeg_version = subprocess.check_output(['ffmpeg', '-version']).decode().split('\n')[0]

        await context.send(
            f"環境チェック:\n"
            f"Discord.pyバージョン: {discord.__version__}\n"
            f"FFmpegバージョン: {ffmpeg_version}\n"
            f"権限: 接続={permissions.connect}, 発言={permissions.speak}"
        )

    @client.command()
    async def join(context):
        """ボイスチャンネルに接続する"""
        if not context.author.voice:
            await context.send("ボイスチャンネルに参加してください。")
            return

        voice_channel = context.author.voice.channel
        if context.voice_client and context.voice_client.is_connected():
            if context.voice_client.channel == voice_channel:
                await context.send("既に接続されています。")
                return
            await context.voice_client.disconnect()

        try:
            voice_client = await voice_channel.connect(timeout=20.0, reconnect=True)
            voice_state.text_channel = context.channel  # joinを実行したテキストチャンネルを保存
            await context.send(f"{voice_channel.name}に接続しました。")
        except asyncio.TimeoutError:
            await context.send("接続がタイムアウトしました。")
        except discord.ClientException as e:
            await context.send(f"接続に失敗しました: {e}")
        except Exception as e:
            await context.send(f"予期しないエラーが発生しました: {e}")

    @client.command()
    async def bye(context):
        """ボイスチャンネルから切断する"""
        if not context.voice_client:
            await context.send("現在、ボイスチャンネルに接続されていません。")
            return

        try:
            await context.voice_client.disconnect()
            await context.send("ボイスチャンネルから切断しました。")
        except Exception as e:
            await context.send(f"切断中にエラーが発生しました: {e}")

    @client.command()
    async def status(context):
        """現在の接続状態を確認する"""
        if context.voice_client and context.voice_client.is_connected():
            channel = context.voice_client.channel
            status_message = f"{channel.name}に接続中"
            if context.voice_client.is_playing():
                status_message += "（再生中）"
            elif context.voice_client.is_paused():
                status_message += "（一時停止中）"
            await context.send(status_message)
        else:
            await context.send("現在、ボイスチャンネルに接続されていません。")

    @client.command()
    async def list(context):
        """利用可能な音声を一覧表示"""
        voices = list_available_voices()
        await context.send(f"利用可能な音声: {', '.join(voices)}")

    @client.command()
    async def set_voice(context, voice_name: str):
        """指定した音声に変更"""
        voices = list_available_voices()
        if voice_name in voices:
            change_voice_path(voice_name)
            await context.send(f"音声を{voice_name}に変更しました。")
        else:
            await context.send(f"音声'{voice_name}'が見つかりません。`flex.list`で利用可能な音声を確認してください。")
