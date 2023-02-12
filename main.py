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
import json

import IrminsulDatabase
from IrminsulTerminal import *
from GuildManager.VoiceChannelCreator import VoiceChannelCreatorModalView
from GuildManager.FirstStepManager import FirstStepManagerModalView
from GuildManager.CharacterInfoButton import CharInfoModalView
from GuildManager.GuildRoleManager import *
from GuildManager.CoOpManager import *

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
        self.add_view(TaoRoleManagerModalView(botName=botName))
        self.add_view(TaoFanRoleManagerModalView())
        self.add_view(TaoSpoilerRoleManagerModalView())
        self.add_view(TaoRoleLinkModalView())
        self.add_view(CoOpManagerModalView())
        self.add_view(HakuUserLanguageRoleManagerModalView())

    async def on_ready(self):
        _log.info(f"Bot is ready. Version: {config['version']}")
        _log.info(f"Logged in as {self.user.name} #{self.user.id}")
        if config["autoDeleteEmptyVoiceChannel"]:
            while True:
                for channel in self.get_all_channels():
                    if type(channel) == discord.VoiceChannel:
                        if len(channel.members) == 0:
                            if channel.guild.id not in config["enabledVCAdministratorGuilds"]:
                                # _log.info(f"Ignore 0-member channel {channel.name}")
                                continue
                            _log.info(f"Find channel {channel.name} in {channel.guild.name} member is 0")
                            now = datetime.datetime.now().astimezone()
                            if (now - channel.created_at).seconds > 60:
                                vcDataFile = f"./cache/vc{channel.id}.json"
                                tcname = f"👂{channel.name}"
                                rname = f"[{bot.user.name}]{channel.name}"
                                try:
                                    with open(vcDataFile, "r") as df:
                                        data = json.load(df)
                                        tcname = data["tcname"]
                                        rname = data["rname"]
                                        tcid = data["tcid"]
                                except FileNotFoundError as e:
                                    _log.exception(f"{vcDataFile} is not found")
                                    continue
                                # textChannel = discord.utils.get(channel.guild.channels, name=tcname)
                                textChannel = discord.utils.get(channel.guild.channels, id=tcid)
                                channelRoleName = rname
                                channelRole = discord.utils.get(channel.guild.roles, name=channelRoleName)
                                try:
                                    await channelRole.delete()
                                    await textChannel.delete()
                                    await channel.delete()
                                    _log.info(f"Delete voice channel {channel.name} success!")
                                except Forbidden as forbidden:
                                    _log.error(f"Delete voice channel {channel.name} fail because of Forbidden")
                                except HTTPException:
                                    _log.error(f"Delete voice channel {channel.name} fail because of HTTPException")
                                except TypeError:
                                    _log.error(f"Delete voice channel {channel.name} fail because of TypeError")
                                except AttributeError:
                                    _log.error(f"Delete voice channel {channel.name} fail because of Attribute")
                            else:
                                _log.info(f"{channel.name} created in 60s, ignore it")
                    elif channel.id == config["tao"]["coopRaiseChannelId"]:
                        async for message in channel.history(limit=30):
                            now = datetime.datetime.now().astimezone()
                            if (now - message.created_at).seconds > 3600 * 6 and message.id != 1073807334465355828:
                                _log.info(f"found message {message.id} created 12 hours ago, delete it")
                                await message.delete()
                await asyncio.sleep(60)


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


@bot.command(name="rmanager")
@commands.is_owner()
async def sendRoleManagerButtons(ctx, guild="tao"):
    _log.info(f"Recognized command sendRolesManager from {ctx.author.name} #{ctx.author.id}, guild = {guild}")
    if guild == "tao" and ctx.author.guild.id in config["enabledVCAdministratorGuilds"]:
        embed = discord.Embed(description=i18n_ja["tao.role.description"], type="gifv", colour=0xcd5c5c)
        embed.set_image(
            url="https://media.discordapp.net/attachments/965396701869375579/1034384610844491827/hu-tao-genshin-impact.gif")
        responseView = TaoRoleManagerModalView(bot.user.name)
        await ctx.send(view=responseView, embed=embed)
    elif guild == "haku" and ctx.author.guild.id in config["enabledVCAdministratorGuilds"]:
        description = """
        Welcome to this Discord server. Choose your language below before you start chatting.
        欢迎来到这个Discord服务器。在开始聊天之前，请选择您的语言。
        このDiscordサーバーへようこそ。チャットを始める前に、言語を選択してください。
        Добро пожаловать на этот сервер Discord. Выберите свой язык ниже, прежде чем начать общение.
        """
        embed = discord.Embed(title="Language Role Assignment",
                              description=description)
        responseView = HakuUserLanguageRoleManagerModalView()
        await ctx.send(view=responseView, embed=embed)


