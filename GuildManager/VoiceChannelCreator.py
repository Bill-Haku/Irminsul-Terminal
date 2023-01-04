import discord
import logging
from discord.ui import Modal, TextInput
from discord import *


_log = logging.getLogger('discord')
logHandler = logging.FileHandler(filename='irminsul.log', encoding='utf-8', mode='w')
_log.addHandler(logHandler)


class VoiceChannelCreator(Modal):
    def __init__(self, i18n, botName) -> None:
        super().__init__(title=i18n["sys.label.createVC"])
        self.i18n = i18n
        textInput = discord.ui.TextInput(label=i18n["sys.label.createVC.text"])
        self.add_item(textInput)
        self.botName = botName

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        name = self.children[0].value
        botName = self.botName
        i18n = self.i18n
        ctx = interaction
        name = f"[{botName}]{name}"
        _log.info(f"Create Voice Channel {name}...")
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
        _log.info(msg)
        await interaction.response.send_message(msg)


class VoiceChannelCreatorModalView(discord.ui.View):
    def __init__(self, i18n, botName) -> None:
        super(VoiceChannelCreatorModalView, self).__init__(timeout=None)
        self.i18n = i18n
        self.botName = botName

    @discord.ui.button(label="Create Voice Channel", style=discord.ButtonStyle.green, custom_id="VCCreatorView:Button")
    async def open_modal(self, interaction: discord.Interaction, button: discord.Button):
        modal = VoiceChannelCreator(i18n=self.i18n, botName=self.botName)
        await interaction.response.send_modal(modal)
