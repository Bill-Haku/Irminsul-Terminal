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


@bot.command(name="绑定")
async def bindUID(ctx, uid):
    _log.info(f"Recognized command bind {uid} from {ctx.author.name} #{ctx.author.id}")
    terminal = IrminsulTerminal(language="zh")
    await ctx.send(terminal.bindUID(user=ctx.author, uid=uid) + uid)


@bot.command(name="バインド")
async def bindUID(ctx, uid):
    _log.info(f"Recognized command bind {uid} from {ctx.author.name} #{ctx.author.id}")
    terminal = IrminsulTerminal(language="ja")
    await ctx.send(terminal.bindUID(user=ctx.author, uid=uid) + uid)


@bot.command(name="lookup")
async def lookup(ctx):
    _log.info(f"Recognized command lookup from {ctx.author.name} #{ctx.author.id}")
    terminal = IrminsulTerminal(language="en")
    resTitle, resView = terminal.lookUpHandler()
    await ctx.send(resTitle, view=resView)


@bot.command(name="検索")
async def lookup(ctx):
    _log.info(f"Recognized command lookup from {ctx.author.name} #{ctx.author.id}")
    terminal = IrminsulTerminal(language="ja")
    resTitle, resView = terminal.lookUpHandler()
    await ctx.send(resTitle, view=resView)


@bot.command(name="查询")
async def lookup(ctx):
    _log.info(f"Recognized command lookup from {ctx.author.name} #{ctx.author.id}")
    terminal = IrminsulTerminal(language="zh")
    resTitle, resView = terminal.lookUpHandler()
    await ctx.send(resTitle, view=resView)


@bot.command(name="char")
async def lookUpChar(ctx, charName):
    _log.info(f"Recognized command look up from {ctx.author.name} #{ctx.author.id}")
    terminal = IrminsulTerminal(language="en")
    resTitle, resView = terminal.lookUpChar(ctx.author.id, charName)
    await ctx.send(resTitle, view=resView)


@bot.command(name="角色")
async def lookUpChar(ctx, charName):
    _log.info(f"Recognized command look up from {ctx.author.name} #{ctx.author.id}")
    terminal = IrminsulTerminal(language="zh")
    resTitle, resView = terminal.lookUpChar(ctx.author.id, charName)
    await ctx.send(resTitle, view=resView)


@bot.command(name="キャラ")
async def lookUpChar(ctx, charName):
    _log.info(f"Recognized command look up from {ctx.author.name} #{ctx.author.id}")
    terminal = IrminsulTerminal(language="ja")
    resTitle, resView = terminal.lookUpChar(ctx.author.id, charName)
    await ctx.send(resTitle, view=resView)


@bot.command(name="createvc")
async def createVoiceChannel(ctx, name):
    _log.info(f"Recognized command createvc from {ctx.author.name} #{ctx.author.id}")
    terminal = IrminsulTerminal(language="en")
    res, msg = await terminal.createVoiceChannel(ctx, name)
    await ctx.send(msg)


_log.info(f"Discord API Version: {discord.__version__}")
bot.run(config["token"], log_handler=logHandler)

