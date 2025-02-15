import edge_tts
import discord
from io import BytesIO
import time

VOICE = "zh-CN-XiaoyiNeural"
OUTPUT_FILE = "test.mp3"
RATE = "-10%"
VOLUME = "+500%"
PITCH = "+10Hz"

async def ReadText(voice_client, text):
    tts = edge_tts.Communicate(text, VOICE, rate=RATE, volume = VOLUME,pitch=PITCH)
    audio_data = b""
    for chunk in tts.stream_sync():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
            print('working')
    print("playing")
    audio_data = BytesIO(audio_data)
    audio_source = discord.FFmpegPCMAudio(audio_data,pipe=True)
    voice_client.play(audio_source)
    print("complete!")

