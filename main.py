import discord
import os
import logging
from botpy.ext.cog_yaml import read
import nacl
import time
import datetime
from discord.ext import commands
from discord import *
from discord.ui import *

import IrminsulDatabase
from IrminsulTerminal import *
from GuildManager.VoiceChannelCreator import VoiceChannelCreatorModalView


_log = logging.getLogger('discord')
logHandler = logging.FileHandler(filename='irminsul.log', encoding='utf-8', mode='w')
_log.addHandler(logHandler)


class IrminsulTerminalBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or('/'), intents=intents)

    async def setup_hook(self) -> None:
        botName = self.user.name
        self.add_view(VoiceChannelCreatorModalView(botName=botName))
        # self.add_view(VoiceChannelCreatorModalView(i18n=terminal.get_i18n("ja"), botName=botName))

    async def on_ready(self):
        _log.info("Bot is ready.")
        _log.info(f"Logged in as {self.user.name} #{self.user.id}")
        if config["autoDeleteEmptyVoiceChannel"]:
            while True:
                await asyncio.sleep(60)
                for channel in self.get_all_channels():
                    if type(channel) == discord.VoiceChannel:
                        if len(channel.members) == 0:
                            _log.info(f"Find channel {channel.name} member is 0")
                            now = datetime.datetime.now().astimezone()
                            if (now - channel.created_at).seconds > 60:
                                textChannel = discord.utils.get(channel.guild.channels, name=f"👂{channel.name}")
                                try:
                                    await channel.delete()
                                    await textChannel.delete()
                                    _log.info(f"Delete voice channel {channel.name} success!")
                                except Forbidden as forbidden:
                                    _log.error(f"Delete voice channel fail because of Forbidden")
                                except HTTPException:
                                    _log.error(f"Delete voice channel fail because of HTTPException")
                                except TypeError:
                                    _log.error(f"Delete voice channel fail because of TypeError")
                            else:
                                _log.info(f"{channel.name} created in 60s, ignore it")


config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
bot = IrminsulTerminalBot()


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


@bot.command(name="bind")
async def bindUID(ctx, uid):
    _log.info(f"Recognized command bind {uid} from {ctx.author.name} #{ctx.author.id}")
    terminal = IrminsulTerminal(language="en")
    await ctx.send(terminal.bindUID(user=ctx.author, uid=uid) + uid)


@bot.tree.command(name="bind")
async def bindUIDCmd(interaction: discord.Interaction, uid: str) -> None:
    _log.info(f"Recognized command bind {uid} from {interaction.user.name} #{interaction.user.id}")
    _, language = IrminsulDatabase.lookUpLanguage(user_id=interaction.user.id)
    terminal = IrminsulTerminal(language=language)
    await interaction.response.send_message(terminal.bindUID(user=interaction.user, uid=uid) + str(uid))


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


@bot.tree.command(name="lookup")
async def lookUpCmd(interaction: discord.Interaction) -> None:
    _log.info(f"Recognized command lookup from {interaction.user.name} #{interaction.user.id}")
    _, language = IrminsulDatabase.lookUpLanguage(user_id=interaction.user.id)
    terminal = IrminsulTerminal(language=language)
    resTitle, resView = terminal.lookUpHandler()
    await interaction.response.send_message(resTitle, view=resView)


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


@bot.tree.command(name="setlanguage")
async def setLanguage(interaction: discord.Interaction, language: str) -> None:
    _log.info(f"Recognized command setlanguage from {interaction.user.name} #{interaction.user.id}")
    terminal = IrminsulTerminal(language=language)
    res = terminal.setLanguage(user=interaction.user, language=language)
    await interaction.response.send_message(res)


@bot.command(name="char")
async def lookUpChar(ctx, charName):
    _log.info(f"Recognized command look up from {ctx.author.name} #{ctx.author.id}")
    terminal = IrminsulTerminal(language="en")
    resTitle, resView = terminal.lookUpChar(ctx.author.id, charName)
    await ctx.send(resTitle, view=resView)


@bot.tree.command(name="character")
async def lookUpCharCmd(interaction: discord.Interaction, name: str):
    _log.info(f"Recognized command look up from {interaction.user.name} #{interaction.user.id}")
    _, language = IrminsulDatabase.lookUpLanguage(user_id=interaction.user.id)
    terminal = IrminsulTerminal(language=language)
    resTitle, resView = terminal.lookUpChar(interaction.user.id, name)
    await interaction.response.send_message(resTitle, view=resView)


# todo: update translated character list
# todo: update enka data, opensource readme, user guide


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
@commands.is_owner()
async def createVoiceChannel(ctx, name=""):
    _log.info(f"Recognized command createvc from {ctx.author.name} #{ctx.author.id}")
    terminal = IrminsulTerminal(language="en")
    # res, msg = await terminal.createVoiceChannel(ctx, name, bot.user.name)
    # await ctx.send(msg)
    responseView = VoiceChannelCreatorModalView(bot.user.name)
    await ctx.send(view=responseView)


# delete voice channel when member is all gone
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        _log.info(f"{member.name} entered channel {after.channel.name}")
    if before.channel is not None and after.channel is None:
        channelName = before.channel.name
        _log.info(f"{member.name} exited channel {channelName}")
        channelPrefix = f"[{bot.user.name}]"
        if config["createChannelWithPrefix"]:
            if not channelName[0:len(channelPrefix)] == channelPrefix:
                _log.info(f"This is not a channel created by bot. Ignore it.")
                return
        if len(before.channel.members) == 0:
            _log.info(f"{channelName} member is 0, wait 30s")
            await asyncio.sleep(30)
            if not len(before.channel.members) == 0:
                _log.info(f"{channelName} member is not 0, stop it")
                return
            _log.info(f"{channelName} member is 0, delete it")
            channel = discord.utils.get(member.guild.channels, name=channelName)
            textChannel = discord.utils.get(member.guild.channels, name=f"👂{channelName}")
            if type(channel) != discord.VoiceChannel or channel is None:
                _log.error(f"Channel {channelName} is not found!")
                return
            try:
                await channel.delete()
                await textChannel.delete()
                _log.info(f"Delete voice channel {channelName} success!")
            except Forbidden as forbidden:
                _log.error(f"Delete voice channel fail because of Forbidden")
            except HTTPException:
                _log.error(f"Delete voice channel fail because of HTTPException")
            except TypeError:
                _log.error(f"Delete voice channel fail because of TypeError")


_log.info(f"Discord API Version: {discord.__version__}")
bot.run(config["token"], log_handler=logHandler)

