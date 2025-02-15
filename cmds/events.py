import discord
from discord.ext import commands
from core.core import Cog_Extension
from oksana.oksana import calling_Oksana
from oksana.internet import extract_urls,get_html
from oksana.tools import get_time
import requests
from io import BytesIO
from PIL import Image

class event(Cog_Extension):
  @commands.Cog.listener()
  async def on_message(self,message):
    if message.author == self.bot.user:
      return
    if self.bot.user.mention in message.content or isinstance(message.channel,discord.DMChannel) or (message.reference and message.reference.resolved and isinstance(message.reference.resolved, discord.Message) and message.reference.resolved.author == self.bot.user):
      if message.content == "d!clear_chat":
          return
      user_message = message.content.replace(f'<@{self.bot.user.id}>','')
      urls = extract_urls(user_message)
      html = {}
      for url in urls:
        try:
          html[url] = get_html(url)
        except Exception as e:
          print(e)
      if len(html) > 0:
        for ht in html:
          user_message += f"\n{ht}:\n{html[ht]}"
      imgs = []
      try:
        if message.attachments:
          for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ['jpg', 'jpeg', 'png', 'gif']):
                response = requests.get(attachment.url)
                img_data = BytesIO(response.content)
                img = Image.open(img_data)
                imgs.append(img)
      except Exception as e:
        print(e)
      await message.channel.typing()
      try:
        await message.reply(calling_Oksana(f"[{get_time()}]{message.author.name}：{user_message}",message.channel.id,ctx=await self.bot.get_context(message), **({"img":imgs} if imgs else {})))
      except Exception as e:
        embed = discord.Embed(title="錯誤！",description=f"```{e}```",color=discord.Color.red())
        await message.reply(embed=embed)
        print(e)

  @commands.Cog.listener()
  async def on_member_join(self,member:discord.Member):
    channel = self.bot.get_channel(1202596441088987156)
    if member.guild.id == 1202596440535343154:
      pass
#      await channel.send(f'{member.mention}，歡迎來到{member.guild.name}！\n你可以看 <#1202599065318326272> 了解O-bot的玩法\n若要開始遊戲，請到 <#1203004488340742214> 使用指令！')

async def setup(bot):
    await bot.add_cog(event(bot))
 
