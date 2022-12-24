import discord
import os
import logging
from botpy.ext.cog_yaml import read
from discord.ext import commands
from discord import *
from discord.ui import *
from IrminsulTerminal import *

config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
# bot = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
_log = logging.getLogger('discord')
logHandler = logging.FileHandler(filename='irminsul.log', encoding='utf-8', mode='w')
_log.addHandler(logHandler)


@bot.event
async def on_ready():
    _log.info("Bot is ready.")
    _log.info(f"Logged in as {bot.user.name} #{bot.user.id}")


# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#
#     terminal = IrminsulTerminal()
#     if message.content.startswith("hello"):
#         _log.info(f"Recognized command hello")
#         await message.channel.send("Hello!")
#
#     elif message.content.startswith("info"):
#         _log.info(f"Recognized command info from {message.author.name} #{message.author.id}")
#         await message.channel.send(embed=terminal.selfInfo(bot=bot, language="en"))
#     elif message.content.startswith("关于"):
#         _log.info(f"Recognized command info in zh_Hans from {message.author.name} #{message.author.id}")
#         await message.channel.send(embed=terminal.selfInfo(bot=bot, language="zh"))
#     elif message.content.startswith("ボット"):
#         _log.info(f"Recognized command info in ja from {message.author.name} #{message.author.id}")
#         await message.channel.send(embed=terminal.selfInfo(bot=bot, language="ja"))


@bot.command(name="paimon")
async def paimon(ctx):
    terminal = IrminsulTerminal(language="en")
    _log.info(f"Recognized command paimon from {ctx.author.name} #{ctx.author.id}")
    await ctx.send(embed=terminal.selfInfo(bot=bot))


@bot.command(name="关于")
async def paimon(ctx):
    terminal = IrminsulTerminal(language="zh")
    _log.info(f"Recognized command 关于 from {ctx.author.name} #{ctx.author.id}")
    await ctx.send(embed=terminal.selfInfo(bot=bot))


@bot.command(name="ボット")
async def paimon(ctx):
    terminal = IrminsulTerminal(language="ja")
    _log.info(f"Recognized command ボット from {ctx.author.name} #{ctx.author.id}")
    await ctx.send(embed=terminal.selfInfo(bot=bot))


@bot.command(name="menu")
async def menuTest(ctx):
    _log.info(f"Recognized command menuTest from {ctx.author.name} #{ctx.author.id}")
    view = View()
    button1 = Button(label="Button 1", style=ButtonStyle.red)
    button2 = Button(label="Button 2", style=ButtonStyle.gray)
    button3 = Button(label="Button 3", style=ButtonStyle.green)

    async def on_button_click(interaction: discord.Interaction):
        _log.info(f"{interaction.id} clicked")
        await interaction.response.send_message(f"{interaction.id} clicked")

    button1.callback = on_button_click
    button2.callback = on_button_click
    button3.callback = on_button_click

    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    await ctx.send("Menu test", view=view)


@bot.command(name="input")
async def inputTest(ctx):
    _log.info(f"Recognized command inputTest from {ctx.author.name} #{ctx.author.id}")
    view = View()
    input = TextInput(label="UID", min_length=9, max_length=9)

    async def on_input(interaction: discord.Interaction):
        _log.info(f"{interaction.id} inputted")
        await interaction.response.send_message(f"{interaction.message} inputted")

    input.callback = on_input
    view.add_item(input)
    await ctx.send("Input test", view=view)


@bot.command(name="bind")
async def bindUID(ctx, uid):
    _log.info(f"Recognized command bind {uid} from {ctx.author.name} #{ctx.author.id}")
    terminal = IrminsulTerminal(language="en")
    await ctx.send(terminal.bindUID(user=ctx.author, uid=uid) + uid)


@bot.command(name="lookup")
async def lookup(ctx):
    _log.info(f"Recognized command lookup from {ctx.author.name} #{ctx.author.id}")
    terminal = IrminsulTerminal(language="en")
    resTitle, resView = terminal.lookUpHandler()
    await ctx.send(resTitle, view=resView)


_log.info(f"Discord API Version: {discord.__version__}")
bot.run(config["token"], log_handler=logHandler)

