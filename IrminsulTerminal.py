import discord
import os
import IrminsulDatabase
import logging
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

        embed = discord.Embed(title=i18n["robot.name"], description=i18n["robot.description"], color=0xeee657)
        embed.add_field(name=i18n["sys.label.author"], value=i18n["robot.author"])
        embed.add_field(name=i18n["sys.label.version"], value=config["version"])
        embed.add_field(name=i18n["sys.label.serverCount"], value=f"{len(bot.guilds)}")
        embed.add_field(name=i18n["sys.label.invite"], value=i18n["robot.inviteLink"])
        embed.add_field(name=i18n["sys.label.about"], value=i18n["robot.about"])
        return embed

    def bindUID(self, user, uid):
        i18n = self.get_i18n(self.language)

        if not uid.isdigit() or len(str(uid)) != 9:
            _log.warning(f"Found UID {uid} is not valid.")
            return i18n["msg.error.uidInvalid"]

        res = IrminsulDatabase.bindUID(user_id=user.id, uid=uid)
        if res:
            return i18n["msg.bindUidSuccess"]
        else:
            return i18n["msg.bindUidFail"]

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