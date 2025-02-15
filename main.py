import discord
from discord.ext import commands
from discord import app_commands
import os,asyncio,datetime,aiohttp
from dotenv import load_dotenv
from oksana.tools import load_json

load_dotenv()

bot_token = os.environ['discord_token']
prefix = load_json("settings/settings")["bot_prefix"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents = intents)

def textmsg(user):
  return f'回覆:{user}'

@bot.event
async def on_ready():
  await bot.tree.sync()
  #channel = bot.get_channel(1204285939124281425)
  #await channel.send('啊？啊？我醒了💦')
  print(f'{bot.user}已上線。')

@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cmds.{extension}")
    await ctx.send(f"已載入{extension}")

@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cmds.{extension}")
    await ctx.send(f"已卸載{extension}")

@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cmds.{extension}")
    await ctx.send(f"已重新載入{extension}")

async def load_extensions():
    for filename in os.listdir("./cmds"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cmds.{filename[:-3]}")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    embed = discord.Embed(title=':x:哎呀，有問題:(',description='必要參數缺失',color=0xff0000)
    embed.set_footer(text=textmsg(ctx.author.display_name))
    await ctx.reply(embed=embed)
  elif isinstance(error, commands.CommandNotFound):
    embed = discord.Embed(title=':x:哎呀，有問題:(',description='找不到這個指令',color=0xff0000)
    embed.set_footer(text=textmsg(ctx.author.display_name))
    await ctx.reply(embed=embed)
  elif isinstance(error, commands.CommandOnCooldown):
    message = f'再等 {error.retry_after:.0f} 秒啦'
    embed = discord.Embed(title=':x:哎呀，有問題:(',description=message,color=discord.Color.red())
    embed.set_footer(text=textmsg(ctx.author.display_name))
    await ctx.reply(embed=embed)
  else: 
    await ctx.reply(f'我不知道你在供三小:({error}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(bot_token)

if __name__ == "__main__":
#    keep_alive.keep_alive()
    asyncio.run(main())
