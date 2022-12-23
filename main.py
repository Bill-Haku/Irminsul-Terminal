import discord
import os
from botpy.ext.cog_yaml import read
from discord.ext import commands
from IrminsulTerminal import *

config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
bot = discord.Client(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot is ready.")
    print(f"Logged in as {bot.user.name} #{bot.user.id}")
    print("------")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    terminal = IrminsulTerminal()
    if message.content.startswith("hello"):
        await message.channel.send("Hello!")

    elif message.content.startswith("info"):
        await message.channel.send(embed=terminal.selfInfo(bot=bot))


print(f"Discord API Version: {discord.__version__}")
bot.run(config["token"])

