import discord
import speech_recognition as sr
import asyncio
from discord.ext.voice_recv.extras import SpeechRecognitionSink
from typing import Optional
from oksana.oksana import calling_Oksana
from oksana.voice import ReadText

"""
def process_cb(recognizer: sr.Recognizer, audio: sr.AudioData, user:Optional[discord.User]):
    print("Got data")
    text = None
    try:
        text = recognizer.recognize_google(audio,language="zh-tw")
    except sr.UnknownValueError:
        print("Bad speech chunk")
    return text

def text_cb(user, text):
    print(f"{user}:{text}")
    res = calling_Oksana(f"{user}:{text}")
"""

class RecoSink(SpeechRecognitionSink):
    def __init__(self,vc,channel,ctx):
        super().__init__()
        self.text_cb = self.text_callback
        self.process_cb = self.process_callback
        self.phrase_time_limit = 8
        self.vc = vc
        self.channel = channel
        self.ctx = ctx
    def text_callback(self, user, text):
        vc = self.vc
        ctx = self.ctx
        channel = self.channel
        if text is None:
            asyncio.run(ReadText(vc,"Error! Tell Koala!"))
            return
        print(f"{user}:{text}")
        #loop = asyncio.get_event_loop()
        #asyncio.run(ctx.send(f"{user.display_name}:{text}"))
        res = calling_Oksana(f"{user}:{text}",str(channel.id),ctx=self.ctx)
        if res:
            #loop = asyncio.get_event_loop()
            #loop.create_task(self.ctx.send(res))
            if vc.is_playing():
                vc.stop_playing()
            asyncio.run(ReadText(vc,res))
        else:
            asyncio.run(ReadText(vc,"Error! Tell Koala!"))

    def process_callback(self, recognizer: sr.Recognizer, audio: sr.AudioData, user:Optional[discord.User]):
        print("Got data")
        text = None
        try:
            text = recognizer.recognize_google(audio,language="zh-tw")
        except sr.UnknownValueError:
            print("Bad speech chunk")
        return text


    @SpeechRecognitionSink.listener()
    def on_voice_member_speaking_start(self, member):
        #self.vc.stop_playing()
        pass