@bot.command(name="rlinks")
@commands.is_owner()
async def sendRoleLinkButtons(ctx, guild="tao"):
    _log.info(f"Recognized command sendRolesManager from {ctx.author.name} #{ctx.author.id}")
    if guild == "tao" and ctx.author.guild.id in config["enabledVCAdministratorGuilds"]:
        embed = discord.Embed(description=i18n_ja["tao.role.link.description"], type="gifv", colour=0xcd5c5c)
        embed.set_image(
            url="https://media.discordapp.net/attachments/965396701869375579/1034407318663737354/hutao-c1.gif")
        responseView = TaoRoleLinkModalView()
        await ctx.send(view=responseView, embed=embed)
    elif guild == "haku" and ctx.author.guild.id in config["enabledVCAdministratorGuilds"]:
        pass


@bot.command(name="fanrole")
@commands.is_owner()
async def sendFanRoleLinkButtons(ctx, guild="tao"):
    _log.info(f"Recognized command sendFanRolesManager from {ctx.author.name} #{ctx.author.id}")
    if guild == "tao" and ctx.author.guild.id in config["enabledVCAdministratorGuilds"]:
        embed = discord.Embed(description=i18n_ja["tao.role.fan.description"], type="image", colour=0xcd5c5c)
        embed.set_image(url="https://media.discordapp.net/attachments/965396701869375579/1068195081682681856/image.png")
        responseView = TaoFanRoleManagerModalView()
        await ctx.send(view=responseView, embed=embed)
    elif guild == "haku" and ctx.author.guild.id in config["enabledVCAdministratorGuilds"]:
        pass


@bot.command(name="spoilerrole")
@commands.is_owner()
async def sendSpoilerRoleLinkButtons(ctx, guild="tao"):
    _log.info(f"Recognized command sendSpoilerRoleManager from {ctx.author.name} #{ctx.author.id}")
    if guild == "tao" and ctx.author.guild.id in config["enabledVCAdministratorGuilds"]:
        embed = discord.Embed(description=i18n_ja["tao.role.spoiler.description"], type="rich", colour=0xcd5c5c)
        responseView = TaoSpoilerRoleManagerModalView()
        await ctx.send(view=responseView, embed=embed)
    elif guild == "haku" and ctx.author.guild.id in config["enabledVCAdministratorGuilds"]:
        pass


@bot.command(name="raisecoop")
@commands.is_owner()
async def sendSpoilerRoleLinkButtons(ctx, guild="tao"):
    _log.info(f"Recognized command raisecoop from {ctx.author.name} #{ctx.author.id}")
    if guild == "tao" and ctx.author.guild.id in config["enabledVCAdministratorGuilds"]:
        embed = discord.Embed(description=i18n_ja["tao.feature.coop.description"], type="rich", colour=0xcd5c5c)
        responseView = CoOpManagerModalView()
        await ctx.send(view=responseView, embed=embed)
    elif guild == "haku" and ctx.author.guild.id in config["enabledVCAdministratorGuilds"]:
        pass


