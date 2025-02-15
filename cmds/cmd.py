import discord
from discord.ext import commands,voice_recv
from core.core import Cog_Extension
from oksana.oksana import clear_chat,calling_Oksana
from oksana.voice import ReadText
from oksana.speech_reco import RecoSink
from datetime import datetime
import asyncio

class cmds(Cog_Extension):
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} (ms)')

    @commands.command()
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command()
    async def avatar(self, ctx, member: discord.User = None):
        if member == None:
            member = ctx.author
        embed = discord.Embed(title=f"{member.name}的頭貼", color=0x00ff00)
        embed.set_image(url=member.avatar)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def clear_chat(self, ctx):
      res = clear_chat(str(ctx.channel.id))
      if res:
        await ctx.send('已清除')
      else:
        await ctx.send('沒有記錄可以清除')

    async def reminder(self, ctx, reminder_message, delay):
        await asyncio.sleep(delay)
        await ctx.send(f"{ctx.author.mention}\n{reminder_message}")

    @commands.command()
    async def remindme(self, ctx, date:str, time: str, *, message: str):
        try:
            date_time = f'{date} {time}'
            target_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
            now = datetime.now()
            delay = (target_time - now).total_seconds()
            if delay <= 0:
                await ctx.send(f"{ctx.author.mention}, 指定的時間已經過去了，請輸入未來的時間。")
            else:
                embed = discord.Embed(
                    title="📌 | 新增提醒",
                    description=f"日期：{date}\n時間：{time}\n訊息內容：{message}",
                    color = discord.Color.green()
                )
                await ctx.send(f"好的！{ctx.author.mention}，我會在 {date_time} 提醒你。",embed=embed)
                await self.reminder(ctx, message, delay)
        except ValueError:
            await ctx.send(f"請輸入正確的日期和時間格式，例如：2024-09-08 15:30")

    @commands.command()
    async def clear_vc(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            res = clear_chat(str(channel.id))
            if res:
                await ctx.send("Cleared!")
            else:
                await ctx.send("No Chat History")
        else:
            await ctx.send("Join a voice channel first!")

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            try:
                vc = await channel.connect(cls=voice_recv.VoiceRecvClient)
            except:
                vc = ctx.guild.voice_client
            vc.listen(RecoSink(vc,channel,ctx=ctx))
            await ctx.send(f"已加入並開始監聽: {channel}")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("已離開語音頻道！")

    @commands.command()
    async def rejoin(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            try:
                vc = await channel.connect(cls=voice_recv.VoiceRecvClient)
            except:
                vc = ctx.guild.voice_client
            await vc.disconnect()
            vc = await channel.connect(cls=voice_recv.VoiceRecvClient)
            vc.listen(RecoSink(vc,channel,ctx=ctx))
            await ctx.send(f"已加入並開始監聽: {channel}")



    @commands.command()
    async def read(self, ctx, * ,text):
        if ctx.author.voice:
            try:
                vc = await ctx.author.voice.channel.connect(cls=voice_recv.VoiceRecvClient)
            except:
                vc = ctx.author.guild.voice_client 
            if vc.is_playing():
                vc.stop()
            await ReadText(vc,text)
    @commands.command()
    async def sum(self,ctx,limit:int = 10):
        messages = []
        async for message in ctx.channel.history(limit=limit):
            messages.append({
                "author": message.author.name,
                "content": message.content,
                "timestamp": message.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        await ctx.channel.typing()
        res = calling_Oksana(f"[System]: Now, Oksana, pls summarize the following conversation with zh-TW and the length of response must lower than 1500:\n\n{messages}",ctx.channel.id)
        await ctx.reply(res)

async def setup(bot):
    await bot.add_cog(cmds(bot))
