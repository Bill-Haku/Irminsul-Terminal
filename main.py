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
from GuildManager.FirstStepManager import FirstStepManagerModalView
from GuildManager.CharacterInfoButton import CharInfoModalView


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
        self.add_view(FirstStepManagerModalView(botName=botName))

    async def on_ready(self):
        _log.info(f"Bot is ready. Version: {config['version']}")
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
                                channelRoleName = f"[{bot.user.name}]{channel.name}"
                                channelRole = discord.utils.get(channel.guild.roles, name=channelRoleName)
                                try:
                                    await channelRole.delete()
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


@bot.tree.command(name="about")
async def aboutCmd(interaction: discord.Interaction):
    _log.info(f"Recognized command about from {interaction.user.name} #{interaction.user.id}")
    _, language = IrminsulDatabase.lookUpLanguage(user_id=interaction.user.id)
    terminal = IrminsulTerminal(language=language)
    await interaction.response.send_message(embed=terminal.selfInfo(bot=bot))


@bot.tree.command(name="bind")
async def bindUIDCmd(interaction: discord.Interaction, uid: str) -> None:
    _log.info(f"Recognized command bind {uid} from {interaction.user.name} #{interaction.user.id}")
    _, language = IrminsulDatabase.lookUpLanguage(user_id=interaction.user.id)
    terminal = IrminsulTerminal(language=language)
    await interaction.response.send_message(terminal.bindUID(user=interaction.user, uid=uid) + str(uid))


@bot.tree.command(name="lookup")
async def lookUpCmd(interaction: discord.Interaction) -> None:
    _log.info(f"Recognized command lookup from {interaction.user.name} #{interaction.user.id}")
    _, language = IrminsulDatabase.lookUpLanguage(user_id=interaction.user.id)
    terminal = IrminsulTerminal(language=language)
    resTitle, resView = terminal.lookUpHandler()
    await interaction.response.send_message(resTitle, view=resView)


@bot.tree.command(name="setlanguage")
async def setLanguage(interaction: discord.Interaction, language: str) -> None:
    _log.info(f"Recognized command setlanguage from {interaction.user.name} #{interaction.user.id}")
    terminal = IrminsulTerminal(language=language)
    res = terminal.setLanguage(user=interaction.user, language=language)
    await interaction.response.send_message(res)


@bot.tree.command(name="character")
async def lookUpCharCmd(interaction: discord.Interaction, name: str):
    _log.info(f"Recognized command character from {interaction.user.name} #{interaction.user.id}")
    _, language = IrminsulDatabase.lookUpLanguage(user_id=interaction.user.id)
    terminal = IrminsulTerminal(language=language)
    await interaction.response.defer()
    resTitle, resView = terminal.lookUpChar(interaction.user.id, name)
    await interaction.followup.send(resTitle, view=resView)


@bot.tree.command(name="sync")
async def updateEnkaData(interaction: discord.Interaction):
    _log.info(f"Recognized command update from {interaction.user.name} #{interaction.user.id}")
    _, language = IrminsulDatabase.lookUpLanguage(user_id=interaction.user.id)
    terminal = IrminsulTerminal(language=language)
    await interaction.response.defer()
    res = terminal.updateEnkaData(userID=interaction.user.id)
    await interaction.followup.send(res)


@bot.tree.command(name="help")
async def helpCmd(interaction: discord.Interaction):
    _log.info(f"Recognized command help from {interaction.user.name} #{interaction.user.id}")
    _, language = IrminsulDatabase.lookUpLanguage(user_id=interaction.user.id)
    terminal = IrminsulTerminal(language=language)
    resView = terminal.sendManual()
    await interaction.response.send_message(view=resView)


@bot.tree.command(name="delrecord")
async def delRecordCmd(interaction: discord.Interaction):
    _log.info(f"Recognized command delrecord from {interaction.user.name} #{interaction.user.id}")
    _, language = IrminsulDatabase.lookUpLanguage(user_id=interaction.user.id)
    terminal = IrminsulTerminal(language=language)
    result = terminal.delUserRecord(userID=interaction.user.id)
    await interaction.response.send_message(result)


@bot.command(name="createvc")
@commands.is_owner()
async def createVoiceChannel(ctx, name=""):
    _log.info(f"Recognized command createvc from {ctx.author.name} #{ctx.author.id}")
    terminal = IrminsulTerminal(language="en")
    # res, msg = await terminal.createVoiceChannel(ctx, name, bot.user.name)
    # await ctx.send(msg)
    responseView = VoiceChannelCreatorModalView(bot.user.name)
    await ctx.send(view=responseView)


@bot.command(name="featbuttons")
@commands.is_owner()
async def sendFeatureButtons(ctx):
    _log.info(f"Recognized command sendFeatureButtons from {ctx.author.name} #{ctx.author.id}")
    responseView = FirstStepManagerModalView(bot.user.name)
    await ctx.send(view=responseView)


# delete voice channel when member is all gone
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        _log.info(f"{member.name} entered channel {after.channel.name}")
        channelRoleName = f"[{bot.user.name}]{after.channel.name}"
        channelRole = discord.utils.get(member.guild.roles, name=channelRoleName)
        await member.add_roles(channelRole)
        _log.info(f"Set role {channelRole.name} for {member.name} SUCCESS")
    if before.channel is not None and after.channel is None:
        channelName = before.channel.name
        _log.info(f"{member.name} exited channel {channelName}")
        channelRoleName = f"[{bot.user.name}]{channelName}"
        channelRole = discord.utils.get(member.guild.roles, name=channelRoleName)
        await member.remove_roles(channelRole)
        _log.info(f"Remove role {channelRole.name} for {member.name} SUCCESS")
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
                await channelRole.delete()
                await channel.delete()
                await textChannel.delete()
                _log.info(f"Delete voice channel {channelName} success!")
            except Forbidden as forbidden:
                _log.error(f"Delete voice channel fail because of Forbidden")
            except HTTPException as he:
                _log.error(f"Delete voice channel fail because of HTTPException")
            except TypeError:
                _log.error(f"Delete voice channel fail because of TypeError")


_log.info(f"Discord API Version: {discord.__version__}")
bot.run(config["token"], log_handler=logHandler)

