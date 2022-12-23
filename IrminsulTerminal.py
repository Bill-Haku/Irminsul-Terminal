import discord
import os
from botpy.ext.cog_yaml import read

config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
i18n_en = read(os.path.join(os.path.dirname(__file__), "i18n-en.yaml"))
i18n_zh = read(os.path.join(os.path.dirname(__file__), "i18n-zh_Hans.yaml"))
i18n_ja = read(os.path.join(os.path.dirname(__file__), "i18n-ja.yaml"))


class IrminsulTerminal:
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

    def selfInfo(self, bot, language="en"):
        i18n = self.get_i18n(language)

        embed = discord.Embed(title=i18n["robot.name"], description=i18n["robot.description"], color=0xeee657)
        embed.add_field(name=i18n["sys.label.author"], value=i18n["robot.author"])
        embed.add_field(name=i18n["sys.label.version"], value=config["version"])
        embed.add_field(name=i18n["sys.label.serverCount"], value=f"{len(bot.guilds)}")
        embed.add_field(name=i18n["sys.label.invite"], value=i18n["robot.inviteLink"])
        embed.add_field(name=i18n["sys.label.about"], value=i18n["robot.about"])
        return embed
