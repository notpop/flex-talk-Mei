from discord.ext import commands, tasks
import discord
import asyncio
from .voice_control import play_voice, change_voice_path, list_available_voices

class VoiceState:
    def __init__(self):
        self.voice_client = None
        self.current_channel = None
        self.text_channel = None

voice_state = VoiceState()

def setup_commands(client):
    print(f"Setting up commands for client: {client}")

    @client.command()
    async def check_environment(context):
        """音声機能の環境をチェックする"""
        print("\n=== Checking Voice Environment ===")

        # Discord.pyのバージョン確認
        import discord
        print(f"Discord.py version: {discord.__version__}")

        # FFmpegの確認
        try:
            import subprocess
            ffmpeg_version = subprocess.check_output(['ffmpeg', '-version']).decode()
            first_line = ffmpeg_version.split('\n')[0]
            print(f"FFmpeg available: {first_line}")
        except Exception as e:
            print(f"FFmpeg check error: {e}")

        # 権限の確認
        try:
            permissions = context.guild.me.guild_permissions
            print(f"Bot permissions: {permissions}")
            print(f"Can connect to voice: {permissions.connect}")
            print(f"Can speak in voice: {permissions.speak}")
        except Exception as e:
            print(f"Permission check error: {e}")

        await context.send("Environment check completed. Check the logs for details.")

    @client.command()
    async def join(context):
        """ボイスチャンネルに接続する"""
        print("\n=== Starting join command ===")
        print(f"Context: {context}")
        print(f"Guild: {context.guild}")

        permissions = context.guild.me.guild_permissions
        print(f"Can connect to voice: {permissions.connect}")
        print(f"Can speak in voice: {permissions.speak}")

        if not context.author.voice:
            await context.send("You need to be in a voice channel first!")
            return

        try:
            voice_channel = context.author.voice.channel
            print(f"Target voice channel: {voice_channel}")
            print(f"Current voice client: {context.voice_client}")

            # 既存の接続確認と切断
            if context.voice_client:
                print(f"Existing voice client found: {context.voice_client}")
                print(f"Connected to channel: {context.voice_client.channel}")
                print(f"Connection status: {context.voice_client.is_connected()}")

                if context.voice_client.channel == voice_channel:
                    if context.voice_client.is_connected():
                        await context.send("Already connected and ready!")
                        print("Already connected to the channel")
                        return
                    else:
                        print("Disconnecting existing voice client")
                        await context.voice_client.disconnect()

            # 新規接続（エラーハンドリングを細分化）
            print("=== Starting connection process ===")
            if context.voice_client:
                print("Disconnecting previous voice client.")
                await context.voice_client.disconnect()

            try:
                print("Attempting to connect to the voice channel...")
                voice_client = await voice_channel.connect(timeout=20.0, reconnect=True)
                print(f"Connection to voice channel {voice_channel.name} successful.")
            except discord.ClientException as e:
                print(f"ClientException during connection: {e}")
                await context.send(f"Connection failed: {e}")
            except asyncio.TimeoutError:
                print("Connection timed out.")
                await context.send("Connection attempt timed out.")
            except Exception as e:
                print(f"Unexpected error during connection: {e}")
                await context.send(f"Unexpected error: {e}")

            try:
                print("=== Checking voice client properties ===")
                print(f"Voice client type: {type(voice_client)}")
                print(f"Voice client: {voice_client}")

                # 各プロパティを個別に確認
                try:
                    print(f"Channel: {voice_client.channel}")
                except Exception as e:
                    print(f"Error getting channel: {e}")

                try:
                    print(f"Guild: {voice_client.guild}")
                except Exception as e:
                    print(f"Error getting guild: {e}")

                try:
                    print(f"Session ID: {voice_client.session_id}")
                except Exception as e:
                    print(f"Error getting session ID: {e}")

                try:
                    print(f"Connected status: {voice_client.is_connected()}")
                except Exception as e:
                    print(f"Error getting connection status: {e}")

                print("=== Starting connection verification ===")
                is_connected = voice_client.is_connected()
                print(f"Initial connection status: {is_connected}")

                if is_connected:
                    print("Connection verified immediately")
                    await context.send(f"Successfully connected to {voice_channel.name}!")
                else:
                    # 接続確立の待機
                    retry_count = 0
                    while retry_count < 10:  # 最大10回まで再試行
                        if voice_client.is_connected():
                            print("Connection successful.")
                            break
                        await asyncio.sleep(2)  # 2秒待機
                        retry_count += 1

                    if not voice_client.is_connected():
                        await context.send("Failed to establish a stable connection after retries.")
                        await voice_client.disconnect()  # 再接続失敗時の切断処理

                    print("Failed to verify connection after all attempts")
                    await context.send("Failed to establish a stable connection.")
                    try:
                        await voice_client.disconnect()
                    except Exception as e:
                        print(f"Error during disconnect: {e}")

            except Exception as check_error:
                print(f"Error checking voice client properties: {check_error}")
                import traceback
                print(f"Property check error traceback:\n{traceback.format_exc()}")
                await context.send("Error occurred while setting up voice client")
                try:
                    await voice_client.disconnect()
                except:
                    pass

        except Exception as e:
            print(f"Unexpected error in join command: {e}")
            import traceback
            print(f"Full error traceback:\n{traceback.format_exc()}")
            await context.send(f"Failed to join: {str(e)}")

    @client.command()
    async def debug_status(context):
        """ボイスクライアントの詳細な状態を確認する"""
        print("\n=== Voice Client Debug Status ===")
        print(f"Guild: {context.guild}")
        print(f"Voice Client: {context.voice_client}")

        if context.voice_client:
            print(f"Current Voice Client: {context.voice_client}")
            print(f"Connected: {context.voice_client.is_connected()}")
            print(f"Channel: {context.voice_client.channel}")
            print(f"Session ID: {context.voice_client.session_id}")

            await context.send(
                f"Voice Client Status:\n"
                f"Connected: {context.voice_client.is_connected()}\n"
                f"Channel: {context.voice_client.channel}\n"
                f"Session ID: {context.voice_client.session_id}"
            )
        else:
            print("No voice client found")
            await context.send("No voice client available")

    @client.command()
    async def bye(context):
        """ボイスチャンネルから切断する"""
        if not context.voice_client:
            await context.send("I'm not in any voice channel.")
            return

        try:
            await context.voice_client.disconnect()  # forceオプションを削除
            if check_voice_channel.is_running():
                check_voice_channel.stop()

            voice_state.voice_client = None
            voice_state.current_channel = None
            voice_state.text_channel = None

            await context.send("Disconnected from voice channel.")
        except Exception as e:
            print(f"Error in bye command: {e}")
            await context.send(f"Error while disconnecting: {str(e)}")

    @client.command()
    async def status(context):
        """現在の接続状態を確認する"""
        if context.voice_client and context.voice_client.is_connected():
            channel = context.voice_client.channel
            await context.send(f"Connected to {channel.name}")
            if context.voice_client.is_playing():
                await context.send("Currently playing audio")
            elif context.voice_client.is_paused():
                await context.send("Audio is paused")
        else:
            await context.send("Not connected to any voice channel")

    @client.event
    async def on_message(message):
        print(f"Received message: {message.content}")
        await client.process_commands(message)

        if message.author == client.user or message.content.startswith('f.'):
            print("Ignoring message")
            return

        voice_client = message.guild.voice_client
        print(f"Voice client exists: {voice_client is not None}")

        if voice_client:
            print(f"Is connected: {voice_client.is_connected()}")
            print(f"Channel: {voice_client.channel.name if voice_client.channel else 'None'}")

            if voice_client.is_connected():
                try:
                    if voice_client.is_playing():
                        voice_client.stop()

                    print(f"Attempting to play voice for: {message.content}")
                    await play_voice(message.content, voice_client)
                except Exception as e:
                    print(f"Error playing voice: {e}")
                    await message.channel.send("Error occurred while playing voice")
            else:
                print("Voice client exists but is not connected")
        else:
            print("No voice client found for this guild")

    @tasks.loop(seconds=10)
    async def check_voice_channel(client):
        """定期的にボイスチャンネルの状態を確認する"""
        for guild in client.guilds:
            voice_client = guild.voice_client
            if not voice_client:
                continue

            try:
                if not voice_client.is_connected():
                    continue

                channel = voice_client.channel
                # ボット以外のメンバーをカウント
                human_count = sum(1 for m in channel.members if not m.bot)

                if human_count == 0:
                    await voice_client.disconnect()
                    # 最初のテキストチャンネルに通知
                    if guild.text_channels:
                        await guild.text_channels[0].send(
                            f"No users left in {channel.name}, disconnecting."
                        )
            except Exception as e:
                print(f"Error in check_voice_channel for guild {guild.id}: {e}")

    # その他のコマンド (list, set_voice) は変更なし
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
