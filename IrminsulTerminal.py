import discord
import os
from botpy.ext.cog_yaml import read

config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))


class IrminsulTerminal:
    def selfInfo(self, bot):
        embed = discord.Embed(title="Paimon Bot", description="A bot from Project Irminsul Terminal", color=0xeee657)
        embed.add_field(name="Author", value="Bill Haku")
        embed.add_field(name="Version", value=config["version"])
        embed.add_field(name="Server count", value=f"{len(bot.guilds)}")
        embed.add_field(name="Invite", value="https://discord.com/api/oauth2/authorize?client_id=964545612831932507&permissions=8&scope=bot")
        embed.add_field(name="About", value="This is a opensource Genshin bot for Discord.")
        return embed