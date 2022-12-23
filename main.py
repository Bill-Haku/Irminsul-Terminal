import discord
import os
from botpy.ext.cog_yaml import read
from discord.ext import commands

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

    if message.content.startswith("hello"):
        await message.channel.send("Hello!")

    if message.content.startswith("info"):
        embed = discord.Embed(title="Paimon Bot", description="A bot from Project Irminsul Terminal", color=0xeee657)
        embed.add_field(name="Author", value="Bill Haku")
        embed.add_field(name="Version", value=config["version"])
        embed.add_field(name="Server count", value=f"{len(bot.guilds)}")
        embed.add_field(name="Invite", value="https://discord.com/api/oauth2/authorize?client_id=964545612831932507&permissions=8&scope=bot")
        embed.add_field(name="About", value="This is a opensource Genshin bot for Discord.")
        await message.channel.send(embed=embed)


print(f"Discord API Version: {discord.__version__}")
bot.run(config["token"])

