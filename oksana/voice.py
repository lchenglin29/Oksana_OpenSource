import edge_tts
import discord
from io import BytesIO
from oksana.tools import load_json

async def ReadText(voice_client, text):
    voice_settings = load_json(name="settings/settings")["voice_settings"]
    VOICE = voice_settings["VOICE"]
    RATE = voice_settings["RATE"]
    VOLUME = voice_settings["VOLUME"]
    PITCH = voice_settings["PITCH"]
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

