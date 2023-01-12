import asyncio

import discord
import os
import IrminsulDatabase
import logging
import CharIDDatabase
import EnkaAPIManager
from EnkaDataHandler.Artifacts import *
from EnkaDataHandler.Calculator import *
from botpy.ext.cog_yaml import read
from discord.ui import *
from discord import *

config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
i18n_en = read(os.path.join(os.path.dirname(__file__), "i18n-en.yaml"))
i18n_zh = read(os.path.join(os.path.dirname(__file__), "i18n-zh_Hans.yaml"))
i18n_ja = read(os.path.join(os.path.dirname(__file__), "i18n-ja.yaml"))
_log = logging.getLogger('discord')
logHandler = logging.FileHandler(filename='irminsul.log', encoding='utf-8', mode='w')
_log.addHandler(logHandler)


class IrminsulTerminal:
    def __init__(self, language):
        self.language = language

    def get_i18n(self, language):
        if language == "en":
            i18n = i18n_en
        elif language == "ja":
            i18n = i18n_ja
        elif language == "zh":
            i18n = i18n_zh
        else:
            i18n = i18n_en
        return i18n

    def selfInfo(self, bot):
        i18n = self.get_i18n(self.language)

        embed = discord.Embed(title=bot.user.name, description=i18n["robot.description"], color=0xeee657)
        embed.add_field(name=i18n["sys.label.author"], value=i18n["robot.author"])
        embed.add_field(name=i18n["sys.label.version"], value=config["version"])
        embed.add_field(name=i18n["sys.label.manual"], value=f"[{i18n['sys.label.manual']}]({i18n['sys.label.manual.url']})")
        # embed.add_field(name=i18n["sys.label.serverCount"], value=f"{len(bot.guilds)}")
        # embed.add_field(name=i18n["sys.label.invite"], value=i18n["robot.inviteLink"])
        embed.add_field(name=i18n["sys.label.about"], value=i18n["robot.about"])
        return embed

    def sendManual(self):
        i18n = self.get_i18n(self.language)
        button = discord.ui.Button(label=i18n["sys.label.manual"], url=i18n["sys.label.manual.url"])
        view = View()
        view.add_item(button)
        return view

    def bindUID(self, user, uid):
        i18n = self.get_i18n(self.language)

        if not str(uid).isdigit() or len(str(uid)) != 9 or int(uid) <= 100000000:
            _log.warning(f"Found UID {uid} is not valid.")
            return i18n["msg.error.uidInvalid"]

        res = IrminsulDatabase.bindUID(user_id=user.id, uid=uid)
        if res:
            return i18n["msg.bindUidSuccess"]
        else:
            return i18n["msg.bindUidFail"]

    def setLanguage(self, user, language):
        i18n = self.get_i18n(self.language)
        res = IrminsulDatabase.setLanguage(user_id=user.id, language=language)
        if res:
            return i18n["msg.setLanguageSuccess"]
        else:
            return i18n["msg.setLanguageFail"]

    def lookUpHandler(self):
        i18n = self.get_i18n(self.language)

        view = View()
        button1 = discord.ui.Button(label=i18n["sys.label.lookUpUID"], style=ButtonStyle.red)

        async def on_button_uid_click(interaction: discord.Interaction):
            _log.info(f"Look up uid of {interaction.user.id}")
            res = self.lookUpUID(interaction.user.id)
            await interaction.response.send_message(f"{res}")

        button1.callback = on_button_uid_click
        title = i18n["sys.label.lookUp"]
        view.add_item(button1)
        return title, view

    def lookUpUID(self, userID):
        i18n = self.get_i18n(self.language)
        res, uid, _ = IrminsulDatabase.lookUpUID(user_id=userID)
        if res:
            return i18n["msg.lookUpUIDSuccess"] + uid
        else:
            return i18n["msg.lookUpUIDFail"]

    def delUserRecord(self, userID):
        i18n = self.get_i18n(self.language)
        res = IrminsulDatabase.delUser(user_id=userID)
        if res:
            return i18n["msg.deluser.success"]
        else:
            return i18n["msg.deluser.fail"]

    def updateEnkaData(self, userID):
        i18n = self.get_i18n(self.language)
        res, uid, updateTime = IrminsulDatabase.lookUpUID(user_id=userID)
        if res:
            success, msg = EnkaAPIManager.updateDataFromEnka(userId=userID, uid=uid, updateTime=updateTime, i18n=i18n)
            if success:
                return i18n["msg.updateEnkaDataSuccess"]
            else:
                return msg
        else:
            # no valid bound UID found
            return i18n["msg.err.noUIDBound"]

    def lookUpChar(self, userID, charName, isPrivate=False):
        i18n = self.get_i18n(self.language)
        res, uid, _ = IrminsulDatabase.lookUpUID(user_id=userID)
        if res:
            # found bound UID
            charID = CharIDDatabase.charName2IDConverter(charName)
            if charID == 0:
                # name invalid
                return i18n["msg.error.charNameInvalid"], None
            else:
                view = View()
                buttonBoard = discord.ui.Button(label=i18n["sys.label.lookUpBoard"], style=ButtonStyle.red)
                buttonArtifacts = discord.ui.Button(label=i18n["sys.label.lookUpArtifacts"], style=ButtonStyle.green)
                buttonCalculator = discord.ui.Button(label=i18n["sys.label.cal"], style=ButtonStyle.gray)

                async def on_button_artifacts(interaction: discord.Interaction):
                    await interaction.response.defer()
                    _log.info(f"Look up artifact of {interaction.user.id}'s {charID}")
                    # get the user's all data
                    enkaData = EnkaAPIManager.getEnkaAPIResult(uid)
                    # check if character in avatarInfoList
                    avatarInfoList = enkaData["avatarInfoList"]
                    inAvatarInfoList = False
                    for avatar in avatarInfoList:
                        if avatar["avatarId"] == charID:
                            inAvatarInfoList = True
                            charData = avatar
                            break
                    if not inAvatarInfoList:
                        # await interaction.response.send_message(i18n["msg.error.avatarNotInList"])
                        await interaction.followup.send(i18n["msg.error.avatarNotInList"], ephemeral=isPrivate)
                        return

                    resEmbeds = getArtifactsDatas(charData, i18n=i18n, language=self.language)
                    await asyncio.sleep(delay=1)
                    try:
                        await interaction.followup.send(embeds=resEmbeds, ephemeral=isPrivate)
                    except Exception as e:
                        _log.error(e.with_traceback())
                        await interaction.followup.send(e, ephemeral=isPrivate)

                async def on_button_Board(interaction: discord.Interaction):
                    await interaction.response.defer()
                    _log.info(f"Look up stats board of {interaction.user.id}'s {charID}")
                    # get the user's all data
                    enkaData = EnkaAPIManager.getEnkaAPIResult(uid)
                    # check if character in avatarInfoList
                    avatarInfoList = enkaData["avatarInfoList"]
                    inAvatarInfoList = False
                    for avatar in avatarInfoList:
                        if avatar["avatarId"] == charID:
                            inAvatarInfoList = True
                            charData = avatar
                            break
                    if not inAvatarInfoList:
                        # await interaction.response.send_message(i18n["msg.error.avatarNotInList"])
                        await interaction.followup.send(i18n["msg.error.avatarNotInList"], ephemeral=isPrivate)
                        return

                    resEmbed = getStatsBoardDatas(charData, i18n, self.language)
                    await asyncio.sleep(delay=1)
                    try:
                        await interaction.followup.send(embed=resEmbed, ephemeral=isPrivate)
                    except Exception as e:
                        _log.error(e.with_traceback())
                        await interaction.followup.send(e, ephemeral=isPrivate)

                async def on_button_cal(interaction: discord.Interaction):
                    await interaction.response.defer()
                    _log.info(f"Calculator of {interaction.user.id}'s {charID}")
                    # get the user's all data
                    enkaData = EnkaAPIManager.getEnkaAPIResult(uid)
                    # check if character in avatarInfoList
                    avatarInfoList = enkaData["avatarInfoList"]
                    inAvatarInfoList = False
                    for avatar in avatarInfoList:
                        if avatar["avatarId"] == charID:
                            inAvatarInfoList = True
                            charData = avatar
                            break
                    if not inAvatarInfoList:
                        # await interaction.response.send_message(i18n["msg.error.avatarNotInList"])
                        await interaction.followup.send(i18n["msg.error.avatarNotInList"], ephemeral=isPrivate)
                        return
                    resEmbed = calculatorHandler(charid=charID, charData=charData, i18n=i18n, language=self.language)
                    await asyncio.sleep(delay=1)
                    try:
                        await interaction.followup.send(embed=resEmbed, ephemeral=isPrivate)
                    except Exception as e:
                        _log.error(e.with_traceback())
                        await interaction.followup.send(e, ephemeral=isPrivate)


                buttonBoard.callback = on_button_Board
                buttonArtifacts.callback = on_button_artifacts
                buttonCalculator.callback = on_button_cal

                charFullName = CharIDDatabase.charFullName(charID, language=self.language)
                title = i18n["sys.label.lookUpChar"] + f" {charFullName} ({charID})"
                view.add_item(buttonBoard)
                view.add_item(buttonArtifacts)
                if charID in calAvailableCharIdList:
                    view.add_item(buttonCalculator)
                return title, view
        else:
            # no valid bound UID found
            return i18n["msg.err.noUIDBound"], None

    async def createVoiceChannel(self, ctx, name, botName):
        i18n = self.get_i18n(self.language)
        name = f"[{botName}]{name}"
        try:
            channel = await ctx.guild.create_voice_channel(name=name)
            res = True
            msg = f"\"{channel.name}\" {i18n['feat.createvc.success']}\n{i18n['feat.createvc.tips']}"
        except Forbidden as forbidden:
            _log.error(f"Create voice channel fail because of Forbidden")
            res = False
            msg = i18n["feat.createvc.fail"] + "Forbidden: No permission"
        except HTTPException:
            _log.error(f"Create voice channel fail because of HTTPException")
            res = False
            msg = i18n["feat.createvc.fail"] + "HTTP Error"
        except TypeError:
            _log.error(f"Create voice channel fail because of TypeError")
            res = False
            msg = i18n["feat.createvc.fail"] + "Type Error"
        return res, msg