# delete voice channel when member is all gone
@bot.event
async def on_voice_state_update(member, before, after):
    if member.guild.id not in config["enabledVCAdministratorGuilds"]:
        _log.info(f"Ignore 0-member channel {member.channel.name}")
        return
    if before.channel is None and after.channel is not None:
        vcDataFile = f"./cache/vc{after.channel.id}.json"
        tcname = f"👂{after.channel.name}"
        rname = f"[{bot.user.name}]{after.channel.name}"
        with open(vcDataFile, "r") as df:
            data = json.load(df)
            tcname = data["tcname"]
            rname = data["rname"]
        _log.info(f"{member.name} entered channel {after.channel.name}")
        channelRoleName = rname
        channelRole = discord.utils.get(member.guild.roles, name=channelRoleName)
        await member.add_roles(channelRole)
        _log.info(f"Set role {channelRole.name} for {member.name} SUCCESS")
    if before.channel is not None and after.channel is None:
        vcDataFile = f"./cache/vc{before.channel.id}.json"
        tcname = f"👂{before.channel.name}"
        rname = f"[{bot.user.name}]{before.channel.name}"
        try:
            with open(vcDataFile, "r") as df:
                data = json.load(df)
                tcname = data["tcname"]
                rname = data["rname"]
                tcid = data["tcid"]
        except FileNotFoundError:
            _log.exception(f"{vcDataFile} is not found")
            return
        channelName = before.channel.name
        _log.info(f"{member.name} exited channel {channelName}")
        channelRoleName = rname
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
            # textChannel = discord.utils.get(member.guild.channels, name=tcname)
            textChannel = discord.utils.get(member.guild.channels, id=tcid)
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


from langdetect import detect


@bot.event
async def on_member_join(member: discord.Member):
    if member.guild.id == config["haku"]["id"]:
        welcomeChannel = member.guild.get_channel(config["haku"]["welcomeChannelId"])
        helloChannel = member.guild.get_channel(config["haku"]["helloChannelId"])
        languageChannel = member.guild.get_channel(config["haku"]["languageChannelId"])
        rulesChannel = member.guild.get_channel(config["haku"]["rulesChannelId"])
        memberNameLang = detect(member.name)
        _log.info(f"{member.name} joined {member.guild.name} and his name is detected {memberNameLang}")
        content = f"Welcome to join this server, {member.mention}! \nSet your language in the {languageChannel.mention} " \
                  f"first and pay attention to the {rulesChannel.mention} please. \nAfter that, jump to other channels " \
                  f"in {welcomeChannel.mention}!"
        if memberNameLang == "ja":
            content += f"\n\nようこそ、GI Pizza Helperのサーバーへ！ {member.mention}さん！\nまず{languageChannel.mention}で言語を設定し、" \
                       f"{rulesChannel.mention}に注意してください。\nその後、{welcomeChannel.mention}で他のチャンネルに飛びま" \
                       f"しょう！\n(このメッセージは、あなたのニックネームが日本語であることを検知して送信されています！）"
        elif memberNameLang == "zh-cn" or memberNameLang == "zh-tw":
            content += f"\n\n欢迎加入本Discord服务器！\n请在{languageChannel.mention}设置你使用的语言，并且请注意" \
                       f"这里的{rulesChannel.mention}！\n然后你就可以在{welcomeChannel.mention}前往你想要的对应的频道了！\n（由于" \
                       f"您的用户名被识别为中文所以您会看到本内容）"
        elif memberNameLang == "ru":
            content += f"\n\n{member.mention}, добро пожаловать на сервер! \nСначала выбери свой язык " \
                       f"в {languageChannel.mention}, а также обрати внимание на {rulesChannel.mention}.\n После " \
                       f"этого, перейди в любой из каналов в {welcomeChannel.mention}!\n (Это сообщение отправлено," \
                       f" т.к. никнейм распознан как русский)"
        await helloChannel.send(content=content)
    elif member.guild.id == config["tao"]["id"]:
        _log.info(f"{member.name} joined {member.guild.name}")
        selfIntroChannel = member.guild.get_channel(config["tao"]["selfIntroChannelId"])
        welcomeChannel = member.guild.get_channel(config["tao"]["welcomeChannelId"])
        msg = f"{member.mention}\nよ！旅人！よろしくな！！"
        embed = discord.Embed(title="新しいメンバーが来たぞ！",
                              description=f"君は{member.guild.name} -{len(member.guild.members)}人目だぞ！！\n"
                                          f"{member.name}\n自己紹介は⬇️ここでやってね！！！！\n{selfIntroChannel.mention}",
                              type="gifv")
        embed.set_image(url="https://media.discordapp.net/attachments/965396701869375579/1073956670360789032/IMG_0823.gif")
        await welcomeChannel.send(content=msg, embed=embed)


_log.info(f"Discord API Version: {discord.__version__}")
bot.run(config["token"], log_handler=logHandler)
